# -*- coding: utf-8 -*-
import unittest
import datetime

from pyboleto.bank.real import BoletoReal

from .testutils import BoletoTestCase


class TestBancoReal(BoletoTestCase):
    def setUp(self):
        self.dados = []
        for i in range(3):
            d = BoletoReal()
            d.carteira = '06'
            d.agencia_cedente = '0531'
            d.conta_cedente = '5705853'
            d.data_vencimento = datetime.date(2011, 2, 5)
            d.data_documento = datetime.date(2011, 1, 18)
            d.data_processamento = datetime.date(2011, 1, 18)
            d.valor_documento = 355.00
            d.nosso_numero = str(123 + i)
            d.numero_documento = str(123 + i)
            self.dados.append(d)

    def test_linha_digitavel(self):
        self.assertEqual(self.dados[0].linha_digitavel,
            '35690.53154 70585.390001 00000.001230 8 48690000035500'
        )

    def test_codigo_de_barras(self):
        self.assertEqual(self.dados[0].barcode,
            '35698486900000355000531570585390000000000123'
        )

suite = unittest.TestLoader().loadTestsFromTestCase(TestBancoReal)

if __name__ == '__main__':
    unittest.main()
