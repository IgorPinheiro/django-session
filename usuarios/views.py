from django.shortcuts import render
from django.http import HttpResponse
from .models import Usuario
from django.shortcuts import redirect
from hashlib import sha256


def login(request):
    return render(request, 'login.html')

def cadastro(request):
    
    return render(request, 'cadastro.html')

def valida_cadastro(request):
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    # Teste de nome ou email sem carictere.
    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        return redirect('/auth/login/?status=1')
    
    # Teste do tamanho da senha
    if len(senha) < 8:
        return redirect('/auth/login/?status=2')
    
    # Testando e-mail, se é igual ao que já existe no db. 
    usuario = Usuario.objects.filter(email = email)
    
    # Passando o teste do email.
    if len(usuario) > 0:
        return redirect('/auth/login/?status=3')
    
    # Testando e se passar gravando no db com a senha criptografada.
    try:
        senha = sha256(senha.encode()).hexdigest()
        usuario = Usuario(nome = nome, email = email, senha = senha)

        usuario.save()
        return redirect('/auth/login/?status=0')
    
    except:
        return redirect('/auth/login/?status=4')