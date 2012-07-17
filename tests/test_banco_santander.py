# -*- coding: utf-8 -*-
import unittest
import datetime

from pyboleto.bank.santander import BoletoSantander

from .testutils import BoletoTestCase


class TestBancoSantander(BoletoTestCase):
    def setUp(self):
        self.dados = []
        for i in range(3):
            d = BoletoSantander()
            d.agencia_cedente = '1333'
            d.conta_cedente = '0707077'
            d.data_vencimento = datetime.date(2012, 7, 22)
            d.data_documento = datetime.date(2012, 7, 17)
            d.data_processamento = datetime.date(2012, 7, 17)
            d.valor_documento = 2952.95
            d.nosso_numero = str(1234567 + i)
            d.numero_documento = str(12345 + i)
            d.ios = '0'
            self.dados.append(d)

    def test_linha_digitavel(self):
        self.assertEqual(self.dados[0].linha_digitavel,
            '03399.07073 07700.000123 34567.901029 5 54020000295295'
        )

    def test_codigo_de_barras(self):
        self.assertEqual(self.dados[0].barcode,
            '03395540200002952959070707700000123456790102'
        )

    def test_agencia(self):
        self.assertEqual(self.dados[0].agencia_cedente, '1333')

    def test_nosso_numero(self):
        self.assertEqual(self.dados[0].nosso_numero, '000001234567')
        self.assertEqual(self.dados[0].format_nosso_numero(), '000001234567-9')

suite = unittest.TestLoader().loadTestsFromTestCase(TestBancoSantander)


if __name__ == '__main__':
    unittest.main()
