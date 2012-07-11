# -*- coding: utf-8
import os.path

from pyboleto.data import BoletoData, custom_property


class BoletoBradesco(BoletoData):
    '''
        Gera Dados necessários para criação de boleto para o banco Bradesco
    '''

    def __init__(self, *args, **kwargs):
        super(BoletoBradesco, self).__init__(*args, **kwargs)

        self.codigo_banco = "237"
        self.logo_image_path = os.path.dirname(__file__) + \
            "/../media/logo_bancobradesco.jpg"

    def format_nosso_numero(self):
        return "%s/%s-%s" % (
            self.carteira,
            self.nosso_numero,
            self.dv_nosso_numero
        )

    # Nosso numero (sem dv) sao 11 digitos
    nosso_numero = custom_property('nosso_numero', 11)

    @property
    def dv_nosso_numero(self):
        resto2 = self.modulo11(self.nosso_numero, 7, 1)
        digito = 11 - resto2
        if digito == 10:
            dv = 'P'
        elif digito == 11:
            dv = 0
        else:
            dv = digito
        return dv

    agencia_cedente = custom_property('agencia_cedente', 4)

    conta_cedente = custom_property('conta_cedente', 7)

    @property
    def campo_livre(self):
        content = "%4s%2s%11s%7s%1s" % (self.agencia_cedente.split('-')[0],
                                        self.carteira,
                                        self.nosso_numero,
                                        self.conta_cedente.split('-')[0],
                                        '0'
                                        )
        return content
