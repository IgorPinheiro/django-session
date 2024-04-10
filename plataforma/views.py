from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

def home(request):
    if request.session['logado']:
        return HttpResponse('Você está no sistema')
    else:
        return redirect('/auth/login/?status=2')
