# App `home` — Khung dùng chung: Đăng nhập (SSO) / Phân quyền / Giao diện / Đa ngôn ngữ

App `home` lo phần CHUNG cho các dự án web con chạy sau chương trình mẹ
**SCM_Control**: đăng nhập (SSO), chặn truy cập, trang chủ, giao diện
(dark mode, ô tìm kiếm, đa ngôn ngữ). Thiết kế để tái sử dụng cho nhiều dự án.

Lưu ý về cấu trúc: **app `home\` (file .py, gồm cả `middleware.py`) và
thư mục `templates\` (giao diện) đặt tách nhau** — template ở cấp gốc dự
án. Khi copy sang dự án khác, mang theo CẢ HAI. File README này đặt ở gốc
dự án (`SA\README.md`).

Các app nghiệp vụ (reports, shipping_advice...) lo chức năng riêng, không
nằm trong `home`.

---

## MỤC LỤC
1. Cơ chế đăng nhập (SSO)
2. Phân quyền (dựa trên auth_user)
3. Đăng xuất (single logout, không rời web con)
4. Giao diện (dark mode, chống nháy, icon, ô tìm, link)
5. Ba kiểu tìm kiếm (client / server / live)
6. Đặt 1 kiểu tìm kiếm cho cả dự án
7. Đa ngôn ngữ (i18n bằng từ điển trong code)
8. Cấu trúc app
9. Cài vào dự án mới
10. Ghi chú kỹ thuật (tránh vấp lại)

---

## 1. Cơ chế đăng nhập (SSO qua session dùng chung)

Web con KHÔNG tự xác thực mật khẩu — việc đăng nhập do web mẹ lo. Web con
"đọc ké" phiên của web mẹ để biết user là ai.

Luồng 3 trạng thái (trong `views.dashboard`):
1. **Chưa đăng nhập web mẹ** -> `parent_username=None` -> `no_login.html`
2. **Đã đăng nhập web mẹ, username KHÔNG có trong auth_user (db con)**
   -> `no_permission.html`
3. **Đã đăng nhập + có trong auth_user** -> `dashboard.html`

### Điều kiện để SSO chạy
- Web mẹ & web con **cùng host** (cookie không phân biệt cổng).
- **Cùng `SECRET_KEY`**.
- Web con dùng cookie riêng (`SA_sessionid`); đọc `sessionid` để lấy phiên
  web mẹ. Hai cookie song song.
- `ParentSessionMiddleware` (trong `home\middleware.py`) đọc session web
  mẹ từ `parent_db` và gán `request.parent_username`. Khai báo trong
  settings dưới tên `home.middleware.ParentSessionMiddleware`.

---

## 2. Phân quyền: dựa trên bảng `auth_user` của database con

Điều kiện vào web con: **username tồn tại trong `auth_user`** của db con.
Không cần model riêng (app `home` không có model -> không cần makemigrations).

Cấp quyền: đăng nhập `/admin/` bằng superuser -> **Users** -> **Add user**
với username trùng đúng username trên web mẹ.

---

## 3. Đăng xuất (single logout, KHÔNG rời web con)

Nút "Đăng xuất" -> view `home:logout`:
1. `django_logout()` xóa phiên web con.
2. Render `logout.html` có thẻ `<img>` ẩn trỏ tới URL logout web mẹ ->
   trình duyệt tải ngầm -> web mẹ xóa phiên. Trang KHÔNG sang web mẹ.
3. Tự về trang chủ web con (-> "Chưa đăng nhập").

Cấu hình: `SCM_LOGOUT_URL`. (Web mẹ phải cho logout bằng GET.)

---

## 4. Giao diện (trong base.html — mọi trang kế thừa)

### Dark mode (3 chế độ, giống Django admin)
Nút tròn trên topbar xoay vòng auto -> light -> dark. Lưu qua localStorage.
Màu dùng biến CSS trong `:root` (sáng) và `:root[data-theme="dark"]` (tối).

> QUY TẮC: trang mới dùng biến CSS (`var(--card-bg)`, `var(--text)`...)
> thay vì màu cố định, để dark mode tự áp dụng.

### Chống nháy khi F5 / đổi ngôn ngữ (QUAN TRỌNG)
Ba thứ phối hợp để không nháy khi tải lại:
1. **Script đặt theme sớm** ở đầu `<head>`: đọc localStorage và set
   `data-theme` TRƯỚC khi trang vẽ -> không chớp sáng ở dark mode.
2. **`html { background: var(--bg); }`**: nền đúng màu ngay lúc tải ->
   không chớp trắng.
3. **Transition chỉ bật SAU khi tải xong**: class `theme-ready` được thêm
   vào body qua requestAnimationFrame. Nhờ đó lúc F5 màu hiện dứt khoát
   (không "trôi"), còn khi bấm đổi theme vẫn chuyển mượt.

> Nếu sao chép base.html sang bản khác, phải mang theo CẢ 3 thứ trên, nếu
> không hiện tượng nháy sẽ quay lại.

### Icon
- Logo 🚚; icon thẻ chức năng: emoji hoặc SVG.
- Icon user trên topbar: SVG `fill="currentColor"` (KHÔNG emoji trên nền màu).

### Vùng nội dung
- `<div class="content">`: max 960px, căn giữa.
- `<div class="content wide">`: rộng gần hết bề ngang.

### Gắn link
- Thẻ -> trang: đổi `href="#"` thành `{% url 'ten:route' %}` (bền nhất)
  hoặc link tương đối. Thêm `target="_blank"` để mở tab mới.
- Logo/tên về trang chủ: bọc `<a class="brand-link">` (ĐỂ nút toggle NGOÀI
  thẻ a).

---

## 5. Ba kiểu tìm kiếm (ô tìm chung, mỗi trang tự chọn)

### CLIENT — lọc text trên màn hình
`{% block search_mode %}client{% endblock %}` + gắn class `searchable` và
`data-search` vào MỌI phần tử muốn lọc.
> Phần tử thiếu `searchable` sẽ luôn hiện.

### SERVER — tìm database, tải lại trang
`{% block search_mode %}server{% endblock %}` +
`{% block search_action %}{% url 'ten' %}{% endblock %}`. View đọc
`request.GET.get('q')`, truy vấn (`Q()|Q()` với `icontains`).

### LIVE — gợi ý xổ xuống, mở link tab mới
`{% block search_api %}{% url 'home:live_search_api' %}{% endblock %}`.
Endpoint trả JSON, mỗi item: `title` (bắt buộc), `url` (bắt buộc),
`tag`/`code`/`desc` (tùy chọn). Đổi giá trị -> sửa views; thêm trường
mới -> sửa cả views và hàm render trong base.html.

---

## 6. Đặt 1 kiểu tìm kiếm cho CẢ DỰ ÁN

settings.py:
```python
SEARCH_MODE = 'client'                         # 'client'|'server'|'live'
# SEARCH_API_URL_NAME = 'home:live_search_api' # CHỈ mở khi dùng 'live'
```
Đăng ký `home.context_processors.search_config` trong context_processors.

> CẢNH BÁO: để `SEARCH_API_URL_NAME` có giá trị thì MỌI trang bị ép sang
> LIVE. Dùng client/server -> COMMENT dòng đó.

---

## 7. Đa ngôn ngữ (i18n bằng từ điển trong code)

KHÔNG dùng gettext, KHÔNG thư viện ngoài. Toàn bộ bản dịch nằm trong
`home\translations.py` dưới dạng dictionary Python.

Hỗ trợ: vi (Việt), en (Anh), ja (Nhật). Nút cờ trên topbar (cạnh nút đổi
màu) để chọn; lựa chọn lưu qua session (nhớ cho lần sau).

### Cấu trúc
- `translations.py`: LANGUAGES (danh sách + nhãn), FLAGS (cờ SVG),
  TRANSLATIONS (bảng dịch), hàm get_language / translate.
- `templatetags/i18n_simple.py`: tag `{% t %}` (dịch) và `{% flag %}` (cờ).
- `context_processors.language_config`: đưa CURRENT_LANG + LANGUAGES tới
  mọi template.
- `views.set_language` + route `home:set_language`: đổi ngôn ngữ, lưu session.

### Thêm 1 câu dịch (3 bước)
1. Thêm vào TRANSLATIONS trong `translations.py`:
   ```python
   'Câu gốc': {'vi': 'Câu gốc', 'en': 'English', 'ja': '日本語'},
   ```
2. Trong template, bọc: `{% t "Câu gốc" %}`
   (câu trong tag phải KHỚP TỪNG KÝ TỰ với khóa: cả dấu câu, dấu cách,
   hoa/thường; lệch 1 ký tự -> giữ nguyên câu gốc).
3. Đầu file template phải có `{% load i18n_simple %}`.

> Câu chưa có trong từ điển -> tag tự giữ nguyên tiếng Việt (an toàn).

### Thêm ngôn ngữ mới
Thêm vào LANGUAGES, FLAGS (cờ SVG), và cột mới trong mỗi câu của
TRANSLATIONS.

### Đăng ký (settings.py -> context_processors)
```python
'home.context_processors.search_config',
'home.context_processors.language_config',
```

---

## 8. Cấu trúc app

```
SA\SA\                          <- package gốc (chứa manage.py)
├── manage.py
├── README.md                   <- tài liệu này
├── home\                       <- APP home: file .py
│   ├── __init__.py
│   ├── apps.py
│   ├── admin.py                # trống
│   ├── models.py               # trống (app không có model)
│   ├── middleware.py           # ParentSessionMiddleware (SSO)
│   ├── migrations/__init__.py
│   ├── urls.py
│   ├── services.py             # kiểm tra user trong auth_user
│   ├── context_processors.py   # search + language config
│   ├── translations.py         # TỪ ĐIỂN DỊCH + cờ SVG
│   ├── views.py                # dashboard, logout, set_language, tìm kiếm
│   └── templatetags\
│       ├── __init__.py         # (bắt buộc, rỗng)
│       └── i18n_simple.py      # tag {% t %} và {% flag %}
├── SA\                         <- package settings (settings.py, wsgi.py)
├── shipping_advice\            <- app nghiệp vụ
├── static\
├── log\
└── templates\                  <- TEMPLATE Ở CẤP GỐC
    ├── base.html               # layout gốc
    └── home\
        ├── dashboard.html
        ├── no_login.html
        ├── no_permission.html
        ├── logout.html
        └── demo_*.html         # demo tìm kiếm (có thể xóa)
```

> base.html ở `templates\base.html` (không phải `templates\home\`), nên
> các trang con kế thừa bằng `{% extends "base.html" %}` (KHÔNG tiền tố
> home/). View render vẫn dùng `render(request, 'home/dashboard.html',...)`.

---

## 9. Cài vào dự án mới

### Bước 1 — Copy 2 phần
- App `home\` (gồm middleware.py, translations.py, templatetags\) -> cạnh manage.py.
- Template -> `templates\`: base.html vào thẳng, còn lại vào `templates\home\`.

### Bước 2 — settings.py
```python
INSTALLED_APPS = [ ..., 'home' ]

TEMPLATES = [{
    ...
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': { 'context_processors': [
        ...,
        'home.context_processors.search_config',
        'home.context_processors.language_config',
    ]},
}]

MIDDLEWARE = [
    ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'home.middleware.ParentSessionMiddleware',   # sau Authentication
    ...
]

SCM_LOGIN_URL  = 'http://<ip-scm>:<cổng>/accounts/login/'
SCM_LOGOUT_URL = 'http://<ip-scm>:<cổng>/accounts/logout/'
PROJECT_NAME   = 'Tên dự án'
SEARCH_MODE    = 'client'
```
Cần sẵn: `SECRET_KEY` giống web mẹ; `SESSION_COOKIE_NAME` riêng; DB `parent_db`.

### Bước 3 — urls.py cấp dự án
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
]
```

### Bước 4 — migrate & tạo superuser
```
python manage.py migrate
python manage.py createsuperuser
```

---

## 10. Ghi chú kỹ thuật (tránh vấp lại)

- **Cache khi sửa CSS/JS**: sau khi sửa base.html luôn **Ctrl+F5**.
- **Nháy khi tải lại**: cần đủ 3 thứ chống nháy ở mục 4 (script theme sớm
  + nền html + transition theme-ready). Thiếu 1 là nháy lại.
- **Comment template**: `{# #}` chỉ 1 dòng; nhiều dòng dùng
  `{% comment %}...{% endcomment %}` hoặc `<!-- -->`.
- **Ô tìm trong `{% if username %}`**: view phải truyền `username`.
- **Dịch không đổi**: kiểm tra đủ 3 bước mục 7 (từ điển + `{% t %}` +
  `{% load i18n_simple %}`), và câu phải khớp từng ký tự.
- **templatetags cần `__init__.py`** (rỗng), nếu không `{% load %}` lỗi.
- **Icon trên nền màu**: SVG `fill="currentColor"`, không emoji.
- **SEARCH_API_URL_NAME ép sang live**: dùng client/server -> comment nó.
- **Link nội bộ**: ưu tiên `{% url %}` thay vì IP cứng.
