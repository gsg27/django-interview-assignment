from django.contrib import admin

from LibraryApp.models import Books, User

# Register your models here.
admin.site.register(User)
admin.site.register(Books)
