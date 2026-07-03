# App `home` — Khung dùng chung: Đăng nhập (SSO) / Phân quyền / Giao diện

App `home` lo phần CHUNG cho các dự án web con chạy sau chương trình mẹ
**SCM_Control**: đăng nhập (SSO), chặn truy cập, trang chủ, giao diện
(dark mode, ô tìm kiếm). Thiết kế để tái sử dụng cho nhiều dự án.

Lưu ý về cấu trúc: **app `home\` (file .py, gồm cả `middleware.py`) và
thư mục `templates\` (giao diện) đặt tách nhau** — template ở cấp gốc dự
án. Khi copy sang dự án khác, mang theo CẢ HAI (xem phần 7 và 8). File
README này đặt ở gốc dự án (`SA\README.md`).

Các app nghiệp vụ (reports, shipping_advice...) lo chức năng riêng, không
nằm trong `home`.

---

## MỤC LỤC
1. Cơ chế đăng nhập (SSO)
2. Phân quyền (dựa trên auth_user)
3. Đăng xuất (single logout, không rời web con)
4. Giao diện (dark mode, icon, ô tìm kiếm, link)
5. Ba kiểu tìm kiếm (client / server / live)
6. Đặt 1 kiểu tìm kiếm cho cả dự án
7. Cấu trúc app
8. Cài vào dự án mới
9. Tùy biến & mở rộng
10. Ghi chú kỹ thuật (tránh vấp lại)

---

## 1. Cơ chế đăng nhập (SSO qua session dùng chung)

Web con KHÔNG tự xác thực mật khẩu — việc đăng nhập do web mẹ lo. Web con
"đọc ké" phiên của web mẹ để biết user là ai.

Luồng 3 trạng thái (xử lý trong `views.dashboard`):

1. **Chưa đăng nhập web mẹ** (không có session)
   -> `parent_username = None` -> `no_login.html` (nút sang web mẹ)
2. **Đã đăng nhập web mẹ, nhưng username KHÔNG có trong auth_user (db con)**
   -> `no_permission.html`
3. **Đã đăng nhập web mẹ + username CÓ trong auth_user (db con)**
   -> `dashboard.html`

### Điều kiện để SSO chạy (cấu hình ở package gốc)
- Web mẹ & web con **cùng host** (cookie không phân biệt cổng: `:8013`
  và `:8019` vẫn chia sẻ cookie `sessionid`).
- **Cùng `SECRET_KEY`** — để web con giải mã session của web mẹ.
- Web con dùng cookie riêng (`SA_sessionid`) cho phiên admin của nó, và
  đọc cookie `sessionid` để lấy phiên web mẹ. Hai cookie song song.
- `ParentSessionMiddleware` (trong `home\middleware.py`) đọc session web
  mẹ từ database `parent_db` và gán `request.parent_username`.

> App `home` phụ thuộc vào `request.parent_username` do middleware gán.
> Middleware nằm trong `home\middleware.py`, khai báo trong settings dưới
> tên `home.middleware.ParentSessionMiddleware`. Copy app `home` sang dự
> án khác là mang theo luôn middleware — chỉ cần khai báo nó trong
> `MIDDLEWARE` + cấu hình `parent_db`.

---

## 2. Phân quyền: dựa trên bảng `auth_user` của database con

Điều kiện để user vào web con: **username tồn tại trong `auth_user`** của
database con. Không cần model phân quyền riêng.

- `auth_user` đóng vai trò "danh sách username được phép".
- Mật khẩu trong `auth_user` KHÔNG dùng (web mẹ lo đăng nhập).
- App `home` KHÔNG có model -> KHÔNG cần `makemigrations home`.

### Cấp quyền cho user
1. Đăng nhập `/admin/` bằng superuser (trang admin không qua middleware
   phân quyền nên luôn vào được).
2. Vào **Users** -> **Add user**, tạo user với username **trùng đúng**
   username trên web mẹ (phân biệt hoa/thường).
3. User đó từ web mẹ truy cập web con -> vào được dashboard.

> Phân quyền chi tiết hơn (theo chức năng trong dashboard) xử lý riêng.

---

## 3. Đăng xuất (single logout, KHÔNG rời web con)

Nút "Đăng xuất" -> view `home:logout`. Vì web con không tự xóa được cookie
web mẹ, view làm:
1. `django_logout()` xóa phiên web con.
2. Render `logout.html` — có thẻ `<img>` ẩn trỏ tới URL logout web mẹ.
   Trình duyệt tự tải ngầm (kèm cookie web mẹ vì cùng host) -> web mẹ xóa
   phiên của nó. **Trang KHÔNG chuyển sang web mẹ.**
3. Trang tự quay về trang chủ web con (-> hiện "Chưa đăng nhập").

Cấu hình: `SCM_LOGOUT_URL` (mặc định `.../accounts/logout/`).

> Điều kiện: web mẹ cho logout bằng GET. Nếu web mẹ chỉ cho POST, kỹ thuật
> ảnh ẩn không đủ, cần cách khác.

---

## 4. Giao diện (trong base.html — mọi trang kế thừa)

### Dark mode (3 chế độ, giống Django admin)
Nút tròn trên topbar xoay vòng: auto -> light -> dark.
- `auto`: theo cài đặt sáng/tối của hệ điều hành (qua
  `@media (prefers-color-scheme: dark)`).
- Lưu lựa chọn qua `localStorage`.
- Mọi màu dùng biến CSS trong `:root` (sáng) và `:root[data-theme="dark"]`
  (tối). `color-scheme` giúp thanh cuộn / input mặc định cũng đổi tông.

> QUY TẮC: trang mới phải dùng biến CSS (`var(--card-bg)`, `var(--text)`,
> `var(--muted)`...) thay vì màu cố định, để dark mode tự áp dụng.

### Icon
- Logo: emoji 🚚. Icon trong thẻ chức năng: emoji (📦 ⚙️ 📈...) hoặc SVG.
- Icon user trên topbar: SVG `fill="currentColor"` -> luôn trắng, rõ trên
  nền xanh ở cả 2 chế độ (KHÔNG dùng emoji cho icon trên nền màu).

### Vùng nội dung
- `<div class="content">`: rộng tối đa 960px, căn giữa.
- `<div class="content wide">`: chiếm gần hết bề ngang (bảng, báo cáo).

### Gắn link
- **Thẻ chức năng về 1 trang**: đổi `href="#"` thành link. Ưu tiên tên URL
  Django (bền nhất): `href="{% url 'home:demo_search_client' %}"`.
  Hoặc link tương đối `href="/demo/search-client/"`. Thêm `target="_blank"`
  nếu muốn mở tab mới.
- **Logo / tên về trang chủ**: bọc trong thẻ `<a>` (ĐỂ nút toggle NẰM
  NGOÀI thẻ a, nếu không bấm toggle sẽ nhảy về trang chủ):
  ```html
  <a href="{% url 'home:dashboard' %}" class="brand-link">
      <span style="font-size:30px;">🚚</span>
      <span>{% block brand %}Shipping Advice{% endblock %}</span>
  </a>
  ```
  CSS: `.topbar .brand-link { color:#fff; text-decoration:none;
  display:inline-flex; align-items:center; gap:10px; }`

### Ô tìm kiếm
- Nằm giữa topbar, chỉ hiện khi đã đăng nhập (`{% if username %}`).
- Là `<form>` đọc block để mỗi trang chọn kiểu (xem phần 5, 6).

---

## 5. Ba kiểu tìm kiếm (ô tìm chung, mỗi trang tự chọn)

### Kiểu 1 — CLIENT (lọc text trên màn hình)
JS lọc ngay khi gõ, không gọi server. Hợp dữ liệu ít (vd ACS Report).

Bật: `{% block search_mode %}client{% endblock %}`
Gắn class `searchable` + `data-search` vào MỌI phần tử muốn lọc:
```html
<a class="feature searchable" data-search="cấu hình tham số hệ thống" href="#">...</a>
```
> QUAN TRỌNG: phần tử nào THIẾU `searchable` sẽ luôn hiện (không bị lọc).
> `data-search` chứa từ khóa muốn tìm được; thiếu nó thì lấy text trong thẻ.

### Kiểu 2 — SERVER (tìm trong database, tải lại trang)
Gõ + Enter -> gửi `?q=` -> view truy vấn DB -> render trang. Hợp dữ liệu lớn.

Bật:
```django
{% block search_mode %}server{% endblock %}
{% block search_action %}{% url 'ten_url' %}{% endblock %}
```
View: đọc `request.GET.get('q')`, truy vấn (`Q(...) | Q(...)` với
`icontains` để tìm gần đúng nhiều cột).

### Kiểu 3 — LIVE (gợi ý xổ xuống, mở link tab mới)
Gõ tới đâu gọi ngầm API tới đó (không tải lại trang) -> dropdown gợi ý ->
bấm 1 gợi ý -> mở URL ở TAB MỚI (vd Shipping Advice).

Bật: `{% block search_api %}{% url 'home:live_search_api' %}{% endblock %}`
(Có `search_api` là tự bật live, ưu tiên hơn client/server.)

Endpoint API trả JSON, mỗi kết quả là 1 dict:
- **`title`** (BẮT BUỘC) — dòng chữ chính.
- **`url`**   (BẮT BUỘC) — link mở khi bấm (tab mới).
- `tag`, `code`, `desc` (TÙY CHỌN) — nhãn trái, nhãn phải, dòng mô tả.

```python
return JsonResponse({'results': [
    {'title': '...', 'url': '...', 'tag': '...', 'code': '...', 'desc': '...'},
]})
```

**Ánh xạ dữ liệu:** tên trường bên trái (`'title'`, `'url'`...) là CỐ ĐỊNH
(JS đọc theo tên này). Bên phải là dữ liệu DB của bạn:
```python
results.append({
    'title': row.ten_bao_cao,   # tên JS cần : dữ liệu DB của bạn
    'url':   row.link_mo,
    'desc':  row.duong_dan,
})
```

**Thêm/đổi/bớt trường:**
- Đổi GIÁ TRỊ trường đã có -> chỉ sửa `views.py`.
- Bỏ 1 trường -> chỉ bỏ ở `views.py` (JS tự cho ra rỗng).
- Thêm LOẠI trường MỚI (vd `ngay_tao`) -> sửa CẢ HAI: `views.py` (gửi
  dữ liệu) + `base.html` hàm `render` (thêm dòng đọc & hiển thị).

**Tiện ích live:** debounce 250ms; phím ↑ ↓ chọn, Enter mở, Esc đóng;
bấm ra ngoài -> đóng dropdown.

---

## 6. Đặt 1 kiểu tìm kiếm cho CẢ DỰ ÁN (không lặp ở từng trang)

Khai báo mặc định 1 lần trong settings, mọi trang tự theo (vẫn ghi đè được).

**settings.py:**
```python
SEARCH_MODE = 'client'                         # 'client' | 'server' | 'live'
# SEARCH_API_URL_NAME = 'home:live_search_api' # CHỈ mở khi dùng 'live'
```

**Đăng ký context processor** (đưa 2 biến trên tới mọi template) trong
settings.py -> TEMPLATES -> OPTIONS -> context_processors:
```python
'home.context_processors.search_config',
```

Sau đó:
- Cả dự án đổi kiểu -> chỉ sửa `SEARCH_MODE`.
- Trang cá biệt muốn khác -> khai báo block để ghi đè.

> CẢNH BÁO QUAN TRỌNG: nếu để `SEARCH_API_URL_NAME` có giá trị thì MỌI trang
> bị ép sang LIVE (vì code ưu tiên API). Dùng client/server thì phải
> COMMENT/XÓA dòng `SEARCH_API_URL_NAME`.
> Không đăng ký context processor -> mặc định về 'client'.

---

## 7. Cấu trúc app

Lưu ý: trong dự án này, **template đặt ở CẤP GỐC dự án** (không nằm trong
app home). `base.html` nằm trực tiếp trong `templates\`, các trang khác
trong `templates\home\`. settings.py trỏ `DIRS: [BASE_DIR / 'templates']`.

```
SA\SA\                          <- package gốc (chứa manage.py)
├── manage.py
├── README.md                   <- tài liệu này (ở gốc dự án)
├── home\                       <- APP home: chứa file .py
│   ├── __init__.py
│   ├── apps.py                 # HomeConfig (name = 'home')
│   ├── admin.py                # trống - không đăng ký model
│   ├── models.py               # trống - app không có model
│   ├── middleware.py           # ParentSessionMiddleware (SSO)  <-- lõi SSO
│   ├── migrations/__init__.py
│   ├── urls.py                 # route: dashboard, logout, demo, api
│   ├── services.py             # kiểm tra user trong auth_user  <-- lõi phân quyền
│   ├── context_processors.py   # đưa cấu hình tìm kiếm mặc định tới template
│   └── views.py                # dashboard, logout, các view tìm kiếm  <-- lõi
├── SA\                         <- package settings (settings.py, wsgi.py...)
├── shipping_advice\            <- app nghiệp vụ
├── static\
├── log\
└── templates\                  <- TEMPLATE Ở CẤP GỐC
    ├── base.html               # layout gốc (topbar, dark mode, ô tìm + JS)
    └── home\
        ├── dashboard.html
        ├── no_login.html
        ├── no_permission.html
        ├── logout.html
        ├── demo_search_client.html   # demo kiểu 1 (có thể xóa)
        ├── demo_search_server.html   # demo kiểu 2 (có thể xóa)
        └── demo_live_search.html     # demo kiểu 3 (có thể xóa)
```

> Vì `base.html` nằm ở `templates\base.html` (không phải `templates\home\`),
> các trang con kế thừa bằng `{% extends "base.html" %}` (KHÔNG có tiền tố
> `home/`). Các view render trang con vẫn dùng đường dẫn có `home/`, vd
> `render(request, 'home/dashboard.html', ...)`.

Các trang `demo_*` chỉ để tham khảo. Khi nắm rồi có thể xóa (template +
route + view tương ứng).

---

## 8. Cài vào dự án mới

### Bước 1 — Copy 2 phần vào dự án
- Thư mục app `home\` (gồm cả `middleware.py`) -> đặt cạnh `manage.py`.
- Các template -> đặt vào `templates\` ở cấp gốc: `base.html` vào thẳng
  `templates\`, phần còn lại vào `templates\home\`.

### Bước 2 — settings.py
```python
INSTALLED_APPS = [ ..., 'home' ]

# Trỏ thư mục template cấp gốc:
TEMPLATES = [{
    ...
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': { 'context_processors': [
        ...,
        'home.context_processors.search_config',
    ]},
}]

SCM_LOGIN_URL  = 'http://<ip-scm>:<cổng>/accounts/login/'
SCM_LOGOUT_URL = 'http://<ip-scm>:<cổng>/accounts/logout/'
PROJECT_NAME   = 'Tên dự án'
SEARCH_MODE    = 'client'
```

Cần sẵn (từ thiết kế web con):
- `SECRET_KEY` giống hệt web mẹ.
- `SESSION_COOKIE_NAME` riêng cho web con (vd `SA_sessionid`).
- Database `parent_db` trỏ tới DB web mẹ (để đọc session).
- Khai báo middleware SSO trong `MIDDLEWARE` (đặt SAU
  `AuthenticationMiddleware`):
  ```python
  MIDDLEWARE = [
      ...
      'django.contrib.auth.middleware.AuthenticationMiddleware',
      'home.middleware.ParentSessionMiddleware',   # <-- SSO web mẹ
      ...
  ]
  ```

### Bước 3 — urls.py cấp dự án
```python
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
]
```

### Bước 4 — Tạo bảng & superuser
```
python manage.py migrate
python manage.py createsuperuser
```
(Không cần `makemigrations home` vì app không có model.)

---

## 9. Tùy biến & mở rộng

- **Đổi màu / logo / tên**: sửa biến CSS + block `brand` trong base.html,
  hoặc đặt `PROJECT_NAME` trong settings.
- **Tự quay về web con sau khi login web mẹ**: web mẹ hỗ trợ `?next=` chuẩn
  Django -> gắn `?next=<url web con>` vào `SCM_LOGIN_URL`.
- **Phân quyền chi tiết trong dashboard**: thêm logic trong view/app nghiệp
  vụ, dựa trên user lấy từ `services.get_user()`.

---

## 10. Ghi chú kỹ thuật (tránh vấp lại)

- **Cache khi sửa CSS/JS**: sau khi sửa base.html (JS/CSS), luôn **Ctrl+F5**
  (tải lại bỏ cache). F5 thường giữ bản cũ -> tưởng code sai.
- **Comment trong template Django**: `{# #}` chỉ cho 1 DÒNG. Nhiều dòng phải
  dùng `{% comment %}...{% endcomment %}` hoặc `<!-- -->`, nếu không phần
  thừa sẽ hiện ra màn hình.
- **Ô tìm nằm trong `{% if username %}`**: view render trang có ô tìm phải
  truyền `username` vào context, nếu không ô tìm bị ẩn.
- **Icon trên nền màu**: dùng SVG `fill="currentColor"`, không dùng emoji
  (emoji màu cố định, dễ chìm).
- **Client search cần đánh dấu**: chế độ client chỉ lọc phần tử có class
  `searchable`. Nó KHÔNG tự lọc mọi thứ trên trang.
- **SEARCH_API_URL_NAME ép sang live**: để nó có giá trị thì client/server
  bị vô hiệu. Dùng client/server -> comment dòng đó.
- **Link nội bộ**: ưu tiên `{% url 'ten:route' %}` thay vì gõ IP cứng, để
  đổi IP/đường dẫn không phải sửa từng link.
