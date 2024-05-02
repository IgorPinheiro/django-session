from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required


@login_required(login_url = '/auth/login/',)
def home(request):
    return render(request, 'home.html')
    #if request.session.get('logado'):
     #   return render(request, 'home.html') #Nuca colocar / neste código, me confundi o coloquei e estava infomrando o caminho errado.
    #else:
     #   messages.add_message(request, constants.WARNING, 'Erro ao autenticar')
      #  return redirect('/auth/login/')
