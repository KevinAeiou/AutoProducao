__author__ = 'Kevin Amazonas'

from modelos.trabalhoVendido import TrabalhoVendido
from db.db import MeuBanco
from repositorio.repositorioVendas import RepositorioVendas

class VendaDaoSqlite:
    def __init__(self, personagem = None):
        self.__conexao = None
        self.__erro = None
        self.__personagem = personagem
        self.__repositorioVendas = RepositorioVendas(personagem)
        try:
            self.__meuBanco = MeuBanco()
            self.__conexao = self.__meuBanco.pegaConexao(1)
            self.__meuBanco.criaTabelas()
        except Exception as e:
            self.__erro = str(e)

    def pegaVendas(self):
        vendas = []
        sql = """
            SELECT * 
            FROM vendas 
            WHERE nomePersonagem == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [self.__personagem.pegaId()])
            for linha in cursor.fetchall():
                vendas.append(TrabalhoVendido(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], linha[6]))
            vendas = sorted(vendas, key=lambda trabalhoVendido: (trabalhoVendido.pegaDataVenda(), trabalhoVendido.pegaNome()))
            self.__meuBanco.desconecta()
            return vendas
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def insereTrabalhoVendido(self, trabalhoVendido):
        sql = """
            INSERT INTO vendas (id, nomeProduto, dataVenda, nomePersonagem, quantidadeProduto, trabalhoId, valorProduto)
            VALUES (?, ?, ?, ?, ?, ?, ?);"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalhoVendido.pegaId(), trabalhoVendido.pegaNome(), trabalhoVendido.pegaDataVenda(), trabalhoVendido.pegaNomePersonagem(), trabalhoVendido.pegaQuantidadeProduto(), trabalhoVendido.pegaTrabalhoId(), trabalhoVendido.pegaValorProduto()))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if self.__repositorioVendas.insereTrabalhoVendido(trabalhoVendido):
                print(f'Nova venda inserida com sucesso no servidor!')
            else:
                print(f'Erro ao inserir nova venda no servidor: {self.__repositorioVendas.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def removeTrabalhoVendido(self, trabalhoVendido):
        sql = """
            DELETE FROM vendas
            WHERE id == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [trabalhoVendido.pegaId()])
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if self.__repositorioVendas.removeVenda(trabalhoVendido):
                print(f'Trabalho vendido removido com sucesso do servidor!')
            else:
                print(f'Erro ao remover trabalho vendido do servidor: {self.__repositorioVendas.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def modificaTrabalhoVendido(self, trabalhoVendido):
        sql = """
            UPDATE vendas
            SET nomeProduto = ?, dataVenda = ?, quantidadeProduto = ?, trabalhoId = ?, valorProduto = ?
            WHERE id == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalhoVendido.pegaNome(), trabalhoVendido.pegaDataVenda(), trabalhoVendido.pegaQuantidadeProduto(), trabalhoVendido.pegaTrabalhoId(), trabalhoVendido.pegaValorProduto(), trabalhoVendido.pegaId()))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if self.__repositorioVendas.modificaVenda(trabalhoVendido):
                print(f'Trabalho vendido modificado com sucesso no servidor!')
            else:
                print(f'Erro ao modificar trabalho vendido no servidor: {self.__repositorioVendas.pegaErro()}')
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
            return vendas
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
            
    def pegaErro(self):
        return self.__erro