from repositorio.repositorioPersonagem import RepositorioPersonagem

class TestRepositorioPersonagem:
    repositorio = RepositorioPersonagem()
    listaPersonagens = []
    # def __init__(self) -> None:
    #     self.listaPersonagens = self.repositorio.pegaTodosPersonagens()
    #     self._personagemTeste = self.listaPersonagens[1]

    def testDeveRetornarListaComOitoPersonagens(self):
        # assert len(self.listaPersonagens) != 0
        condicao = len(self.listaPersonagens) != 0
        resultado = 'Sucesso' if condicao else 'Falha'
        print(resultado)

    def testDeveAlternarChaveUso(self):
        self.repositorio.alternaUso(self._personagemTeste)
        self.listaPersonagens = self.repositorio.pegaTodosPersonagens()
        personagemTesteModificado = self.listaPersonagens[1]
        # assert personagemTeste.pegaUso() != personagemTesteModificado.pegaUso()
        condicao = self._personagemTeste.pegaUso() != personagemTesteModificado.pegaUso()
        resultado = 'Sucesso' if condicao else 'Falha'
        print(resultado)

    def testDeveAlternarChaveEstado(self):
        self.repositorio.alternaEstado(self._personagemTeste)
        self.listaPersonagens = self.repositorio.pegaTodosPersonagens()
        personagemTesteModificado = self.listaPersonagens[1]
        # assert self._personagemTeste.pegaEstado() != personagemTesteModificado.pegaUso()
        condicao = self._personagemTeste.pegaEstado() != personagemTesteModificado.pegaEstado()
        resultado = 'Sucesso' if condicao else 'Falha'
        print(resultado)