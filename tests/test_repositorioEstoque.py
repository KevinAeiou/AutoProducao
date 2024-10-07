from repositorio.repositorioEstoque import RepositorioEstoque
from repositorio.repositorioPersonagem import RepositorioPersonagem
from modelos.trabalhoEstoque import TrabalhoEstoque

class TestRepositorioEstoque:
    _listaTrabalhosEstoque = []
    _repositorioPersonagem = RepositorioPersonagem()
    _personagemTeste = _repositorioPersonagem.pegaTodosPersonagens()[0]
    _repositorioEstoque = RepositorioEstoque(_personagemTeste)
    _trabalhoTeste = TrabalhoEstoque('', 'NomeTeste', 'ProfissaoTeste', 0, 1, 'RaridadeTeste', 'IdTeste')

    def testDeveRetornaListaComMaisDeZeroItens(self):
        esperado = 0
        self._listaTrabalhosEstoque = self._repositorioEstoque.pegaTodosTrabalhosEstoque()
        recebido = len(self._listaTrabalhosEstoque)
        assert esperado != recebido

    def testDeveAdicionarItemAoEstoque(self):
        self._listaTrabalhosEstoque = self._repositorioEstoque.pegaTodosTrabalhosEstoque()
        esperado = len(self._listaTrabalhosEstoque)
        self._repositorioEstoque.insereTrabalhoEstoque(self._trabalhoTeste)
        self._listaTrabalhosEstoque = self._repositorioEstoque.pegaTodosTrabalhosEstoque()
        recebido = len(self._listaTrabalhosEstoque) - 1
        assert esperado == recebido

    def testDeveModificarQuantidadeDoPrimeiroItemDoEstoque(self):
        self._listaTrabalhosEstoque = self._repositorioEstoque.pegaTodosTrabalhosEstoque()
        trabalhoTeste = self._listaTrabalhosEstoque[0]
        esperado = trabalhoTeste.pegaQuantidade() + 1
        trabalhoTeste.setQuantidade(esperado)
        self._repositorioEstoque.modificaTrabalhoEstoque(trabalhoTeste)
        self._listaTrabalhosEstoque = self._repositorioEstoque.pegaTodosTrabalhosEstoque()
        trabalhoTeste = self._listaTrabalhosEstoque[0]
        recebido = trabalhoTeste.pegaQuantidade()
        assert esperado == recebido