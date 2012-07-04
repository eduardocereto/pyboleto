# -*- coding: utf-8 -*-
import unittest
import datetime

from pyboleto.bank.real import BoletoReal

class TestBancoBradesco(unittest.TestCase):
    def setUp(self):
        d = BoletoReal()
        d.carteira = '06'
        d.agencia_cedente = '0531'
        d.conta_cedente = '5705853'
        d.data_vencimento = datetime.date(2011, 2, 5)
        d.data_documento = datetime.date(2011, 1, 18)
        d.data_processamento = datetime.date(201, 1, 18)
        d.valor_documento = 355.00
        d.nosso_numero = '123'
        d.numero_documento = '123'
        self.dados = d

    def test_linha_digitavel(self):
        self.assertEqual(self.dados.linha_digitavel, 
            '35690.53154 70585.390001 00000.001230 8 48690000035500'
        )
    
    def test_codigo_de_barras(self):
        self.assertEqual(self.dados.barcode, 
            '35698486900000355000531570585390000000000123'
        )

if __name__ == '__main__':
    unittest.main()

