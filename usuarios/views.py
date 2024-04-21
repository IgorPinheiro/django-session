from django.shortcuts import render
from django.http import HttpResponse
from .models import Usuario
from django.shortcuts import redirect
from hashlib import sha256
from django.contrib import messages
from django.contrib.messages import constants


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
        messages.add_message(request, constants.ERROR, 'Preencher nome e email corretamente, não pode ficar vazio.')
        return redirect('/auth/cadastro/')
    
    # Teste do tamanho da senha
    if len(senha) < 8:
        messages.add_message(request, constants.ERROR, 'Prencher senha maior que 7 digitos!')
        return redirect('/auth/cadastro/')
    
    # Testando e-mail, se é igual ao que já existe no db. 
    usuario = Usuario.objects.filter(email = email)
    
    # Passando o teste do email.
    if len(usuario) > 0:
        messages.add_message(request, constants.ERROR, 'Email já cadastrado')
        return redirect('/auth/cadastro/')
    
    # Testando e se passar gravando no db com a senha criptografada.
    try:
        senha = sha256(senha.encode()).hexdigest()
        usuario = Usuario(nome = nome, email = email, senha = senha)

        usuario.save()
        messages.add_message(request, constants.SUCCESS, 'Usuário Cadastrado com scuesso')
        return redirect('/auth/cadastro/')
    
    except:
        messages.add_message(request, constants.ERROR, 'Erro interno do sitema')
        return redirect('/auth/cadastro/')
    


def valida_login(request):
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    senha = sha256(senha.encode()).hexdigest()

    usuario = Usuario.objects.filter(email = email).filter(senha = senha)


    if len(usuario) == 0:
        messages.add_message(request, constants.WARNING, 'Email ou Senha Inválido')
        return redirect('/auth/login/')
    
    elif len(usuario) > 0:
        request.session['logado'] = True
        request.session['usuario_id'] = usuario[0].id
        return redirect('/plataforma/home/')
    
def sair(request):
    #return HttpResponse(request.session.get_expiry_age())
    #return HttpResponse(request.session.get_expiry_date())
    request.session.flush()
    messages.add_message(request, constants.WARNING, 'Faça login antes de acessar a plataforma')
    return redirect('/auth/login/')