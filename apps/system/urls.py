from django.urls import path
from . import views, views_instructor, views_menu, views_permission, views_group, views_home

app_name = 'system'
urlpatterns = [
    path('home/profile/', views_home.InstructorProfileView.as_view(), name='home-profile'),
    path('home/login_pwd_change/', views_home.LoginPwdChangeView.as_view(), name='home-login_pwd_change'),
    path('home/private_pwd_change/', views_home.PrivatePwdChangeView.as_view(), name='home-private_pwd_change'),

    path('', views.IndexView.as_view(), name='system-index'),
    path('instructor/', views_instructor.InstructorView.as_view(), name='instructor'),
    path('instructor/list/', views_instructor.InstructorListView.as_view(), name='instructor-list'),
    path('instructor/create/', views_instructor.InstructorCreateView.as_view(), name='instructor-create'),
    path('instructor/update/', views_instructor.InstructorUpdateView.as_view(), name='instructor-update'),
    path('instructor/password_change/', views_instructor.PasswordChangeView.as_view(),
         name='instructor-password-change'),
    path('instructor/delete/', views_instructor.InstructorDeleteView.as_view(), name='instructor-delete'),
    path('instructor/enable/', views_instructor.InstructorEnableView.as_view(), name='instructor-enable'),
    path('instructor/disable/', views_instructor.InstructorDisableView.as_view(), name='instructor-disable'),

    path('menu/', views_menu.MenuView.as_view(), name='menu'),
    path('menu/edit/', views_menu.MenuEditView.as_view(), name='menu-edit'),
    path('menu/delete/', views_menu.MenuDeleteView.as_view(), name='menu-delete'),
    path('menu/list/', views_menu.MenuListView.as_view(), name='menu-list'),

    path('permission/', views_permission.PermissionView.as_view(), name='permission'),
    path('permission/edit/', views_permission.PermissionEditView.as_view(), name='permission-edit'),
    path('permission/delete/', views_permission.PermissionDeleteView.as_view(), name='permission-delete'),
    path('permission/list/', views_permission.PermissionListView.as_view(), name='permission-list'),

    path('group/', views_group.GroupView.as_view(), name='group'),
    path('group/edit/', views_group.GroupEditView.as_view(), name='group-edit'),
    path('group/delete/', views_group.GroupDeleteView.as_view(), name='group-delete'),
    path('group/list/', views_group.GroupListView.as_view(), name='group-list'),
    path('group/group2instructor/', views_group.Group2InstructorView.as_view(), name="group-group2instructor"),
    path('group/group2menu/', views_group.Group2MenuView.as_view(), name="group-group2menu"),
    path('group/group2menu_list/', views_group.Group2MenuListView.as_view(), name="group-group2menu_list"),
    path('group/group2permission/', views_group.Group2PermissionView.as_view(), name="group-group2permission"),
    # path('demo/', views.demo, name='system-demo'),
    # path('demoview1/', permission_required('base.add_department')(views.DemoView.as_view()), name='viewAssetHistory'),
    # path('demoview2/', permission_required('base.change_department')(views.DemoView.as_view()),
    #     name='viewAssetHistory'),
]
