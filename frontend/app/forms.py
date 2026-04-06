from django import forms
from .models import User

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'})
    )


    class Meta:
        model = User
        fields = ['first_name', 'email', 'image']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter first name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter email'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control mb-3'}),
        }
        labels = {
            'first_name': 'Full Name',
            'email': 'Email Address',
            'image': 'Profile Image (Optional)',
        }

    def clean(self):
        cleaned_data = super().clean()

        
        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'image']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
