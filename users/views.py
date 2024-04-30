from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm


def login_user(request):
    is_login_page = True
    page = 'login'

    if request.user.is_authenticated:
        return redirect('products')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            pass

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next') if 'next' in request.GET else 'home_page')

    context = {
        'is_login_page': is_login_page,
        'page': page,
    }

    return render(request, 'users/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('login_user')


def register_user(request):
    is_register_page = True

    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home_page')

    context = {
        'is_register_page': is_register_page,
        'form': form,
    }

    return render(request, 'users/login_register.html', context)
