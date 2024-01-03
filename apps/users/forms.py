from .models import *
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.core import validators
from django.utils.translation import gettext_lazy as _

class UserEditForm(forms.ModelForm):
   class Meta:
      model= User
      fields= "__all__"
      
      
# this uses in login
def startWithZero(string):
   if string[0] != "0" :
      raise ValidationError(
         message=_("value %(value)s doesn't start with zero"),
         code="invalid",
         params={"value":string}
      )

class UserCreationForm(forms.ModelForm):
   """A form for creating new users. Includes all the required."""
   password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
   password2 = forms.CharField(label="Password confirm", widget=forms.PasswordInput)

   class Meta:
      model = User
      fields = ["username", "phone_number", "email"]
   
   # form.is_valid() runs clean_[fieldname] function
   # function clean_[fieldname] is for field validation 
   def clean_username(self):
      print("RUN clean_username")
      username = self.cleaned_data.get("username")
      if username:
         if User.objects.filter(username=username).first() :
            raise ValidationError("username %(value)s is exist", code="invalid", params={"value": username})
         return username
      
   def clean_phone_number(self):
      print("RUN clean_phone_number")
      phone_number = self.cleaned_data.get("phone_number")
      if phone_number:
         if len(phone_number) > 13 or len(phone_number) < 11:
            raise ValidationError("phone %(value)s is invalid", code="invalid", params={"value": phone_number})
         elif not phone_number[0:2] == "09":
            raise ValidationError("phone %(value)s is invalid", code="invalid", params={"value": phone_number})
         elif User.objects.filter(phone_number=phone_number).first():
            raise ValidationError("phone %(value)s is exist", code="invalid", params={"value": phone_number})
         return phone_number
      
   def clean_email(self):
      print("RUN clean_email")
      email = self.cleaned_data.get("email")
      if email:
         if User.objects.filter(email=email).first():
            raise ValidationError("email %(value)s is exist", code="invalid", params={"value": email})
         return email
   
   def clean_password2(self):
      print("RUN clean_password2")
      # Check that the two password entries match
      password1 = self.cleaned_data.get("password1")
      password2 = self.cleaned_data.get("password2")
      if password1 and password2 and password1 != password2:
         raise ValidationError("Passwords don't match")
      return password2

   # form.save() runs this function
   def save(self, commit=True):
      print("RUN save()")
      # Save the provided password in hashed format
      user = super().save(commit=False)
      user.set_password(self.cleaned_data["password1"])
      if commit:
         user.save()
      return user


class UserChangeForm(forms.ModelForm):
   """A form for updating users. Includes all the fields """
   password = ReadOnlyPasswordHashField()
   class Meta:
      model = User
      fields = ["email", "password", "date_of_birth", "is_active", "is_staff"]





