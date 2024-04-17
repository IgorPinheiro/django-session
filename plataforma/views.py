from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

def home(request):
    if request.session.get('logado'):
        return render(request, 'home.html') #Nuca colocar / neste código, me confundi o coloquei e estava infomrando o caminho errado.
    else:
        return redirect('/auth/login/?status=2')
