from repositorio.repositorioProfissao import RepositorioProfissao
from repositorio.repositorioPersonagem import RepositorioPersonagem

class TestRepositorioProfisssao:
    _personagemTeste = RepositorioPersonagem().pegaTodosPersonagens()[0]
    _repositorioProfissao = RepositorioProfissao(_personagemTeste)

    def testDeveRetornarListaComNoveProfissoes(self):
        esperado = 9
        listaProfissoes = self._repositorioProfissao.listaProfissoes
        recebido = len(listaProfissoes)
        assert esperado == recebido

    def testDeveModificarPrimeiraProfissao(self):
        esperado = 1000
        listaProfissoes = self._repositorioProfissao.listaProfissoes
        listaProfissoes[0].setExperiencia(1000)
        self._repositorioProfissao.modificaProfissao(listaProfissoes[0])
        listaProfissoes = self._repositorioProfissao.pegaTodasProfissoes()
        recebido = listaProfissoes[0].pegaExperiencia()
        assert esperado == recebido
        
    def testDeveRetornarPosicaoUmQuandoProfissaoEhPrimeira(self):
        profissaoTeste = self._repositorioProfissao.listaProfissoes[0]
        esperado = 1
        recebido = profissaoTeste.pegaPosicao()
        assert esperado == recebido
        
    def testDeveRetornarPosicaoDoisQuandoProfissaoEhSegunda(self):
        profissaoTeste = self._repositorioProfissao.listaProfissoes[1]
        esperado = 2
        recebido = profissaoTeste.pegaPosicao()
        assert esperado == recebido