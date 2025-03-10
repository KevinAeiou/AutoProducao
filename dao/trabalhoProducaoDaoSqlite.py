__author__ = 'Kevin Amazonas'

from modelos.trabalhoProducao import TrabalhoProducao
from modelos.personagem import Personagem
from db.db import MeuBanco
import logging
from repositorio.repositorioTrabalhoProducao import RepositorioTrabalhoProducao
from constantes import *

class TrabalhoProducaoDaoSqlite:
    logging.basicConfig(level = logging.INFO, filename = 'logs/aplicacao.log', encoding='utf-8', format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt = '%d/%m/%Y %I:%M:%S %p')
    def __init__(self, personagem: Personagem = None):
        self.__conexao = None
        self.__erro = None
        self.__personagem: Personagem = personagem
        self.__logger = logging.getLogger('trabalhoProducaoDao')
        try:
            self.__meuBanco = MeuBanco()
            self.__conexao = self.__meuBanco.pegaConexao(1)
            self.__meuBanco.criaTabelas()
            self.__repositorioTrabalhoProducao = RepositorioTrabalhoProducao(personagem)
        except Exception as e:
            self.__erro = str(e)
    
    def pegaTodosTrabalhosProducao(self):
        trabalhosProducao = []
        sql = """
            SELECT Lista_desejo.id, trabalhos.id, trabalhos.nome, trabalhos.nomeProducao, trabalhos.experiencia, trabalhos.nivel, trabalhos.profissao, trabalhos.raridade, trabalhos.trabalhoNecessario, Lista_desejo.recorrencia, Lista_desejo.tipoLicenca, Lista_desejo.estado
            FROM Lista_desejo
            INNER JOIN trabalhos
            ON Lista_desejo.idTrabalho == trabalhos.id;
            """
        try:
            cursor = self.__conexao.cursor()
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
            self.__meuBanco.desconecta()
            return trabalhosProducao
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhosProducao(self):
        trabalhosProducao = []
        sql = """
            SELECT Lista_desejo.id, trabalhos.id, trabalhos.nome, trabalhos.nomeProducao, trabalhos.experiencia, trabalhos.nivel, trabalhos.profissao, trabalhos.raridade, trabalhos.trabalhoNecessario, Lista_desejo.recorrencia, Lista_desejo.tipoLicenca, Lista_desejo.estado
            FROM Lista_desejo
            INNER JOIN trabalhos
            ON Lista_desejo.idTrabalho == trabalhos.id
            WHERE idPersonagem == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [self.__personagem.id])
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
            self.__meuBanco.desconecta()
            trabalhosProducao = sorted(trabalhosProducao, key = lambda trabalhoProducao: (trabalhoProducao.estado, trabalhoProducao.profissao, trabalhoProducao.nivel, trabalhoProducao.nome))
            return trabalhosProducao
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhosProducaoParaProduzirProduzindo(self):
        trabalhosProducao = []
        sql = """
            SELECT Lista_desejo.id, trabalhos.id, trabalhos.nome, trabalhos.nomeProducao, trabalhos.experiencia, trabalhos.nivel, trabalhos.profissao, trabalhos.raridade, trabalhos.trabalhoNecessario, Lista_desejo.recorrencia, Lista_desejo.tipoLicenca, Lista_desejo.estado
            FROM Lista_desejo
            INNER JOIN trabalhos
            ON Lista_desejo.idTrabalho == trabalhos.id
            WHERE idPersonagem == ? AND (estado == 0 OR estado == 1);"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [self.__personagem.id])
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
            self.__meuBanco.desconecta()
            return trabalhosProducao
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhosParaProduzirPorProfissaoRaridade(self, trabalho: TrabalhoProducao) -> list[TrabalhoProducao]:
        trabalhosProducao = []
        sql = f"""
            SELECT {CHAVE_LISTA_TRABALHOS_PRODUCAO}.{CHAVE_ID}, {CHAVE_TRABALHOS}.{CHAVE_ID}, {CHAVE_TRABALHOS}.{CHAVE_NIVEL}, {CHAVE_TRABALHOS}.{CHAVE_PROFISSAO}
            FROM {CHAVE_LISTA_TRABALHOS_PRODUCAO}
            INNER JOIN {CHAVE_TRABALHOS}
            ON {CHAVE_LISTA_TRABALHOS_PRODUCAO}.{CHAVE_ID_TRABALHO} == {CHAVE_TRABALHOS}.{CHAVE_ID}
            WHERE {CHAVE_ID_PERSONAGEM} == ? 
            AND {CHAVE_ESTADO} == {CODIGO_PARA_PRODUZIR}
            AND {CHAVE_TRABALHOS}.{CHAVE_RARIDADE} == ?
            AND {CHAVE_TRABALHOS}.{CHAVE_PROFISSAO} == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (self.__personagem.id, trabalho.raridade, trabalho.profissao))
            for linha in cursor.fetchall():
                trabalhoProducao = TrabalhoProducao()
                trabalhoProducao.id = linha[0]
                trabalhoProducao.idTrabalho = linha[1]
                trabalhoProducao.nivel = linha[2]
                trabalhoProducao.profissao = linha[3]
                trabalhosProducao.append(trabalhoProducao)
            self.__meuBanco.desconecta()
            return trabalhosProducao
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def pegaQuantidadeTrabalhoProducaoProduzindo(self, trabalhoId):
        sql = """
            SELECT COUNT(*) AS quantidade
            FROM Lista_desejo
            WHERE idPersonagem == ?
            AND idTrabalho == ?
            AND estado == 1;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (self.__personagem.id, trabalhoId))
            linha = cursor.fetchone()
            quantidade = 0 if linha is None else linha[0]
            self.__meuBanco.desconecta()
            return quantidade
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def pegaQuantidadeTrabalhoProducaoProduzirProduzindo(self, trabalhoId):
        sql = """
            SELECT COUNT(*) AS quantidade
            FROM Lista_desejo
            WHERE idPersonagem == ?
            AND idTrabalho == ?
            AND (estado == 0
            OR estado == 1);"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (self.__personagem.id, trabalhoId))
            linha = cursor.fetchone()
            quantidade = 0 if linha is None else linha[0]
            self.__meuBanco.desconecta()
            return quantidade
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhoProducaoPorId(self, id):
        trabalhoProducao = TrabalhoProducao()
        sql = """
            SELECT id, idTrabalho, recorrencia, tipoLicenca, estado
            FROM Lista_desejo
            WHERE id == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [id])
            for linha in cursor.fetchall():
                recorrencia = True if linha[2] == 1 else False
                trabalhoProducao.id = linha[0]
                trabalhoProducao.idTrabalho = linha[1]
                trabalhoProducao.recorrencia = recorrencia
                trabalhoProducao.tipoLicenca = linha[3]
                trabalhoProducao.estado = linha[4]
            self.__meuBanco.desconecta()
            return trabalhoProducao
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhosProducaoPorIdTrabalho(self, id: str) -> list[TrabalhoProducao] | None:
        trabalhosProducaoEncontrados: list[TrabalhoProducao] = []
        sql = f"""
            SELECT {CHAVE_ID}, {CHAVE_ID_TRABALHO}, {CHAVE_RECORRENCIA}, tipoLicenca, {CHAVE_ESTADO}
            FROM {CHAVE_LISTA_TRABALHOS_PRODUCAO}
            WHERE {CHAVE_ID_TRABALHO} == ?
            AND {CHAVE_ID_PERSONAGEM} == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (id, self.__personagem.id))
            for linha in cursor.fetchall():
                trabalhoProducao = TrabalhoProducao()
                recorrencia = True if linha[2] == 1 else False
                trabalhoProducao.id = linha[0]
                trabalhoProducao.idTrabalho = linha[1]
                trabalhoProducao.recorrencia = recorrencia
                trabalhoProducao.tipoLicenca = linha[3]
                trabalhoProducao.estado = linha[4]
                trabalhosProducaoEncontrados.append(trabalhoProducao)
            self.__meuBanco.desconecta()
            return trabalhosProducaoEncontrados
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def insereTrabalhoProducao(self, trabalhoProducao: TrabalhoProducao, modificaServidor: bool= True) -> bool:
        trabalhoProducaoLimpo:TrabalhoProducao = TrabalhoProducao()
        trabalhoProducaoLimpo.id = trabalhoProducao.id
        trabalhoProducaoLimpo.idTrabalho = trabalhoProducao.idTrabalho
        trabalhoProducaoLimpo.recorrencia = trabalhoProducao.recorrencia
        trabalhoProducaoLimpo.tipoLicenca = trabalhoProducao.tipoLicenca
        trabalhoProducaoLimpo.estado = trabalhoProducao.estado
        recorrencia = 1 if trabalhoProducaoLimpo.recorrencia else 0
        sql = f"""
            INSERT INTO {CHAVE_LISTA_TRABALHOS_PRODUCAO} ({CHAVE_ID}, {CHAVE_ID_TRABALHO}, {CHAVE_ID_PERSONAGEM}, {CHAVE_RECORRENCIA}, {CHAVE_TIPO_LICENCA}, {CHAVE_ESTADO}) 
            VALUES (?, ?, ?, ?, ?, ?);
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, (trabalhoProducaoLimpo.id, trabalhoProducaoLimpo.idTrabalho, self.__personagem.id, recorrencia, trabalhoProducaoLimpo.tipoLicenca, trabalhoProducaoLimpo.estado))
            if modificaServidor:
                if self.__repositorioTrabalhoProducao.insereTrabalhoProducao(trabalhoProducao= trabalhoProducaoLimpo):
                    self.__logger.info(f'({trabalhoProducaoLimpo}) inserido no servidor com sucesso!')
                    self.__conexao.commit()
                    self.__meuBanco.desconecta()
                    return True
                self.__logger.error(f'Erro ao inserir ({trabalhoProducaoLimpo}) no servidor: {self.__repositorioTrabalhoProducao.pegaErro()}')
                self.__conexao.rollback()
                self.__meuBanco.desconecta()
                self.__erro= self.__repositorioTrabalhoProducao.pegaErro()
                return False
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__conexao.rollback()
        self.__meuBanco.desconecta()
        return False
    
    def removeTrabalhoProducao(self, trabalhoProducao: TrabalhoProducao, modificaServidor: bool= True) -> bool:
        sql = f"""
            DELETE FROM {CHAVE_LISTA_TRABALHOS_PRODUCAO}
            WHERE {CHAVE_ID} == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, [trabalhoProducao.id])
            if modificaServidor:
                if self.__repositorioTrabalhoProducao.removeTrabalhoProducao(trabalhoProducao= trabalhoProducao):
                    self.__logger.info(f'({trabalhoProducao}) removido do servidor com sucesso!')
                    self.__conexao.commit()
                    self.__meuBanco.desconecta()
                    return True
                self.__logger.error(f'Erro ao remover ({trabalhoProducao}) do servidor: {self.__repositorioTrabalhoProducao.pegaErro()}')
                self.__erro= self.__repositorioTrabalhoProducao.pegaErro()
                self.__conexao.rollback()
                self.__meuBanco.desconecta()
                return False
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__conexao.rollback()
        self.__meuBanco.desconecta()
        return False
        
    def modificaTrabalhoProducao(self, trabalhoProducao: TrabalhoProducao, modificaServidor: bool= True):
        trabalhoProducaoLimpo: TrabalhoProducao= TrabalhoProducao()
        trabalhoProducaoLimpo.id = trabalhoProducao.id
        trabalhoProducaoLimpo.idTrabalho = trabalhoProducao.idTrabalho
        trabalhoProducaoLimpo.recorrencia = trabalhoProducao.recorrencia
        trabalhoProducaoLimpo.tipoLicenca = trabalhoProducao.tipoLicenca
        trabalhoProducaoLimpo.estado = trabalhoProducao.estado
        recorrencia: int= 1 if trabalhoProducaoLimpo.recorrencia else 0
        sql = f"""
            UPDATE {CHAVE_LISTA_TRABALHOS_PRODUCAO} 
            SET {CHAVE_ID_TRABALHO} = ?, {CHAVE_RECORRENCIA} = ?, {CHAVE_TIPO_LICENCA} = ?, {CHAVE_ESTADO} = ? 
            WHERE {CHAVE_ID} == ?;
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, (trabalhoProducaoLimpo.idTrabalho, recorrencia, trabalhoProducaoLimpo.tipoLicenca, trabalhoProducaoLimpo.estado, trabalhoProducaoLimpo.id))
            if modificaServidor:
                if self.__repositorioTrabalhoProducao.modificaTrabalhoProducao(trabalhoProducao= trabalhoProducaoLimpo):
                    self.__logger.info(f'({trabalhoProducaoLimpo}) modificado no servidor com sucesso!')
                    self.__conexao.commit()
                    self.__meuBanco.desconecta()
                    return True
                self.__logger.error(f'Erro ao modificar ({trabalhoProducaoLimpo}) no servidor: {self.__repositorioTrabalhoProducao.pegaErro()}')
                self.__erro= self.__repositorioTrabalhoProducao.pegaErro()
                self.__conexao.rollback()
                self.__meuBanco.desconecta()
                return False
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__conexao.rollback()
        self.__meuBanco.desconecta()
        return False
    
    def modificaIdTrabalhoEmProducao(self, idTrabalhoNovo, idTrabalhoAntigo):
        sql = """
            UPDATE Lista_desejo 
            SET idTrabalho = ?
            WHERE idTrabalho == ?"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (idTrabalhoNovo, idTrabalhoAntigo))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
    
    
    def modificaIdPersonagemTrabalhoEmProducao(self, idPersonagemNovo, idPersonagemAntigo):
        sql = """
            UPDATE Lista_desejo 
            SET idPersonagem = ?
            WHERE idPersonagem == ?"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (idPersonagemNovo, idPersonagemAntigo))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
    
    def pegaErro(self):
        return self.__erro