__author__ = 'Kevin Amazonas'

from modelos.trabalhoVendido import TrabalhoVendido
from db.db import MeuBanco
from repositorio.repositorioVendas import RepositorioVendas
import logging

class VendaDaoSqlite:
    logging.basicConfig(level = logging.INFO, filename = 'logs/aplicacao.log', encoding='utf-8', format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt = '%d/%m/%Y %I:%M:%S %p')
    def __init__(self, personagem = None):
        self.__conexao = None
        self.__erro = None
        self.__personagem = personagem
        self.__repositorioVendas = RepositorioVendas(personagem)
        self.__logger = logging.getLogger('vendaDao')
        try:
            self.__meuBanco = MeuBanco()
            self.__conexao = self.__meuBanco.pegaConexao(1)
            self.__meuBanco.criaTabelas()
        except Exception as e:
            self.__erro = str(e)

    def pegaVendas(self):
        vendas = []
        sql = """
            SELECT vendas.id, trabalhos.id, trabalhos.nome, trabalhos.nivel, trabalhos.profissao, trabalhos.raridade, trabalhos.trabalhoNecessario, vendas.nomeProduto, vendas.dataVenda, vendas.quantidadeProduto, vendas.valorProduto
            FROM vendas
            INNER JOIN trabalhos
            ON vendas.trabalhoId == trabalhos.id
            WHERE nomePersonagem == ?;
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [self.__personagem.id])
            for linha in cursor.fetchall():
                trabalhoVendido = TrabalhoVendido()
                trabalhoVendido.id = linha[0]
                trabalhoVendido.trabalhoId = linha[1]
                trabalhoVendido.nome = linha[2]
                trabalhoVendido.nivel = linha[3]
                trabalhoVendido.profissao = linha[4]
                trabalhoVendido.raridade = linha[5]
                trabalhoVendido.trabalhoNecessario = linha[6]
                trabalhoVendido.nomeProduto = linha[7]
                trabalhoVendido.dataVenda = linha[8]
                trabalhoVendido.quantidadeProduto = linha[9]
                trabalhoVendido.valorProduto = linha[10]
                vendas.append(trabalhoVendido)
            vendas = sorted(vendas, key=lambda trabalhoVendido: (trabalhoVendido.dataVenda, trabalhoVendido.nome))
            self.__meuBanco.desconecta()
            return vendas
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None

    def pegaTrabalhoVendidoPorId(self, trabalhoVendidoBuscado):
        trabalhoVendido = TrabalhoVendido()
        sql = """
            SELECT * 
            FROM vendas 
            WHERE id == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [trabalhoVendidoBuscado.id])
            for linha in cursor.fetchall():
                trabalhoVendido.id = linha[0]
                trabalhoVendido.nomeProduto = linha[1]
                trabalhoVendido.dataVenda = linha[2]
                trabalhoVendido.nomePersonagem = linha[3]
                trabalhoVendido.quantidadeProduto = linha[4]
                trabalhoVendido.trabalhoId = linha[5]
                trabalhoVendido.valorProduto = linha[6]
            self.__meuBanco.desconecta()
            return trabalhoVendido
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def insereTrabalhoVendido(self, trabalhoVendido, modificaServidor = True):
        sql = """
            INSERT INTO vendas (id, nomeProduto, dataVenda, nomePersonagem, quantidadeProduto, trabalhoId, valorProduto)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalhoVendido.id, trabalhoVendido.nomeProduto, trabalhoVendido.dataVenda, self.__personagem.id, trabalhoVendido.quantidadeProduto, trabalhoVendido.trabalhoId, trabalhoVendido.valorProduto))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaServidor:
                if self.__repositorioVendas.insereTrabalhoVendido(trabalhoVendido):
                    self.__logger.info(f'({trabalhoVendido}) inserido no servidor com sucesso!')
                else:
                    self.__logger.error(f'Erro ao inserir ({trabalhoVendido}) no servidor: {self.__repositorioVendas.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def removeTrabalhoVendido(self, trabalhoVendido, modificaServidor = True):
        sql = """
            DELETE FROM vendas
            WHERE id == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [trabalhoVendido.id])
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaServidor:
                if self.__repositorioVendas.removeVenda(trabalhoVendido):
                    self.__logger.info(f'({trabalhoVendido}) removido do servidor com sucesso!')
                else:
                    self.__logger.error(f'Erro ao remover ({trabalhoVendido}) do servidor: {self.__repositorioVendas.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def modificaTrabalhoVendido(self, trabalhoVendido, modificaServidor = True):
        sql = """
            UPDATE vendas
            SET nomeProduto = ?, dataVenda = ?, quantidadeProduto = ?, trabalhoId = ?, valorProduto = ?
            WHERE id == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalhoVendido.nomeProduto, trabalhoVendido.dataVenda, trabalhoVendido.quantidadeProduto, trabalhoVendido.trabalhoId, trabalhoVendido.valorProduto, trabalhoVendido.id))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaServidor:
                if self.__repositorioVendas.modificaVenda(trabalhoVendido):
                    self.__logger.info(f'({trabalhoVendido}) modificado no servidor com sucesso!')
                else:
                    self.__logger.error(f'Erro ao modificar ({trabalhoVendido}) no servidor: {self.__repositorioVendas.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def modificaIdTrabalhoVendido(self, idTrabalhoNovo, idTrabalhoAntigo):
        sql = """
            UPDATE vendas 
            SET trabalhoId = ?
            WHERE trabalhoId == ?"""
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
    
    def modificaIdPersonagemTrabalhoVendido(self, idTrabalhoNovo, idTrabalhoAntigo):
        sql = """
            UPDATE vendas 
            SET nomePersonagem = ?
            WHERE nomePersonagem == ?"""
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
    
        
    def pegaTodosTrabalhosVendidos(self):
        vendas = []
        sql = """
            SELECT * 
            FROM vendas"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql)
            for linha in cursor.fetchall():
                trabalhoVendido = TrabalhoVendido()
                trabalhoVendido.id = linha[0]
                trabalhoVendido.nomeProduto = linha[1]
                trabalhoVendido.dataVenda = linha[2]
                trabalhoVendido.nomePersonagem = linha[3]
                trabalhoVendido.quantidadeProduto = linha[4]
                trabalhoVendido.trabalhoId = linha[5]
                trabalhoVendido.valorProduto = linha[6]
                vendas.append(trabalhoVendido)
            return vendas
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
            
    def pegaErro(self):
        return self.__erro