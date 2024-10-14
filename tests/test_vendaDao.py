from dao.vendaDaoSqlite import VendaDaoSqlite
from dao.personagemDaoSqlite import PersonagemDaoSqlite
from modelos.trabalhoVendido import TrabalhoVendido
import uuid

class TesteVendaDao:
    __personagemTeste = PersonagemDaoSqlite.pegaPersonagens()[0]
    __vendaDao = VendaDaoSqlite(__personagemTeste)
    __trabalhoVendido = TrabalhoVendido(str(uuid.uuid4()), 'Nome produto teste', '20/06/1995', 'Id personagem teste', 0, 'Id trabalho teste', 999)

    def testDeveInserirNovaVendaQuandoMetodoInsereVendaEhChamado(self):
        esperado = 'Sucesso'
        if self.__vendaDao.insereTrabalhoVendido(self.__trabalhoVendido):
            recebido = 'Sucesso'
        else:
            recebido = self.__vendaDao.pegaErro()
        assert esperado == recebido