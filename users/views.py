# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# Получаем нашу кастомную модель User
User = get_user_model()

def register(request):
    """
    Представление для регистрации нового пользователя.
    """
    if request.method == 'POST':
        # Используем форму, которая знает о нашей кастомной модели
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Автоматически логиним пользователя после регистрации
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})