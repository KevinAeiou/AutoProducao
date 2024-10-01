from dao.estoqueDaoSqlite import EstoqueDaoSqlite
from dao.personagemDaoSqlite import PersonagemDaoSqlite

class TesteEstoqueDaoSqlite:
    __personagemTeste = PersonagemDaoSqlite().pegaPersonagens()[8]
    estoqueDaoSqlite = EstoqueDaoSqlite(__personagemTeste)

    def testDeveRetornarListaQuandoMetodoPegaEstoque(self):
        esperado = 0
        recebido = len(self.estoqueDaoSqlite.pegaEstoque())
        assert esperado == recebido