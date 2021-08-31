from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('register',views.user_register,name='register'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('add',views.add,name='add_post'),
    path('posts/<str:authors>',views.home_post,name='ghost'),
    path('post',views.all,name='post'),
    path('edit/<int:id>',views.edit_post,name='edit'),
    path ('delete/<int:id>', views.del_post, name='delete'),
    path ('post/<int:id>', views.show, name='show'),
    path('profile',views.profile,name='profile'),
    path ('change_password', views.pass_change, name='password_change'),
    path('about_us',views.about,name='about_us'),
    path('contact_us',views.contra,name='contact_us'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user/reset_password.html'),name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="user/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),
    path('search/',views.search,name='search'),
    # path('login/', auth_views.LoginView.as_view(template_name='user/login.html'),
    #      name='login'),
]
