from django.contrib import admin
from .models import Users
from .forms import UserChangeForm, UserCreationForms
from django.contrib.auth import admin as admin_auth_django

#admin.site.register(Users)

@admin.register(Users)
class UsersAdmin(admin_auth_django.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForms
    model = Users
    fieldsets = admin_auth_django.UserAdmin.fieldsets + (
        ('Informações residenciais', {'fields': ('rua', 'numero', 'cep')}),
    )
    readonly_fields = ('rua','numero', 'cep')