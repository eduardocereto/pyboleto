# -*- coding: utf-8
import os.path

from pyboleto.data import BoletoData, custom_property


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

# From http://jrimum.org/bopepo/browser/trunk/src/br/com/nordestefomento/jrimum/bopepo/campolivre/AbstractCLBanrisul.java


def calculaDuploDigito(seisPrimeirosCamposConcatenados):
    def sum11(s, lmin, lmax):
        soma = 0
        peso = lmin
        for c in reversed(s):
            soma += peso * int(c)
            peso += 1
            if peso > lmax:
                peso = lmin
        return soma
    primeiroDV = modulo10(seisPrimeirosCamposConcatenados)
    somaMod11 = sum11(
        seisPrimeirosCamposConcatenados + str(primeiroDV), 2, 7)
    restoMod11 = calculeRestoMod11(somaMod11)
    while restoMod11 == 1:
        primeiroDV = encontreValorValidoParaPrimeiroDV(primeiroDV)
        somaMod11 = sum11(
            seisPrimeirosCamposConcatenados + str(primeiroDV), 2, 7)
        restoMod11 = calculeRestoMod11(somaMod11)
    segundoDV = calculeSegundoDV(restoMod11)
    return str(primeiroDV) + str(segundoDV)


def calculeSegundoDV(restoMod11):
    if restoMod11 == 0:
        return restoMod11
    else:
        return 11 - restoMod11


def calculePrimeiroDV(restoMod10):
    if restoMod10 == 0:
        return 0
    else:
        return 10 - restoMod10


def calculeRestoMod10(somaMod10):
    if somaMod10 < 10:
        return somaMod10
    else:
        return somaMod10 % 10


def encontreValorValidoParaPrimeiroDV(primeiroDV):
    if primeiroDV == 9:
        return 0
    else:
        return primeiroDV + 1


def calculeRestoMod11(somaMod11):
    if somaMod11 < 11:
        return somaMod11
    else:
        return somaMod11 % 11


class BoletoBanrisul(BoletoData):
    nosso_numero = custom_property('nosso_numero', 8)
    conta = custom_property('conta', 6)

    def __init__(self, **kwargs):
        BoletoData.__init__(self, **kwargs)
        self.codigo_banco = "041"
        self.logo_image_path = os.path.dirname(__file__) + \
            "/../media/logo_banrisul.jpg"

    @property
    def campo_livre(self):
        content = '21%04d%07d%08d40' % (int(self.agencia),
                                        int(self.conta),
                                        int(self.nosso_numero))
        dv = calculaDuploDigito(content)
        return '%s%s' % (content, dv)

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
            raise Exception(
                'The barcode must have 44 caracteres, found %d' % len(num))
        return num
