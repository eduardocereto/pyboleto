# -*- coding: utf-8 -*-
from ..data import BoletoData, CustomProperty


class BoletoBanrisul(BoletoData):
    nosso_numero = CustomProperty('nosso_numero', 8)
    conta = CustomProperty('conta', 6)

    # From http://jrimum.org/bopepo/browser/trunk/src/br/com/nordestefomento/
    # jrimum/bopepo/campolivre/AbstractCLBanrisul.java
    def calculaDuploDigito(self, seisPrimeirosCamposConcatenados):

        primeiroDV = self.modulo10(seisPrimeirosCamposConcatenados)

        digitos = seisPrimeirosCamposConcatenados + str(primeiroDV)

        restoMod11 = self.modulo11(digitos, 7, 1)

        while restoMod11 == 1:
            if primeiroDV == 9:
                primeiroDV = 0
            else:
                primeiroDV += 1

            digitos = seisPrimeirosCamposConcatenados + str(primeiroDV)

            restoMod11 = self.modulo11(digitos, 7, 1)

        if restoMod11 == 0:
            segundoDV = 0
        else:
            segundoDV = 11 - restoMod11
        return str(primeiroDV) + str(segundoDV)

    def __init__(self):
        BoletoData.__init__(self)
        self.codigo_banco = "041"
        self.logo_image = "logo_banrisul.jpg"

    @property
    def campo_livre(self):
        content = '21%04d%07d%08d40' % (int(self.agencia),
                                        int(self.conta),
                                        int(self.nosso_numero))
        dv = self.calculaDuploDigito(content)
        return '%s%s' % (content, dv)
