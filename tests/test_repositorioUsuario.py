from repositorio.repositorioUsuario import RepositorioUsuario

class TestRepositorioUsuario:

    def testDeveRetornarVerdadeiroQuandoIdPersonagemEhEncontradoNaLista(self):
        esperado: bool= True
        repositorioUsuario: RepositorioUsuario= RepositorioUsuario()
        idTeste: str= '64103364-22d9-463b-89f0-e2630f05c13c'
        recebido: bool= repositorioUsuario.verificaIdPersonagem(id= idTeste)
        assert esperado == recebido

    def testDeveRetornarFalsoQuandoIdPersonagemNaoEhEncontradoNaLista(self):
        esperado: bool= False
        repositorioUsuario: RepositorioUsuario= RepositorioUsuario()
        idTeste: str= 'qualquerIdErrado'
        recebido: bool= repositorioUsuario.verificaIdPersonagem(id= idTeste)
        assert esperado == recebido