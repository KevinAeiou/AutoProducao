from main import Aplicacao
from repositorio.repositorioProfissao import *
from repositorio.repositorioPersonagem import *
from repositorio.repositorioTrabalhoProducao import *
from constantes import *

class TesteAplicacao:
    _personagemTeste = RepositorioPersonagem().pegaTodosPersonagens()[0]
    aplicacao = Aplicacao()
    _repositorioProfissao = RepositorioProfissao(_personagemTeste)
    _repositorioTrabalhoProducao = RepositorioTrabalhoProducao(_personagemTeste)

    def testDeveRetornarQuantidadeUmQuandoProdutoForVendido(self):
        texto = 'Item vendido Atiradora do silêncioabsoluto x1 por 58888 de Ouro'
        esperado = 1
        listaTextoCarta = texto.split()
        recebido = self.aplicacao.retornaQuantidadeTrabalhoVendido(listaTextoCarta)
        assert esperado == recebido

    def testDeveRetornarValor58888QuandoProdutoForVendido(self):
        texto = 'Item vendido Atiradora do silêncioabsoluto x1 por 58888 de Ouro'
        esperado = 58888
        listaTextoCarta = texto.split()
        recebido = self.aplicacao.retornaValorTrabalhoVendido(listaTextoCarta)
        assert esperado == recebido

    def testDeveRetornarZeroQuandoPalavraPorNaoForEncontrada(self):
        texto = 'Item vendido Atiradora do silêncioabsoluto x1 58888 de Ouro'
        esperado = 0
        listaTextoCarta = texto.split()
        recebido = self.aplicacao.retornaValorTrabalhoVendido(listaTextoCarta)
        assert esperado == recebido

    def testDeveDefinirListaDeProfissoesNecessariasComUmItem(self):
        self.aplicacao._dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO] = self._personagemTeste
        self.aplicacao.inicializaChavesPersonagem()
        self.aplicacao.defineChaveListaDicionariosProfissoesNecessarias()
        esperado = 1
        recebido = len(self.aplicacao._dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSOES_NECESSARIAS])
        assert esperado == recebido

    def testDeveRetornarPosicaoUmQuandoProfissaoForArmaDeLongoAlcance(self):
        self.aplicacao._dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO] = self._personagemTeste
        self.aplicacao.inicializaChavesPersonagem()
        self.aplicacao.defineChaveListaDicionariosProfissoesNecessarias()
        esperado = 1    
        profissao = self.aplicacao._dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSOES_NECESSARIAS][0]
        recebido =profissao.pegaPosicao()
        assert esperado == recebido