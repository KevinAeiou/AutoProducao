from repositorio.repositorioProfissao import RepositorioProfissao
from repositorio.repositorioPersonagem import RepositorioPersonagem

class TestRepositorioProfisssao:
    repositorioProfissao = None
    listaProfissoes = []

    def __init__(self) -> None:
        self.repositorioPersonagem = RepositorioPersonagem()
        self.personagemTeste = self.repositorioPersonagem.pegaTodosPersonagens()[0]
        self.repositorioProfissao = RepositorioProfissao(self.personagemTeste)
        self.listaProfissoes = self.repositorioProfissao.pegaTodasProfissoes()

    def testDeveRetornarListaComNoveProfissoes(self):
        self.listaProfissoes = self.repositorioProfissao.pegaTodasProfissoes()
        # assert len(self.listaProfissoes) != 0
        condicao = len(self.listaProfissoes) == 9
        resultado = 'Sucesso' if condicao else 'Falha'
        print(resultado)

    def testDeveModificarPrimeiraProfissao(self):
        self.primeiraProfissao = self.listaProfissoes[0]
        self.primeiraProfissao.setExperiencia(1000)
        self.repositorioProfissao.modificaProfissao(self.primeiraProfissao)
        self.listaProfissoes = self.repositorioProfissao.pegaTodasProfissoes()
        condicao = self.listaProfissoes[0].pegaExperiencia() == 1000
        resultado = 'Sucesso' if condicao else 'Falha'
        print(resultado)

    def testDeveMostrarListadeProfissoesOrdenadaPorExperiencia(self):
        self.repositorioProfissao.mostraListaProfissoes()
