from typing import Any
from . models import *
from django import forms
from django.core.exceptions import ValidationError
from apps.tickets.models import Ticket


FAVORITE_COLOR = [
   ("blue", "Blue"),
   ("green", "Green"),
   ("red", "Red"),
   ("grey", "Grey"),
]

class ContactForms(forms.Form):
   fullname= forms.CharField(max_length=32, label="fullname")
   title= forms.CharField(max_length=32, label="title")
   text= forms.CharField(max_length=128, label="text")
   date= forms.DateField( label="date",widget=forms.SelectDateWidget(attrs={'class':'form-control'}))
   food= forms.ChoiceField( label="food", choices=FAVORITE_COLOR)
   colors= forms.MultipleChoiceField(
      label= "colors",
      widget= forms.CheckboxSelectMultiple(),
      choices= FAVORITE_COLOR
   )

   def clean(self):
      title = self.cleaned_data.get("title")
      text = self.cleaned_data.get("text")
      if "a" in text :
         self.add_error("text", error="not  a  in field must be.  belive me")
      
      if title == text :
         raise ValidationError("you had some err", code="same_text")

   
   def clean_title(self):
      title = self.cleaned_data.get("title")
      if "a" in title :
         raise ValidationError("you had bad text", code="bad_text")
      return title
   


class TicketForm(forms.ModelForm):
   class Meta:
      model= Ticket  
      fields= "__all__"
      widgets={
         "title ": forms.TextInput(attrs={"class": "title form-control"})
      }





