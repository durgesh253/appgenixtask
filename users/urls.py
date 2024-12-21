from django.urls import path
from . import views

urlpatterns = [
    # User-related views
    path('signup/', views.UserCreateView.as_view(), name='user-create'),
    path('update/', views.UserUpdateView.as_view(), name='user-update'),
    path('delete/', views.UserDeleteView.as_view(), name='user-delete'),
    
    # Post-related views
    path('create-post/', views.PostCreateView.as_view(), name='post-create'),
    
    # Forgot Password and Reset Password
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset-password'),
    
    # Login (For generating JWT tokens)
    path('login/', views.login, name='login'),
]
