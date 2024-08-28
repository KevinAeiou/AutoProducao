from repositorio.repositorioVendas import RepositorioVendas
from repositorio.repositorioPersonagem import RepositorioPersonagem
from modelos.trabalhoVendido import TrabalhoVendido

class TestRespositorioVendas:
    _repositorioVendas = None
    _listaVendas = []
    def __init__(self) -> None:
        self._repositorioPersonagem = RepositorioPersonagem()
        self._vendaTeste = TrabalhoVendido('-O4xG-Ucqy-0BWoqvmwL', 'Nome teste', '01/01/2000', 'idTeste', 1, 'idTeste', 999)
        self._personagemTeste = self._repositorioPersonagem.pegaTodosPersonagens()[0]
        self._repositorioVendas = RepositorioVendas(self._personagemTeste)
        self._listaVendas = self._repositorioVendas.pegaTodosTrabalhoVendidos()

    def testDeveRetornarListaComMaisDeZeroItens(self):
        self._listaVendas = self._repositorioVendas.pegaTodosTrabalhoVendidos()
        condicao = len(self._listaVendas) != 0
        resultado = 'Sucesso' if condicao else 'Falha'
        print(resultado)

    def testDeveAdicionarNovaVendaALista(self):
        tamanhoLista = len(self._listaVendas)
        self._repositorioVendas.adicionaNovaVenda(self._vendaTeste)
        self._listaVendas = self._repositorioVendas.pegaTodosTrabalhoVendidos()
        novoTamanhoLista = len(self._listaVendas)
        condicao = tamanhoLista == novoTamanhoLista - 1
        resultado = 'Sucesso' if condicao else 'Falha'
        print(resultado)

    def testDeveRemoverPrimeiraVendaDaLista(self):
        tamanhoLista = len(self._listaVendas)
        self._repositorioVendas.removeVenda(self._listaVendas[0])
        self._listaVendas = self._repositorioVendas.pegaTodosTrabalhoVendidos()
        novoTamanhoLista = len(self._listaVendas)
        condicao = tamanhoLista - 1 == novoTamanhoLista
        resultado = 'Sucesso' if condicao else 'Falha'
        print(resultado)

    def testDeveLimparListaVenda(self):
        self._repositorioVendas.limpaListaVenda()
        novoTamanhoLista = len(self._repositorioVendas.pegaTodosTrabalhoVendidos())
        condicao = novoTamanhoLista == 0
        resultado = 'Sucesso' if condicao else 'Falha'
        print(resultado)