"""
App 'home' - đăng nhập / phân quyền / trang chủ dùng chung.

============================================================
LUỒNG TRUY CẬP (đã chốt)
============================================================
1. Chưa đăng nhập web mẹ (không có session)
   -> parent_username = None
   -> no_login.html (nút sang web mẹ đăng nhập)

2. Đã đăng nhập web mẹ, NHƯNG username không tồn tại trong auth_user (db con)
   -> no_permission.html ("đã đăng nhập nhưng chưa được cấp quyền")

3. Đã đăng nhập web mẹ + username có trong auth_user (db con)
   -> dashboard.html

============================================================
ĐĂNG XUẤT (single logout - thoát cả hệ thống)
============================================================
Web con KHÔNG tự xóa được cookie session của web mẹ. Nên nút Đăng xuất
sẽ: (1) xóa phiên web con, rồi (2) chuyển hướng sang URL đăng xuất của
web mẹ để web mẹ tự xóa phiên của nó -> user thoát khỏi toàn hệ thống.

Phụ thuộc:
- request.parent_username do ParentSessionMiddleware (package gốc) gán.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from django.conf import settings

from .services import get_username_from_request, user_exists


# === Cấu hình (nên đặt trong settings.py, không sửa file này) ===
SCM_LOGIN_URL = getattr(settings, 'SCM_LOGIN_URL', 'http://10.92.184.241:8888/accounts/login/')
SCM_LOGOUT_URL = getattr(settings, 'SCM_LOGOUT_URL', 'http://10.92.184.241:8888/accounts/logout/')
PROJECT_NAME = getattr(settings, 'PROJECT_NAME', 'Shipping Advice')


def dashboard(request):
    """Trang chủ - kiểm tra đăng nhập (web mẹ) rồi kiểm tra user tồn tại (db con)."""
    username = get_username_from_request(request)

    # 1. Chưa đăng nhập web mẹ
    if not username:
        return render(request, 'home/no_login.html', {
            'scm_login_url': SCM_LOGIN_URL,
            'project_name': PROJECT_NAME,
        })

    # 2. Đã đăng nhập web mẹ, nhưng username không có trong auth_user (db con)
    if not user_exists(username):
        return render(request, 'home/no_permission.html', {
            'username': username,
            'project_name': PROJECT_NAME,
        })

    # 3. Có trong db con -> dashboard
    return render(request, 'home/dashboard.html', {
        'username': username,
        'project_name': PROJECT_NAME,
    })


def logout(request):
    """
    Đăng xuất cả web con lẫn web mẹ, nhưng KHÔNG chuyển trang sang web mẹ.

    Bước 1: django_logout() xóa phiên web con (cookie SA_sessionid).
    Bước 2: render trang trung gian logout.html. Trang này có thẻ <img> ẩn
            trỏ tới URL logout web mẹ -> trình duyệt tự tải ngầm (kèm cookie
            web mẹ vì cùng host) -> web mẹ xóa phiên của nó.
    Bước 3: trang tự chuyển về trang chủ web con (lúc này cả 2 phiên đã hết
            -> hiện "Chưa đăng nhập").

    User luôn ở lại web con, không bị nhảy sang giao diện web mẹ.
    """
    django_logout(request)
    return render(request, 'home/logout.html', {
        'scm_logout_url': SCM_LOGOUT_URL,
        'project_name': PROJECT_NAME,
    })


# =========================================================================
# DEMO TÌM KIẾM (2 kiểu) - tham khảo, có thể xóa khi không cần
# =========================================================================

def demo_search_client(request):
    """Demo kiểu 1: lọc text trên màn hình. View chỉ render trang tĩnh;
    việc lọc do JavaScript ở base.html làm (chế độ 'client')."""
    return render(request, 'home/demo_search_client.html', {
        'project_name': PROJECT_NAME,
        'username': get_username_from_request(request),
    })


def demo_search_server(request):
    """Demo kiểu 2: tìm trong database. Nhận ?q= rồi truy vấn.
    Dùng bảng auth_user làm dữ liệu mẫu (có sẵn, khỏi tạo model)."""
    from django.contrib.auth import get_user_model
    from django.db.models import Q

    User = get_user_model()
    query = (request.GET.get('q') or '').strip()

    results = []
    if query:
        # icontains = tìm gần đúng, không phân biệt hoa/thường.
        # Q(...) | Q(...) = khớp MỘT TRONG các trường.
        results = User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).order_by('username')[:50]     # giới hạn 50 để tránh trả quá nhiều

    return render(request, 'home/demo_search_server.html', {
        'project_name': PROJECT_NAME,
        'username': get_username_from_request(request),
        'query': query,
        'results': results,
    })


# =========================================================================
# LIVE SEARCH (gợi ý xổ xuống + mở link tab mới)
# =========================================================================

def demo_live_search(request):
    """Trang demo live search - chỉ render giao diện. Việc gợi ý do JS gọi
    tới endpoint live_search_api bên dưới."""
    return render(request, 'home/demo_live_search.html', {
        'project_name': PROJECT_NAME,
        'username': get_username_from_request(request),
    })


def live_search_api(request):
    """
    Endpoint trả JSON cho live search. Nhận ?q=... , trả danh sách gợi ý.

    Mỗi gợi ý có: tiêu đề, mô tả phụ, và URL để mở (tab mới).
    Ở đây dùng DỮ LIỆU MẪU cứng cho dễ hình dung. Trong dự án thật, thay
    phần SAMPLE bằng truy vấn database của bạn và ghép URL tương ứng.
    """
    from django.http import JsonResponse

    query = (request.GET.get('q') or '').strip().lower()

    # === DỮ LIỆU MẪU - thay bằng truy vấn database thật ===
    SAMPLE = [
        {'title': 'Exchange Rate into SAP', 'tag': 'FICO', 'code': '0B08',
         'desc': r'\\10.92.184.241\share\Auto\FICO\0B08\Exchange_rate',
         'url': 'http://10.92.184.241:8019/demo/search-client/'},
        {'title': 'Material Master Upload', 'tag': 'MM', 'code': 'MM01',
         'desc': r'\\10.92.184.241\share\Auto\MM\MM01\Material',
         'url': 'http://10.92.184.241:8019/demo/search-server/'},
        {'title': 'Vendor Master Create', 'tag': 'MM', 'code': 'XK01',
         'desc': r'\\10.92.184.241\share\Auto\MM\XK01\Vendor',
         'url': 'http://10.92.184.241:8019/'},
        {'title': 'Post FI Document', 'tag': 'FICO', 'code': 'FB01',
         'desc': r'\\10.92.184.241\share\Auto\FICO\FB01\Posting',
         'url': 'http://10.92.184.241:8019/demo/search-server/'},
    ]

    if not query:
        results = []
    else:
        # Lọc gần đúng: khớp nếu query nằm trong tiêu đề, tag, hoặc mã.
        results = [
            item for item in SAMPLE
            if query in item['title'].lower()
            or query in item['tag'].lower()
            or query in item['code'].lower()
        ]

    return JsonResponse({'results': results})
