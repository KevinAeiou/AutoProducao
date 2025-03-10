from repositorio.repositorioTrabalhoProducao import RepositorioTrabalhoProducao
from repositorio.repositorioPersonagem import RepositorioPersonagem
from modelos.trabalhoProducao import TrabalhoProducao

class TestRepositorioTrabalhoProducao:
    _repositorioPersonagem = RepositorioPersonagem()
    _personagemTeste = _repositorioPersonagem.pegaTodosPersonagens()[0]
    _repositorioTrabalhoProducao = RepositorioTrabalhoProducao(_personagemTeste)
    _trabalhoProducaoTeste = TrabalhoProducao()
    _trabalhoProducaoTeste.idTrabalho = 'IdTrabalhoTeste'
    _trabalhoProducaoTeste.recorrencia = True
    _trabalhoProducaoTeste.tipoLicenca = 'LicencaTeste'
    _trabalhoProducaoTeste.estado = 0

    def testDeveRetornarListaComMaisDeZeroItens(self):
        esperado = 0
        listaTrabalhosProducao = self._repositorioTrabalhoProducao.pegaTodosTrabalhosProducao()
        recebido = len(listaTrabalhosProducao)
        assert esperado < recebido

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
        assert esperado == recebido