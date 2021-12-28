from django.urls import path

from .views import CustomUserDetailView, login_view, logout_view, password_change_view, \
    password_reset_view, password_reset_cofirm_view, registration_view


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('user/', CustomUserDetailView.as_view(), name='user-detail'),
    path('password/change/', password_change_view, name='password-change'),
    path('password/reset/', password_reset_view, name='password-reset'),
    path('password/reset/confirm/', password_reset_cofirm_view, name='password-reset-confirm'),
    path('registration/', registration_view, name='registration'),
]
