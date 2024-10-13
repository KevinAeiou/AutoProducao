from modelos.trabalho import Trabalho
from dao.trabalhoDaoSqlite import PersonagemDaoSqlite

class TesteTrabalhoDaoSqlite:
    trabalhoDaoSqlite = PersonagemDaoSqlite()

    def testDeveRetornarListaComMiasDeZeroItens(self):
        esperado = 0
        recebido = len(self.trabalhoDaoSqlite.pegaTrabalhos())
        assert esperado != recebido