from repositorio.repositorioEstoque import RepositorioEstoque
from repositorio.repositorioPersonagem import RepositorioPersonagem
from modelos.trabalhoEstoque import TrabalhoEstoque

class TestRepositorioEstoque:
    _repositorioEstoque = None
    listaTrabalhosEstoque = []

    def __init__(self) -> None:
        self._repositorioPersonagem = RepositorioPersonagem()
        self._trabalhoTeste = TrabalhoEstoque('', 'NomeTeste', 'ProfissaoTeste', 0, 1, 'RaridadeTeste', 'IdTeste')
        self._personagemTeste = self._repositorioPersonagem.pegaTodosPersonagens()[0]
        self._repositorioEstoque = RepositorioEstoque(self._personagemTeste)
        self.listaTrabalhosEstoque = self._repositorioEstoque.pegaTodosTrabalhosEstoque()

    def testDeveRetornaListaComMaisDeZeroItens(self):
        self.listaTrabalhosEstoque = self._repositorioEstoque.pegaTodosTrabalhosEstoque()
        condicao = len(self.listaTrabalhosEstoque) != 0
        resultado = 'Sucesso' if condicao else 'Falha'
        print(resultado)

    def testDeveAdicionarItemAoEstoque(self):
        tamanhoLista1 = len(self.listaTrabalhosEstoque)
        self._repositorioEstoque.adicionaTrabalhoEstoque(self._trabalhoTeste)
        self.listaTrabalhosEstoque = self._repositorioEstoque.pegaTodosTrabalhosEstoque()
        tamanhoLista2 = len(self.listaTrabalhosEstoque)
        condicao = tamanhoLista1 == tamanhoLista2 - 1
        resultado = 'Sucesso' if condicao else 'Falha'
        print(resultado)

    def testDeveModificarQuantidadeDoPrimeiroItemDoEstoque(self):
        primeiroTrabalho = self.listaTrabalhosEstoque[0]
        quantidade1 = primeiroTrabalho.pegaQuantidade()
        primeiroTrabalho.setQuantidade(quantidade1+1)
        self._repositorioEstoque.modificaTrabalhoEstoque(primeiroTrabalho)
        self.listaTrabalhosEstoque = self._repositorioEstoque.pegaTodosTrabalhosEstoque()
        primeiroTrabalho = self.listaTrabalhosEstoque[0]
        quantidade2 = primeiroTrabalho.pegaQuantidade()
        condicao = quantidade1 == quantidade2 - 1
        resultado = 'Sucesso' if condicao else 'Falha'
        print(resultado)