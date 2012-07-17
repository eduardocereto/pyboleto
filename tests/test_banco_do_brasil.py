# -*- coding: utf-8 -*-
import unittest
import datetime

from pyboleto.bank.bancodobrasil import BoletoBB

from .testutils import BoletoTestCase


class TestBancoBrasil(BoletoTestCase):
    def setUp(self):
        self.dados = []
        for i in range(3):
            d = BoletoBB(7, 1)
            d.carteira = '18'
            d.data_documento = datetime.date(2011, 3, 8)
            d.data_vencimento = datetime.date(2011, 3, 8)
            d.data_processamento = datetime.date(2012, 7, 4)
            d.valor_documento = 2952.95
            d.agencia = '9999'
            d.conta = '99999'
            d.convenio = '7777777'
            d.nosso_numero = str(87654 + i)
            d.numero_documento = str(87654 + i)
            self.dados.append(d)

    def test_linha_digitavel(self):
        self.assertEqual(self.dados[0].linha_digitavel,
            '00190.00009 07777.777009 00087.654182 6 49000000295295'
        )

    def test_codigo_de_barras(self):
        self.assertEqual(self.dados[0].barcode,
            '00196490000002952950000007777777000008765418'
        )

suite = unittest.TestLoader().loadTestsFromTestCase(TestBancoBrasil)


if __name__ == '__main__':
    unittest.main()
