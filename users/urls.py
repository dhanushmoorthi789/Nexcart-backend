from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('profile/', views.ProfileView.as_view()),
    path('change-password/', views.ChangePasswordView.as_view()),
    # Admin
    path('admin/users/', views.AdminUserListView.as_view()),
    path('admin/users/<int:pk>/', views.AdminUserDetailView.as_view()),
    path('admin/users/<int:pk>/toggle_active/', views.AdminToggleActiveView.as_view()),
    path('admin/users/<int:pk>/toggle_admin/', views.AdminToggleAdminView.as_view()),
]
