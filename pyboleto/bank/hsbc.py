# -*- coding: utf-8
import os.path

from pyboleto.data import BoletoData, custom_property


### CAUTION - NÃO TESTADO ###


class BoletoHsbc(BoletoData):
    '''
        Gera Dados necessários para criação de boleto para o banco HSBC
    '''

    def __init__(self, *args, **kwargs):
        super(BoletoHsbc, self).__init__(*args, **kwargs)

        self.codigo_banco = "399"
        self.logo_image_path = os.path.dirname(__file__) + \
            "/../media/logo_bancohsbc.jpg"
        self.carteira = 'CNR'

    # Nosso número deve ser calculado automaticamente
    @property
    def nosso_numero(self):
        nosso_numero = self.numero_documento
        # Primeiro DV
        nosso_numero += str(self.modulo11(nosso_numero))
        # Cobrança com vencimento = 4
        nosso_numero += "4"
        # Segundo DV
        sum_params = int(nosso_numero) + int(self.conta_cedente)
        sum_params += int(self.data_vencimento.strftime('%d%m%y'))
        sum_params = str(sum_params)
        nosso_numero += str(self.modulo11(sum_params))
        return nosso_numero

    numero_documento = custom_property('numero_documento', 13)

    @property
    def data_vencimento_juliano(self):
        data_vencimento = str(self.data_vencimento.timetuple().tm_yday)
        data_vencimento += str(self.data_vencimento.year)[-1:]
        return data_vencimento.zfill(4)

    # Numero para o codigo de barras com 44 digitos
    @property
    def barcode(self):
        num = "%3s%1s%1s%4s%10s%7s%13s%4s%1s" % (
            self.codigo_banco,
            self.moeda,
            'X',
            self.fator_vencimento,
            self.formata_valor(self.valor_documento, 10),
            self.conta_cedente,
            self.numero_documento,
            self.data_vencimento_juliano,
            '2'
        )
        dv = self.calculate_dv_barcode(num.replace('X', '', 1))

        num = num.replace('X', str(dv), 1)
        return num


class BoletoHsbcComRegistro(BoletoData):
    '''
        Gera Dados necessários para criação de boleto para o banco HSBC
        com registro
    '''
    def __init__(self, *args, **kwargs):

        super(BoletoHsbcComRegistro, self).__init__(*args, **kwargs)

        self.codigo_banco = "399"
        self.logo_image_path = os.path.dirname(__file__) + \
            "/../media/logo_bancohsbc.jpg"
        self.carteira = 'CSB'
        self.especie_documento = 'PD'

    # Nosso numero (sem dv) sao 10 digitos
    nosso_numero = custom_property('nosso_numero', 10)

    @property
    def dv_nosso_numero(self):
        resto = self.modulo11(self.nosso_numero, 7, 1)
        if resto == 0 or resto == 1:
            return 0
        else:
            return 11 - resto

    # Numero para o codigo de barras com 44 digitos
    @property
    def barcode(self):
        num = "%3s%1s%1s%4s%10s%10s%1s%4s%7s%2s%1s" % (
            self.codigo_banco,
            self.moeda,
            'X',
            self.fator_vencimento,
            self.formata_valor(self.valor_documento, 10),
            self.nosso_numero,
            self.dv_nosso_numero,
            self.agencia_cedente.split('-')[0],
            self.conta_cedente.split('-')[0],
            '00',
            '1'
        )

        dv = self.calculate_dv_barcode(num.replace('X', '', 1))

        num = num.replace('X', str(dv), 1)
        return num
