from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from core.forms import UserProfileForm
from user_profile.models import UserProfile , City
# from .forms import PhoneLoginForm  # Optional if using custom form


def home(request):

    return render(request,'dashboard.html')



def phone_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Could be phone or username
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect based on role (optional)
            
            return redirect('admin_dashboard')
            
            error = "Invalid phone number or password"
            return render(request, 'account/login.html', {'error': error})
    
    return render(request, 'account/login.html')


def user_list(request):
    # Get all users (or filter based on role, etc.)
    users = UserProfile.objects.all().order_by('-date_joined')  # Example: newest first
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} created successfully!')
            return redirect('users_list')  # Replace with your actual redirect URL
    else:
        print(form.errors)
        form = UserProfileForm()
    
    context = {
        'form': form,
        'cities': City.objects.all(),
        'users': users
    }
    # Pass users to the template
    return render(request, 'user_list.html',context)