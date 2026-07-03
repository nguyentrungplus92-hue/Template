"""
URL của app 'home'.

Trong urls.py cấp dự án (vd acs_report/urls.py), include như sau:

    from django.urls import path, include
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('home.urls')),          # trang chủ + phân quyền
        # path('reports/', include('reports.urls')),   # app nghiệp vụ
    ]
"""

from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),

    # Demo tìm kiếm (tham khảo, có thể xóa khi không cần)
    path('demo/search-client/', views.demo_search_client, name='demo_search_client'),
    path('demo/search-server/', views.demo_search_server, name='demo_search_server'),
    path('demo/live-search/', views.demo_live_search, name='demo_live_search'),
    path('api/live-search/', views.live_search_api, name='live_search_api'),
]