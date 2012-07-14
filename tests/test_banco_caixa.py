# -*- coding: utf-8 -*-
import unittest
import datetime

from pyboleto.bank.caixa import BoletoCaixa

from .testutils import BoletoTestCase


class TestBancoCaixa(BoletoTestCase):
    def setUp(self):
        d = BoletoCaixa()
        d.carteira = 'SR'
        d.agencia_cedente = '1565'
        d.conta_cedente = '87000000414'
        d.data_vencimento = datetime.date(2012, 7, 8)
        d.data_documento = datetime.date(2012, 7, 3)
        d.data_processamento = datetime.date(2012, 7, 3)
        d.valor_documento = 2952.95
        d.nosso_numero = '8019525086'
        d.numero_documento = '270319510'
        self.dados = d

    def test_linha_digitavel(self):
        self.assertEqual(self.dados.linha_digitavel,
            '10498.01952 25086.156582 70000.004146 1 53880000295295'
        )

    def test_tamanho_codigo_de_barras(self):
        self.assertEqual(len(self.dados.barcode), 44)

    def test_codigo_de_barras(self):
        self.assertEqual(self.dados.barcode,
            '10491538800002952958019525086156587000000414'
        )

suite = unittest.TestLoader().loadTestsFromTestCase(TestBancoCaixa)


if __name__ == '__main__':
    unittest.main()
