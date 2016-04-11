# -*- coding: utf-8 -*-
"""
    pyboleto.html
    ~~~~~~~~~~~~~

    Classe Responsável por fazer o output do boleto em html.

    :copyright: © 2012 by Artur Felipe de Sousa
    :license: BSD, see LICENSE for more details.

"""
import os
import string
import sys
import codecs
import base64

from itertools import chain
if sys.version_info < (3,):
    from itertools import izip_longest as zip_longest
    zip_longest  # chamando para evitar erro de nao uso do zip_longest
else:
    from itertools import zip_longest

DIGITS = [
    ['n', 'n', 'w', 'w', 'n'],
    ['w', 'n', 'n', 'n', 'w'],
    ['n', 'w', 'n', 'n', 'w'],
    ['w', 'w', 'n', 'n', 'n'],
    ['n', 'n', 'w', 'n', 'w'],
    ['w', 'n', 'w', 'n', 'n'],
    ['n', 'w', 'w', 'n', 'n'],
    ['n', 'n', 'n', 'w', 'w'],
    ['w', 'n', 'n', 'w', 'n'],
    ['n', 'w', 'n', 'w', 'n'],
]


class BoletoHTML(object):
    """Geração do Boleto em HTML

    Esta classe é responsável por imprimir o boleto em HTML.
    Outras classes podem ser implementadas no futuro com a mesma interface,
    para fazer output em LaTeX, etc ...

    Esta classe pode imprimir boletos em formato de carnê (2 boletos por
    página) ou em formato de folha cheia.

    :param file_descr: Um arquivo ou *file-like* class.
    :param landscape: Formato da folha. Usar ``True`` para boleto
        tipo carnê.

    """

    def __init__(self, file_descr, landscape=False):
        # Tamanhos em px
        self.width = 750
        self.widthCanhoto = 0
        self.fontSizeTitle = 9
        self.heightLine = 27
        self.fontSizeValue = 12
        self.title = 'Boleto bancário'
        self.fileDescr = file_descr

        if landscape:
            raise NotImplementedError('Em desenvolvimento...')
        else:
            tpl = string.Template(self._load_template('head.html'))
            self.html = tpl.substitute(title=self.title, width=self.width,
                                       font_size_value=self.fontSizeValue,
                                       height_line=self.heightLine,
                                       font_size_title=self.fontSizeTitle)

    def _load_template(self, template):
        pyboleto_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(pyboleto_dir, 'templates', template)
        with open(template_path, 'r') as tpl:
            template_content = tpl.read()
        return template_content

    def _load_image(self, logo_image):
        pyboleto_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(pyboleto_dir, 'media', logo_image)
        return image_path

    def _drawReciboSacado(self, boletoDados):
        """Imprime o Recibo do Sacado para modelo de página inteira

        :param boletoDados: Objeto com os dados do boleto a ser preenchido.
            Deve ser subclasse de :class:`pyboleto.data.BoletoData`
        :type boletoDados: :class:`pyboleto.data.BoletoData`

        """
        tpl = string.Template(self._load_template('recibo_sacado.html'))
        tpl_data = {}

        # Cabeçalho
        tpl_data['logo_img'] = ''
        if boletoDados.logo_image:
            img = codecs.open(self._load_image(boletoDados.logo_image))
            aux = img.read()
            aux = base64.b64encode(aux)
            img_base64 = 'data:image/jpeg;base64,{0}'.format(aux)
            tpl_data['logo_img'] = img_base64
        tpl_data['codigo_dv_banco'] = boletoDados.codigo_dv_banco

        # Corpo
        tpl_data['cedente'] = boletoDados.cedente
        tpl_data['agencia_conta_cedente'] = boletoDados.agencia_conta_cedente
        tpl_data['cedente_documento'] = boletoDados.cedente_documento

        data_vencimento = boletoDados.data_vencimento
        tpl_data['data_vencimento'] = data_vencimento.strftime('%d/%m/%Y')
        tpl_data['sacado'] = boletoDados.sacado[0]
        tpl_data['nosso_numero_format'] = boletoDados.format_nosso_numero()
        tpl_data['numero_documento'] = boletoDados.numero_documento

        data_documento = boletoDados.data_documento
        tpl_data['data_documento'] = data_documento.strftime('%d/%m/%Y')
        tpl_data['cedente_endereco'] = boletoDados.cedente_endereco

        valor_doc = self._formataValorParaExibir(boletoDados.valor_documento)
        tpl_data['valor_documento'] = valor_doc

        # Demonstrativo
        tpl_data['demonstrativo'] = ''
        for dm in boletoDados.demonstrativo:
            tpl_data['demonstrativo'] += '<p>{0}</p>'.format(dm)

        self.html += tpl.substitute(tpl_data)

    def _drawHorizontalCorteLine(self):
        self.html += '<hr />'

    def _drawReciboCaixa(self, boletoDados):
        """Imprime o Recibo do Caixa

        :param boletoDados: Objeto com os dados do boleto a ser preenchido.
            Deve ser subclasse de :class:`pyboleto.data.BoletoData`
        :type boletoDados: :class:`pyboleto.data.BoletoData`

        """
        tpl = string.Template(self._load_template('recibo_caixa.html'))
        tpl_data = {}

        # Cabeçalho
        tpl_data['logo_img'] = ''
        if boletoDados.logo_image:
            tpl_data['logo_img'] = self._load_image(boletoDados.logo_image)
        tpl_data['codigo_dv_banco'] = boletoDados.codigo_dv_banco
        tpl_data['linha_digitavel'] = boletoDados.linha_digitavel

        # Corpo
        data_vencimento = boletoDados.data_vencimento
        tpl_data['data_vencimento'] = data_vencimento.strftime('%d/%m/%Y')

        # value em unicode em data.py
        if isinstance(boletoDados.local_pagamento, unicode):
            tpl_data['local_pagamento'] = boletoDados.local_pagamento.encode
            ('utf-8')
        else:
            tpl_data['local_pagamento'] = boletoDados.local_pagamento
        tpl_data['cedente'] = boletoDados.cedente
        tpl_data['agencia_conta_cedente'] = boletoDados.agencia_conta_cedente

        data_documento = boletoDados.data_documento
        tpl_data['data_documento'] = data_documento.strftime('%d/%m/%Y')
        tpl_data['numero_documento'] = boletoDados.numero_documento
        tpl_data['especie_documento'] = boletoDados.especie_documento
        tpl_data['aceite'] = boletoDados.aceite

        data_process = boletoDados.data_processamento
        tpl_data['data_processamento'] = data_process.strftime('%d/%m/%Y')
        tpl_data['nosso_numero_format'] = boletoDados.format_nosso_numero()
        tpl_data['carteira'] = boletoDados.carteira
        tpl_data['especie'] = boletoDados.especie
        tpl_data['quantidade'] = boletoDados.quantidade

        valor = self._formataValorParaExibir(boletoDados.valor)
        tpl_data['valor'] = valor

        valor_doc = self._formataValorParaExibir(boletoDados.valor_documento)
        tpl_data['valor_documento'] = valor_doc

        # Instruções
        tpl_data['instrucoes'] = ''
        for instrucao in boletoDados.instrucoes:
            tpl_data['instrucoes'] += '<p>{0}</p>'.format(instrucao)

        # Rodapé
        tpl_data['sacado_info'] = ''
        for linha_sacado in boletoDados.sacado:
            tpl_data['sacado_info'] += '<p>{0}</p>'.format(linha_sacado)

        # Código de barras
        tpl_data['barcode'] = self._codigoBarraI25(boletoDados.barcode)

        self.html += tpl.substitute(tpl_data)

    def drawBoletoCarneDuplo(self, boletoDados1, boletoDados2=None):
        """Imprime um boleto tipo carnê com 2 boletos por página.

        :param boletoDados1: Objeto com os dados do boleto a ser preenchido.
            Deve ser subclasse de :class:`pyboleto.data.BoletoData`
        :param boletoDados2: Objeto com os dados do boleto a ser preenchido.
            Deve ser subclasse de :class:`pyboleto.data.BoletoData`
        :type boletoDados1: :class:`pyboleto.data.BoletoData`
        :type boletoDados2: :class:`pyboleto.data.BoletoData`

        """
        raise NotImplementedError('Em desenvolvimento')

    def drawBoleto(self, boletoDados):
        """Imprime Boleto Convencional

        Você pode chamar este método diversas vezes para criar um arquivo com
        várias páginas, uma por boleto.

        :param boletoDados: Objeto com os dados do boleto a ser preenchido.
            Deve ser subclasse de :class:`pyboleto.data.BoletoData`
        :type boletoDados: :class:`pyboleto.data.BoletoData`
        """
        self._drawReciboSacado(boletoDados)
        self._drawHorizontalCorteLine()
        self._drawReciboCaixa(boletoDados)
        self._drawHorizontalCorteLine()

    def nextPage(self):
        """Força início de nova página"""
        self.html += '</div><div class="pagina">'

    def save(self):
        """Fecha boleto e constroi o arquivo"""
        self.html += '</div></body></html>'
        if hasattr(self.fileDescr, 'write'):
            self.fileDescr.write(self.html)
        else:
            with open(self.fileDescr, 'w') as fd:
                fd.write(self.html)

    def _formataValorParaExibir(self, nfloat):
        if nfloat:
            txt = nfloat
            txt = txt.replace('.', ',')
        else:
            txt = ""
        return txt

    def _codigoBarraI25(self, code):
        """Imprime Código de barras otimizado para boletos
        http://en.wikipedia.org/wiki/Interleaved_2_of_5
        """
        digits = ['n', 'n s', 'n', 'n s']

        if len(code) % 2 != 0:
            code = '0' + code

        for digt1, digt2 in self._grouper(2, code):
            digt1_repr = DIGITS[int(digt1)]
            digt2_repr = map(lambda x: x + ' s', DIGITS[int(digt2)])
            digits.extend(chain(*zip(digt1_repr, digt2_repr)))

        digits.extend(['w', 'n s', 'n'])

        result = []
        for digit in digits:
            result.append('<span class="{0}"></span>'.format(digit))

        return ''.join(result)

    def _grouper(self, n, iterable, fillvalue=None):
        """grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"""
        args = [iter(iterable)] * n
        return zip_longest(fillvalue=fillvalue, *args)
