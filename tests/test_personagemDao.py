from dao.personagemDaoSqlite import PersonagemDaoSqlite

class TestePersonagemDaoSqlite:
    personagemDaoSqlite = PersonagemDaoSqlite()

    def testDeveRetornarListaComNoveItens(self):
        esperado = 8
        recebido = len(self.personagemDaoSqlite.pegaPersonagens())
        assert esperado == recebido