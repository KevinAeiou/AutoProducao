from repositorio.repositorioPersonagem import RepositorioPersonagem

class TestRepositorioPersonagem:
    _repositorio = RepositorioPersonagem()
    _personagemTeste = _repositorio.listaPersonagens[0]

    def testDeveRetornarListaComOitoPersonagens(self):
        esperado = 8
        recebido = len(self._repositorio.listaPersonagens)
        assert esperado == recebido

    def testDeveAlternarChaveUso(self):
        esperado = not self._personagemTeste.pegaUso()
        self._repositorio.alternaUso(self._personagemTeste)
        self._listaPersonagens = self._repositorio.pegaTodosPersonagens()
        personagemTesteModificado = self._listaPersonagens[0]
        recebido = personagemTesteModificado.pegaUso()
        assert esperado == recebido

    def testDeveAlternarChaveEstado(self):
        esperado = not self._personagemTeste.pegaEstado()
        self._repositorio.alternaEstado(self._personagemTeste)
        self._listaPersonagens = self._repositorio.pegaTodosPersonagens()
        personagemTesteModificado = self._listaPersonagens[0]
        recebido = personagemTesteModificado.pegaEstado()
        assert esperado == recebido