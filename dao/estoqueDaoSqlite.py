__author__ = 'Kevin Amazonas'

from modelos.trabalhoEstoque import TrabalhoEstoque
from db.db import MeuBanco

class EstoqueDaoSqlite:
    def __init__(self, personagem = None):
        self.__conexao = None
        self.__erro = None
        self.__personagem = personagem
        try:
            self.__meuBanco = MeuBanco()
            self.__conexao = self.__meuBanco.pegaConexao(1)
            self.__meuBanco.criaTabelas()
        except Exception as e:
            self.__erro = str(e)

    def pegaEstoque(self):
        estoque = []
        sql = """
            SELECT * 
            FROM Lista_estoque 
            WHERE idPersonagem = ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [self.__personagem.pegaId()])
            for linha in cursor.fetchall():
                estoque.append(TrabalhoEstoque(linha[0], linha[3], linha[4], linha[5], linha[6], linha[7], linha[2]))
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return estoque

    def pegaTodosTrabalhosEstoque(self):
        estoque = []
        sql = """
            SELECT * 
            FROM Lista_estoque"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql)
            for linha in cursor.fetchall():
                estoque.append(TrabalhoEstoque(linha[0], linha[3], linha[4], linha[5], linha[6], linha[7], linha[2]))
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return estoque
    
    def insereTrabalhoEstoque(self, trabalhoEstoque):
        sql = """
            INSERT INTO Lista_estoque (id, idPersonagem, idTrabalho, nome, profissao, nivel, quantidade, raridade)
            VALUES (?,?,?,?,?,?,?,?)"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalhoEstoque.pegaId(), self.__personagem.pegaId(), trabalhoEstoque.pegaTrabalhoId(), trabalhoEstoque.pegaNome(), trabalhoEstoque.pegaProfissao(), trabalhoEstoque.pegaNivel(), trabalhoEstoque.pegaQuantidade(), trabalhoEstoque.pegaRaridade()))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False

    def modificaTrabalhoEstoque(self, trabalhoEstoque):
        sql = """
            UPDATE Lista_estoque 
            SET idTrabalho = ?, nome = ?, profissao = ?, nivel = ?, quantidade = ?, raridade = ? WHERE id = ?"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalhoEstoque.pegaTrabalhoId(), trabalhoEstoque.pegaNome(), trabalhoEstoque.pegaProfissao(), trabalhoEstoque.pegaNivel(), trabalhoEstoque.pegaQuantidade(), trabalhoEstoque.pegaRaridade(), trabalhoEstoque.pegaId()))
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
            cursor.execute(sql, [trabalhoEstoque.pegaId()])
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False

    def pegaErro(self):
        return self.__erro