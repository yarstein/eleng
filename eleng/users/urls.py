from django.urls import path
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


from . import views

app_name = "users"

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('password-change/', views.UserPasswordChange.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(
                        template_name='users/password_change_done.html'),
                        name='password_change_done'),
    path('password-reset/', PasswordResetView.as_view(
                        template_name='users/password_reset_form.html', 
                        email_template_name="users/password_reset_email.html",
                        success_url=reverse_lazy("users:password_reset_done")), name="password_reset"),
    path('password-reset/done/', PasswordResetDoneView.as_view(
                        template_name='users/password_reset_done.html'),
                        name="password_reset_done"),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
                        template_name="users/password_reset_confirm.html",
                        success_url=reverse_lazy("users:password_reset_complete")),
                        name="password_reset_confirm"),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(
                        template_name="users/password_reset_complete.html"), name="password_reset_complete"),
    
    path('invalid_verify/', TemplateView.as_view(template_name='users/invalid_verify.html'), name='invalid_verify'),
    path('verify_email/<uidb64>/<token>/', views.EmailVerify.as_view(), name='verify_email'),
    path('confirm_email/', TemplateView.as_view(template_name='users/confirm_email.html'), name='confirm_email'),

    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
]