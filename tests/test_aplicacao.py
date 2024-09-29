from main import Aplicacao

class TesteAplicacao:
    __aplicacao = Aplicacao()

    def testDeveRetornarQuantidadeUmQuandoProdutoForVendido(self):
        texto = 'Item vendido BraceleteTranscendental x1 por 173333 deOuroTaxa do mercado 17333 de Ouro'
        esperado = 1
        listaTextoCarta = texto.split()
        recebido = self.__aplicacao.retornaQuantidadeTrabalhoVendido(listaTextoCarta)
        assert esperado == recebido

    def testDeveRetornarValor58888QuandoProdutoForVendido(self):
        texto = 'Item vendido BraceleteTranscendental x1 por 173333 deOuroTaxa do mercado 17333 de Ouro'
        esperado = 173333
        listaTextoCarta = texto.split()
        recebido = self.__aplicacao.retornaValorTrabalhoVendido(listaTextoCarta)
        assert esperado == recebido

    def testDeveRetornarZeroQuandoPalavraPorNaoForEncontrada(self):
        texto = 'Item vendido Atiradora do silêncioabsoluto x1 58888 de Ouro'
        esperado = 0
        listaTextoCarta = texto.split()
        recebido = self.__aplicacao.retornaValorTrabalhoVendido(listaTextoCarta)
        assert esperado == recebido

    def testDeveRetornarStringIdQuandoMetodoRetornaChaveIdTrabalhoEhChamado(self):
        texto = 'Item vendido BraceleteTranscendental x1 por 173333 deOuroTaxa do mercado 17333 de Ouro'
        listaTextoCarta = texto.split()
        esperado = 'e0e6eb2f-3665-47c9-8c70-956e871f3eb1'
        recebido = self.__aplicacao.retornaChaveIdTrabalho(listaTextoCarta)
        assert esperado == recebido