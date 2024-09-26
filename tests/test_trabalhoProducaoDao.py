from dao.trabalhoProducaoDaoSqlite import TrabalhoProducaoDaoSqlite
from dao.personagemDaoSqlite import PersonagemDaoSqlite
from modelos.trabalhoProducao import TrabalhoProducao
import uuid

class TesteTrabalhoProducaoDao:
    personagemTeste = PersonagemDaoSqlite().pegaPersonagens()[0]
    __trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagemTeste)
    __trabalhoProducaoTeste = TrabalhoProducao(str(uuid.uuid4()), 'testTrabalhoId', 'Trabalho teste', 'Trabalho teste', 999, 0, 'Profissao teste', 'Comum', 'Trabalho necessario teste', False, 'Licença teste', 0)

    def testDeveInserirTrabalhoProducaoQuandoMetodoInsereTrabalhoProducaoEhChamado(self):
        esperadoMensagem = 'Sucesso'
        if self.__trabalhoProducaoDao.insereTrabalhoProducao(self.__trabalhoProducaoTeste):
            recebidoMensagem = 'Sucesso'
        else:
            recebidoMensagem = self.__trabalhoProducaoDao.pegaErro()
        assert esperadoMensagem == recebidoMensagem

    def testeRemoverTrabalhoProducaoQuandoMetodoRemoveTrabalhoProducaoEhChamada(self):
        esperadoMensagem = 'Sucesso'
        if self.__trabalhoProducaoDao.removeTrabalhoProducao(self.__trabalhoProducaoTeste):
            recebidoMensagem = 'Sucesso'
        else:
            recebidoMensagem = self.__trabalhoProducaoDao.pegaErro()
        assert esperadoMensagem == recebidoMensagem

    def testDeveRetornarListaComMaisDeZeroItensQuandoMetodoPegaTrabalhosProducaoParaProduzirProduzindo(self):
        esperado = 0
        recebido = len(self.__trabalhoProducaoDao.pegaTrabalhosProducaoParaProduzirProduzindo())
        assert esperado != recebido

    def testDeveRetornarListaComMaisDeZeroItensQuandoMetodoPegaTrabalhosProducaoEhChamado(self):
        esperado = 0
        recebido = len(self.__trabalhoProducaoDao.pegaTrabalhosProducao())
        assert esperado != recebido

    def testDeveModificarTrabalhoProducaoQuandoMetodoModificaTrabalhoProducaoEhChamado(self):
        trabalhoProducao = self.__trabalhoProducaoDao.pegaTrabalhosProducao()[0]
        esperadoMenssagem = 'Sucesso'
        esperadoValor = trabalhoProducao.pegaRecorrencia()
        trabalhoProducao.alternaRecorrencia()
        if self.__trabalhoProducaoDao.modificaTrabalhoProducao(trabalhoProducao):
            recebidoMenssagem = 'Sucesso'
        else:
            recebidoMenssagem = self.__trabalhoProducaoDao.pegaErro()
        assert esperadoMenssagem == recebidoMenssagem
        trabalhoProducaoModificado = self.__trabalhoProducaoDao.pegaTrabalhosProducao()[0]
        recebidoValor = trabalhoProducaoModificado.pegaRecorrencia()
        assert esperadoValor != recebidoValor
