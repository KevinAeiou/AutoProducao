from main import Aplicacao
from modelos.trabalhoProducao import TrabalhoProducao

class TesteAplicacao:
    __aplicacao = Aplicacao()

    def testDeveRetornarQuantidadeUmQuandoProdutoForVendido(self):
        texto = 'Item vendido BraceleteTranscendental x1 por 173333 deOuroTaxa do mercado 17333 de Ouro'
        esperado = 1
        recebido = self.__aplicacao.retornaQuantidadeTrabalhoVendido(texto)
        assert esperado == recebido

    def testDeveRetornarValor58888QuandoProdutoForVendido(self):
        texto = 'Item vendido BraceleteTranscendental x1 por 173333 deOuroTaxa do mercado 17333 de Ouro'
        esperado = 173333
        recebido = self.__aplicacao.retornaValorTrabalhoVendido(texto)
        assert esperado == recebido

    def testDeveRetornarZeroQuandoPalavraPorNaoForEncontrada(self):
        texto = 'Item vendido Atiradora do silêncioabsoluto x1 58888 de Ouro'
        esperado = 0
        recebido = self.__aplicacao.retornaValorTrabalhoVendido(texto)
        assert esperado == recebido

    def testDeveRetornarStringIdQuandoMetodoRetornaChaveIdTrabalhoEhChamado(self):
        texto = 'Item vendido BraceleteTranscendental x1 por 173333 deOuroTaxa do mercado 17333 de Ouro'
        esperado = 'Jj77Su2yveC7DKuWSaflMxo1Mhbl'
        recebido = self.__aplicacao.retornaChaveIdTrabalho(texto)
        assert esperado == recebido

    def testDeveRetornarMesmoObjetoTrabalhoProducaoComNomeIdQuandoMetodoDefineCloneDicionarioTrabalhoDesejadoEhChamado(self):
        trabalhoTeste = TrabalhoProducao()
        trabalhoTeste.idTrabalho = '123'
        trabalhoTeste.nome = 'Nome teste'
        trabalhoTeste.nomeProducao = 'Nome teste'
        trabalhoTeste.setExperiencia = 0
        trabalhoTeste.setNivel = 10
        trabalhoTeste.profissao = 'Profissão teste'
        trabalhoTeste.raridade = 'Comum'
        trabalhoTeste.trabalhoNecessario = ''
        trabalhoTeste.recorrencia = False
        trabalhoTeste.tipo_licenca = 'Licença teste'
        trabalhoTeste.estado = 0
        cloneTrabalhoTeste = self.__aplicacao.defineCloneTrabalhoProducao(trabalhoTeste)
        idEsperado = trabalhoTeste.id
        idRecebido = cloneTrabalhoTeste.id
        nomeEsperado = trabalhoTeste.nome
        nomeRecebido = cloneTrabalhoTeste.nome
        assert idEsperado != idRecebido
        assert nomeEsperado == nomeRecebido