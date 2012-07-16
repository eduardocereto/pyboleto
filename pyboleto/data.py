# -*- coding: utf-8 -*-
"""
    pyboleto.data
    ~~~~~~~~~~~~~

    Base para criação dos módulos dos bancos. Comtém funções genéricas
    relacionadas a geração dos dados necessários para o boleto bancário.

    :copyright: © 2011 - 2012 by Eduardo Cereto Carvalho
    :license: BSD, see LICENSE for more details.

"""
import datetime
from decimal import Decimal


class BoletoException(Exception):
    """ Exceções para erros no pyboleto"""
    def __init__(self, message):
        Exception.__init__(self, message)


def custom_property(name, num_length):
    """Função para criar propriedades nos boletos

    Cria propriedades com getter, setter e delattr.

    Propriedades criadas com essa função sempre são strings internamente.

    O Setter sempre tentará remover qualquer digito verificador se existir.

    Aceita um numero com ou sem DV e remove o DV caso exista. Então preenxe
    com zfill até o tamanho adequado. Note que sempre que possível não use DVs
    ao entrar valores no pyboleto. De preferência o pyboleto vai calcular
    todos os DVs quando necessário.

    :param name: O nome da propriedade.
    :type name: string
    :param num_length: Tamanho para preencher com '0' na frente.
    :type num_length: integer

    """
    internal_attr = '_%s' % name

    def _set_attr(self, val):
        val = val.split('-')

        if len(val) == 1:
            val[0] = str(val[0]).zfill(num_length)
            setattr(self, internal_attr, ''.join(val))

        elif len(val) == 2:
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
    """Interface para implementações específicas de bancos

    Esta classe geralmente nunca será usada diretamente. Geralmente o usuário
    irá usar uma das subclasses com a implementação específica de cada banco.

    As classes dentro do pacote :mod:`pyboleto.bank` extendem essa classe
    para implementar as especificações de cada banco.
    Portanto as especificações dentro desta classe são genéricas seguindo as
    normas da FEBRABAN.

    Todos os parâmetros devem ser passados como ``**kwargs`` para o construtor
    ou então devem ser passados depois, porém antes de imprimir o boleto.

    eg::

        bData = BoletoData(agencia='123', valor='650')
        bData.cedente = u'João Ninguém'
        bData.cedente_cidade = u'Rio de Janeiro'
        bData.cedente_uf = u'RJ'
        # Assim por diante até preencher todos os campos obrigatórios.

    **Parâmetros obrigatórios**:

    :param aceite: 'N' para o caixa não acetitar o boleto após a
        validade ou 'A' para aceitar. *(default: 'N')*
    :param agencia_cedente: Tamanho pode variar com o banco.
    :param carteira: Depende do Banco.
    :param cedente: Nome do Cedente
    :param cedente_cidade:
    :param cedente_uf:
    :param cedente_logradouro: Endereço do Cedente
    :param cedente_bairro:
    :param cedente_cep:
    :param cedente_documento: CPF ou CNPJ do Cedente.
    :param conta_cedente: Conta do Cedente sem o dígito verificador.
    :param data_documento:
    :type data_documento: `datetime.date`
    :param data_processamento:
    :type data_processamento: `datetime.date`
    :param data_vencimento:
    :type data_vencimento: `datetime.date`
    :param numero_documento: Número Customizado para controle. Pode ter até 13
        caracteres dependendo do banco.
    :param sacado_nome: Nome do Sacado
    :param sacado_documento: CPF ou CNPJ do Sacado
    :param sacado_cidade:
    :param sacado_uf:
    :param sacado_endereco: Endereco do Sacado
    :param sacado_bairro:
    :param sacado_cep:

    **Parâmetros não obrigatórios**:

    :param quantidade:
    :param especie: Nunca precisa mudar essa opção *(default: 'R$')*
    :param especie_documento:
    :param local_pagamento: *(default: 'Pagável em qualquer banco
        até o vencimento')*
    :param moeda: Nunca precisa mudar essa opção *(default: '9')*

    """

    def __init__(self, **kwargs):
        self.aceite = getattr(kwargs, 'aceite', "N")
        self.agencia_cedente = getattr(kwargs, 'agencia_cedente', "")
        self.carteira = getattr(kwargs, 'carteira', "")
        self.cedente = getattr(kwargs, 'cedente', "")
        self.cedente_cidade = getattr(kwargs, 'cedente_cidade', "")
        self.cedente_uf = getattr(kwargs, 'cedente_uf', "")
        self.cedente_logradouro = getattr(kwargs, 'cedente_logradouro', "")
        self.cedente_bairro = getattr(kwargs, 'cedente_bairro', "")
        self.cedente_cep = getattr(kwargs, 'cedente_cep', "")
        self.cedente_documento = getattr(kwargs, 'cedente_documento', "")
        self.codigo_banco = getattr(kwargs, 'codigo_banco', "")
        self.conta_cedente = getattr(kwargs, 'conta_cedente', "")
        self.data_documento = getattr(kwargs, 'data_documento', "")
        self.data_processamento = getattr(kwargs, 'data_processamento',
                                          datetime.date.today())
        self.data_vencimento = getattr(kwargs, 'data_vencimento', "")
        self.especie = getattr(kwargs, 'especie', "R$")
        self.especie_documento = getattr(kwargs, 'especie_documento', "")
        self.local_pagamento = getattr(kwargs, 'local_pagamento',
            u"Pagável em qualquer banco até o vencimento")
        self.logo_image = getattr(kwargs, 'logo_image', "")
        self.moeda = getattr(kwargs, 'moeda', "9")
        self.numero_documento = getattr(kwargs, 'numero_do_documento', "")
        self.quantidade = getattr(kwargs, 'quantidade', "")
        self.sacado_nome = getattr(kwargs, 'sacado_nome', "")
        self.sacado_documento = getattr(kwargs, 'sacado_documento', "")
        self.sacado_cidade = getattr(kwargs, 'sacado_cidade', "")
        self.sacado_uf = getattr(kwargs, 'sacado_uf', "")
        self.sacado_endereco = getattr(kwargs, 'sacado_endereco', "")
        self.sacado_bairro = getattr(kwargs, 'sacado_bairro', "")
        self.sacado_cep = getattr(kwargs, 'sacado_cep', "")

        self._cedente_endereco = None
        self._demonstrativo = []
        self._instrucoes = []
        self._sacado = None
        self._valor = None
        self._valor_documento = None

    @property
    def barcode(self):
        num = "%s%1s%1s%4s%10s%24s" % (
            self.codigo_banco,
            self.moeda,
            'X',
            self.fator_vencimento,
            self.formata_valor(self.valor_documento, 10),
            self.campo_livre
        )

        dv = self.calculate_dv_barcode(num.replace('X', '', 1))

        num = num.replace('X', str(dv), 1)
        if len(num) != 44:
            raise BoletoException(
                'The barcode must have 44 caracteres, found %d' % len(num))
        return num

    @property
    def dv_nosso_numero(self):
        """Retorna DV do nosso número

        :exception NotImplementedError: Precisa ser implementado pela classe
            derivada

        """
        raise NotImplementedError(
            'This method has not been implemented by this class'
        )

    def calculate_dv_barcode(self, line):
        """Calcula DV para código de barras

        Está é uma implementação genérica mas pode ser reimplementada pela
        classe derivada dependendo das definições de cada bancoGeralmente
        é implementado pela classe derivada.

        """
        resto2 = self.modulo11(line, 9, 1)
        if resto2 in [0, 1, 10]:
            dv = 1
        else:
            dv = 11 - resto2
        return dv

    def format_nosso_numero(self):
        """
            Geralmente é implementado pela classe derivada. Usada para formatar
            como o noso número será impresso no boleto. Às vezes é o mesmo
            do :prop:`numero_do_documento` e às vezes contém outros campos
            juntos.
        """
        return self.nosso_numero

    nosso_numero = custom_property('nosso_numero', 13)
    """Nosso Número geralmente tem 13 posições

    Algumas subclasses podem alterar isso dependendo das normas do banco

    """

    agencia_cedente = custom_property('agencia_cedente', 4)
    """Agência do Cedente geralmente tem 4 posições

    Algumas subclasses podem alterar isso dependendo das normas do banco

    """

    conta_cedente = custom_property('conta_cedente', 7)
    """Conta do Cedente geralmente tem 7 posições

    Algumas subclasses podem alterar isso dependendo das normas do banco

    """

    def _cedente_endereco_get(self):
        if self._cedente_endereco is None:
            self._cedente_endereco = '%s - %s - %s - %s - %s' % (
                self.cedente_logradouro,
                self.cedente_bairro,
                self.cedente_cidade,
                self.cedente_uf,
                self.cedente_cep
            )
        return self._cedente_endereco

    def _cedente_endereco_set(self, endereco):
        if len(endereco) > 80:
            raise BoletoException(
                u'Linha de endereço possui mais que 80 caracteres')
        self._cedente_endereco = endereco
    cedente_endereco = property(_cedente_endereco_get, _cedente_endereco_set)
    """Endereço do Cedente com no máximo 80 caracteres"""

    def _get_valor(self):
        if self._valor is not None:
            return "%.2f" % self._valor

    def _set_valor(self, val):
        if type(val) is Decimal:
            self._valor = val
        else:
            self._valor = Decimal(str(val), 2)
    valor = property(_get_valor, _set_valor)
    """Valor convertido para :class:`Decimal`.

    Geralmente valor e valor_documento são o mesmo número.

    :type: Decimal

    """

    def _get_valor_documento(self):
        if self._valor_documento is not None:
            return "%.2f" % self._valor_documento

    def _set_valor_documento(self, val):
        if type(val) is Decimal:
            self._valor_documento = val
        else:
            self._valor_documento = Decimal(str(val), 2)
    valor_documento = property(_get_valor_documento, _set_valor_documento)
    """Valor do Documento convertido para :class:`Decimal`.

    De preferência para passar um valor em :class:`Decimal`, se não for passado
    outro tipo será feito um cast para :class:`Decimal`.

    """

    def _instrucoes_get(self):
        return self._instrucoes

    def _instrucoes_set(self, list_inst):
        if isinstance(list_inst, basestring):
            list_inst = list_inst.splitlines()

        if len(list_inst) > 7:
            raise BoletoException(
                u'Número de linhas de instruções maior que 7')
        for line in list_inst:
            if len(line) > 90:
                raise BoletoException(
                    u'Linha de instruções possui mais que 90 caracteres')
        self._instrucoes = list_inst
    instrucoes = property(_instrucoes_get, _instrucoes_set)
    """Instruções para o caixa do banco que recebe o bilhete

    Máximo de 7 linhas com 90 caracteres cada.
    Geralmente contém instruções para aplicar multa ou não aceitar caso tenha
    passado a data de validade.

    """

    def _demonstrativo_get(self):
        return self._demonstrativo

    def _demonstrativo_set(self, list_dem):
        if isinstance(list_dem, basestring):
            list_dem = list_dem.splitlines()

        if len(list_dem) > 12:
            raise BoletoException(
                u'Número de linhas de demonstrativo maior que 12')
        for line in list_dem:
            if len(line) > 90:
                raise BoletoException(
                    u'Linha de demonstrativo possui mais que 90 caracteres')
        self._demonstrativo = list_dem
    demonstrativo = property(_demonstrativo_get, _demonstrativo_set)
    """Texto que vai impresso no corpo do Recibo do Sacado

    Máximo de 12 linhas com 90 caracteres cada.

    """

    def _sacado_get(self):
        """Tenta usar o sacado que foi setado ou constroi um

        Se você não especificar um sacado o boleto tentará construir um sacado
        a partir de outras proriedades setadas.

        Para facilitar você deve sempre setar essa propriedade.

        """
        if self._sacado is None:
            self.sacado = [
                '%s - CPF/CNPJ: %s' % (self.sacado_nome,
                                       self.sacado_documento),
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
        self._sacado = list_sacado
    sacado = property(_sacado_get, _sacado_set)
    """Campo sacado composto por até 3 linhas.

    A primeira linha precisa ser o nome do sacado.
    As outras duas linhas devem ser usadas para o endereço do sacado.

    """

    @property
    def fator_vencimento(self):
        """Usado na geração do barcode

            :return: numero de dias entre 07/10/1997 e :attr:`data_vencimento`
            :rtype: int

        """
        date_ref = datetime.date(2000, 7, 3)  # Fator = 1000
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
        """Monta a linha digitável a partir do barcode

        Esta é a linha que o cliente pode utilizar para digitar se o código
        de barras não estiver legível.

        Essa função sempre é a mesma para todos os bancos. Então basta
        implementar o método :func:`barcode` para o pyboleto calcular a linha
        digitável.

        Posição    Conteúdo
        1 a 3    Número do banco
        4        Código da Moeda - 9 para Real
        5        Digito verificador do Código de Barras
        6 a 19   Valor (12 inteiros e 2 decimais)
        20 a 44  Campo Livre definido por cada banco

        """
        linha = self.barcode
        if not linha:
            raise BoletoException("Boleto doesn't have a barcode")

        def monta_campo(campo):
            campo_dv = "%s%s" % (campo, self.modulo10(campo))
            return "%s.%s" % (campo_dv[0:5], campo_dv[5:])

        return ' '.join([monta_campo(linha[0:4] + linha[19:24]),
                         monta_campo(linha[24:34]),
                         monta_campo(linha[34:44]),
                         linha[4],
                         linha[5:19]])

    def formata_valor(self, nfloat, tamanho):
        txt = nfloat.replace('.', '')
        if len(txt) > tamanho:
            raise BoletoException(
                u'Tamanho em caracteres do número está maior que o permitido')
        return txt.zfill(tamanho)

    @staticmethod
    def modulo10(num):
        soma = 0
        peso = 2
        for i in range(len(num) - 1, -1, -1):
            parcial = int(num[i]) * peso
            if parcial > 9:
                s = "%d" % parcial
                parcial = int(s[0]) + int(s[1])
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
    def modulo11(num, base=9, r=0):
        soma = 0
        fator = 2
        for c in reversed(str(num)):
            soma += int(c) * fator
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
