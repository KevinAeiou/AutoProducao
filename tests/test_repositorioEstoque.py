from repositorio.repositorioEstoque import RepositorioEstoque
from repositorio.repositorioPersonagem import RepositorioPersonagem
from modelos.trabalhoEstoque import TrabalhoEstoque

class TestRepositorioEstoque:
    _repositorioPersonagem = RepositorioPersonagem()
    _personagemTeste = _repositorioPersonagem.pegaTodosPersonagens()[0]
    _repositorioEstoque = RepositorioEstoque(_personagemTeste)
    listaTrabalhosEstoque = _repositorioEstoque.pegaTodosTrabalhosEstoque()
    _trabalhoTeste = TrabalhoEstoque('', 'NomeTeste', 'ProfissaoTeste', 0, 1, 'RaridadeTeste', 'IdTeste')

    def testDeveRetornaListaComMaisDeZeroItens(self):
        self._repositorioEstoque = RepositorioEstoque(self._personagemTeste)
        self.listaTrabalhosEstoque = self._repositorioEstoque.pegaTodosTrabalhosEstoque()
        assert len(self.listaTrabalhosEstoque) != 0

    def testDeveAdicionarItemAoEstoque(self):
        tamanhoLista1 = len(self.listaTrabalhosEstoque)
        self._repositorioEstoque.adicionaTrabalhoEstoque(self._trabalhoTeste)
        self.listaTrabalhosEstoque = self._repositorioEstoque.pegaTodosTrabalhosEstoque()
        tamanhoLista2 = len(self.listaTrabalhosEstoque)
        assert tamanhoLista1 == tamanhoLista2 - 1

    def testDeveModificarQuantidadeDoPrimeiroItemDoEstoque(self):
        primeiroTrabalho = self.listaTrabalhosEstoque[0]
        quantidade1 = primeiroTrabalho.pegaQuantidade()
        primeiroTrabalho.setQuantidade(quantidade1+1)
        self._repositorioEstoque.modificaTrabalhoEstoque(primeiroTrabalho)
        self.listaTrabalhosEstoque = self._repositorioEstoque.pegaTodosTrabalhosEstoque()
        primeiroTrabalho = self.listaTrabalhosEstoque[0]
        quantidade2 = primeiroTrabalho.pegaQuantidade()
        assert quantidade1 == quantidade2 - 1