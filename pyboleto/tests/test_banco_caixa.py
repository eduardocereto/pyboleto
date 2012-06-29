# -*- coding: utf-8 -*-
import unittest
import datetime

from pyboleto.bank.caixa import BoletoCaixa

class TestBancoCaixa(unittest.TestCase):
    def setUp(self):
        d = BoletoCaixa()
        d.carteira = 'SR'
        d.inicio_nosso_numero = '80'
        d.agencia_cedente = '1565'
        d.conta_cedente = '414-3'
        d.data_vencimento = datetime.date(2011, 2, 5)
        d.data_documento = datetime.date(2011, 1, 18)
        d.data_processamento = datetime.date(201, 1, 18)
        d.valor_documento = 355.00
        d.nosso_numero = '19525086'
        d.numero_documento = '19525086'
        self.dados = d

    def test_linha_digitavel(self):
        self.assertEqual(self.dados.linha_digitavel, 
            '10498.01952 25086.156509 00000.004143 7 48690000035500'
        )
    
    def test_tamanho_codigo_de_barras(self):
        self.assertEqual(len(self.dados.barcode), 44)

    def test_codigo_de_barras(self):
        self.assertEqual(self.dados.barcode, 
            '10497486900000355008019525086156500000000414'
        )

if __name__ == '__main__':
    unittest.main()

