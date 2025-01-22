from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Message, ChatRoom
from django.db.models import Q

def home_view(request):
    if request.user.is_authenticated:
        return redirect('chat:index')
    return redirect('chat:login')

@login_required
def index(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/index.html', {
        'users': users,
        'current_user': request.user
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('chat:index')
        
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('chat:index')
    else:
        form = AuthenticationForm()
    return render(request, 'chat/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('chat:login')

def register(request):
    if request.user.is_authenticated:
        return redirect('chat:index')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat:index')
    else:
        form = UserCreationForm()
    return render(request, 'chat/register.html', {'form': form})

@login_required
def room(request, user_id):
    other_user = User.objects.get(id=user_id)
    users = User.objects.exclude(id=request.user.id)
    
    # Get messages between the two users
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')
    
    # Create a unique room name using sorted user IDs
    room_name = f"{min(request.user.id, other_user.id)}_{max(request.user.id, other_user.id)}"
    
    return render(request, 'chat/room.html', {
        'other_user': other_user,
        'users': users,
        'messages': messages,
        'room_name': room_name
    })