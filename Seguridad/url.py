from django.urls import path

from Seguridad.views import  login_session,logout_user
from Seguridad.viewrecuperar import recuperar
from Seguridad.perfil import perfil
from Seguridad.view_registroperfil import  registro
urlpatterns = [
path('login/' ,login_session ,name='login'),
path('logout/', logout_user ,name='logout'),
path('recuperar/', recuperar ,name='recuperar'),
path('perfil/', perfil ,name='perfil'),
path('registro/', registro ,name='registro'),

]