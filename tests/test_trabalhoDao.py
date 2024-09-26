from modelos.trabalho import Trabalho
from dao.trabalhoDaoSqlite import TrabalhoDaoSqlite

class TesteTrabalhoDaoSqlite:
    trabalhoDaoSqlite = TrabalhoDaoSqlite()

    def testDeveRetornarListaComMiasDeZeroItens(self):
        esperado = 0
        recebido = len(self.trabalhoDaoSqlite.pegaTrabalhos())
        assert esperado != recebido