#-*- coding: utf-8 -*-
from ..data import BoletoData, custom_property, BoletoException


class BoletoCaixaSigcb(BoletoData):
    '''
        Gera Dados necessários para criação de boleto para o banco Caixa
        Economica Federal
    '''

    agencia_cedente = custom_property('agencia_cedente', 4)
    conta_cedente = custom_property('conta_cedente', 6)
    nosso_numero = custom_property('nosso_numero', 18)

    def __init__(self):
        super(BoletoCaixaSigcb, self).__init__()

        self.codigo_banco = "104"
        self.local_pagamento = "Preferencialmente nas Casas Lotéricas e \
Agências da Caixa"
        self.logo_image = "logo_bancocaixa.jpg"

    @property
    def dv_nosso_numero(self):
        resto2 = self.modulo11(self.nosso_numero[9:].split('-')[0], 9, 1)
        digito = 11 - resto2
        if digito == 10 or digito == 11:
            dv = 0
        else:
            dv = digito
        return dv

    @property
    def campo_livre(self):  #24 digits
        content = "%6s%1s%3s%1s%3s%1s%9s%1s" % ((self.conta_cedente.split('-')[0]),
                                             (self.conta_cedente.split('-')[1]),
                                             self.nosso_numero[2:5],
                                             self.nosso_numero[0:1],
                                             self.nosso_numero[6:9],
                                             self.nosso_numero[1:2],
                                             self.nosso_numero[9:],
                                             self.dv_nosso_numero)

        return content

    def format_nosso_numero(self):
        return self.nosso_numero + '-' + str(self.dv_nosso_numero)