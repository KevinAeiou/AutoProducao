__author__ = 'Kevin Amazonas'

from modelos.trabalhoVendido import TrabalhoVendido
from db.db import MeuBanco

class VendaDaoSqlite:
    def __init__(self, personagem):
        self.__conexao = None
        self.__erro = None
        self.__personagem = personagem
        try:
            meuBanco = MeuBanco()
            self.__conexao = meuBanco.pegaConexao(1)
            meuBanco.criaTabelas()
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
        except Exception as e:
            self.__erro = str(e)
        return vendas
    
    def insereVenda(self, venda):
        sql = """
            INSERT INTO vendas (id, nomeProduto, dataVenda, nomePersonagem, quantidadeProduto, trabalhoId, valorProduto)
            VALUES (?, ?, ?, ?, ?, ?, ?);"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (venda.pegaId(), venda.pegaNomeProduto(), venda.pegaDataVenda(), venda.pegaNomePersonagem(), venda.pegaQuantidadeProduto(), venda.pegaTrabalhoId(), venda.pegaValorProduto()))
            self.__conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            return False
            
    def pegaErro(self):
        return self.__erro