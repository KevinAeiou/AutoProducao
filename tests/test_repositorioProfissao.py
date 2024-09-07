from repositorio.repositorioProfissao import RepositorioProfissao
from repositorio.repositorioPersonagem import RepositorioPersonagem

class TestRepositorioProfisssao:
    _repositorioPersonagem = RepositorioPersonagem()
    _personagemTeste = _repositorioPersonagem.pegaTodosPersonagens()[0]
    _repositorioProfissao = RepositorioProfissao(_personagemTeste)

    def testDeveRetornarListaComNoveProfissoes(self):
        esperado = 9
        listaProfissoes = self._repositorioProfissao.pegaTodasProfissoes()
        recebido = len(listaProfissoes)
        assert esperado == recebido

    def testDeveModificarPrimeiraProfissao(self):
        esperado = 1000
        listaProfissoes = self._repositorioProfissao.pegaTodasProfissoes()
        self.listaProfissoes[0].setExperiencia(1000)
        self._repositorioProfissao.modificaProfissao(self.listaProfissoes[0])
        listaProfissoes = self._repositorioProfissao.pegaTodasProfissoes()
        recebido = listaProfissoes[0].pegaExperiencia()
        assert esperado == recebido