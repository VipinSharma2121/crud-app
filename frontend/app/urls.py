from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_user, name='create_user'),
    path('users/', views.user_list, name='user_list'),
    path('upload-excel/', views.upload_excel, name='upload_excel'),
    path('download-excel/', views.download_excel, name='download_excel'),
    path('edit-user/<int:pk>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:pk>/', views.delete_user, name='delete_user'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

