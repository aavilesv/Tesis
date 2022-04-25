from django.urls import path
from compra.views_compra import compra
urlpatterns = [
    path('compra/' ,compra ,name='compra'),
]