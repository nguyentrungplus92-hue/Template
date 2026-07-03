"""
Context processor cho app 'home'.

Đưa cấu hình tìm kiếm mặc định (khai báo trong settings.py) tới MỌI template
mà không phải truyền tay ở từng view. Nhờ đó cả dự án có thể dùng chung một
kiểu tìm kiếm chỉ bằng 1 dòng trong settings.

Đăng ký trong settings.py -> TEMPLATES -> OPTIONS -> context_processors:
    'home.context_processors.search_config',
"""
from django.conf import settings


def search_config(request):
    """
    Trả về:
    - SEARCH_MODE: kiểu tìm kiếm mặc định toàn dự án ('client'|'server'|'live').
      Mặc định 'client' nếu settings không khai báo.
    - SEARCH_API_URL_NAME: tên URL của endpoint API (chỉ dùng khi kiểu 'live').
      Để trống nếu không dùng live.
    """
    return {
        'SEARCH_MODE': getattr(settings, 'SEARCH_MODE', 'client'),
        'SEARCH_API_URL_NAME': getattr(settings, 'SEARCH_API_URL_NAME', ''),
    }
