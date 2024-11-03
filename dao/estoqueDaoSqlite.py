__author__ = 'Kevin Amazonas'

from modelos.trabalhoEstoque import TrabalhoEstoque
from db.db import MeuBanco
from repositorio.repositorioEstoque import RepositorioEstoque
import logging

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

    def pegaEstoque(self):
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
    
    def pegaTrabalhoEstoquePorId(self, trabalhoBuscado):
        trabalhoEncontrado = TrabalhoEstoque()
        sql = """
            SELECT Lista_estoque.id, trabalhos.nome, trabalhos.profissao, trabalhos.nivel, Lista_estoque.quantidade, trabalhos.raridade, Lista_estoque.idTrabalho
            FROM Lista_estoque
            INNER JOIN trabalhos
            ON Lista_estoque.idTrabalho == trabalhos.id
            WHERE Lista_estoque.id == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [trabalhoBuscado.id])
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
    
    def insereTrabalhoEstoque(self, trabalhoEstoque, modificaServidor = True):
        sql = """
            INSERT INTO Lista_estoque (id, idPersonagem, idTrabalho, quantidade)
            VALUES (?,?,?,?)"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalhoEstoque.id, self.__personagem.id, trabalhoEstoque.trabalhoId, trabalhoEstoque.quantidade))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaServidor:
                if self.__repositorioEstoque.insereTrabalhoEstoque(trabalhoEstoque):
                    self.__logger.info(f'({trabalhoEstoque}) inserido no servidor com sucesso!')
                else:
                    self.__logger.error(f'Erro ao inserir ({trabalhoEstoque}) no servidor!')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False

    def modificaTrabalhoEstoque(self, trabalhoEstoque, modificaServidor = True):
        sql = """
            UPDATE Lista_estoque 
            SET idTrabalho = ?, quantidade = ?
            WHERE id == ?"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalhoEstoque.trabalhoId, trabalhoEstoque.quantidade, trabalhoEstoque.id))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaServidor:
                if self.__repositorioEstoque.modificaTrabalhoEstoque(trabalhoEstoque):
                    self.__logger.info(f'({trabalhoEstoque}) modificado no servidor com sucesso!')
                else:
                    self.__logger.error(f'Erro ao modificar ({trabalhoEstoque}) no servidor: {self.__repositorioEstoque.pegaErro()}')
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
    
    def removeTrabalhoEstoque(self, trabalhoEstoque):
        sql = """
            DELETE FROM Lista_estoque
            WHERE id == ?;
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [trabalhoEstoque.id])
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if self.__repositorioEstoque.removeTrabalho(trabalhoEstoque):
                self.__logger.info(f'({trabalhoEstoque}) removido do servidor com sucesso!')
            else:
                self.__logger.error(f'Erro ao remover ({trabalhoEstoque}) do servidor: {self.__repositorioEstoque.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False

    def pegaErro(self):
        return self.__erro