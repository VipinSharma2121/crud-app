import pandas as pd
import openpyxl
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
import requests

API_URL = 'http://localhost:8000'

def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            # Form valid, but AJAX handled in template - just re-render if needed
            pass
    else:
        form = CustomUserCreationForm()
    return render(request, 'create_user.html', {'form': form})

def user_list(request):
    try:
        response = requests.get(f'{API_URL}/users/')
        response.raise_for_status()
        users_data = response.json()
        users = []
        for u in users_data:
            users.append({
                'id': u[0],
                'first_name': u[1],
                'email': u[2],
                'image_url': u[4] if len(u) > 4 and u[4] else None,
            })
    except Exception as e:
        print(f'API error: {e}')
        users = []
    return render(request, 'user_list.html', {'users': users})

def dashboard(request):
    try:
        response = requests.get(f'{API_URL}/users/')
        response.raise_for_status()
        users_data = response.json()
        users_list = [{'pk': u[0], 'first_name': u[1], 'email': u[2], 'image': u[4].replace('media/', '') if len(u) > 4 and u[4] else None} for u in users_data]
        total_users = len(users_list)
        users_with_images = len([u for u in users_list if u['image']])
    except Exception:
        users_list = []
        total_users = 0
        users_with_images = 0
    context = {
        'users': users_list,
        'total_users': total_users,
        'users_with_images': users_with_images,
    }
    return render(request, "dashboard.html", context)

def download_excel(request):
    try:
        response = requests.get(f'{API_URL}/users/')
        response.raise_for_status()
        users_data = response.json()
        df = pd.DataFrame(users_data, columns=['id', 'first_name', 'email', 'password', 'image_url'])
        df = df[['first_name', 'email', 'image_url']]
        df.columns = ['First Name', 'Email', 'Image URL']
    except Exception:
        df = pd.DataFrame(columns=['First Name', 'Email', 'Image URL'])
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Users', index=False)
    output.seek(0)
    response_obj = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response_obj['Content-Disposition'] = 'attachment; filename="users.xlsx"'
    return response_obj

def upload_excel(request):
    messages.info(request, 'Upload Excel via Backend API or download template first.')
    return render(request, 'upload.html')


def edit_user(request, pk):
    API_URL = 'http://localhost:8000'
    if request.method == 'POST':
        try:
            data = {k: v for k, v in request.POST.items() if k in ['first_name', 'email']}
            files = request.FILES or None
            response = requests.put(
                f'{API_URL}/users/{pk}',
                data=data,
                files={'image': files.get('image')} if files and 'image' in files else None
            )
            response.raise_for_status()
            messages.success(request, 'User updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating user: {str(e)}')
        return redirect('dashboard')
    
    # GET: Prefill edit form - fetch user data
    try:
        response = requests.get(f'{API_URL}/users/')
        response.raise_for_status()
        users_data = response.json()
        user_data = next((u for u in users_data if u[0] == pk), None)
        if user_data:
            context = {'pk': pk, 'user': {'first_name': user_data[1], 'email': user_data[2]}}
        else:
            raise ValueError('User not found')
    except:
        context = {'pk': pk}
    
    return render(request, 'edit_user.html', context)


def delete_user(request, pk):
    if request.method == 'POST':
        try:
            API_URL = 'http://localhost:8000'
            response = requests.delete(f'{API_URL}/users/{pk}')
            response.raise_for_status()
            messages.success(request, 'User deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting user: {str(e)}')
        return redirect('dashboard')
    return redirect('dashboard')
