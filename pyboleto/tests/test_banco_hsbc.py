# -*- coding: utf-8 -*-
import unittest
import datetime

from pyboleto.bank.hsbc import BoletoHsbc

class TestBancoHsbc(unittest.TestCase):
    def setUp(self):
        d = BoletoHsbc()
        d.carteira = '06'
        d.agencia_cedente = '1172'
        d.conta_cedente = '8351202'
        d.data_vencimento = datetime.date(2011, 2, 5)
        d.data_documento = datetime.date(2011, 1, 18)
        d.data_processamento = datetime.date(2011, 1, 18)
        d.valor_documento = 8280.00
        d.nosso_numero = '2125525'
        d.numero_documento = '2125525'
        self.dados = d

    def test_linha_digitavel(self):
        self.assertEqual(self.dados.linha_digitavel, 
            '23790.27804 60000.212559 25003.923205 4 48690000828000'
        )
    
    def test_codigo_de_barras(self):
        self.assertEqual(self.dados.barcode, 
            '23794486900008280000278060000212552500392320'
        )

    def test_agencia(self):
        self.assertEqual(self.dados.agencia_cedente, '1172-0')

    def test_conta(self):
        self.assertEqual(self.dados.conta_cedente, '8351202')

if __name__ == '__main__':
    unittest.main()

