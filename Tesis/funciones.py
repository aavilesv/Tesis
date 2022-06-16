from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.utils.timezone import now
from io import BytesIO
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from Tesis.config import LOGO_SISTEMA, NOMBRE_SISTEMA, NOMBRE_AUTOR, NOMBRE_INSTITUCION
from Seguridad.models import ModuloGrupo
from delivery.models import T_Pedido

'''
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

'''
def render_to_pdf(template_src, context_dict={}):
    template_path = template_src
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context_dict)


    # create a pdf
    pisa_status = pisa.CreatePDF(
       html.encode('UTF-8'), dest=response, encoding='UTF-8')
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def addUserData(request, data):
    data['hoy'] = now
    data['usuario'] = request.user
    data['logo'] = LOGO_SISTEMA
    data['sistema'] = NOMBRE_SISTEMA
    data['institucion'] = NOMBRE_INSTITUCION
    data['autor'] = NOMBRE_AUTOR
    data['grupos'] = ModuloGrupo.objects.filter(grupos__in=request.user.groups.all()).order_by('prioridad')

    data['facturacion'] = False
    if T_Pedido.objects.filter(status=True).exists():
        segurid = User.groups.through.objects.get(user_id=request.user.id)
        if segurid.group.name == 'Gerente':
            data['truepedidos'] = T_Pedido.objects.filter(status=True)
            data['facturacion']=True
    data['grupo'] = request.user.groups.all()[0]



class MiPaginador(Paginator):
    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True, rango=1):
        super(MiPaginador, self).__init__(object_list, per_page, orphans=orphans,
                                          allow_empty_first_page=allow_empty_first_page)
        self.rango = rango
        self.paginas = []
        self.primera_pagina = False
        self.ultima_pagina = False

    def rangos_paginado(self, pagina):
        left = pagina - self.rango
        right = pagina + self.rango
        if left < 1:
            left = 1
        if right > self.num_pages:
            right = self.num_pages
        self.paginas = range(left, right + 1)
        self.primera_pagina = True if left > 1 else False
        self.ultima_pagina = True if right < self.num_pages else False
        self.ellipsis_izquierda = left - 1
        self.ellipsis_derecha = right + 1