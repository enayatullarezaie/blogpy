from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.users.models import User
from apps.users.forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
   # The forms to add and change user instances
   form = UserChangeForm
   add_form = UserCreationForm

   # The fields to be used in displaying the User model.
   # These override the definitions on the base UserAdmin
   # that reference specific fields on auth.User.
   list_display = ["username","phone_number", "email", "date_of_birth", "is_staff", "id"]
   list_filter = ["is_staff"]
   fieldsets = [
      (None, {"fields": [ "email", "password", "username", "phone_number"]}),
      ("Personal info", {"fields": ["date_of_birth"]}),
      ("Permissions", {"fields": ["is_staff", "is_superuser", "is_active"]}),
   ]
   # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
   # overrides get_fieldsets to use this attribute when creating a user.
   add_fieldsets = [
      (
         None,
         {
            "classes": ["wide"],
            "fields": ["username", "email", "date_of_birth", "password1", "password2"],
         },
      ),
   ]
   search_fields = ["username"]
   ordering = ["username"]
   filter_horizontal = []

# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

