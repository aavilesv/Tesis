from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy



from Tesis.funciones import addUserData
@login_required(login_url='/seguridad/login/')
def index(request):
    data = {
        'titulo': 'Empresa -FULL AUTO MILAGRO',
        'name': 'Inicio',
        'saludo': 'Bienvenido',
    }
    addUserData(request,data)
    return render(request, 'main/index.html', data)





def login_session(request):
    data = {'titulo': 'Inicio de sesión - Susanita'}
    success_url = reverse_lazy('index')
    if request.user.is_authenticated:
         return HttpResponseRedirect(success_url)
    if request.method == 'POST':
        print(request.POST)
        user = authenticate(username=request.POST['username'],password=request.POST['password'])
        data['resp'] = False
        if user is not None:
            if user.is_active:
                login(request, user)
                data['resp'] = True
                data['user'] = user.username

            else:
                data['error'] = 'Usuario no esta Activo'
        else:
            data['error'] = 'El Usuario es Incorrecto'
        return JsonResponse(data)
    else:
        data['sistema'] = 'TALLER HERRERA'
        data['logo'] = "fas fa-spinner fa-spin"
        data['ruta']='/seguridad/login/'
        data['institucion'] = 'CAROLINA HERRERA'
        return render(request, 'seguridad/login.html', data)


def logout_user(request):
    logout(request)
    return redirect('/seguridad/login/')