from modelos.profissao import Profissao
from modelos.personagem import Personagem
from dao.profissaoDaoSqlite import ProfissaoDaoSqlite
from dao.personagemDaoSqlite import PersonagemDaoSqlite

class TesteProfissaoDaoSqlite:
    personagemTeste = PersonagemDaoSqlite().pegaPersonagens()[0]
    profissaoDaoSqlite = ProfissaoDaoSqlite(personagemTeste)

    def testDeveRetornarListaComMaisDeZeroIntens(self):
        esperado = 0
        recebido = len(self.profissaoDaoSqlite.pegaProfissoesPorIdPersonagem())
        assert esperado != recebido