from repositorio.repositorioPersonagem import RepositorioPersonagem

class TestRepositorioPersonagem:
    _repositorio = RepositorioPersonagem()
    _personagemTeste = _repositorio.pegaTodosPersonagens()[0]

    def testDeveRetornarListaComMaisDeZeroPersonagens(self):
        esperado = 0
        recebido = len(self._repositorio.pegaTodosPersonagens())
        assert esperado < recebido

    def testDeveAlternarChaveUso(self):
        esperado = not self._personagemTeste.uso
        self._personagemTeste.alternaUso
        self._repositorio.modificaPersonagem(self._personagemTeste)
        personagemTesteModificado = self._repositorio.pegaTodosPersonagens()[0]
        recebido = personagemTesteModificado.uso
        assert esperado == recebido

    def testDeveAlternarChaveEstado(self):
        esperado = not self._personagemTeste.estado
        self._personagemTeste.alternaEstado
        self._repositorio.modificaPersonagem(self._personagemTeste)
        personagemTesteModificado = self._repositorio.pegaTodosPersonagens()[0]
        recebido = personagemTesteModificado.estado
        assert esperado == recebido