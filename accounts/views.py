from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . models import ContactForm


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    user = request.POST.get('user')
    password = request.POST.get('password')

    user_login = auth.authenticate(request, username=user, password=password)

    if not user_login:
        messages.error(request, 'Invalid username or password.')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user_login)
        messages.success(request, 'You are now logged in.')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('login')


def register(request):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')

    name = request.POST.get('name')
    surname = request.POST.get('surname')
    email = request.POST.get('email')
    user = request.POST.get('user')
    password = request.POST.get('password')
    conf_pass = request.POST.get('conf_pass')

    if not name or not surname or not email or not user or not password or not conf_pass:
        messages.error(request, "Form fields cannot be empty.")

    try:
        validate_email(email)
    except:
        messages.error(request, 'Invalid email.')
        return render(request, 'accounts/register.html')

    if len(password) < 6:
        messages.error(request, 'Password must be at least 6 characters long.')
        return render(request, 'accounts/register.html')

    if len(user) < 6:
        messages.error(request, 'User must be at least 6 characters long.')
        return render(request, 'accounts/register.html')

    if password != conf_pass:
        messages.error(request, 'Passwords do not match.')
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=user).exists():
        messages.error(request, 'User already exists.')
        return render(request, 'accounts/register.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email already exists.')
        return render(request, 'accounts/register.html')

    messages.success(request, 'Success! You can now login')

    user = User.objects.create_user(username=user, email=email, password=password, first_name=name, last_name=surname)
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = ContactForm()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = ContactForm(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Error submiting form.')
        form = ContactForm(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    description = request.POST.get('description')

    if len(description) < 5:
        messages.error(request, 'Description must have more than 5 characters')
        form = ContactForm(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(request, f'Contact {request.POST.get("name")} saved.')
    return redirect('dashboard')