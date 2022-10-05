from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name="register_user"),
    path('activate/<uidb64>/<token>/', views.activate_user, name='activate_user'),
    path('login/', views.login_user, name="login_user"),
    
    path('forgot_pasword/', views.forgot_password, name="forgot_pasword"),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    # path('resetPassword/', views.resetPassword, name='reset_password'),
]