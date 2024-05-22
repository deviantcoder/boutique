from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Profile, ProfileImage
from django.forms.models import inlineformset_factory


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
            self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First name'})
            self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last name'})
            self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
            self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
            self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password Confirmation'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            # 'image'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

ProfileImageFormSet = inlineformset_factory(Profile, ProfileImage, fields=('image',))
