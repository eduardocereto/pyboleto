# -*- coding: utf-8 -*-
from django.db import models


class Boleto(models.Model):
    # Informações Gerais
    codigo_banco = models.CharField(u'Código do Banco', max_length=3)
    carteira = models.CharField(max_length=5)
    aceite = models.CharField(max_length=1, default='N')

    valor_documento = models.DecimalField(u'Valor do Documento',
                                          max_digits=8, decimal_places=2)
    valor = models.DecimalField(max_digits=8,
                                decimal_places=2, blank=True, null=True)

    data_vencimento = models.DateField(u'Data de Vencimento')
    data_documento = models.DateField(u'Data do Documento')
    data_processamento = models.DateField(u'Data de Processamento',
                                          auto_now=True)

    numero_documento = models.CharField(u'Número do Documento', max_length=11)

    # Informações do Cedente
    agencia_cedente = models.CharField(u'Agência Cedente', max_length=4)
    conta_cedente = models.CharField('Conta Cedente', max_length=7)

    cedente = models.CharField(u'Nome do Cedente', max_length=255)
    cedente_documento = models.CharField(u'Documento do Cedente',
                                         max_length=50)
    cedente_cidade = models.CharField(u'Cidade do Cedente', max_length=255)
    cedente_uf = models.CharField(u'Estado do Cedente', max_length=2)
    cedente_endereco = models.CharField(u'Endereço do Cedente',
                                          max_length=255)
    cedente_bairro = models.CharField(u'Bairro do Cedente', max_length=255)
    cedente_cep = models.CharField(u'CEP do Cedente', max_length=9)

    # Informações do Sacado
    sacado_nome = models.CharField(u'Nome do Sacado', max_length=255)
    sacado_documento = models.CharField(u'Documento do Sacado', max_length=255)
    sacado_cidade = models.CharField(u'Cidade do Sacado', max_length=255)
    sacado_uf = models.CharField(u'Estado do Sacado', max_length=2)
    sacado_endereco = models.CharField(u'Endereço do Sacado', max_length=255)
    sacado_bairro = models.CharField(u'Bairro do Sacado', max_length=255)
    sacado_cep = models.CharField(u'CEP do Sacado', max_length=9)

    # Informações Opcionais
    quantidade = models.CharField(u'Quantidade', max_length=10, blank=True)
    especie_documento = models.CharField(u'Espécie do Documento',
                                         max_length=255, blank=True)
    especie = models.CharField(u'Espécie', max_length=2, default="R$")
    moeda = models.CharField(max_length=2, default='9')
    local_pagamento = models.CharField(u'Local de Pagamento', max_length=255,
        default=u'Pagável em qualquer banco até o vencimento')
    demonstrativo = models.TextField(blank=True)
    instrucoes = models.TextField(default=u"""1- Não receber após 30 dias.
2- Multa de 2% após o vencimento.
3- Taxa diária de permanência de 0,2%.""")

    def __unicode__(self):
        return self.numero_documento

    def print_pdf_pagina(self, pdf_file):
        from .. import bank

        ClasseBanco = bank.get_class_for_codigo(self.codigo_banco)

        boleto_dados = ClasseBanco()

        for field in self._meta.get_all_field_names():
            if getattr(self, field):
                setattr(boleto_dados, field, getattr(self, field))

        setattr(boleto_dados, 'nosso_numero',
                getattr(self, 'numero_documento'))

        pdf_file.drawBoleto(boleto_dados)
