#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from pyboleto.bank.bancodobrasil import BoletoBB
from pyboleto.bank.bradesco import BoletoBradesco
from pyboleto.bank.caixa import BoletoCaixa
from pyboleto.bank.itau import BoletoItau
from pyboleto.bank.real import BoletoReal
from pyboleto.bank.santander import BoletoSantander
from pyboleto.html import BoletoHTML
import datetime


if sys.version_info < (3,):
    from pyboleto.pdf import BoletoPDF


def get_data_bb():
    listaDados = []
    for i in range(2):
        d = BoletoBB(7, 2)
        d.nosso_numero = '87654'
        d.numero_documento = '27.030195.10'
        d.convenio = '7777777'
        d.especie_documento = 'DM'

        d.carteira = '18'
        d.cedente = 'Empresa ACME LTDA'
        d.cedente_documento = "102.323.777-01"
        d.cedente_endereco = "Rua Acme, 123 - Centro - Sao Paulo/SP - \
        CEP: 12345-678"
        d.agencia_cedente = '9999'
        d.conta_cedente = '99999'

        d.data_vencimento = datetime.date(2010, 3, 27)
        d.data_documento = datetime.date(2010, 2, 12)
        d.data_processamento = datetime.date(2010, 2, 12)

        d.instrucoes = [
            "- Linha 1",
            "- Sr Caixa, cobrar multa de 2% após o vencimento",
            "- Receber até 10 dias após o vencimento",
            ]
        d.demonstrativo = [
            "- Serviço Teste R$ 5,00",
            "- Total R$ 5,00",
            ]
        d.valor_documento = 255.00

        d.sacado = [
            "Cliente Teste %d" % (i + 1),
            "Rua Desconhecida, 00/0000 - Não Sei - Cidade - Cep. 00000-000",
            ""
            ]
        listaDados.append(d)
    return listaDados


def get_data_real():
    listaDados = []
    for i in range(2):
        d = BoletoReal()
        d.carteira = '57'  # Contrato firmado com o Banco Real
        d.cedente = 'Empresa ACME LTDA'
        d.cedente_documento = "102.323.777-01"
        d.cedente_endereco = "Rua Acme, 123 - Centro - Sao Paulo/SP - \
        CEP: 12345-678"
        d.agencia_cedente = '0531'
        d.conta_cedente = '5705853'

        d.data_vencimento = datetime.date(2010, 3, 27)
        d.data_documento = datetime.date(2010, 2, 12)
        d.data_processamento = datetime.date(2010, 2, 12)

        d.instrucoes = [
            "- Linha 1",
            "- Sr Caixa, cobrar multa de 2% após o vencimento",
            "- Receber até 10 dias após o vencimento",
            ]
        d.demonstrativo = [
            "- Serviço Teste R$ 5,00",
            "- Total R$ 5,00",
            ]
        d.valor_documento = 5.00

        d.nosso_numero = "%d" % (i + 2)
        d.numero_documento = "%d" % (i + 2)
        d.sacado = [
            "Cliente Teste %d" % (i + 1),
            "Rua Desconhecida, 00/0000 - Não Sei - Cidade - Cep. 00000-000",
            ""
            ]
        listaDados.append(d)
    return listaDados


def get_data_bradesco():
    listaDados = []
    for i in range(2):
        d = BoletoBradesco()
        d.carteira = '06'  # Contrato firmado com o Banco Bradesco
        d.cedente = 'Empresa ACME LTDA'
        d.cedente_documento = "102.323.777-01"
        d.cedente_endereco = "Rua Acme, 123 - Centro - Sao Paulo/SP - \
        CEP: 12345-678"
        d.agencia_cedente = '0278-0'
        d.conta_cedente = '43905-3'

        d.data_vencimento = datetime.date(2011, 1, 25)
        d.data_documento = datetime.date(2010, 2, 12)
        d.data_processamento = datetime.date(2010, 2, 12)

        d.instrucoes = [
            "- Linha 1",
            "- Sr Caixa, cobrar multa de 2% após o vencimento",
            "- Receber até 10 dias após o vencimento",
            ]
        d.demonstrativo = [
            "- Serviço Teste R$ 5,00",
            "- Total R$ 5,00",
            ]
        d.valor_documento = 2158.41

        d.nosso_numero = "1112011668"
        d.numero_documento = "1112011668"
        d.sacado = [
            "Cliente Teste %d" % (i + 1),
            "Rua Desconhecida, 00/0000 - Não Sei - Cidade - \
            Cep. 00000-000",
            ""
            ]
        listaDados.append(d)
    return listaDados


def get_data_santander():
    listaDados = []
    for i in range(2):
        d = BoletoSantander()
        d.agencia_cedente = '1333'
        d.conta_cedente = '0707077'
        d.data_vencimento = datetime.date(2012, 7, 22)
        d.data_documento = datetime.date(2012, 7, 17)
        d.data_processamento = datetime.date(2012, 7, 17)
        d.valor_documento = 2952.95
        d.nosso_numero = '1234567'
        d.numero_documento = '12345'
        d.ios = '0'

        d.cedente = 'Empresa ACME LTDA'
        d.cedente_documento = "102.323.777-01"
        d.cedente_endereco = "Rua Acme, 123 - Centro - Sao Paulo/SP - \
        CEP: 12345-678"

        d.instrucoes = [
            "- Linha 1",
            "- Sr Caixa, cobrar multa de 2% após o vencimento",
            "- Receber até 10 dias após o vencimento",
            ]
        d.demonstrativo = [
            "- Serviço Teste R$ 5,00",
            "- Total R$ 5,00",
            ]
        d.valor_documento = 255.00

        d.sacado = [
            "Cliente Teste %d" % (i + 1),
            "Rua Desconhecida, 00/0000 - Não Sei - Cidade - Cep. 00000-000",
            ""
            ]
        listaDados.append(d)
    return listaDados


def get_data_caixa():
    listaDados = []
    for i in range(2):
        d = BoletoCaixa()
        d.carteira = 'SR'  # Contrato firmado com o Banco Bradesco
        d.cedente = 'Empresa ACME LTDA'
        d.cedente_documento = "102.323.777-01"
        d.cedente_endereco = "Rua Acme, 123 - Centro - Sao Paulo/SP - \
        CEP: 12345-678"
        d.agencia_cedente = '1565'
        d.conta_cedente = '414-3'

        d.data_vencimento = datetime.date(2010, 3, 27)
        d.data_documento = datetime.date(2010, 2, 12)
        d.data_processamento = datetime.date(2010, 2, 12)

        d.instrucoes = [
            "- Linha 1",
            "- Sr Caixa, cobrar multa de 2% após o vencimento",
            "- Receber até 10 dias após o vencimento",
            ]
        d.demonstrativo = [
            "- Serviço Teste R$ 5,00",
            "- Total R$ 5,00",
            ]
        d.valor_documento = 255.00

        d.nosso_numero = "8019525086"
        d.numero_documento = "8019525086"
        d.sacado = [
            "Cliente Teste %d" % (i + 1),
            "Rua Desconhecida, 00/0000 - Não Sei - Cidade - Cep. 00000-000",
            ""
            ]
        listaDados.append(d)
    return listaDados


def get_data_itau():
    listaDados = []
    for i in range(2):
        d = BoletoItau()
        d.nosso_numero = '87654'
        d.numero_documento = '27.030195.10'

        d.carteira = '18'
        d.cedente = 'Empresa ACME LTDA'
        d.cedente_documento = "102.323.777-01"
        d.cedente_endereco = "Rua Acme, 123 - Centro - Sao Paulo/SP - \
        CEP: 12345-678"
        d.agencia_cedente = '9999'
        d.conta_cedente = '99999'

        d.data_vencimento = datetime.date(2010, 3, 27)
        d.data_documento = datetime.date(2010, 2, 12)
        d.data_processamento = datetime.date(2010, 2, 12)

        d.instrucoes = [
            "- Linha 1",
            "- Sr Caixa, cobrar multa de 2% após o vencimento",
            "- Receber até 10 dias após o vencimento",
            ]
        d.demonstrativo = [
            "- Serviço Teste R$ 5,00",
            "- Total R$ 5,00",
            ]
        d.valor_documento = 255.00

        d.sacado = [
            "Cliente Teste %d" % (i + 1),
            "Rua Desconhecida, 00/0000 - Não Sei - Cidade - Cep. 00000-000",
            ""
            ]
        listaDados.append(d)
    return listaDados


def print_all():
    banks = {
        # "itau": "Itau",
        "bb": "Banco do Brasil",
        "caixa": "Caixa",
        "real": "Real",
        "santander": "Santander",
        "bradesco": "Bradesco",
    }
    for bank in banks:
        print("Gerando boleto para o banco " + banks[bank])
        data_func_name = "get_data_" + bank
        data_func = eval(data_func_name)
        boleto_datas = data_func()
        if sys.version_info < (3,):
            boleto_PDF = BoletoPDF('boleto-' + bank + '-normal-teste.pdf')
        boleto_HTML = BoletoHTML('boleto-' + bank + '-normal-teste.html')
        for boleto_data in boleto_datas:
            if sys.version_info < (3,):
                boleto_PDF.drawBoleto(boleto_data)
                boleto_PDF.nextPage()
                boleto_PDF.save()
            boleto_HTML.drawBoleto(boleto_data)
            boleto_HTML.nextPage()
            boleto_HTML.save()


if __name__ == "__main__":
    print_all()
