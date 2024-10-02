__author__ = 'Kevin Amazonas'

from modelos.trabalhoVendido import TrabalhoVendido
from db.db import MeuBanco

class VendaDaoSqlite:
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

    def pegaVendas(self):
        vendas = []
        sql = """SELECT * FROM vendas WHERE nomePersonagem == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, self.__personagem.pegaId())
            for linha in cursor.fetchall():
                vendas.append(TrabalhoVendido(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], linha[6]))
            vendas = sorted(vendas, key=lambda trabalhoVendido: (trabalhoVendido.pegaData(), trabalhoVendido.pegaNome()))
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return vendas
    
    def insereVenda(self, venda):
        sql = """
            INSERT INTO vendas (id, nomeProduto, dataVenda, nomePersonagem, quantidadeProduto, trabalhoId, valorProduto)
            VALUES (?, ?, ?, ?, ?, ?, ?);"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (venda.pegaId(), venda.pegaNome(), venda.pegaDataVenda(), venda.pegaNomePersonagem(), venda.pegaQuantidadeProduto(), venda.pegaTrabalhoId(), venda.pegaValorProduto()))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
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
                vendas.append(TrabalhoVendido(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], linha[6]))
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return vendas
            
    def pegaErro(self):
        return self.__erro