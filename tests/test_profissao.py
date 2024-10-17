from modelos.profissao import Profissao

class TesteProfissao:

    def testDeveRetornarNivelUmQuandoExperienciaEhZero(self):
        profissaoTeste = Profissao()
        profissaoTeste.experiencia = 0
        esperado = 1
        recebido = profissaoTeste.pegaNivel()
        assert esperado == recebido

    def testDeveRetornarNivelUmQuandoExperienciaEhUm(self):
        profissaoTeste = Profissao()
        profissaoTeste.experiencia = 1
        esperado = 1
        recebido = profissaoTeste.pegaNivel()
        assert esperado == recebido

    def testDeveRetornarNivelUmQuandoExperienciaAtualEh19(self):
        profissaoTeste = Profissao()
        profissaoTeste.experiencia = 19
        esperado = 1
        recebido = profissaoTeste.pegaNivel()
        assert esperado == recebido

    def testDeveRetornarNivelDoisQuandoExperienciaAtualEhVinte(self):
        profissaoTeste = Profissao()
        profissaoTeste.experiencia = 20
        esperado = 2
        recebido = profissaoTeste.pegaNivel()
        assert esperado == recebido

    def testDeveRetornarNivelTresQuandoExperienciaAtualEhDuzentos(self):
        profissaoTeste = Profissao()
        profissaoTeste.experiencia = 200
        esperado = 3
        recebido = profissaoTeste.pegaNivel()
        assert esperado == recebido

    def testDeveRetornarNivelVinteECincoQuandoExperienciaEh829999(self):
        profissaoTeste = Profissao()
        profissaoTeste.experiencia = 829999
        esperado = 25
        recebido = profissaoTeste.pegaNivel()
        assert esperado == recebido

    def testDeveRetornarNivelVinteESeisQuandoExperienciaAtualEh830000(self):
        profissaoTeste = Profissao()
        profissaoTeste.experiencia = 830000
        esperado = 26
        recebido = profissaoTeste.pegaNivel()
        assert esperado == recebido
    
    def testDeveRetornarNivelZeroQuandoExperienciaEhInvalida(self):
        profissaoTeste = Profissao()
        profissaoTeste.experiencia = 830001
        esperado = 0
        recebido = profissaoTeste.pegaNivel()
        assert esperado == recebido