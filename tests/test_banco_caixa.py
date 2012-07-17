# -*- coding: utf-8 -*-
import unittest
import datetime

from pyboleto.bank.caixa import BoletoCaixa

from .testutils import BoletoTestCase


class TestBancoCaixa(BoletoTestCase):
    def setUp(self):
        self.dados = []
        for i in range(3):
            d = BoletoCaixa()
            d.carteira = 'SR'
            d.agencia_cedente = '1565'
            d.conta_cedente = '87000000414'
            d.data_vencimento = datetime.date(2012, 7, 8)
            d.data_documento = datetime.date(2012, 7, 3)
            d.data_processamento = datetime.date(2012, 7, 3)
            d.valor_documento = 2952.95
            d.nosso_numero = str(8019525086 + i)
            d.numero_documento = str(270319510 + i)
            self.dados.append(d)

    def test_linha_digitavel(self):
        self.assertEqual(self.dados[0].linha_digitavel,
            '10498.01952 25086.156582 70000.004146 1 53880000295295'
        )

    def test_tamanho_codigo_de_barras(self):
        self.assertEqual(len(self.dados[0].barcode), 44)

    def test_codigo_de_barras(self):
        self.assertEqual(self.dados[0].barcode,
            '10491538800002952958019525086156587000000414'
        )

suite = unittest.TestLoader().loadTestsFromTestCase(TestBancoCaixa)


if __name__ == '__main__':
    unittest.main()
