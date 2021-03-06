from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita

def cadastro(request):
    """Cadastra uma nova pessoa no sistema"""
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']

        if campo_vazio(nome):
            messages.error(request, 'O campo email deve ser preenchido')
            return redirect('cadastro')

        if campo_vazio(email):
            messages.error(request, 'O campo email deve ser preenchido')
            return redirect('cadastro')

        if senha_diferente(senha, senha2):
            messages.error(request, 'Senhas não conferem')
            return redirect('cadastro')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado')
            return redirect('cadastro') 

        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Nome já cadastrado')
            return redirect('cadastro') 

        user = User.objects.create_user(username=nome,email=email, password=senha)
        user.save()
        messages.success(request, 'Cadastro realizado com sucesso')

        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, 'Preencha os campos')
            return redirect('login')
        
        if verifica_usuario(email):
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Dados invalidos')
            return redirect('login')        

    return render(request, 'usuarios/login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=id)

        dados = {
            'receitas': receitas
        }
        
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')

def campo_vazio(campo):
    return not campo.strip()

def senha_diferente(senha, senha2):
    return senha != senha2
    
def verifica_usuario(email):
    return User.objects.filter(email=email).exists()

