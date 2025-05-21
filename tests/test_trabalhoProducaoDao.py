from dao.trabalhoProducaoDaoSqlite import TrabalhoProducaoDaoSqlite
from dao.personagemDaoSqlite import PersonagemDaoSqlite
from modelos.trabalhoProducao import TrabalhoProducao
import uuid

class TesteTrabalhoProducaoDao:
    __personagemTeste = PersonagemDaoSqlite().pegaPersonagens()[0]

    def testDeveInserirTrabalhoProducaoQuandoMetodoInsereTrabalhoProducaoEhChamado(self):
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemTeste)
        esperadoMensagem = 'Sucesso'
        trabalhoProducaoTeste = TrabalhoProducao()
        trabalhoProducaoTeste.idTrabalho = 'IdTrabalhoTeste'
        trabalhoProducaoTeste.estado = 0
        trabalhoProducaoTeste.tipoLicenca = 'LicencaTeste'
        if trabalhoProducaoDao.insere_trabalho_producao(trabalhoProducaoTeste):
            recebidoMensagem = 'Sucesso'
        else:
            recebidoMensagem = trabalhoProducaoDao.pegaErro
        assert esperadoMensagem == recebidoMensagem

    def testeRemoverTrabalhoProducaoQuandoMetodoRemoveTrabalhoProducaoEhChamada(self):
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemTeste)
        mensagemInsereEsperado = 'Sucesso'
        trabalhoProducaoTeste = TrabalhoProducao()
        trabalhoProducaoTeste.idTrabalho = 'IdTrabalhoTeste'
        trabalhoProducaoTeste.estado = 0
        trabalhoProducaoTeste.tipoLicenca = 'LicencaTeste'
        if trabalhoProducaoDao.insere_trabalho_producao(trabalhoProducaoTeste):
            mensagemInsereRecebido = 'Sucesso'
        else:
            mensagemInsereRecebido = trabalhoProducaoDao.pegaErro
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemTeste)
        mensagemRemoveEsperado = 'Sucesso'
        if trabalhoProducaoDao.removeTrabalhoProducao(trabalhoProducaoTeste):
            mensagemRemoveRecebido = 'Sucesso'
        else:
            mensagemRemoveRecebido = trabalhoProducaoDao.pegaErro
        assert mensagemInsereEsperado == mensagemInsereRecebido
        assert mensagemRemoveEsperado == mensagemRemoveRecebido

    def testDeveModificarTrabalhoProducaoQuandoMetodoModificaTrabalhoProducaoEhChamado(self):
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemTeste)
        trabalhoProducaoTeste = TrabalhoProducao()
        trabalhoProducaoTeste.idTrabalho = 'IdTrabalhoTeste'
        trabalhoProducaoTeste.estado = 0
        trabalhoProducaoTeste.tipoLicenca = 'LicencaTeste'
        mensagemInsereEsperado = 'Sucesso'
        if trabalhoProducaoDao.insere_trabalho_producao(trabalhoProducaoTeste):
            mensagemInsereRecebido = 'Sucesso'
        else:
            mensagemInsereRecebido = trabalhoProducaoDao.pegaErro
        mensagemModificaEsperado = 'Sucesso'
        trabalhoProducaoTeste.estado = 1
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemTeste)
        if trabalhoProducaoDao.modifica_trabalho_producao(trabalhoProducaoTeste):
            mensagemModificaRecebido = 'Sucesso'
        else:
            mensagemModificaRecebido = trabalhoProducaoDao.pegaErro
        assert mensagemInsereEsperado == mensagemInsereRecebido
        assert mensagemModificaEsperado == mensagemModificaRecebido
