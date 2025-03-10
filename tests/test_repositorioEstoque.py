from repositorio.repositorioEstoque import RepositorioEstoque
from repositorio.repositorioPersonagem import RepositorioPersonagem
from modelos.trabalhoEstoque import TrabalhoEstoque

class TestRepositorioEstoque:
    _listaTrabalhosEstoque = []
    _repositorioPersonagem = RepositorioPersonagem()
    _personagemTeste = _repositorioPersonagem.pegaTodosPersonagens()[0]
    _repositorioEstoque = RepositorioEstoque(_personagemTeste)
    _trabalhoTeste = TrabalhoEstoque()
    _trabalhoTeste.idTrabalho = 'IdTrabalhoTeste'
    _trabalhoTeste.quantidade = 1

    def testDeveInserirTrabalhoAoEstoque(self):
        esperado = 'Sucesso'
        if self._repositorioEstoque.insereTrabalhoEstoque(self._trabalhoTeste):
            recebido = 'Sucesso'
        else:
            recebido = self._repositorioEstoque.pegaErro()
        assert esperado == recebido

    def testDeveModificarQuantidadeDoPrimeiroItemDoEstoque(self):
        self._repositorioEstoque.insereTrabalhoEstoque(self._trabalhoTeste)
        esperado = 'Sucesso'
        self._trabalhoTeste.setQuantidade(20)
        if self._repositorioEstoque.modificaTrabalhoEstoque(self._trabalhoTeste):
            recebido = 'Sucesso'
        else:
            recebido = self._repositorioEstoque.pegaErro()
        assert esperado == recebido