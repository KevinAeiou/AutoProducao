from modelos.profissao import Profissao

class TesteProfissao:

    def testDeveRetornarNivelUmQuandoExperienciaEhZero(self):
        profissaoTeste = Profissao('', '', 0, False)
        esperado = 1
        recebido = profissaoTeste.pegaNivel()
        assert esperado == recebido

    def testDeveRetornarNivelUmQuandoExperienciaEhUm(self):
        profissaoTeste = Profissao('', '', 1, False)
        esperado = 1
        recebido = profissaoTeste.pegaNivel()
        assert esperado == recebido

    def testDeveRetornarNivelUmQuandoExperienciaAtualEh19(self):
        profissaoTeste = Profissao('', '', 19, False)
        esperado = 1
        recebido = profissaoTeste.pegaNivel()
        assert esperado == recebido

    def testDeveRetornarNivelDoisQuandoExperienciaAtualEhVinte(self):
        profissaoTeste = Profissao('', '', 20, False)
        esperado = 2
        recebido = profissaoTeste.pegaNivel()
        assert esperado == recebido

    def testDeveRetornarNivelTresQuandoExperienciaAtualEhDuzentos(self):
        profissaoTeste = Profissao('', '', 200, False)
        esperado = 3
        recebido = profissaoTeste.pegaNivel()
        assert esperado == recebido

    def testDeveRetornarNivelVinteECincoQuandoExperienciaEh829999(self):
        profissaoTeste = Profissao('', '', 829999, False)
        esperado = 25
        recebido = profissaoTeste.pegaNivel()
        assert esperado == recebido

    def testDeveRetornarNivelVinteESeisQuandoExperienciaAtualEh830000(self):
        profissaoTeste = Profissao('', '', 830000, False)
        esperado = 26
        recebido = profissaoTeste.pegaNivel()
        assert esperado == recebido
    
    def testDeveRetornarNivelZeroQuandoExperienciaEhInvalida(self):
        profissaoTeste = Profissao('', '', 830001, False)
        esperado = 0
        recebido = profissaoTeste.pegaNivel()
        assert esperado == recebido