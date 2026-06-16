from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view()),
    path('<int:pk>/', views.ProductDetailView.as_view()),
    path('<int:pk>/add_review/', views.AddReviewView.as_view()),
    path('<int:pk>/delete_review/', views.DeleteReviewView.as_view()),
    path('<int:pk>/toggle_favourite/', views.ToggleFavouriteView.as_view()),
    path('favourites/', views.FavouritesListView.as_view()),
    path('categories/', views.CategoryListView.as_view()),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view()),
]
