# -*- coding: utf-8
import os.path

from pyboleto.data import BoletoData, custom_property


# From http://jrimum.org/bopepo/browser/trunk/src/br/com/nordestefomento/jrimum/bopepo/campolivre/AbstractCLBanrisul.java

class BoletoBanrisul(BoletoData):
    nosso_numero = custom_property('nosso_numero', 8)
    conta = custom_property('conta', 6)

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
        dv = self.calculaDuploDigito(content)
        return '%s%s' % (content, dv)
