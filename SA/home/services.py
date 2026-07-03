"""
Tầng logic phân quyền cho app 'home'.

Trả lời: "username (đã xác thực ở web mẹ) có được dùng web con không?"

Quy tắc (đã chốt):
- Điều kiện DUY NHẤT: username tồn tại trong bảng auth_user của database con.
- Không tồn tại -> không có quyền (ra trang no_permission).

Ghi chú:
- Dùng bảng user mặc định của Django (auth_user) làm "danh sách cho phép".
- Web con KHÔNG xác thực mật khẩu (việc đó do web mẹ lo). Bản ghi auth_user
  ở đây chỉ đóng vai trò danh sách username được phép truy cập.
- Phân quyền chi tiết hơn (nếu cần) xử lý riêng bên trong dashboard.
"""
from django.contrib.auth import get_user_model

User = get_user_model()


def get_username_from_request(request):
    """Lấy username do ParentSessionMiddleware gán (từ session web mẹ)."""
    return getattr(request, 'parent_username', '') or ''


def user_exists(username):
    """True nếu username tồn tại trong bảng user (auth_user) của database con."""
    if not username:
        return False
    return User.objects.filter(username=username).exists()


def get_user(username):
    """
    Trả về đối tượng User của database con theo username, hoặc None.
    Dùng khi cần thêm thông tin user (email, tên, cờ is_staff...) trong view.
    """
    if not username:
        return None
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None
