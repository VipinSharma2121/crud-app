from django.contrib import messages
from django.shortcuts import render, redirect
import requests

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import User

# ✅ CREATE USER
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully!')
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'create_user.html', {'form': form})

# ✅ USER LIST (STANDALONE ORM)
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})
