from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from movies.models import *

class UsersInLine(admin.StackedInline):
    model=Users
    can_delete = False
    verbose_name: 'Users'
    
class CustomizedUserAdmin(UserAdmin):
    inlines=(UsersInLine,)

admin.site.unregister(User)
admin.site.register(User,CustomizedUserAdmin)

admin.site.register(Views)
admin.site.register(Ratings)
admin.site.register(Movie)
admin.site.register(Users)
admin.site.register(Catalog)
admin.site.register(Categories)
admin.site.register(Languages)
admin.site.register(Actor)
admin.site.register(Actress)
admin.site.register(Director)
admin.site.register(Cat_list)
admin.site.register(Lang_list)
admin.site.register(Contact)