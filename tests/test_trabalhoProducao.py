from modelos.trabalhoProducao import TrabalhoProducao

class TestTrabalhoProducao:
    def testDeveRetornarTrueQuandoEstadoTrabalhoEhZero(self):
        trabalhoProducaoTeste = TrabalhoProducao('', '', '', '', 0, 0, '', '', '', False, '', 0)
        esperado = True
        recebido = trabalhoProducaoTeste.ehParaProduzir()
        assert esperado == recebido

    def testDeveRetornarTrueQuandoEstadoTrabalhoEhUm(self):
        trabalhoProducaoTeste = TrabalhoProducao('', '', '', '', 0, 0, '', '', '', False, '', 1)
        esperado = True
        recebido = trabalhoProducaoTeste.ehProduzindo()
        assert esperado == recebido

    def testDeveRetornarTrueQuandoEstadoTrabalhoEhDois(self):
        trabalhoProducaoTeste = TrabalhoProducao('', '', '', '', 0, 0, '', '', '', False, '', 2)
        esperado = True
        recebido = trabalhoProducaoTeste.ehConcluido()
        assert esperado == recebido