"""
Middleware SSO với chương trình mẹ SCM_NAVI.

Logic xác định username cho các URL không phải /admin/:

1. Ưu tiên: Django Admin user (login trực tiếp qua /admin/)
   → request.user.is_authenticated → dùng user.username

2. Fallback: Session từ SCM_NAVI (SSO)
   → đọc cookie sessionid, query parent_db

Nhờ vậy:
- Admin login Django Admin → vào được / và /reports/
- User login SCM_NAVI → vào được / và /reports/
"""
import logging
import time
from django.db import connections


log = logging.getLogger(__name__)

# Simple in-memory cache (session_key → (username, expires_at))
_SESSION_CACHE: dict = {}
_CACHE_TTL_SECONDS = 60


class ParentSessionMiddleware:
    """
    Xác định username từ 2 nguồn:
    1. Django User (nếu login Admin trực tiếp)
    2. SCM_NAVI session (qua cookie)
    
    Set request.parent_username = username | None.
    Bỏ qua /admin/ → Django Admin tự quản lý auth.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Bỏ qua /admin/ - Django Admin tự quản lý auth
        if request.path.startswith('/admin/'):
            request.parent_username = None
            return self.get_response(request)
        
        request.parent_username = self._resolve_username(request)
        return self.get_response(request)
    
    def _resolve_username(self, request):
        """
        Ưu tiên Django user > SCM_NAVI session.
        """
        # 1. Check Django Admin user (login trực tiếp)
        if hasattr(request, 'user') and request.user.is_authenticated:
            log.debug(f"Django Admin user: {request.user.username}")
            return request.user.username
        
        # 2. Fallback: SCM_NAVI session
        return self._get_username_from_scm_navi(request)
    
    def _get_username_from_scm_navi(self, request):
        try:
            session_key = request.COOKIES.get('sessionid', '')
            if not session_key:
                return None
            
            cached = self._get_from_cache(session_key)
            if cached is not None:
                return cached
            
            username = self._get_username_from_parent(session_key)
            if username:
                self._set_cache(session_key, username)
                return username
            
            return None
        except Exception as e:
            log.exception(f"Session lookup error: {e}")
            return None
    
    @staticmethod
    def _get_from_cache(session_key):
        entry = _SESSION_CACHE.get(session_key)
        if entry is None:
            return None
        username, expires_at = entry
        if time.time() > expires_at:
            _SESSION_CACHE.pop(session_key, None)
            return None
        return username
    
    @staticmethod
    def _set_cache(session_key, username):
        _SESSION_CACHE[session_key] = (username, time.time() + _CACHE_TTL_SECONDS)
        if len(_SESSION_CACHE) > 1000:
            _SESSION_CACHE.clear()
    
    def _get_username_from_parent(self, session_key):
        """Lấy username từ DB mẹ (SCM_control)."""
        try:
            with connections['parent_db'].cursor() as cursor:
                cursor.execute(
                    "SELECT session_data FROM django_session "
                    "WHERE session_key = %s AND expire_date > NOW()",
                    [session_key],
                )
                row = cursor.fetchone()
                if not row:
                    return None
                
                from django.contrib.sessions.backends.db import SessionStore
                store = SessionStore()
                data = store.decode(row[0])
                
                user_id = data.get('_auth_user_id')
                if not user_id:
                    return None
                
                cursor.execute(
                    "SELECT username FROM auth_user WHERE id = %s",
                    [user_id],
                )
                row = cursor.fetchone()
                username = row[0] if row else None
                
                if username:
                    log.debug(f"SCM_NAVI login: {username}")
                return username
        except Exception as e:
            log.warning(f"Parent DB session lookup failed: {e}")
            return None
