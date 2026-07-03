"""
Context processor cho app 'home'.

Đưa các biến dùng chung tới MỌI template mà không phải truyền tay ở từng view:
- Cấu hình tìm kiếm mặc định (SEARCH_MODE, SEARCH_API_URL_NAME).
- Ngôn ngữ hiện tại và danh sách ngôn ngữ (cho tag {% t %} và nút đổi ngôn ngữ).

Đăng ký trong settings.py -> TEMPLATES -> OPTIONS -> context_processors:
    'home.context_processors.search_config',
    'home.context_processors.language_config',
"""
from django.conf import settings
from .translations import get_language, LANGUAGES

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


def language_config(request):
    """
    CURRENT_LANG: mã ngôn ngữ hiện tại ('vi'|'en'|'ja') - tag {% t %} dùng.
    LANGUAGES:    danh sách (mã, nhãn) - để dựng nút/dropdown chọn ngôn ngữ.
    """
    return {
        'CURRENT_LANG': get_language(request),
        'LANGUAGES': LANGUAGES,
    }