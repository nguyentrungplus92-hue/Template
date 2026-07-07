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
    path('set-language/', views.set_language, name='set_language'),

    # Demo tìm kiếm (tham khảo, có thể xóa khi không cần)
    path('demo/search-client/', views.demo_search_client, name='demo_search_client'),
    path('demo/search-server/', views.demo_search_server, name='demo_search_server'),
    path('demo/live-search/', views.demo_live_search, name='demo_live_search'),
    path('api/live-search/', views.live_search_api, name='live_search_api'),
    
    # Demo gridview (tham khảo, có thể xóa)
    path('demo/grid/', views.demo_grid_display, name='demo_grid_display'),
    path('demo/grid-crud/', views.demo_grid_crud, name='demo_grid_crud'),
    path('demo/grid-editable/', views.demo_grid_editable, name='demo_grid_editable'),
    path('demo/grid-export/', views.grid_export, name='grid_export'),

    # Form Thêm/Sửa (dùng chung 1 view)
    path('demo/route/add/', views.route_form, name='route_add'),
    path('demo/route/<int:pk>/edit/', views.route_form, name='route_edit'),
]