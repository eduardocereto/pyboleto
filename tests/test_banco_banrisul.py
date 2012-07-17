# -*- coding: utf-8 -*-
import datetime
import unittest

from pyboleto.bank.banrisul import BoletoBanrisul

from .testutils import BoletoTestCase


class TestBancoBanrisul(BoletoTestCase):
    def setUp(self):
        self.dados = []
        for i in range(3):
            d = BoletoBanrisul()
            d.data_documento = datetime.date(2000, 7, 4)
            d.data_vencimento = datetime.date(2000, 7, 4)
            d.data_processamento = datetime.date(2012, 7, 11)
            d.valor_documento = 550
            d.agencia_cedente = '1102'
            d.conta_cedente = '9000150'
            d.convenio = 7777777
            d.nosso_numero = str(22832563 + i)
            d.numero_documento = str(22832563 + i)
            self.dados.append(d)

    def test_linha_digitavel(self):
        self.assertEqual(
            self.dados[0].linha_digitavel,
            '04192.11107 29000.150226 83256.340593 8 10010000055000'
        )

    def test_tamanho_codigo_de_barras(self):
        self.assertEqual(len(self.dados[0].barcode), 44)

    def test_codigo_de_barras(self):
        self.assertEqual(self.dados[0].barcode,
                         '04198100100000550002111029000150228325634059')

    def test_campo_livre(self):
        self.assertEqual(self.dados[0].campo_livre,
                         '2111029000150228325634059')


suite = unittest.TestLoader().loadTestsFromTestCase(TestBancoBanrisul)

if __name__ == '__main__':
    unittest.main()
