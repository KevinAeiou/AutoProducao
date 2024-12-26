from dao.vendaDaoSqlite import VendaDaoSqlite
from dao.personagemDaoSqlite import PersonagemDaoSqlite
from modelos.trabalhoVendido import TrabalhoVendido

class TesteVendaDao:
    __personagemTeste = PersonagemDaoSqlite().pegaPersonagens()[0]
    __vendaDao = VendaDaoSqlite(__personagemTeste)
    __trabalhoVendido = TrabalhoVendido()
    __trabalhoVendido.trabalhoId = 'IdTrabalhoTeste'
    __trabalhoVendido.nomeProduto = 'Descrição teste'
    __trabalhoVendido.dataVenda = '01/01/2000'
    __trabalhoVendido.quantidadeProduto = 1
    __trabalhoVendido.valorProduto = 200
    __trabalhoVendido.nomePersonagem = 'IdPersonagemTeste'

    def testDeveInserirNovaVendaQuandoMetodoInsereVendaEhChamado(self):
        esperado = 'Sucesso'
        if self.__vendaDao.insereTrabalhoVendido(self.__trabalhoVendido):
            recebido = 'Sucesso'
        else:
            recebido = self.__vendaDao.pegaErro()
        assert esperado == recebido