from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve
from system.views import IndexView, LoginView, LogoutView, mytest
from tools import views as tools_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='temp-index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('system/', include('system.urls')),
    path('base/', include('base.urls', namespace='base')),
    path('attendance/', include('attendance.urls', namespace='attendance')),

    path('mytest/', mytest),

]
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
]
