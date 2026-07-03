"""
Shipping advise - Django Settings.
Tên dự án
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# === SECRET_KEY phải GIỐNG chương trình mẹ (SCM_NAVI) ===
SECRET_KEY = 'django-insecure-hh4_o(87l9d3*48q$xehb0vyr)k(+5r%*ts1qb+#p1u32-xe9o'

DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'home',
    'shipping_advice',                  # App của dự án
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',        # Phải chạy TRƯỚC ParentSession
    'home.middleware.ParentSessionMiddleware',                     # SSO với SCM_NAVI + detect Django user
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SA.urls'                                        # Để đúng đường dẫn file urls chính của dự án
WSGI_APPLICATION = 'SA.wsgi.application'                        # Để đúng đường dẫn file wsgi của dự án

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'home.context_processors.search_config',        # Gắn tìm kiếm vào template để cả dự án cùng dùng chung 1 kiểu
                'home.context_processors.language_config',      # Gắn đa ngôn ngữ
            ],
        },
    },
]

# === DATABASES ===
DATABASES = {
    'default': {
        # Database chính của dự án
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Shipping_advice',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'parent_db': {
        # Database chương trình mẹ (SCM_NAVI) - chỉ đọc session
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'SCM_control',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',     # Đổi thành IP server SCM_NAVI khi deploy
        'PORT': '5432',
    },
}

# Note: SAP data lấy qua RFC (reports/sap_client.py), không qua Django ORM
# nên không cần DATABASE_ROUTERS.

LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True

# === Session/Cookie config cho SSO ===
# Web me (SCM_NAVI) van dung 'sessionid' (cookie mac dinh).
# Web con (ví dụ: SA) phai dung TEN COOKIE KHAC de:
#   1. Khong de ghi cookie sessionid cua web me khi login Django Admin
#   2. SSO van doc duoc cookie sessionid tu web me qua middleware
SESSION_COOKIE_NAME = 'SA_sessionid'                                    # Tên của dự án để không bị nhầm lẫn với các session khác
CSRF_COOKIE_NAME = 'SA_csrftoken'                                       # Tên của dự án để không bị nhầm lẫn với các session khác

# Session khong expire qua nhanh (giu user login lau hon)
SESSION_COOKIE_AGE = 60 * 60 * 8       # 8 hours
SESSION_SAVE_EVERY_REQUEST = True       # Reset expiry moi request

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# === Logging ===
import os
os.makedirs(BASE_DIR / 'log', exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'verbose'},
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'log' / 'history.log',
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'home': {'handlers': ['console', 'file'], 'level': 'INFO'},         # Thư mục được lấy log
        # hoặc bắt tất cả bằng logger rỗng:
        # '': {'handlers': ['console', 'file'], 'level': 'INFO'},
    },
}

# === Email ===
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '157.8.1.154'
EMAIL_PORT = 25
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'psnv.isg@vn.panasonic.com'


# === Thanh tìm kiếm ===
SEARCH_MODE = 'client'                          # 'client' | 'server' | 'live'
# SEARCH_API_URL_NAME = 'home:live_search_api'  # chỉ cần khi dùng 'live'. Với 'client' | 'server'  cần rào lại




# =============================================================================
# SAP RFC Configuration
# =============================================================================
# Dùng 1 shared user (BGD_MM) cho toàn project.
# Toggle giữa ECC (production hiện tại) và HANA (tương lai S/4HANA).

# SAP_SYSTEM = 'ECC'  # 'ECC' | 'HANA'

# SAP_CONFIG = {
#     'ECC': {
#         'ASHOST': '10.209.11.76',
#         'CLIENT': '300',
#         'SYSNR': '00',
#         'USER': 'BGD_MM',
#         'PASSWD': 'SapMM123',
#         'BATCH_SIZE': 15,
#     },
#     'HANA': {
#         'ASHOST': 'hana.cmcconsulting.vn',
#         'CLIENT': '120',
#         'SYSNR': '12',
#         'USER': 'locnx',
#         'PASSWD': 'Lockhongvui98',
#         'BATCH_SIZE': 15,
#     },
# }
