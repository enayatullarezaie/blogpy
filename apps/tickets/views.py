from django.shortcuts import render, redirect
from .forms import *
# Create your views here.



def get_tickets(request):
   tickets= Ticket.objects.all().order_by("-created_at")
   return render(request, 'tickets/index.html', context={"tickets": tickets, "title": "tickets"})


def add_ticket(request):
   ticket=TicketForms(request.POST)

   if request.method == "POST":
      ticket.save()
      return redirect("/tickets/")
   
   if request.method == "GET":
      title = request.GET.get("title")
      body = request.GET.get("body")
      if title and body :
         new_ticket = Ticket.objects.create(title= title, body=body)
         new_ticket.save()
         return redirect("/tickets/")

   
   return render(request, 'tickets/add_ticket.html', context={"form": ticket})