"""
Từ điển dịch đa ngôn ngữ - định nghĩa NGAY TRONG CODE (không cần gettext).

Cách dùng:
- Thêm câu mới: thêm 1 dòng vào TRANSLATIONS với 3 bản dịch vi/en/ja.
- Trong template: {% load i18n_simple %} rồi {% t "Câu gốc" %}
- Khóa (bên trái) nên là câu TIẾNG VIỆT gốc để dễ đọc.

Ngôn ngữ hỗ trợ: 'vi' (Việt), 'en' (Anh), 'ja' (Nhật).
"""

# Ngôn ngữ hỗ trợ và nhãn hiển thị trên nút chọn
LANGUAGES = [
    ('vi', 'Tiếng Việt'),
    ('en', 'English'),
    ('ja', '日本語'),
]

# Cờ SVG cho từng ngôn ngữ (hiển thị đúng trên mọi máy, kể cả Windows).
# Dùng trong template qua tag {% flag 'vi' %}.
FLAGS = {
    'vi': (
        '<svg viewBox="0 0 24 16" width="22" height="15" '
        'xmlns="http://www.w3.org/2000/svg" style="border-radius:2px;display:block">'
        '<rect width="24" height="16" fill="#da251d"/>'
        '<path d="M12 3.2 L13.29 7.16 L17.46 7.16 L14.09 9.61 '
        'L15.37 13.58 L12 11.13 L8.63 13.58 L9.91 9.61 L6.54 7.16 '
        'L10.71 7.16 Z" fill="#ff0"/></svg>'
    ),
    'en': (
        '<svg viewBox="0 0 24 16" width="22" height="15" '
        'xmlns="http://www.w3.org/2000/svg" style="border-radius:2px;display:block">'
        '<rect width="24" height="16" fill="#012169"/>'
        '<path d="M0 0 L24 16 M24 0 L0 16" stroke="#fff" stroke-width="3"/>'
        '<path d="M0 0 L24 16 M24 0 L0 16" stroke="#c8102e" stroke-width="1.5"/>'
        '<rect x="10" y="0" width="4" height="16" fill="#fff"/>'
        '<rect x="0" y="6" width="24" height="4" fill="#fff"/>'
        '<rect x="10.75" y="0" width="2.5" height="16" fill="#c8102e"/>'
        '<rect x="0" y="6.75" width="24" height="2.5" fill="#c8102e"/></svg>'
    ),
    'ja': (
        '<svg viewBox="0 0 24 16" width="22" height="15" '
        'xmlns="http://www.w3.org/2000/svg" style="border-radius:2px;display:block">'
        '<rect width="24" height="16" fill="#fff" stroke="#ddd" stroke-width="0.5"/>'
        '<circle cx="12" cy="8" r="4.5" fill="#bc002d"/></svg>'
    ),
}

DEFAULT_LANG = 'vi'
LANG_CODES = [code for code, _ in LANGUAGES]


# === Bảng dịch: 'câu gốc tiếng Việt': {mã ngôn ngữ: bản dịch} ===
TRANSLATIONS = {
    # -- Chung / topbar --
    'Đăng xuất':   {'vi': 'Đăng xuất',   'en': 'Logout',    'ja': 'ログアウト'},
    'Tìm kiếm...': {'vi': 'Tìm kiếm...',  'en': 'Search...', 'ja': '検索...'},

    # -- Trang chưa đăng nhập --
    'Chưa đăng nhập': {'vi': 'Chưa đăng nhập', 'en': 'Not logged in', 'ja': '未ログイン'},
    'Đăng nhập SCM Control': {'vi': 'Đăng nhập SCM Control', 'en': 'Login via SCM Control', 'ja': 'SCM Control でログイン'},
    'Bạn cần đăng nhập từ hệ thống chính': {
        'vi': 'Bạn cần đăng nhập từ hệ thống chính',
        'en': 'You need to log in from the main system',
        'ja': 'メインシステムからログインしてください',
    },
    'để truy cập': {'vi': 'để truy cập', 'en': 'to access', 'ja': 'にアクセスするには'},
    'Sau khi đăng nhập, quay lại trang này để tiếp tục.': {
        'vi': 'Sau khi đăng nhập, quay lại trang này để tiếp tục.',
        'en': 'After logging in, return to this page to continue.',
        'ja': 'ログイン後、このページに戻って続行してください。',
    },
    'Hoặc đăng nhập thông qua giao diện': {
        'vi': 'Hoặc đăng nhập thông qua giao diện',
        'en': 'Or log in through the',
        'ja': 'または次の画面からログイン',
    },
    'administrator': {'vi': 'administrator', 'en': 'administrator', 'ja': '管理者画面'},

    # -- Trang không có quyền --
    'Không có quyền truy cập': {'vi': 'Không có quyền truy cập', 'en': 'Access denied', 'ja': 'アクセス権限がありません'},
    'Không có quyền': {'vi': 'Không có quyền', 'en': 'Access denied', 'ja': '権限がありません'},
    'chưa được cấp quyền truy cập.': {
        'vi': 'chưa được cấp quyền truy cập.',
        'en': 'has not been granted access.',
        'ja': 'にはアクセス権限が付与されていません。',
    },
    'Tài khoản': {'vi': 'Tài khoản', 'en': 'Account', 'ja': 'アカウント'},
    'Vui lòng liên hệ quản trị viên để được cấp quyền.': {
        'vi': 'Vui lòng liên hệ quản trị viên để được cấp quyền.',
        'en': 'Please contact the administrator to be granted access.',
        'ja': '権限を付与してもらうには管理者に連絡してください。',
    },

    # -- Dashboard --
    'Hãy chọn các chức năng bên dưới để sử dụng': {
        'vi': 'Hãy chọn các chức năng bên dưới để sử dụng',
        'en': 'Choose a function below to get started',
        'ja': '下の機能を選択してください',
    },
    'Xin chào': {'vi': 'Xin chào', 'en': 'Hello', 'ja': 'こんにちは'},
    'Cập nhật Route': {'vi': 'Cập nhật Route', 'en': 'Update Route', 'ja': 'ルート更新'},
    'Báo cáo': {'vi': 'Báo cáo', 'en': 'Report', 'ja': 'レポート'},
    'Cấu hình': {'vi': 'Cấu hình', 'en': 'Settings', 'ja': '設定'},
    'Thống kê': {'vi': 'Thống kê', 'en': 'Statistics', 'ja': '統計'},
    'Người dùng': {'vi': 'Người dùng', 'en': 'Users', 'ja': 'ユーザー'},
    'Maker': {'vi': 'Maker', 'en': 'Maker', 'ja': 'メーカー'},
    'Route': {'vi': 'Route', 'en': 'Route', 'ja': 'ルート'},
    'Không có chức năng nào khớp từ khóa.': {
        'vi': 'Không có chức năng nào khớp từ khóa.',
        'en': 'No function matches your keyword.',
        'ja': 'キーワードに一致する機能がありません。',
    },
    # Mô tả các thẻ (thêm câu thật của bạn vào đây theo cùng mẫu)
    'Quản lý nhà cung cấp của Vendor.': {
        'vi': 'Quản lý nhà cung cấp của Vendor.',
        'en': "Manage Vendor's suppliers.",
        'ja': 'ベンダーのサプライヤー管理。',
    },
    'Gợi ý giao hàng theo Mode': {
        'vi': 'Gợi ý giao hàng theo Mode',
        'en': 'Delivery suggestion by Mode',
        'ja': 'モード別の配送提案',
    },
    'Route và Delivery time thời gian đi đường route giao hàng': {
        'vi': 'Route và Delivery time thời gian đi đường route giao hàng',
        'en': 'Route and Delivery time for shipping routes',
        'ja': 'ルートと配送ルートの所要時間',
    },
}


def get_language(request):
    """Lấy mã ngôn ngữ hiện tại từ session (mặc định DEFAULT_LANG)."""
    lang = None
    if hasattr(request, 'session'):
        lang = request.session.get('lang')
    return lang if lang in LANG_CODES else DEFAULT_LANG


def translate(text, lang):
    """
    Trả về bản dịch của 'text' theo ngôn ngữ 'lang'.
    Nếu không có trong từ điển -> trả nguyên văn (an toàn, không vỡ giao diện).
    """
    entry = TRANSLATIONS.get(text)
    if not entry:
        return text                 # chưa dịch -> giữ nguyên câu gốc
    return entry.get(lang, text)    # thiếu ngôn ngữ đó -> giữ nguyên câu gốc
