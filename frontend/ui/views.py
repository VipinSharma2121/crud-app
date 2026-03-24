import requests
from django.shortcuts import render
from django.contrib import messages

def create_user(request):
    if request.method == "POST":
        try:
            data = {
                "username": request.POST.get('username'),
                "address": request.POST.get('address'),
                "email": request.POST.get('email'),
                "password": request.POST.get('password'),
            }

            files = {}
            if 'image' in request.FILES:
                files['image'] = request.FILES['image']

            response = requests.post(
                "http://127.0.0.1:8000/users/",
                data=data,
                files=files
            )

            if response.status_code == 200:
                messages.success(request, "User created successfully!")
            else:
                messages.error(request, f"API error: {response.status_code} - {response.text}")

        except Exception as e:
            messages.error(request, f"Error creating user: {str(e)}")

    return render(request, "create.html")