from repositorio.repositorioVendas import RepositorioVendas
from repositorio.repositorioPersonagem import RepositorioPersonagem
from modelos.trabalhoVendido import TrabalhoVendido

class TestRespositorioVendas:
    _listaVendas = []
    _repositorioPersonagem = RepositorioPersonagem()
    _vendaTeste = TrabalhoVendido()
    _vendaTeste.descricao = 'DescriçãoTeste'
    _vendaTeste.dataVenda = '01/01/2000'
    _vendaTeste.idTrabalho = 'IdTrabalhoTeste'
    _vendaTeste.quantidade = 1
    _vendaTeste.valor = 200
    _personagemTeste = _repositorioPersonagem.pegaTodosPersonagens()[0]
    _repositorioVendas = RepositorioVendas(_personagemTeste)

    def testDeveAdicionarNovaVendaALista(self):
        self._listaVendas = self._repositorioVendas.pegaTrabalhosVendidos()
        esperado = len(self._listaVendas) + 1
        self._repositorioVendas.insereTrabalhoVendido(self._vendaTeste)
        self._listaVendas = self._repositorioVendas.pegaTrabalhosVendidos()
        recebido = len(self._listaVendas)
        assert esperado == recebido

    def testDeveRetornarListaComMaisDeZeroItens(self):
        esperado = 0
        self._listaVendas = self._repositorioVendas.pegaTrabalhosVendidos()
        recebido = len(self._listaVendas)
        assert esperado != recebido

    def testDeveRemoverPrimeiraVendaDaLista(self):
        self._repositorioVendas.insereTrabalhoVendido(self._vendaTeste)
        self._repositorioVendas.insereTrabalhoVendido(self._vendaTeste)
        self._listaVendas = self._repositorioVendas.pegaTrabalhosVendidos()
        esperado = len(self._listaVendas) - 1
        self._repositorioVendas.removeTrabalhoVendido(self._listaVendas[0])
        self._listaVendas = self._repositorioVendas.pegaTrabalhosVendidos()
        recebido = len(self._listaVendas)
        assert esperado == recebido