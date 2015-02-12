# -*- coding: utf-8 -*-
from ..data import BoletoData, custom_property

'''
/*
#################################################
- Convenio de 4 digitos
  Nosso número: pode ser de até 7 dígitos
- Convenio de 6 digitos
  Nosso número:
  de 1 a 99999 para opção de até 5 dígitos
  de 1 a 99999999999999999 para opção de até 17 dígitos
- Convenio de 7 digitos
  Nosso número: pode ser até 10 dígitos (Carteiras 16 e 18)
- Convenio de 8 digitos
  Nosso número: pode ser até 9 dígitos
#################################################
*/
'''


class BoletoBB(BoletoData):
    '''
        Gera Dados necessários para criação de boleto para o Banco do Brasil
    '''

    agencia_cedente = custom_property('agencia_cedente', 4)
    conta_cedente = custom_property('conta_cedente', 8)

    def __init__(self, format_convenio, format_nnumero):
        '''
            Construtor para boleto do Banco deo Brasil

            Args:
                format_convenio Formato do convenio 4, 6, 7 ou 8
                format_nnumero Formato nosso numero 1 ou 2 (apenas para convenio 6)
        '''
        super(BoletoBB, self).__init__()

        self.codigo_banco = "001"
        self.carteira = 18
        self.logo_image = "logo_bb.jpg"

        # Size of convenio 4, 6, 7 or 8
        self.format_convenio = format_convenio

        #  Nosso Numero format. 1 or 2
        #  Used only for convenio=6
        #  1: Nosso Numero with 5 positions
        #  2: Nosso Numero with 17 positions
        self.format_nnumero = format_nnumero

    def format_nosso_numero(self):
        if self.format_convenio == 7:
            return "%7s%10s" % (
                self.convenio,
                self.nosso_numero
            )
        else:
            return "%s%s-%s" % (
                self.convenio,
                self.nosso_numero,
                self.dv_nosso_numero
            )

    # Nosso numero (sem dv) sao 11 digitos
    def _get_nosso_numero(self):
        return self._nosso_numero

    def _set_nosso_numero(self, val):
        val = str(val)
        if self.format_convenio == 4:
            nn = val.zfill(7)
        elif self.format_convenio == 6:
            if self.format_nnumero == 1:
                nn = val.zfill(5)
            elif self.format_nnumero == 2:
                nn = val.zfill(17)
        elif self.format_convenio == 7:
            nn = val.zfill(10)
        elif self.format_convenio == 8:
            nn = val.zfill(9)
        self._nosso_numero = nn

    nosso_numero = property(_get_nosso_numero, _set_nosso_numero)

    def _get_convenio(self):
        return self._convenio

    def _set_convenio(self, val):
        self._convenio = str(val).ljust(self.format_convenio, '0')
    convenio = property(_get_convenio, _set_convenio)

    @property
    def agencia_conta_cedente(self):
        return "%s-%s / %s-%s" % (
            self.agencia_cedente,
            self.modulo11(self.agencia_cedente),
            self.conta_cedente,
            self.modulo11(self.conta_cedente)
        )

    @property
    def dv_nosso_numero(self):
        '''
            This function uses a modified version of modulo11
        '''
        num = self.convenio + self.nosso_numero
        base = 2
        fator = 9
        soma = 0
        for c in reversed(num):
            soma += int(c) * fator
            if fator == base:
                fator = 10
            fator -= 1
        r = soma % 11
        if r == 10:
            return 'X'
        return r

    @property
    def campo_livre(self):
        if self.format_convenio == 4:
                content = "%s%s%s%s%s" % (self.convenio,
                                           self.nosso_numero,
                                           self.agencia_cedente,
                                           self.conta_cedente,
                                           self.carteira)
        elif self.format_convenio in (7, 8):
            content = "000000%s%s%s" % (self.convenio,
                                         self.nosso_numero,
                                         self.carteira)
        elif self.format_convenio == 6:
            if self.format_nnumero == 1:
                content = "%s%s%s%s%s" % (self.convenio,
                                           self.nosso_numero,
                                           self.agencia_cedente,
                                           self.conta_cedente,
                                           self.carteira)
            if self.format_nnumero == 2:
                content = "%s%s%s" % (self.convenio,
                                        self.nosso_numero,
                                        '21'  # numero do serviço
                                        )
        return content
