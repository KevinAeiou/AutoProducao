from repositorio.repositorioTrabalhoProducao import RepositorioTrabalhoProducao
from repositorio.repositorioPersonagem import RepositorioPersonagem
from modelos.trabalhoProducao import TrabalhoProducao

class TestRepositorioTrabalhoProducao:
    _repositorioTrabalhoProducao = None
    listaTrabalhosProducao = []

    # def __init__(self) -> None:
    #     self._repositorioPersonagem = RepositorioPersonagem()
    #     self._trabalhoProducaoTeste = TrabalhoProducao('', 'NomeTeste', 'NomeProducaoTeste', 0, 999, 0, 'ProfissaoTeste', 'RaridadeTeste', False, 'LicencaTeste', 'TrabalhoIdTeste')
    #     self._personagemTeste = self._repositorioPersonagem.pegaTodosPersonagens()[0]
    #     self._repositorioTrabalhoProducao = RepositorioTrabalhoProducao(self._personagemTeste)
    #     self.listaTrabalhosProducao = self._repositorioTrabalhoProducao.pegaTodosTrabalhosProducao()

    def testDeveRetornarListaComMaisDeZeroItens(self):
        self.listaTrabalhosProducao = self._repositorioTrabalhoProducao.pegaTodosTrabalhosProducao()
        condicao = len(self.listaTrabalhosProducao) != 0
        resultado = 'Sucesso' if condicao else 'Falha'
        print(resultado)

    def testDeveRemoverPrimeiroItemDaLista(self):
        tamanho1 = len(self.listaTrabalhosProducao)
        self._repositorioTrabalhoProducao.removeTrabalhoProducao(self.listaTrabalhosProducao[0])
        self.listaTrabalhosProducao = self._repositorioTrabalhoProducao.pegaTodosTrabalhosProducao()
        tamanho2 = len(self.listaTrabalhosProducao)
        condicao = tamanho1 == tamanho2 + 1
        resultado = 'Sucesso' if condicao else 'Falha'
        print(resultado)

    def testDeveAdicionarItemNaLista(self):
        tamanho1 = len(self.listaTrabalhosProducao)
        trabalhoProducaoComId = self._repositorioTrabalhoProducao.adicionaTrabalhoProducao(self._trabalhoProducaoTeste)
        print(trabalhoProducaoComId)
        self.listaTrabalhosProducao = self._repositorioTrabalhoProducao.pegaTodosTrabalhosProducao()
        tamanho2 = len(self.listaTrabalhosProducao)
        condicao = tamanho1 == tamanho2 - 1
        resultado = 'Sucesso' if condicao else 'Falha'
        print(resultado)

    def testDeveRetornarZeroItensQuandoLimparListaProducao(self):
        self._repositorioTrabalhoProducao.limpaListaProducao()
        self.listaTrabalhosProducao = self._repositorioTrabalhoProducao.pegaTodosTrabalhosProducao()
        tamanho = len(self.listaTrabalhosProducao)
        condicao = tamanho == 0
        resultado = 'Sucesso' if condicao else 'Falha'
        print(resultado)

    def testDeveModificarPrimeiroItemDaLista(self):
        self.primeiroTrabalhoProducao = self.listaTrabalhosProducao[0]
        self.primeiroTrabalhoProducao.setEstado(1)
        self._repositorioTrabalhoProducao.modificaTrabalhoProducao(self.primeiroTrabalhoProducao)
        self.listaTrabalhosProducao = self._repositorioTrabalhoProducao.pegaTodosTrabalhosProducao()
        condicao = 1 == self.listaTrabalhosProducao[0].pegaEstado()
        resultado = 'Sucesso' if condicao else 'Falha'
        print(resultado)