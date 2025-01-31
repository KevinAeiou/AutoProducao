__author__ = 'Kevin Amazonas'

from modelos.trabalhoEstoque import TrabalhoEstoque
from db.db import MeuBanco
from repositorio.repositorioEstoque import RepositorioEstoque
import logging
from constantes import *

class EstoqueDaoSqlite:
    logging.basicConfig(level = logging.INFO, filename = 'logs/aplicacao.log', encoding='utf-8', format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt = '%d/%m/%Y %I:%M:%S %p')
    def __init__(self, personagem = None):
        self.__conexao = None
        self.__erro = None
        self.__personagem = personagem
        self.__repositorioEstoque = RepositorioEstoque(personagem)
        self.__logger = logging.getLogger('estoqueDao')
        try:
            self.__meuBanco = MeuBanco()
            self.__conexao = self.__meuBanco.pegaConexao(1)
            self.__meuBanco.criaTabelas()
        except Exception as e:
            self.__erro = str(e)

    def pegaTrabalhosEstoque(self):
        estoque = []
        sql = """
            SELECT Lista_estoque.id, trabalhos.nome, trabalhos.profissao, trabalhos.nivel, Lista_estoque.quantidade, trabalhos.raridade, Lista_estoque.idTrabalho
            FROM Lista_estoque
            INNER JOIN trabalhos
            ON Lista_estoque.idTrabalho == trabalhos.id
            WHERE idPersonagem = ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [self.__personagem.id])
            for linha in cursor.fetchall():
                trabalhoEstoque = TrabalhoEstoque()
                trabalhoEstoque.id = linha[0]
                trabalhoEstoque.nome = linha[1]
                trabalhoEstoque.profissao = linha[2]
                trabalhoEstoque.nivel = linha[3]
                trabalhoEstoque.quantidade = linha[4]
                trabalhoEstoque.raridade = linha[5]
                trabalhoEstoque.trabalhoId = linha[6]
                estoque.append(trabalhoEstoque)
            self.__meuBanco.desconecta()
            return estoque
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None

    def pegaTodosTrabalhosEstoque(self):
        estoque = []
        sql = """
            SELECT Lista_estoque.id, trabalhos.nome, trabalhos.profissao, trabalhos.nivel, Lista_estoque.quantidade, trabalhos.raridade, Lista_estoque.idTrabalho
            FROM Lista_estoque
            INNER JOIN trabalhos
            ON Lista_estoque.idTrabalho == trabalhos.id;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql)
            for linha in cursor.fetchall():
                trabalhoEstoque = TrabalhoEstoque()
                trabalhoEstoque.id = linha[0]
                trabalhoEstoque.nome = linha[1]
                trabalhoEstoque.profissao = linha[2]
                trabalhoEstoque.nivel = linha[3]
                trabalhoEstoque.quantidade = linha[4]
                trabalhoEstoque.raridade = linha[5]
                trabalhoEstoque.trabalhoId = linha[6]
                estoque.append(trabalhoEstoque)
            self.__meuBanco.desconecta()
            return estoque
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhoEstoquePorId(self, id: str) -> TrabalhoEstoque | None:
        trabalhoEncontrado = TrabalhoEstoque()
        sql = """
            SELECT Lista_estoque.id, trabalhos.nome, trabalhos.profissao, trabalhos.nivel, Lista_estoque.quantidade, trabalhos.raridade, Lista_estoque.idTrabalho
            FROM Lista_estoque
            INNER JOIN trabalhos
            ON Lista_estoque.idTrabalho == trabalhos.id
            WHERE Lista_estoque.id == ?
            LIMIT 1;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [id])
            for linha in cursor.fetchall():
                trabalhoEncontrado.id = linha[0]
                trabalhoEncontrado.nome = linha[1]
                trabalhoEncontrado.profissao = linha[2]
                trabalhoEncontrado.nivel = linha[3]
                trabalhoEncontrado.quantidade = linha[4]
                trabalhoEncontrado.raridade = linha[5]
                trabalhoEncontrado.trabalhoId = linha[6]
            self.__meuBanco.desconecta()
            return trabalhoEncontrado
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhoEstoquePorIdTrabalho(self, id: str) -> TrabalhoEstoque | None:
        sql = f"""
            SELECT {CHAVE_ID}, {CHAVE_QUANTIDADE}, {CHAVE_ID_TRABALHO}
            FROM {CHAVE_LISTA_ESTOQUE}
            WHERE {CHAVE_ID_TRABALHO} == ?
            LIMIT 1;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [id])
            trabalhoEncontrado = TrabalhoEstoque()
            for linha in cursor.fetchall():
                trabalhoEncontrado.id = linha[0]
                trabalhoEncontrado.quantidade = linha[1]
                trabalhoEncontrado.trabalhoId = linha[2]
            self.__meuBanco.desconecta()
            return trabalhoEncontrado
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def pegaQuantidadeTrabalho(self, idTrabalho: str) -> int | None:            
        sql = """
            SELECT quantidade
            FROM Lista_estoque
            WHERE idTrabalho == ?
            AND idPersonagem == ?
            LIMIT 1;
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (idTrabalho, self.__personagem.id))
            linha = cursor.fetchone()
            quantidade = 0 if linha is None else linha[0]
            self.__meuBanco.desconecta()
            return quantidade
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def insereTrabalhoEstoque(self, trabalho: TrabalhoEstoque, modificaServidor: bool = True) -> bool:
        sql = f"""
            INSERT INTO {CHAVE_LISTA_ESTOQUE} ({CHAVE_ID}, {CHAVE_ID_PERSONAGEM}, {CHAVE_ID_TRABALHO}, {CHAVE_QUANTIDADE})
            VALUES (?,?,?,?);
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalho.id, self.__personagem.id, trabalho.trabalhoId, trabalho.quantidade))
            if modificaServidor:
                if self.__repositorioEstoque.insereTrabalhoEstoque(trabalho):
                    self.__logger.info(f'({trabalho}) inserido no servidor com sucesso!')
                else:
                    self.__logger.error(f'Erro ao inserir ({trabalho}) no servidor!')
                    self.__conexao.rollback()
                    self.__meuBanco.desconecta()
                    return False
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False

    def modificaTrabalhoEstoque(self, trabalho: TrabalhoEstoque, modificaServidor: bool = True) -> bool:
        sql = f"""
            UPDATE {CHAVE_LISTA_ESTOQUE} 
            SET {CHAVE_ID_TRABALHO} = ?, {CHAVE_QUANTIDADE} = ?
            WHERE {CHAVE_ID} == ?"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalho.trabalhoId, trabalho.quantidade, trabalho.id))
            if modificaServidor:
                if self.__repositorioEstoque.modificaTrabalhoEstoque(trabalho):
                    self.__logger.info(f'({trabalho}) modificado no servidor com sucesso!')
                else:
                    self.__logger.error(f'Erro ao modificar ({trabalho}) no servidor: {self.__repositorioEstoque.pegaErro()}')
                    self.__conexao.rollback()
                    self.__meuBanco.desconecta()
                    return False
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False

    def modificaIdTrabalhoEstoque(self, idTrabalhoNovo, idTrabalhoAntigo):
        sql = """
            UPDATE Lista_estoque 
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

    def modificaIdPersonagemTrabalhoEstoque(self, idPersonagemNovo, idPersonagemAntigo):
        sql = """
            UPDATE Lista_estoque 
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
    
    def removeTrabalhoEstoque(self, trabalhoEstoque, modificaServidor = True):
        sql = """
            DELETE FROM Lista_estoque
            WHERE id == ?;
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [trabalhoEstoque.id])
            if modificaServidor:
                if self.__repositorioEstoque.removeTrabalho(trabalhoEstoque):
                    self.__logger.info(f'({trabalhoEstoque}) removido do servidor com sucesso!')
                else:
                    self.__logger.error(f'Erro ao remover ({trabalhoEstoque}) do servidor: {self.__repositorioEstoque.pegaErro()}')
                    self.__conexao.rollback()
                    self.__meuBanco.desconecta()
                    return False
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
    
    def removeColunasTabelaEstoque(self):
        sqlDropNome = """
            ALTER TABLE Lista_estoque
            DROP COLUMN nome;
            """
        sqlDropProfissao = """
            ALTER TABLE Lista_estoque
            DROP COLUMN profissao;
            """
        sqlDropNivel = """
            ALTER TABLE Lista_estoque
            DROP COLUMN nivel;
            """
        sqlDropRaridade = """
            ALTER TABLE Lista_estoque
            DROP COLUMN raridade;
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sqlDropNome)
            cursor.execute(sqlDropProfissao)
            cursor.execute(sqlDropNivel)
            cursor.execute(sqlDropRaridade)
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False

    def pegaErro(self):
        return self.__erro