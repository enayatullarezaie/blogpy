from django.urls import path
from . import views


urlpatterns = [
   path("" , views.get_tickets, name="tickets"),
   path("add-ticket" , views.add_ticket, name="add-ticket"),
]