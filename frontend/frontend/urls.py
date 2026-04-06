from django.contrib import admin
from django.urls import path, include
from .views import user_list, create_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('users/', user_list),
    path('', create_user, name="create_user"),
    path('users/', user_list, name="user_list"),

]
