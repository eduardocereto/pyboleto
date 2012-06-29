#-*- coding: utf-8 -*-
from pyboleto.data import BoletoData, custom_property
import os.path

### CAUTION - NÃO TESTADO ###
class BoletoCaixa( BoletoData ):
    '''
        Gera Dados necessários para criação de boleto para o banco Caixa
        Economica Federal
    '''

    def __init__(self, *args, **kwargs):
        super(BoletoCaixa , self).__init__(*args, **kwargs)

        self.codigo_banco = "104"
        self.logo_image_path = os.path.dirname(__file__) + \
            "/../media/logo_bancocaixa.jpg"

        ''' 
            Carteira SR: 80, 81 ou 82  -  
            Carteira CR: 90 (Confirmar com gerente qual usar)
        '''
        self.inicio_nosso_numero = '80'

    # Nosso numero (sem dv) sao 10 digitos
    def _nosso_numero_get(self):
        return self._nosso_numero
    '''
        Nosso Número sem DV, máximo 8 chars
    '''
    def _nosso_numero_set(self, val):
        try:
            self._nosso_numero = self.inicio_nosso_numero + \
                self.formata_numero(val, 8)
        except AttributeError:
            pass

    nosso_numero = property(_nosso_numero_get, _nosso_numero_set)

    @property
    def dv_nosso_numero(self):
        resto2 = self.modulo11(self.nosso_numero.split('-')[0],9,1)
        digito = 11 - resto2
        if digito == 10 or digito == 11:
            dv = 0
        else:
            dv = digito
        return dv

    '''
        agencia do cedente sem DV
    '''
    agencia_cedente = custom_property('agencia_cedente', 4)

    conta_cedente = custom_property('conta_cedente', 11)

    # Numero para o codigo de barras com 44 digitos
    @property
    def barcode(self):
        num = "%3s%1s%1s%4s%10s%10s%4s%11s" % (
            self.codigo_banco,
            self.moeda,
            'X',
            self.fator_vencimento,
            self.formata_valor(self.valor_documento,10),
            self.nosso_numero, 
            self.agencia_cedente,
            self.conta_cedente.split('-')[0],
        )
        dv = self.calculate_dv_barcode(num.replace('X', '', 1))

        num = num.replace('X', str(dv), 1)
        return num

