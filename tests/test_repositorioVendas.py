from repositorio.repositorioVendas import RepositorioVendas
from repositorio.repositorioPersonagem import RepositorioPersonagem
from modelos.trabalhoVendido import TrabalhoVendido

class TestRespositorioVendas:
    _listaVendas = []
    _repositorioPersonagem = RepositorioPersonagem()
    _vendaTeste = TrabalhoVendido('-O4xG-Ucqy-0BWoqvmwL', 'Nome teste', '01/01/2000', 'idTeste', 1, 'idTeste', 999)
    _personagemTeste = _repositorioPersonagem.pegaTodosPersonagens()[0]
    _repositorioVendas = RepositorioVendas(_personagemTeste)

    def testDeveAdicionarNovaVendaALista(self):
        self._listaVendas = self._repositorioVendas.pegaTodasVendas()
        esperado = len(self._listaVendas) + 1
        self._repositorioVendas.insereTrabalhoVendido(self._vendaTeste)
        self._listaVendas = self._repositorioVendas.pegaTodasVendas()
        recebido = len(self._listaVendas)
        assert esperado == recebido

    def testDeveRetornarListaComMaisDeZeroItens(self):
        esperado = 0
        self._listaVendas = self._repositorioVendas.pegaTodasVendas()
        recebido = len(self._listaVendas)
        assert esperado != recebido

    def testDeveRemoverPrimeiraVendaDaLista(self):
        self._repositorioVendas.insereTrabalhoVendido(self._vendaTeste)
        self._repositorioVendas.insereTrabalhoVendido(self._vendaTeste)
        self._listaVendas = self._repositorioVendas.pegaTodasVendas()
        esperado = len(self._listaVendas) - 1
        self._repositorioVendas.removeVenda(self._listaVendas[0])
        self._listaVendas = self._repositorioVendas.pegaTodasVendas()
        recebido = len(self._listaVendas)
        assert esperado == recebido

    def testDeveLimparListaVenda(self):
        esperado = 0
        self._repositorioVendas.limpaListaVenda()
        recebido = len(self._repositorioVendas.pegaTodasVendas())
        assert recebido == esperado

    def testDeveRetornarStringTrabalhoVendido(self):
        imagemTeste = self.imagem
        esperado = ''
