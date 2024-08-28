from repositorio.repositorioTrabalho import RepositorioTrabalho

class TestRepositorioTrabalho:
    def __init__(self) -> None:
        self._repositorioTrabalho = RepositorioTrabalho()

    def testDeveRetornarListaComMaisDeZeroItens(self):
        self._listaTrabalhos = self._repositorioTrabalho.pegaTodosTrabalhos()
        condicao = len(self._listaTrabalhos) != 0
        resultado = 'Sucesso' if condicao else 'Falha'
        print(resultado)