# -*- coding: utf-8 -*-
from StringIO import StringIO
from datetime import date

from django.http import HttpResponse
from django.contrib import admin

from pyboleto.django.models import Boleto
from pyboleto.pdf import BoletoPDF


def print_boletos(modeladmin, request, queryset):

    buffer = StringIO()
    boleto_pdf = BoletoPDF(buffer)

    for b in queryset:
        b.print_pdf_pagina(boleto_pdf)
        boleto_pdf.nextPage()
    boleto_pdf.save()

    pdf_file = buffer.getvalue()

    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=%s' % (
        u'boletos_%s.pdf' % (
            date.today().strftime('%Y%m%d'),
        ),
    )
    response.write(pdf_file)
    return response
print_boletos.short_description = u'Imprimir Boletos Selecionados'


class BoletoAdmin(admin.ModelAdmin):
    list_display = ('numero_documento',
                    'sacado_nome',
                    'data_vencimento',
                    'data_documento',
                    'valor_documento')
    search_fields = ('numero_documento', 'sacado_nome')
    date_hierarchy = 'data_documento'
    list_filter = ('data_vencimento', 'data_documento')
    actions = (print_boletos, )
admin.site.register(Boleto, BoletoAdmin)
