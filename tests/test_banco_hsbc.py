# -*- coding: utf-8 -*-
import unittest
import datetime

from pyboleto.bank.hsbc import BoletoHsbc

from .testutils import BoletoTestCase


class TestBancoHsbc(BoletoTestCase):
    def setUp(self):
        self.dados = []
        for i in range(3):
            d = BoletoHsbc()
            d.agencia_cedente = '1172-0'
            d.conta_cedente = '3903036'
            d.data_vencimento = datetime.date(2009, 5, 25)
            d.data_documento = datetime.date(2009, 5, 25)
            d.data_processamento = datetime.date(2009, 5, 25)
            d.valor_documento = 35.00
            d.nosso_numero = str(100010103120 + i)
            d.numero_documento = str(100010103120 + i)
            self.dados.append(d)

    def test_linha_digitavel(self):
        self.assertEqual(self.dados[0].linha_digitavel,
            '39993.90309 36010.001018 03120.145929 3 42480000003500'
        )

    def test_codigo_de_barras(self):
        self.assertEqual(self.dados[0].barcode,
            '39993424800000035003903036010001010312014592'
        )

    def test_agencia(self):
        self.assertEqual(self.dados[0].agencia_cedente, '1172-0')

    def test_conta(self):
        self.assertEqual(self.dados[0].conta_cedente, '3903036')

    def test_nosso_numero(self):
        self.assertEqual(self.dados[0].format_nosso_numero(),
                '0100010103120947')

suite = unittest.TestLoader().loadTestsFromTestCase(TestBancoHsbc)


if __name__ == '__main__':
    unittest.main()
