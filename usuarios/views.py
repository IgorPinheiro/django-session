from django.shortcuts import render
from django.http import HttpResponse
from .models import Usuario
from django.shortcuts import redirect
from hashlib import sha256


def login(request):
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})

def cadastro(request):
    status = request.GET.get('status')
    return render(request, 'cadastro.html',{'status': status})

def valida_cadastro(request):
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    # Teste de nome ou email sem carictere.
    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        return redirect('/auth/cadastro/?status=1')
    
    # Teste do tamanho da senha
    if len(senha) < 8:
        return redirect('/auth/cadastro/?status=2')
    
    # Testando e-mail, se é igual ao que já existe no db. 
    usuario = Usuario.objects.filter(email = email)
    
    # Passando o teste do email.
    if len(usuario) > 0:
        return redirect('/auth/cadastro/?status=3')
    
    # Testando e se passar gravando no db com a senha criptografada.
    try:
        senha = sha256(senha.encode()).hexdigest()
        usuario = Usuario(nome = nome, email = email, senha = senha)

        usuario.save()
        return redirect('/auth/cadastro/?status=0')
    
    except:
        return redirect('/auth/cadastro/?status=4')
    


def valida_login(request):
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    senha = sha256(senha.encode()).hexdigest()

    usuario = Usuario.objects.filter(email = email).filter(senha = senha)


    if len(usuario) == 0:
        return redirect('/auth/login/?status=1')
    
    elif len(usuario) > 0:
        request.session['logado'] = True
        return redirect('/plataforma/home/')
    
def sair(request):
    request.session['logado'] = None
    return redirect('/auth/login/')