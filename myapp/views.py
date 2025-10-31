from django.shortcuts import render, redirect
from . import models, codes
from datetime import datetime, date
from django.contrib import messages

def index(request):
    return render(request, 'page.html')


def input_date(request):
    if request.method == "POST":
        date = request.POST['date']
        
        if(date == ""):
            messages.error(request, "please entert the date", extra_tags="date")
            return redirect('/')
        
        
        
        return redirect('/')
    return redirect('/')