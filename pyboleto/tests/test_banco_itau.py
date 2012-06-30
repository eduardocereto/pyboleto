# -*- coding: utf-8 -*-
import unittest
import datetime

from pyboleto.bank.itau import BoletoItau

class TestBancoItau(unittest.TestCase):
    def setUp(self):
        d = BoletoItau()
        d.carteira = '175'
        d.agencia_cedente = '1565'
        d.conta_cedente = '13877'
        d.data_vencimento = datetime.date(2012, 7, 4)
        d.data_documento = datetime.date(2012, 6, 29)
        d.data_processamento = datetime.date(2012, 6, 29)
        d.valor_documento = 2952.95
        d.nosso_numero = '0123'
        d.numero_documento = '0123'
        self.dados = d

    def test_linha_digitavel(self):
        self.assertEqual(self.dados.linha_digitavel, 
            '34191.75124 34567.861561 51387.710000 7 53840000295295'
        )
    
    def test_codigo_de_barras(self):
        self.assertEqual(self.dados.barcode, 
            ''
        )

    def test_agencia(self):
        self.assertEqual(self.dados.agencia_cedente, '1565')

    def test_conta(self):
        self.assertEqual(self.dados.conta_cedente, '13877')

if __name__ == '__main__':
    unittest.main()

