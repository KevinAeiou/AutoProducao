from repositorio.repositorioTrabalhoProducao import RepositorioTrabalhoProducao
from repositorio.repositorioPersonagem import RepositorioPersonagem
from modelos.trabalhoProducao import TrabalhoProducao

class TestRepositorioTrabalhoProducao:
    _repositorioPersonagem = RepositorioPersonagem()
    _personagemTeste = _repositorioPersonagem.pegaTodosPersonagens()[0]
    _repositorioTrabalhoProducao = RepositorioTrabalhoProducao(_personagemTeste)
    _trabalhoProducaoTeste = TrabalhoProducao('', '', 'NomeTeste', 'NomeProducaoTeste', 999, 0, 'ProfissaoTeste', 'RaridadeTeste', 'TrabalhoNecessarioTeste', False, 'LicencaTeste', 0)

    def testDeveRetornarListaComMaisDeZeroItens(self):
        esperado = 0
        listaTrabalhosProducao = self._repositorioTrabalhoProducao.pegaTodosTrabalhosProducao()
        recebido = len(listaTrabalhosProducao)
        assert esperado != recebido

    def testDeveAdicionarItemNaLista(self):
        listaTrabalhosProducao = self._repositorioTrabalhoProducao.pegaTodosTrabalhosProducao()
        esperado = len(listaTrabalhosProducao) + 1
        self._repositorioTrabalhoProducao.insereTrabalhoProducao(self._trabalhoProducaoTeste)
        listaTrabalhosProducao = self._repositorioTrabalhoProducao.pegaTodosTrabalhosProducao()
        recebido = len(listaTrabalhosProducao)
        assert esperado == recebido

    def testDeveRemoverPrimeiroItemDaLista(self):
        listaTrabalhosProducao = self._repositorioTrabalhoProducao.pegaTodosTrabalhosProducao()
        esperado = len(listaTrabalhosProducao) - 1
        self._repositorioTrabalhoProducao.removeTrabalhoProducao(listaTrabalhosProducao[0])
        listaTrabalhosProducao = self._repositorioTrabalhoProducao.pegaTodosTrabalhosProducao()
        recebido = len(listaTrabalhosProducao)
        assert esperado != recebido

    def testDeveModificarPrimeiroItemDaLista(self):
        esperado = 1
        trabalhoProducaoTeste = self._repositorioTrabalhoProducao.insereTrabalhoProducao(self._trabalhoProducaoTeste)
        trabalhoProducaoTeste.setEstado(1)
        trabalhoProducaoModificadoTeste = self._repositorioTrabalhoProducao.modificaTrabalhoProducao(trabalhoProducaoTeste)
        recebido = trabalhoProducaoModificadoTeste.pegaEstado()
        assert esperado == recebido

    def testDeveRetornarZeroItensQuandoLimparListaProducao(self):
        esperado = 0
        self._repositorioTrabalhoProducao.limpaListaProducao()
        listaTrabalhosProducao = self._repositorioTrabalhoProducao.pegaTodosTrabalhosProducao()
        recebido = len(listaTrabalhosProducao)
        assert esperado == recebido

    def testDeveRetornarListaComuUmTrabalhoProducao(self):
        esperado = 1
        trabalhoProducaoTeste = self._repositorioTrabalhoProducao.insereTrabalhoProducao(self._trabalhoProducaoTeste)
        trabalhoProducaoTeste.setEstado(1)
        self._repositorioTrabalhoProducao.modificaTrabalhoProducao(trabalhoProducaoTeste)
        listaTrabalhosProducaoProduzirProduzindo = self._repositorioTrabalhoProducao.retornaListaTrabalhosProducaoParaProduzirProduzindo()
        recebido = len(listaTrabalhosProducaoProduzirProduzindo)
        assert esperado == recebido