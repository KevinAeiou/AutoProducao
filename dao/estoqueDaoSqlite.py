__author__ = 'Kevin Amazonas'

from modelos.trabalhoEstoque import TrabalhoEstoque
from modelos.personagem import Personagem
from db.db import MeuBanco
from repositorio.repositorioEstoque import RepositorioEstoque
from modelos.logger import MeuLogger
from constantes import *

class EstoqueDaoSqlite:
    def __init__(self, banco: MeuBanco):
        self.__conexao = None
        self.__erro = None
        self.__logger: MeuLogger= MeuLogger(nome= 'estoqueDao')
        self.__meuBanco = banco

    def pegaTrabalhosEstoque(self, personagem: Personagem) -> list[TrabalhoEstoque]:
        try:
            self.__conexao = self.__meuBanco.pegaConexao()
            estoque: list[TrabalhoEstoque]= []
            sql = f"""
                SELECT {CHAVE_LISTA_ESTOQUE}.{CHAVE_ID}, {CHAVE_TRABALHOS}.{CHAVE_NOME}, {CHAVE_TRABALHOS}.{CHAVE_PROFISSAO}, {CHAVE_TRABALHOS}.{CHAVE_NIVEL}, {CHAVE_LISTA_ESTOQUE}.{CHAVE_QUANTIDADE}, {CHAVE_TRABALHOS}.{CHAVE_RARIDADE}, {CHAVE_LISTA_ESTOQUE}.{CHAVE_ID_TRABALHO}
                FROM {CHAVE_LISTA_ESTOQUE}
                INNER JOIN {CHAVE_TRABALHOS}
                ON {CHAVE_LISTA_ESTOQUE}.{CHAVE_ID_TRABALHO} == {CHAVE_TRABALHOS}.{CHAVE_ID}
                WHERE {CHAVE_ID_PERSONAGEM} == ?;"""
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [personagem.id])
            for linha in cursor.fetchall():
                trabalhoEstoque: TrabalhoEstoque= TrabalhoEstoque()
                trabalhoEstoque.id = linha[0]
                trabalhoEstoque.nome = linha[1]
                trabalhoEstoque.profissao = linha[2]
                trabalhoEstoque.nivel = linha[3]
                trabalhoEstoque.quantidade = linha[4]
                trabalhoEstoque.raridade = linha[5]
                trabalhoEstoque.idTrabalho = linha[6]
                estoque.append(trabalhoEstoque)
            return estoque
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None

    def pegaTrabalhoEstoquePorId(self, id: str) -> TrabalhoEstoque | None:
        try:
            trabalhoEncontrado: TrabalhoEstoque= TrabalhoEstoque()
            sql = f"""
                SELECT {CHAVE_LISTA_ESTOQUE}.{CHAVE_ID}, {CHAVE_TRABALHOS}.{CHAVE_NOME}, {CHAVE_TRABALHOS}.{CHAVE_PROFISSAO}, {CHAVE_TRABALHOS}.{CHAVE_NIVEL}, {CHAVE_LISTA_ESTOQUE}.{CHAVE_QUANTIDADE}, {CHAVE_TRABALHOS}.{CHAVE_RARIDADE}, {CHAVE_LISTA_ESTOQUE}.{CHAVE_ID_TRABALHO}
                FROM {CHAVE_LISTA_ESTOQUE}
                INNER JOIN {CHAVE_TRABALHOS}
                ON {CHAVE_LISTA_ESTOQUE}.{CHAVE_ID_TRABALHO} == {CHAVE_TRABALHOS}.{CHAVE_ID}
                WHERE {CHAVE_LISTA_ESTOQUE}.{CHAVE_ID} == ?
                LIMIT 1;
                """
            self.__conexao = self.__meuBanco.pegaConexao()
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [id])
            for linha in cursor.fetchall():
                trabalhoEncontrado.id = linha[0]
                trabalhoEncontrado.nome = linha[1]
                trabalhoEncontrado.profissao = linha[2]
                trabalhoEncontrado.nivel = linha[3]
                trabalhoEncontrado.quantidade = linha[4]
                trabalhoEncontrado.raridade = linha[5]
                trabalhoEncontrado.idTrabalho = linha[6]
            return trabalhoEncontrado
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhoEstoquePorIdTrabalho(self, id: str) -> TrabalhoEstoque | None:
        try:
            sql = f"""
                SELECT {CHAVE_ID}, {CHAVE_QUANTIDADE}, {CHAVE_ID_TRABALHO}
                FROM {CHAVE_LISTA_ESTOQUE}
                WHERE {CHAVE_ID_TRABALHO} == ?
                LIMIT 1;"""
            self.__conexao = self.__meuBanco.pegaConexao()
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [id])
            trabalhoEncontrado = TrabalhoEstoque()
            for linha in cursor.fetchall():
                trabalhoEncontrado.id = linha[0]
                trabalhoEncontrado.quantidade = linha[1]
                trabalhoEncontrado.idTrabalho = linha[2]
            return trabalhoEncontrado
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def pegaQuantidadeTrabalho(self, personagem: Personagem, idTrabalho: str) -> int | None:            
        try:
            sql = f"""
                SELECT quantidade
                FROM {CHAVE_LISTA_ESTOQUE}
                WHERE idTrabalho == ?
                AND idPersonagem == ?
                LIMIT 1;
                """
            self.__conexao = self.__meuBanco.pegaConexao()
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (idTrabalho, personagem.id))
            linha = cursor.fetchone()
            quantidade = 0 if linha is None else linha[0]
            return quantidade
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def insereTrabalhoEstoque(self, personagem: Personagem, trabalho: TrabalhoEstoque, modificaServidor: bool = True) -> bool:
        try:
            sql = f"""INSERT INTO {CHAVE_LISTA_ESTOQUE} ({CHAVE_ID}, {CHAVE_ID_PERSONAGEM}, {CHAVE_ID_TRABALHO}, {CHAVE_QUANTIDADE}) VALUES (?,?,?,?);"""
            repositorioEstoque = RepositorioEstoque(personagem)
            self.__conexao = self.__meuBanco.pegaConexao()
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, (trabalho.id, personagem.id, trabalho.idTrabalho, trabalho.quantidade))
            if modificaServidor:
                if repositorioEstoque.insereTrabalhoEstoque(trabalho= trabalho):
                    self.__logger.info(f'({trabalho}) inserido no servidor com sucesso!')
                    self.__conexao.commit()
                    return True
                self.__logger.error(f'Erro ao inserir ({trabalho}) no servidor: {repositorioEstoque.pegaErro()}')
                self.__erro= repositorioEstoque.pegaErro()
                self.__conexao.rollback()
                return False
            self.__conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__conexao.rollback()
        finally:
            self.__meuBanco.desconecta()
        return False

    def modificaTrabalhoEstoque(self, personagem: Personagem, trabalho: TrabalhoEstoque, modificaServidor: bool = True) -> bool:
        try:
            sql = f"""
                UPDATE {CHAVE_LISTA_ESTOQUE} 
                SET {CHAVE_ID_TRABALHO} = ?, {CHAVE_QUANTIDADE} = ?
                WHERE {CHAVE_ID} == ?"""
            repositorioEstoque = RepositorioEstoque(personagem)
            self.__conexao = self.__meuBanco.pegaConexao()
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, (trabalho.idTrabalho, trabalho.quantidade, trabalho.id))
            if modificaServidor:
                if repositorioEstoque.modificaTrabalhoEstoque(trabalho= trabalho):
                    self.__logger.info(f'({trabalho}) modificado no servidor com sucesso!')
                    self.__conexao.commit()
                    return True
                self.__logger.error(f'Erro ao modificar ({trabalho}) no servidor: {repositorioEstoque.pegaErro()}')
                self.__erro= repositorioEstoque.pegaErro()
                self.__conexao.rollback()
                return False
            self.__conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__conexao.rollback()
        finally:
            self.__meuBanco.desconecta()
        return False
    
    def removeTrabalhoEstoque(self, personagem: Personagem, trabalhoEstoque: TrabalhoEstoque, modificaServidor: bool= True) -> bool:
        try:
            sql = f"""
                DELETE FROM {CHAVE_LISTA_ESTOQUE}
                WHERE {CHAVE_ID} == ?;
                """
            self.__conexao = self.__meuBanco.pegaConexao()
            repositorioEstoque = RepositorioEstoque(personagem)
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, [trabalhoEstoque.id])
            if modificaServidor:
                if repositorioEstoque.removeTrabalho(trabalho= trabalhoEstoque):
                    self.__logger.info(f'({trabalhoEstoque}) removido do servidor com sucesso!')
                    self.__conexao.commit()
                    return True
                self.__logger.error(f'Erro ao remover ({trabalhoEstoque}) do servidor: {repositorioEstoque.pegaErro()}')
                self.__erro= repositorioEstoque.pegaErro()
                self.__conexao.rollback()
                return False
            self.__conexao.commit()
            return True
        except Exception as e:
            self.__conexao.rollback()
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return False
    
    def sincronizaTrabalhosEstoque(self, personagem: Personagem) -> bool:
        '''
            Função para sincronizar os trabalhos no estoque no servidor com o banco de dados local
            Returns:
                bool: Verdadeiro caso a sincronização seja concluída com sucesso
        '''
        try:
            self.__conexao = self.__meuBanco.pegaConexao()
            sql = f"""DELETE FROM {CHAVE_LISTA_ESTOQUE} WHERE {CHAVE_ID_PERSONAGEM} == ?;"""
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, [personagem.id])
            repositorioTrabalhoEstoque: RepositorioEstoque= RepositorioEstoque(personagem= personagem)
            trabalhosServidor: list[TrabalhoEstoque]= repositorioTrabalhoEstoque.pegaTodosTrabalhosEstoque()
            if trabalhosServidor is None:
                self.__logger.error(f'Erro ao buscar trabalhos no estoque no servidor: {repositorioTrabalhoEstoque.pegaErro()}')
                raise Exception(repositorioTrabalhoEstoque.pegaErro())
            for trabalho in trabalhosServidor:
                sql = f"""INSERT INTO {CHAVE_LISTA_ESTOQUE} ({CHAVE_ID}, {CHAVE_ID_PERSONAGEM}, {CHAVE_ID_TRABALHO}, {CHAVE_QUANTIDADE}) VALUES (?,?,?,?);"""
                try:
                    cursor.execute(sql, (trabalho.id, personagem.id, trabalho.idTrabalho, trabalho.quantidade))
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