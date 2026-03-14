from repositorio.repositorioTrabalho import RepositorioTrabalho

class TestRepositorioTrabalho:
    _repositorioTrabalho = RepositorioTrabalho()

    def testDeveRetornarListaComMaisDeZeroItens(self):
        self._listaTrabalhos = self._repositorioTrabalho.pega_todos_trabalhos()
        assert len(self._listaTrabalhos) != 0