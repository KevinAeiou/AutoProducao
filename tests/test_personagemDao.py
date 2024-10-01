from dao.personagemDaoSqlite import PersonagemDaoSqlite

class TestePersonagemDaoSqlite:
    personagemDaoSqlite = PersonagemDaoSqlite()

    def testDeveRetornarListaComNoveItens(self):
        esperado = 8
        recebido = len(self.personagemDaoSqlite.pegaPersonagens())
        assert esperado == recebido

    def testDeveModificarPersonagem(self):
        personagens = self.personagemDaoSqlite.pegaPersonagens()
        personagemTeste = personagens[0]
        personagemTeste.alternaEstado()
        self.personagemDaoSqlite.modificaPersonagem(personagemTeste)
        personagemTesteModificado = self.personagemDaoSqlite.pegaPersonagens()[0]
        esperado = personagemTeste.pegaEstado()
        recebido = personagemTesteModificado.pegaEstado()
        assert esperado != recebido