from pyboleto.data import BoletoData
import os.path

class BoletoReal( BoletoData ):

    def __init__(self, *args, **kwargs):
        super(BoletoReal , self).__init__(*args, **kwargs)

        self.codigo_banco = "356"
        self.logo_image_path = os.path.dirname(__file__) + \
            "/../media/logo_bancoreal.jpg"

    @property
    def agencia_conta_cedente(self):
        dv = self.digitao_cobranca
        s = "%s/%s-%s" % (self.agencia_cedente, self.conta_cedente, dv)
        return s

    @property
    def digitao_cobranca(self):
        num = "%s%s%s" % (
            self.nosso_numero, 
            self.agencia_cedente, 
            self.conta_cedente
        )
        dv = self.modulo10(num)
        return dv

    def calculate_dv_barcode(self, line):
        dv = self.modulo11(line)
        return dv

    @property
    def barcode(self):
        num = "%3s%1s%1s%4s%10s%4s%7s%1s%13s" % ( \
            self.codigo_banco, \
            self.moeda,
            'X',
            self.fator_vencimento,
            self.formata_valor(self.valor_documento,10),
            self.agencia_cedente,
            self.conta_cedente,
            self.digitao_cobranca,
            self.nosso_numero,
        )
        dv = self.calculate_dv_barcode(num.replace('X', '', 1))

        num = num.replace('X', str(dv), 1)
        return num

