__author__ = 'Kevin Amazonas'

from modelos.trabalhoProducao import TrabalhoProducao
from modelos.personagem import Personagem
from db.db import MeuBanco
from modelos.logger import MeuLogger
from repositorio.repositorioTrabalhoProducao import RepositorioTrabalhoProducao
from constantes import *

class TrabalhoProducaoDaoSqlite:
    def __init__(self, banco: MeuBanco):
        self.__meuBanco: MeuBanco= banco
        self.__logger: MeuLogger= MeuLogger(nome= 'trabalhoProducaoDao')
        self.__erro = None
    
    def pegaTodosTrabalhosProducao(self):
        try:
            trabalhosProducao: list[TrabalhoProducao]= []
            sql = """SELECT Lista_desejo.id, trabalhos.id, trabalhos.nome, trabalhos.nomeProducao, trabalhos.experiencia, trabalhos.nivel, trabalhos.profissao, trabalhos.raridade, trabalhos.trabalhoNecessario, Lista_desejo.recorrencia, Lista_desejo.tipoLicenca, Lista_desejo.estado FROM Lista_desejo INNER JOIN trabalhos ON Lista_desejo.idTrabalho == trabalhos.id;"""
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute(sql)
            for linha in cursor.fetchall():
                recorrencia = True if linha[9] == 1 else False
                trabalhoProducao = TrabalhoProducao()
                trabalhoProducao.id = linha[0]
                trabalhoProducao.idTrabalho = linha[1]
                trabalhoProducao.nome = linha[2]
                trabalhoProducao.nomeProducao = linha[3]
                trabalhoProducao.experiencia = linha[4]
                trabalhoProducao.nivel = linha[5]
                trabalhoProducao.profissao = linha[6]
                trabalhoProducao.raridade = linha[7]
                trabalhoProducao.trabalhoNecessario = linha[8]
                trabalhoProducao.recorrencia = recorrencia
                trabalhoProducao.tipoLicenca = linha[10]
                trabalhoProducao.estado = linha[11]
                trabalhosProducao.append(trabalhoProducao)
            return trabalhosProducao
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhosProducao(self, personagem: Personagem):
        try:
            trabalhosProducao: list[TrabalhoProducao]= []
            sql = """SELECT Lista_desejo.id, trabalhos.id, trabalhos.nome, trabalhos.nomeProducao, trabalhos.experiencia, trabalhos.nivel, trabalhos.profissao, trabalhos.raridade, trabalhos.trabalhoNecessario, Lista_desejo.recorrencia, Lista_desejo.tipoLicenca, Lista_desejo.estado FROM Lista_desejo INNER JOIN trabalhos ON Lista_desejo.idTrabalho == trabalhos.id WHERE idPersonagem == ?;"""
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute(sql, [personagem.id])
            for linha in cursor.fetchall():
                recorrencia = True if linha[9] == 1 else False
                trabalhoProducao = TrabalhoProducao()
                trabalhoProducao.id = linha[0]
                trabalhoProducao.idTrabalho = linha[1]
                trabalhoProducao.nome = linha[2]
                trabalhoProducao.nomeProducao = linha[3]
                trabalhoProducao.experiencia = linha[4]
                trabalhoProducao.nivel = linha[5]
                trabalhoProducao.profissao = linha[6]
                trabalhoProducao.raridade = linha[7]
                trabalhoProducao.trabalhoNecessario = linha[8]
                trabalhoProducao.recorrencia = recorrencia
                trabalhoProducao.tipoLicenca = linha[10]
                trabalhoProducao.estado = linha[11]
                trabalhosProducao.append(trabalhoProducao)
            trabalhosProducao = sorted(trabalhosProducao, key = lambda trabalhoProducao: (trabalhoProducao.estado, trabalhoProducao.profissao, trabalhoProducao.nivel, trabalhoProducao.nome))
            return trabalhosProducao
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhosProducaoParaProduzirProduzindo(self, personagem: Personagem):
        try:
            trabalhosProducao: list[TrabalhoProducao]= []
            sql = """SELECT Lista_desejo.id, trabalhos.id, trabalhos.nome, trabalhos.nomeProducao, trabalhos.experiencia, trabalhos.nivel, trabalhos.profissao, trabalhos.raridade, trabalhos.trabalhoNecessario, Lista_desejo.recorrencia, Lista_desejo.tipoLicenca, Lista_desejo.estado FROM Lista_desejo INNER JOIN trabalhos ON Lista_desejo.idTrabalho == trabalhos.id WHERE idPersonagem == ? AND (estado == 0 OR estado == 1);"""
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute(sql, [personagem.id])
            for linha in cursor.fetchall():
                recorrencia = True if linha[9] == 1 else False
                trabalhoProducao: TrabalhoProducao= TrabalhoProducao()
                trabalhoProducao.id = linha[0]
                trabalhoProducao.idTrabalho = linha[1]
                trabalhoProducao.nome = linha[2]
                trabalhoProducao.nomeProducao = linha[3]
                trabalhoProducao.experiencia = linha[4]
                trabalhoProducao.nivel = linha[5]
                trabalhoProducao.profissao = linha[6]
                trabalhoProducao.raridade = linha[7]
                trabalhoProducao.trabalhoNecessario = linha[8]
                trabalhoProducao.recorrencia = recorrencia
                trabalhoProducao.tipoLicenca = linha[10]
                trabalhoProducao.estado = linha[11]
                trabalhosProducao.append(trabalhoProducao)
            return trabalhosProducao
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhosParaProduzirPorProfissaoRaridade(self, personagem: Personagem, trabalho: TrabalhoProducao) -> list[TrabalhoProducao]:
        try:
            trabalhosProducao: list[TrabalhoProducao]= []
            sql= f"""SELECT {CHAVE_LISTA_TRABALHOS_PRODUCAO}.{CHAVE_ID}, {CHAVE_TRABALHOS}.{CHAVE_ID}, {CHAVE_TRABALHOS}.{CHAVE_NIVEL}, {CHAVE_TRABALHOS}.{CHAVE_PROFISSAO} FROM {CHAVE_LISTA_TRABALHOS_PRODUCAO} INNER JOIN {CHAVE_TRABALHOS} ON {CHAVE_LISTA_TRABALHOS_PRODUCAO}.{CHAVE_ID_TRABALHO} == {CHAVE_TRABALHOS}.{CHAVE_ID} WHERE {CHAVE_ID_PERSONAGEM} == ? AND {CHAVE_ESTADO} == {CODIGO_PARA_PRODUZIR} AND {CHAVE_TRABALHOS}.{CHAVE_RARIDADE} == ? AND {CHAVE_TRABALHOS}.{CHAVE_PROFISSAO} == ?;"""
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute(sql, (personagem.id, trabalho.raridade, trabalho.profissao))
            for linha in cursor.fetchall():
                trabalhoProducao = TrabalhoProducao()
                trabalhoProducao.id = linha[0]
                trabalhoProducao.idTrabalho = linha[1]
                trabalhoProducao.nivel = linha[2]
                trabalhoProducao.profissao = linha[3]
                trabalhosProducao.append(trabalhoProducao)
            return trabalhosProducao
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def pegaQuantidadeTrabalhoProducaoProduzindo(self, personagem: Personagem, trabalhoId: str):
        try:
            sql = """SELECT COUNT(*) AS quantidade FROM Lista_desejo WHERE idPersonagem == ? AND idTrabalho == ? AND estado == 1;"""
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute(sql, (personagem.id, trabalhoId))
            linha = cursor.fetchone()
            quantidade = 0 if linha is None else linha[0]
            return quantidade
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def pegaQuantidadeTrabalhoProducaoProduzirProduzindo(self, personagem: Personagem, idTrabalho: str):
        try:
            sql = """SELECT COUNT(*) AS quantidade FROM Lista_desejo WHERE idPersonagem == ? AND idTrabalho == ? AND (estado == 0 OR estado == 1);"""
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute(sql, (personagem.id, idTrabalho))
            linha = cursor.fetchone()
            quantidade = 0 if linha is None else linha[0]
            return quantidade
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhoProducaoPorId(self, id: str):
        try:
            trabalhoProducao: TrabalhoProducao= TrabalhoProducao()
            sql = """SELECT id, idTrabalho, recorrencia, tipoLicenca, estado FROM Lista_desejo WHERE id == ?;"""
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute(sql, [id])
            for linha in cursor.fetchall():
                recorrencia = True if linha[2] == 1 else False
                trabalhoProducao.id = linha[0]
                trabalhoProducao.idTrabalho = linha[1]
                trabalhoProducao.recorrencia = recorrencia
                trabalhoProducao.tipoLicenca = linha[3]
                trabalhoProducao.estado = linha[4]
            return trabalhoProducao
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhosProducaoPorIdTrabalho(self, personagem: Personagem, id: str) -> list[TrabalhoProducao] | None:
        try:
            trabalhosProducaoEncontrados: list[TrabalhoProducao]= []
            sql = f"""SELECT {CHAVE_ID}, {CHAVE_ID_TRABALHO}, {CHAVE_RECORRENCIA}, {CHAVE_TIPO_LICENCA}, {CHAVE_ESTADO} FROM {CHAVE_LISTA_TRABALHOS_PRODUCAO} WHERE {CHAVE_ID_TRABALHO} == ? AND {CHAVE_ID_PERSONAGEM} == ?;"""
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute(sql, (id, personagem.id))
            for linha in cursor.fetchall():
                trabalhoProducao = TrabalhoProducao()
                recorrencia = True if linha[2] == 1 else False
                trabalhoProducao.id = linha[0]
                trabalhoProducao.idTrabalho = linha[1]
                trabalhoProducao.recorrencia = recorrencia
                trabalhoProducao.tipoLicenca = linha[3]
                trabalhoProducao.estado = linha[4]
                trabalhosProducaoEncontrados.append(trabalhoProducao)
            return trabalhosProducaoEncontrados
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def insereTrabalhoProducao(self, personagem: Personagem, trabalhoProducao: TrabalhoProducao, modificaServidor: bool= True) -> bool:
        try:
            trabalhoProducaoLimpo:TrabalhoProducao = TrabalhoProducao()
            trabalhoProducaoLimpo.id = trabalhoProducao.id
            trabalhoProducaoLimpo.idTrabalho = trabalhoProducao.idTrabalho
            trabalhoProducaoLimpo.recorrencia = trabalhoProducao.recorrencia
            trabalhoProducaoLimpo.tipoLicenca = trabalhoProducao.tipoLicenca
            trabalhoProducaoLimpo.estado = trabalhoProducao.estado
            recorrencia = 1 if trabalhoProducaoLimpo.recorrencia else 0
            sql = f"""INSERT INTO {CHAVE_LISTA_TRABALHOS_PRODUCAO} ({CHAVE_ID}, {CHAVE_ID_TRABALHO}, {CHAVE_ID_PERSONAGEM}, {CHAVE_RECORRENCIA}, {CHAVE_TIPO_LICENCA}, {CHAVE_ESTADO}) VALUES (?, ?, ?, ?, ?, ?);"""
            repositorioTrabalhoProducao: RepositorioTrabalhoProducao= RepositorioTrabalhoProducao(personagem= personagem)
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, (trabalhoProducaoLimpo.id, trabalhoProducaoLimpo.idTrabalho, personagem.id, recorrencia, trabalhoProducaoLimpo.tipoLicenca, trabalhoProducaoLimpo.estado))
            if modificaServidor:
                if repositorioTrabalhoProducao.insereTrabalhoProducao(trabalhoProducao= trabalhoProducaoLimpo):
                    self.__logger.info(f'({trabalhoProducaoLimpo}) inserido no servidor com sucesso!')
                    conexao.commit()
                    return True
                self.__logger.error(f'Erro ao inserir ({trabalhoProducaoLimpo}) no servidor: {repositorioTrabalhoProducao.pegaErro()}')
                conexao.rollback()
                self.__erro= repositorioTrabalhoProducao.pegaErro()
                return False
            conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            conexao.rollback()
        finally:
            self.__meuBanco.desconecta()
        return False
    
    def removeTrabalhoProducao(self, personagem: Personagem, trabalhoProducao: TrabalhoProducao, modificaServidor: bool= True) -> bool:
        try:
            sql = f"""DELETE FROM {CHAVE_LISTA_TRABALHOS_PRODUCAO} WHERE {CHAVE_ID} == ?;"""
            repositorioTrabalhoProducao: RepositorioTrabalhoProducao= RepositorioTrabalhoProducao(personagem= personagem)
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, [trabalhoProducao.id])
            if modificaServidor:
                if repositorioTrabalhoProducao.removeTrabalhoProducao(trabalhoProducao= trabalhoProducao):
                    self.__logger.info(f'({trabalhoProducao}) removido do servidor com sucesso!')
                    conexao.commit()
                    return True
                self.__logger.error(f'Erro ao remover ({trabalhoProducao}) do servidor: {repositorioTrabalhoProducao.pegaErro()}')
                self.__erro= repositorioTrabalhoProducao.pegaErro()
                conexao.rollback()
                return False
            conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            conexao.rollback()
        finally:
            self.__meuBanco.desconecta()
        return False
        
    def modificaTrabalhoProducao(self, personagem: Personagem, trabalhoProducao: TrabalhoProducao, modificaServidor: bool= True):
        try:
            trabalhoProducaoLimpo: TrabalhoProducao= TrabalhoProducao()
            trabalhoProducaoLimpo.id = trabalhoProducao.id
            trabalhoProducaoLimpo.idTrabalho = trabalhoProducao.idTrabalho
            trabalhoProducaoLimpo.recorrencia = trabalhoProducao.recorrencia
            trabalhoProducaoLimpo.tipoLicenca = trabalhoProducao.tipoLicenca
            trabalhoProducaoLimpo.estado = trabalhoProducao.estado
            recorrencia: int= 1 if trabalhoProducaoLimpo.recorrencia else 0
            sql = f"""UPDATE {CHAVE_LISTA_TRABALHOS_PRODUCAO} SET {CHAVE_ID_TRABALHO} = ?, {CHAVE_RECORRENCIA} = ?, {CHAVE_TIPO_LICENCA} = ?, {CHAVE_ESTADO} = ? WHERE {CHAVE_ID} == ?;"""
            repositorioTrabalhoProducao: RepositorioTrabalhoProducao= RepositorioTrabalhoProducao(personagem= personagem)
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, (trabalhoProducaoLimpo.idTrabalho, recorrencia, trabalhoProducaoLimpo.tipoLicenca, trabalhoProducaoLimpo.estado, trabalhoProducaoLimpo.id))
            if modificaServidor:
                if repositorioTrabalhoProducao.modificaTrabalhoProducao(trabalhoProducao= trabalhoProducaoLimpo):
                    self.__logger.info(f'({trabalhoProducaoLimpo}) modificado no servidor com sucesso!')
                    conexao.commit()
                    return True
                self.__logger.error(f'Erro ao modificar ({trabalhoProducaoLimpo}) no servidor: {repositorioTrabalhoProducao.pegaErro()}')
                self.__erro= repositorioTrabalhoProducao.pegaErro()
                conexao.rollback()
                return False
            conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            conexao.rollback()
        finally:
            self.__meuBanco.desconecta()
        return False
    
    def sincronizaTrabalhosProducao(self, personagem: Personagem):
        '''
            Função para sincronizar os trabalhos para produção no servidor com o banco de dados local
            Returns:
                bool: Verdadeiro caso a sincronização seja concluída com sucesso
        '''
        try:
            self.__conexao = self.__meuBanco.pegaConexao()
            sql = f"""DELETE FROM {CHAVE_LISTA_TRABALHOS_PRODUCAO} WHERE {CHAVE_ID_PERSONAGEM} == ?;"""
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, [personagem.id])
            repositorioTrabalhoProducao: RepositorioTrabalhoProducao= RepositorioTrabalhoProducao(personagem= personagem)
            trabalhosServidor: list[TrabalhoProducao]= repositorioTrabalhoProducao.pegaTodosTrabalhosProducao()
            if trabalhosServidor is None:
                self.__logger.error(f'Erro ao buscar trabalhos para produção no servidor: {repositorioTrabalhoProducao.pegaErro()}')
                raise Exception(repositorioTrabalhoProducao.pegaErro())
            for trabalho in trabalhosServidor:
                sql = f"""INSERT INTO {CHAVE_LISTA_TRABALHOS_PRODUCAO} ({CHAVE_ID}, {CHAVE_ID_TRABALHO}, {CHAVE_ID_PERSONAGEM}, {CHAVE_RECORRENCIA}, {CHAVE_TIPO_LICENCA}, {CHAVE_ESTADO}) VALUES (?, ?, ?, ?, ?, ?);"""
                try:
                    recorrencia = 1 if trabalho.recorrencia else 0
                    cursor.execute(sql, (trabalho.id, trabalho.idTrabalho, personagem.id, recorrencia, trabalho.tipoLicenca, trabalho.estado))
                    self.__logger.info(menssagem= f'Trabalho para produção ({trabalho.nome}) inserido com sucesso!')
                except Exception as e:
                    raise e
            self.__conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__conexao.rollback()
        finally:
            self.__meuBanco.desconecta()
        return False
    
    def pegaErro(self):
        return self.__erro