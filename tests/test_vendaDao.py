from dao.vendaDaoSqlite import VendaDaoSqlite
from dao.personagemDaoSqlite import PersonagemDaoSqlite
from modelos.trabalhoVendido import TrabalhoVendido

class TesteVendaDao:
    __personagemTeste = PersonagemDaoSqlite().pegaPersonagens()[0]
    __vendaDao = VendaDaoSqlite(__personagemTeste)
    __trabalhoVendido = TrabalhoVendido()
    __trabalhoVendido.idTrabalho = 'IdTrabalhoTeste'
    __trabalhoVendido.descricao = 'Descrição teste'
    __trabalhoVendido.dataVenda = '01/01/2000'
    __trabalhoVendido.quantidade = 1
    __trabalhoVendido.valor = 200

    def testDeveInserirNovaVendaQuandoMetodoInsereVendaEhChamado(self):
        esperado = 'Sucesso'
        if self.__vendaDao.insereTrabalhoVendido(self.__trabalhoVendido):
            recebido = 'Sucesso'
        else:
            recebido = self.__vendaDao.pegaErro
        assert esperado == recebido