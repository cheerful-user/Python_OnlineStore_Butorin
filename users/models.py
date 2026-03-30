from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Кастомная модель пользователя.
    Наследуемся от AbstractUser, чтобы сохранить все стандартные поля (username, email, password).
    """

    def __str__(self):
        # Возвращаем username для отображения в админке
        return self.username