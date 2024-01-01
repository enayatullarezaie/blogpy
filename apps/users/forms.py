from .models import *
from django import forms


class UserEditForm(forms.ModelForm):
   class Meta:
      model= User
      fields= "__all__"
      





