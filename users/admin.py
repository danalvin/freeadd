from users.models import User
from django.contrib import admin
from users.models import User
# Register your models here.

@admin.register(User)

class Useradmin(admin.ModelAdmin):
    list_display = ('username', 'rating', 'phone')


