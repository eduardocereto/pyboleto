# -*- coding: utf-8 -*-
import datetime
import re
from decimal import Decimal

class BoletoException(Exception):
    def __init__(self, message ):
        Exception.__init__(self, message)

def custom_property(name, num_length):
    '''
        Function to create properties on boleto

        It accepts a number with or without a DV and zerofills it
    '''
    internal_attr = '_%s'%name

    def _set_attr(self,val):
        val = val.split('-')
        
        if len(val) is 1:
            val[0] = str(val[0]).zfill(num_length)
            setattr(self, internal_attr, ''.join(val))

        elif len(val) is 2:
            val[0] = str(val[0]).zfill(num_length)
            setattr(self, internal_attr, '-'.join(val))
        
        else:
            raise BoletoException('Wrong value format')

    return property(
        lambda self: getattr(self, internal_attr),
        _set_attr,
        lambda self: delattr(self, internal_attr),
        name
    )

class BoletoData(object):
    
    def __init__(self, *args, **kwargs):
        self.aceite = "N"
        self.agencia_cedente = ""
        self.carteira = ""
        self.cedente = ""
        self.codigo_banco = ""
        self.conta_cedente = ""
        self.data_documento = ""
        self.data_processamento = datetime.date.today()
        self.data_vencimento = ""
        self.demonstrativo = []
        self.especie = "R$"
        self.especie_documento = ""
        self.instrucoes = []
        self.local_pagamento = "Pagável em qualquer banco até o vencimento"
        self.logo_image_path = ""
        self.moeda = "9"
        self.numero_documento = ""
        self.quantidade = ""
        self.sacado_nome = ""
        self.sacado_cidade = ""
        self.sacado_uf = ""
        self.sacado_endereco = ""
        self.sacado_bairro = ""
        self.sacado_cep = ""
    
    @property
    def barcode(self):
        '''
            Returns string used to generate barcodes

            It should be implemented by derived class
        '''
        raise NotImplementedError(
            'This method has not been implemented by this class'
        )

    @property
    def dv_nosso_numero(self):
        '''
            Returns nosso número DV

            It should be implemented by derived class
        '''
        raise NotImplementedError(
            'This method has not been implemented by this class'
        )

    def calculate_dv_barcode(self, line):
        '''
            Calculates de DV for barcode

            It should be implemented by derived class
        '''
        resto2 = self.modulo11(line,9,1)
        if resto2 in [0, 1, 10]:
            dv = 1
        else:
            dv = 11 - resto2
        return dv

    def format_nosso_numero(self):
        '''
            Return Formatted Nosso Número

            It should be implemented by derived class
        '''
        return self.nosso_numero

    nosso_numero = custom_property('nosso_numero', 13)

    agencia_cedente = custom_property('agencia_cedente', 4)

    conta_cedente = custom_property('conta_cedente', 7)

    def _get_valor(self):
        try:
            return "%.2f" % self._valor
        except AttributeError:
            pass
    def _set_valor(self, val):
        if type(val) is Decimal:
            self._valor = val
        else:
            self._valor = Decimal(str(val), 2)
    valor = property(_get_valor, _set_valor)

    def _get_valor_documento(self):
        try:
            return "%.2f" % self._valor_documento
        except AttributeError:
            pass
    def _set_valor_documento(self, val):
        if type(val) is Decimal:
            self._valor_documento = val
        else:
            self._valor_documento = Decimal(str(val), 2)
    valor_documento = property(
        _get_valor_documento,
        _set_valor_documento
    )

    def _instrucoes_get(self):
        try:
            return self._instrucoes
        except AttributeError:
            pass
    def _instrucoes_set(self, list_inst):
        if len(list_inst) > 7:
            raise BoletoException(
                u'Número de linhas de instruções maior que 7')
        for line in list_inst:
            if len(line) > 90:
                raise BoletoException(
                    u'Linha de instruções possui mais que 90 caracteres')
        self._instrucoes = list_inst
    instrucoes = property(_instrucoes_get, _instrucoes_set)

    def _demonstrativo_get(self):
        try:
            return self._demonstrativo
        except AttributeError:
            pass
    def _demonstrativo_set(self,list_dem):
        if len(list_dem) > 12:
            raise BoletoException(
                u'Número de linhas de demonstrativo maior que 12')
        for line in list_dem:
            if len(line) > 90:
                raise BoletoException(
                    u'Linha de demonstrativo possui mais que 90 caracteres')
        self._demonstrativo = list_dem
    demonstrativo = property(_demonstrativo_get, _demonstrativo_set)

    def _sacado_get(self):
        if not hasattr(self, '_sacado'):
            self.sacado = [
                self.sacado_nome,
                self.sacado_endereco,
                '%s - %s - %s - %s' % (
                    self.sacado_bairro, 
                    self.sacado_cidade, 
                    self.sacado_uf, 
                    self.sacado_cep
                )
            ]
        return self._sacado
    def _sacado_set(self, list_sacado):
        if len(list_sacado) > 3:
            raise BoletoException(u'Número de linhas do sacado maior que 3')
        for line in list_sacado:
            if len(line) > 80:
                raise BoletoException(
                    u'Linha de sacado possui mais que 80 caracteres')
        self._sacado = list_sacado
    sacado = property(_sacado_get, _sacado_set)
    
    @property
    def fator_vencimento(self):
        date_ref = datetime.date(2000,7,3) # Fator = 1000
        delta = self.data_vencimento - date_ref
        fator = delta.days + 1000
        return fator

    @property
    def agencia_conta_cedente(self):
        return "%s/%s" % (self.agencia_cedente, self.conta_cedente)

    @property
    def codigo_dv_banco(self):
        cod = "%s-%s" % (self.codigo_banco, self.modulo11(self.codigo_banco))
        return cod

    @property
    def linha_digitavel(self):
        '''
            Monta a linha que o cliente pode utilizar para digitar se o código 
            de barras não puder ser lido
            Posição    Conteúdo
            1 a 3    Número do banco
            4        Código da Moeda - 9 para Real
            5        Digito verificador do Código de Barras
            6 a 19   Valor (12 inteiros e 2 decimais)
            20 a 44  Campo Livre definido por cada banco
        '''
        linha = self.barcode
        if not linha:
            BoletoException("Boleto doesn't have a barcode")

        p1 = linha[0:4]
        p2 = linha[19:24]        
        p3 = self.modulo10("%s%s"%(p1,p2))
        p4 = "%s%s%s" %(p1,p2,p3)
        p5 = p4[0:5]
        p6 = p4[5:]
        campo1 = "%s.%s" %(p5,p6)

        p1 = linha[24:34]
        p2 = self.modulo10(p1)
        p3 = "%s%s" %(p1,p2)
        p4 = p3[0:5]
        p5 = p3[5:]
        campo2 = "%s.%s" %(p4,p5)

        p1 = linha[34:44]
        p2 = self.modulo10(p1)
        p3 = "%s%s" %(p1,p2)
        p4 = p3[0:5]
        p5 = p3[5:]
        campo3 = "%s.%s" %(p4,p5)
        campo4 = linha[4]        
        campo5 = linha[5:19]

        return "%s %s %s %s %s" %(campo1,campo2,campo3,campo4,campo5)

    @staticmethod
    def formata_numero(numero, tamanho):
        if len(numero) > tamanho:
            raise BoletoException(
                u'Tamanho em caracteres do número está maior que o permitido' )
        return numero.zfill(tamanho)
    
    @staticmethod
    def formata_texto(texto, tamanho):
        if len(texto) > tamanho:
            raise BoletoException( 
                u'Tamanho em caracteres do texto está maior que o permitido' )
        return texto.ljust(tamanho)
    
    def formata_valor(self,nfloat, tamanho):
        try:
            txt = nfloat.replace( '.', '' )
            txt = self.formata_numero(txt, tamanho)
            return txt
        except AttributeError:
            pass
    
    @staticmethod
    def modulo10(num):
        soma = 0
        peso = 2
        for i in range(len(num)-1,-1,-1):
            parcial = int(num[i]) * peso
            if parcial > 9:
                s = "%d" % parcial
                parcial = int(s[0])+int(s[1])
            soma += parcial
            if peso == 2:
                peso = 1
            else:
                peso = 2
        
        resto10 = soma % 10
        if resto10 == 0:
            modulo10 = 0
        else:
            modulo10 = 10 - resto10
            
        return modulo10

    @staticmethod
    def modulo11(num,base=9,r=0):
        soma=0
        fator=2
        for i in range(len(str(num))).__reversed__():
            parcial10 = int(num[i]) * fator
            soma += parcial10
            if fator == base:
                fator = 1
            fator += 1
        if r == 0:
            soma = soma * 10
            digito = soma % 11
            if digito == 10:
                digito = 0
            return digito     
        if r == 1:
            resto = soma % 11
            return resto

