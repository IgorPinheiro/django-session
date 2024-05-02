from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from hashlib import sha256
from django.contrib import messages, auth
from django.contrib.messages import constants
from django.contrib.auth.models import User



def login(request):
    if request.user.is_authenticated:
        return redirect('/plataforma/home')
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})

def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/plataforma/home')
    status = request.GET.get('status')
    return render(request, 'cadastro.html',{'status': status})

def valida_cadastro(request):
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    rua = request.POST.get('rua')
    numero = request.POST.get('numero')
    cep = request.POST.get('cep')

    # Teste de nome ou email sem carictere.
    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencher nome e email corretamente, não pode ficar vazio.')
        return redirect('/auth/cadastro/')
    
    # Teste do tamanho da senha
    if len(senha) < 8:
        messages.add_message(request, constants.ERROR, 'Prencher senha maior que 7 digitos!')
        return redirect('/auth/cadastro/')
    
    
    # Passando o teste do email.
    if User.objects.filter(email = email).exists():
        messages.add_message(request, constants.ERROR, 'Email já cadastrado')
        return redirect('/auth/cadastro/')
    
    if User.objects.filter(username = nome).exists():
        messages.add_message(request, constants.ERROR, 'Já existe um usuário com este nome!')
        return redirect('/auth/cadastro/')
    
    # Testando e se passar gravando no db com a senha criptografada.
    try:

        usuario = User.objects.create_user(username = nome, 
                                           email = email, 
                                           password = senha)
        usuario.save()

        usuario_endereco = UsuarioEndereco(rua = rua, 
                                           numero = numero, 
                                           cep = cep, 
                                           usuario = usuario)
        usuario_endereco.save()

        messages.add_message(request, constants.SUCCESS, 'Usuário Cadastrado com scuesso')
        return redirect('/auth/login/')
    
    except:
        messages.add_message(request, constants.ERROR, 'Erro interno do sitema')
        return redirect('/auth/cadastro/')
    


def valida_login(request):
    nome = request.POST.get('nome')
    senha = request.POST.get('senha')
    
    usuario = auth.authenticate(request, username = nome, password = senha)
    
    if not usuario:
        messages.add_message(request, constants.WARNING, 'Email ou Senha Inválido')
        return redirect('/auth/login/')
    
    else :
        auth.login(request, usuario)
        return redirect('/plataforma/home/')
    
def sair(request):
    auth.logout(request)
    #return HttpResponse(request.session.get_expiry_age())
    #return HttpResponse(request.session.get_expiry_date())
    #request.session.flush()
    messages.add_message(request, constants.WARNING, 'Faça login antes de acessar a plataforma')
    return redirect('/auth/login/')