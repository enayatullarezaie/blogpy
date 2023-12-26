from .models import *
from django  import forms


class TicketForms(forms.ModelForm):
   class Meta:
      model= Ticket
      fields= ("title", "body")