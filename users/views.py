from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm, ProfileForm, ProfileImageFormSet
from django.contrib.auth.decorators import login_required
from .models import Profile, ProfileImage
from django.db.utils import IntegrityError
from django.contrib import messages
from cart.models import Order


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
            messages.success(request, f'Welcome back, {username}')
            return redirect(request.GET.get('next') if 'next' in request.GET else 'home_page')

    context = {
        'is_login_page': is_login_page,
        'page': page,
    }

    return render(request, 'users/login_register.html', context)


def logout_user(request):
    logout(request)
    messages.info(request, 'Logged out')
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


@login_required(login_url='login_user')
def profile(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    orders = user_profile.order_set.filter(is_ordered=True)

    context = {
        'profile': user_profile,
        'orders': orders,
    }

    return render(request, 'users/profile.html', context)


@login_required(login_url='login_user')
def edit_profile(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    form = ProfileForm(instance=user_profile)
    formset = ProfileImageFormSet(instance=user_profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        formset = ProfileImageFormSet(request.POST, request.FILES, instance=user_profile)
        if form.is_valid() and formset.is_valid():
            profile = form.save()
            
            formset.instance = profile
            formset.save()

            messages.success(request, 'Profile saved')
            return redirect('profile')
        
    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login_user')
def get_user_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    context = {'order': order}

    return render(request, 'users/order.html', context)
