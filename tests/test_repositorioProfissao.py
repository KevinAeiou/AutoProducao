from repositorio.repositorioProfissao import RepositorioProfissao
from repositorio.repositorioPersonagem import RepositorioPersonagem

class TestRepositorioProfisssao:
    repositorioPersonagem = RepositorioPersonagem()
    personagemTeste = repositorioPersonagem.pegaTodosPersonagens()[0]
    repositorioProfissao = RepositorioProfissao(personagemTeste)

    def testDeveRetornarListaComNoveProfissoes(self):
        listaProfissoes = self.repositorioProfissao.pegaTodasProfissoes()
        assert len(listaProfissoes) == 9
        # condicao = len(self.listaProfissoes) == 9
        # resultado = 'Sucesso' if condicao else 'Falha'
        # print(resultado)

    def testDeveModificarPrimeiraProfissao(self):
        listaProfissoes = self.repositorioProfissao.pegaTodasProfissoes()
        self.primeiraProfissao = listaProfissoes[0]
        self.primeiraProfissao.setExperiencia(1000)
        self.repositorioProfissao.modificaProfissao(self.primeiraProfissao)
        listaProfissoes = self.repositorioProfissao.pegaTodasProfissoes()
        assert listaProfissoes[0].pegaExperiencia() == 1000
        # condicao = self.listaProfissoes[0].pegaExperiencia() == 1000
        # resultado = 'Sucesso' if condicao else 'Falha'
        # print(resultado)

    def testDeveMostrarListadeProfissoesOrdenadaPorExperiencia(self):
        self.repositorioProfissao.mostraListaProfissoes()
