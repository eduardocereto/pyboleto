# -*- coding: utf-8 -*-
"""
    pyboleto.html
    ~~~~~~~~~~~~

    Classe Responsável por fazer o output do boleto em html.

    :copyright: © 2011 - 2012 by Eduardo Cereto Carvalho
    :license: BSD, see LICENSE for more details.

"""
import os

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
        self.width = 750
        self.widthCanhoto = 0
        self.fontSizeTitle = 9
        self.heightLine = 27
        self.fontSizeValue = 12
        self.htmlTitle = 'Boleto bancário'
        self.fileDescr = file_descr # Posso atribuir um file handler também aqui

        if landscape:
            style = '' # Tratar landscape
        else:
            style = """html,body{{margin:0;padding:0}}
            hr{{border:1px dashed #000}}
            p{{margin:0}}
            .pagina{{width:{}px;font-family:Helvetica, Arial, "Lucida Grande", sans-serif;font-size:{}px;margin:50px auto;page-break-a}}
            .recibo-sacado{{margin-bottom:50px}}
            .demonstrativo{{height:190px}}
            .autenticacao-mecanica{{height:80px}}
            .recibo-caixa{{margin-top:30px}}
            .cabecalho td{{border-bottom:4px solid #000;vertical-align:bottom;padding:0}}
            .cabecalho td.banco-logo{{width:170px}}
            .cabecalho td.banco-logo img{{float:left;margin:0;padding:0}}
            .cabecalho td.banco-codigo{{width:70px;font-size:22px;font-weight:700;text-align:center}}
            .cabecalho td.bol-linha-digitavel{{border-right:none;text-align:right;font-size:16px;font-weight:700}}
            .cabecalho .linhas-v{{border-left:3px solid #000;border-right:3px solid #000}}
            .corpo td{{border-bottom:1px solid #000;border-right:1px solid #000;vertical-align:top;height:{}px;padding:0 2px}}
            .corpo td.linha-vazia{{border-bottom:none}}
            .recibo-sacado .corpo tr td:last-child{{border-right:none;text-align:left}}
            .recibo-caixa .corpo tr td:last-child{{border-right:none;text-align:right;width:140px}}
            .rodape td{{border:none;vertical-align:top;padding-left:2px}}
            .rodape td.bol-codigo-barras{{padding:8px 6px}}
            .rotulo{{text-align:left;font-size:{}px;margin-bottom:2px}}
            .autenticacao-mecanica .rotulo{{text-align:right}}
            tr.linha-grossa td{{border-bottom:3px solid #000}}
            .recibo-sacado .corpo .col-cedente-agencia,.recibo-sacado .corpo .col-cedente-documento{{width:130px}}
            .recibo-sacado .corpo .col-vencimento{{width:100px}}
            .recibo-caixa .corpo .col-data-documento{{width:120px}}
            .recibo-caixa .corpo .col-numero-documento{{width:140px}}
            .recibo-caixa .rodape .col-sacado{{width:40px}}
            .recibo-caixa .rodape .col-codigo-baixa{{width:210px}}
            .cabecalho,.corpo,.rodape{{width:100%;border-collapse:collapse}}
            .recibo-caixa .corpo .col-especie-documento,.recibo-caixa .corpo .col-aceite{{width:70px}}
            .bol-codigo-barras{{height:40px}}
            /* @media print{{.pagina {{page-break-after:always}} }} */
            """.format(self.width, self.fontSizeValue, self.heightLine, self.fontSizeTitle)

        self.html = '<!DOCTYPE html><html lang="en"><head><title>{}</title><meta charset="utf-8" /><style>{}</style></head><body><div class="pagina">'.format(self.htmlTitle, style)

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

        # Cabeçalho
        logo_image_path = ''
        if boletoDados.logo_image:
            # Verificar carregamento da imagem
            logo_image_path = '<img src="{}" alt="Logo do banco" />'.format(self._load_image(boletoDados.logo_image))

        self.html += """<div class="recibo-sacado">
        <table class="cabecalho">
            <tbody>
                <tr>
                    <td class="banco-logo">{}</td>
                    <td class="banco-codigo"><div class="linhas-v">{}</div></td>
                    <td class="bol-linha-digitavel">Recibo do Sacado</td>
                </tr>
            </tbody>
        </table>
        """.format(logo_image_path, boletoDados.codigo_dv_banco)
        
        # Corpo
        self.html += """<table class="corpo">
        <tbody>
            <tr>
                <td>
                    <div class="rotulo">Cedente</div> {}
                </td>
                <td class="col-cedente-agencia">
                    <div class="rotulo">Agência/Código Cedente</div> {}
                </td>
                <td class="col-cedente-documento">
                    <div class="rotulo">CPF/CNPJ Cedente</div> {}
                </td>
                <td class="col-vencimento">
                    <div class="rotulo">Vencimento</div> {}
                </td>
            </tr>
        """.format(boletoDados.cedente, boletoDados.agencia_conta_cedente, 
            boletoDados.cedente_documento, boletoDados.data_vencimento.strftime('%d/%m/%Y'))

        sacado0 = boletoDados.sacado[0]
        if len(sacado0) > 63: # Melhorar isso
            sacado0 = sacado0[:63-len(sacado0)-4] + ' ...'

        self.html += """<tr>
                <td>
                    <div class="rotulo">Sacado</div> {}
                </td>
                <td>
                    <div class="rotulo">Nosso Número</div> {}
                </td>
                <td>
                    <div class="rotulo">N. do documento</div> {}
                </td>
                <td>
                    <div class="rotulo">Data Documento</div> {}
                </td>
            </tr>
        """.format(sacado0, boletoDados.format_nosso_numero(), 
            boletoDados.numero_documento, boletoDados.data_documento.strftime('%d/%m/%Y'))

        valorDocumento = self._formataValorParaExibir(boletoDados.valor_documento)

        self.html += """<tr>
                <td colspan="3">
                    <div class="rotulo">Endereço Cedente</div> {}
                </td>
                <td width="100px" class="col-dir">
                    <div class="rotulo">Valor Documento</div> {}
                </td>
            </tr>
        </tbody></table></div>
        """.format(boletoDados.cedente_endereco, valorDocumento)

        # Demonstrativo
        self.html += '<div class="demonstrativo"><div class="rotulo">Demonstrativo</div>'
        for dm in boletoDados.demonstrativo:
            self.html += '<p>{}</p>'.format(dm)
        self.html += '</div>'

        # Autenticação mecânica
        self.html += """<div class="autenticacao-mecanica">
            <div class="rotulo">Autenticação Mecânica</div>
        </div>"""

    def _drawHorizontalCorteLine(self):
        self.html += '<hr />'

    def _drawReciboCaixa(self, boletoDados):
        """Imprime o Recibo do Caixa

        :param boletoDados: Objeto com os dados do boleto a ser preenchido.
            Deve ser subclasse de :class:`pyboleto.data.BoletoData`
        :type boletoDados: :class:`pyboleto.data.BoletoData`

        """

        # Cabeçalho
        logo_image_path = ''
        if boletoDados.logo_image:
            # Verificar carregamento da imagem
            logo_image_path = '<img src="{}" alt="Logo do banco" />'.format(self._load_image(boletoDados.logo_image))

        self.html += """<div class="recibo-caixa">
        <table class="cabecalho">
            <tbody>
                <tr>
                    <td class="banco-logo">{}</td>
                    <td class="banco-codigo"><div class="linhas-v">{}</div></td>
                    <td class="bol-linha-digitavel">{}</td>
                </tr>
            </tbody>
        </table>
        """.format(logo_image_path, boletoDados.codigo_dv_banco, boletoDados.linha_digitavel)

        # Corpo
        self.html += """<table class="corpo">
        <tbody>
            <tr>
                <td colspan="6">
                    <div class="rotulo">Local de pagamento</div> {}
                </td>
                <td>
                    <div class="rotulo">Vencimento</div> {}
                </td>
            </tr>
            <tr>
                <td colspan="6">
                    <div class="rotulo">Cedente</div> {}
                </td>
                <td>
                    <div class="rotulo">Agência/Código cedente</div> {}
                </td>
            </tr>
        """.format(boletoDados.local_pagamento.encode('utf-8'), boletoDados.data_vencimento.strftime('%d/%m/%Y'),
            boletoDados.cedente, boletoDados.agencia_conta_cedente)

        self.html += """<tr>
                <td class="col-data-documento">
                    <div class="rotulo">Data do documento</div> {}
                </td>
                <td class="col-numero-documento" colspan="2">
                    <div class="rotulo">N. do documento</div> {}
                </td>
                <td class="col-especie-documento">
                    <div class="rotulo">Espécie doc</div> {}
                </td>
                <td class="col-aceite">
                    <div class="rotulo">Aceite</div> {}
                </td>
                <td>
                    <div class="rotulo">Data processamento</div> {}
                </td>
                <td>
                    <div class="rotulo">Nosso número</div> {}
                </td>
            </tr>
        """.format(boletoDados.data_documento.strftime('%d/%m/%Y'), boletoDados.numero_documento,
            boletoDados.especie_documento, boletoDados.aceite, 
            boletoDados.data_processamento.strftime('%d/%m/%Y'), boletoDados.format_nosso_numero())

        valorDocumento = self._formataValorParaExibir(boletoDados.valor_documento)
        valor = self._formataValorParaExibir(boletoDados.valor)
        self.html += """<tr>
                <td>
                    <div class="rotulo">Uso do banco</div>
                </td>
                <td>
                    <div class="rotulo">Carteira</div> {}
                </td>
                <td>
                    <div class="rotulo">Espécie</div> {}
                </td>
                <td colspan="2">
                    <div class="rotulo">Quantidade</div> {}
                </td>
                <td>
                    <div class="rotulo">Valor</div> {}
                </td>
                <td>
                    <div class="rotulo">(=) Valor documento</div> {}
                </td>
            </tr>
        """.format(boletoDados.carteira, boletoDados.especie, boletoDados.quantidade, valor, valorDocumento)

        intrucoes = ['','','']
        for i in range(3):
            try:
                intrucoes[i] = boletoDados.instrucoes[i]
            except:
                pass

        self.html += """<tr>
                <td colspan="6" class="linha-vazia">
                    <div class="rotulo">Instruções 
                    (Todas as informações deste bloqueto são de exclusiva responsabilidade do cedente)</div> {}
                </td>
                <td>
                    <div class="rotulo">(-) Descontos/Abatimentos</div>
                </td>
            </tr>
            <tr>
                <td colspan="6" class="linha-vazia">{}</td>
                <td>
                    <div class="rotulo">(-) Outras deduções</div>
                </td>
            </tr>
            <tr>
                <td colspan="6" class="linha-vazia">{}</td>
                <td>
                    <div class="rotulo">(+) Mora/Multa</div>
                </td>
            </tr>
            <tr>
                <td colspan="6" class="linha-vazia"></td>
                <td>
                    <div class="rotulo">(+) Outros acréscimos</div>
                </td>
            </tr>
            <tr class="linha-grossa">
                <td colspan="6"></td>
                <td>
                    <div class="rotulo">(=) Valor cobrado</div>
                </td>
            </tr>
        </tbody></table>
        """.format(intrucoes[0], intrucoes[1], intrucoes[2])

        # Rodapé
        self.html += """<table class="rodape">
        <tbody>
            <tr>
                <td class="col-sacado"><div class="rotulo">Sacado</div></td>
                <td colspan="3">"""

        for linha_sacado in boletoDados.sacado:
            self.html += '<p>{}</p>'.format(linha_sacado)

        self.html += """</td>
            </tr>
            <tr class="linha-grossa">
                <td colspan="3"><div class="rotulo">Sacador / Avalista</div></td>
                <td class="col-codigo-baixa"><div class="rotulo">Código de baixa</div></td>
            </tr>
            <tr>
                <td colspan="3" class="bol-codigo-barras">
                    <!--<img src="cod_barras.jpg" alt="Código de barras" />-->
                </td>
                <td><div class="rotulo">Autenticação Mecânica / Ficha de Compensação</div></td>
            </tr>
        </tbody></table></div>
        """.format()

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

        self.html += """</div><div class="pagina">"""

    def save(self):
        """Fecha boleto e constroi o arquivo"""

        self.html += """</div></body></html>"""
        try:
            fd = open(self.fileDescr, 'w')
            fd.write(self.html)
        except:
            raise IOError('Falha ao escrever o arquivo')
        else:
            fd.close()

    def _formataValorParaExibir(self, nfloat):
        if nfloat:
            txt = nfloat
            txt = txt.replace('.', ',')
        else:
            txt = ""
        return txt