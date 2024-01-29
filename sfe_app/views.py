from django.shortcuts import render, redirect
from django.http import HttpResponse
from sfe_app.forms import *
from django.contrib import messages

# Create your views here.

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def contact(request):
  return render(request, 'contact.html')


def support(request):
  
  if request.method == 'POST':
    
    form = SupportForm(request.POST)
    
    if form.is_valid():
      form.save()
      messages.success(request, 'Your mesage has been send')
      return redirect('home')
    
    else:
      messages.error(request, 'Correct the messages below')
      
  else:
    form = SupportForm()
    
  return render(request, 'support.html', {'form': form})




      

