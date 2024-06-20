from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='catalog'),
    path('search/', views.ProductListView.as_view(), name='search'),
    path('<slug:arc_slug>/', views.ProductDetailView.as_view(), name='catalog_detail'),
    path('category/<slug:slug>/', views.ProductByCategory.as_view(), name='catalog_by_category'),
    path('product/<slug:arc_slug>/comments/create/', views.CommentCreateView.as_view(), name='comment_create_view'),
    path('comment/<int:comment_id>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('tag/<slug:tag_slug>/', views.ProductTagView.as_view(), name='tag'),
]