__author__ = 'Kevin Amazonas'

from modelos.trabalhoEstoque import TrabalhoEstoque
from db.db import MeuBanco

class EstoqueDaoSqlite:
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

    def pegaEstoque(self):
        estoque = []
        sql = f"""SELECT * FROM Lista_estoque WHERE idPersonagem = {self.__personagem.pegaId()};"""
        try:
            cursor = self.conexao.cursor()
            cursor.execute(sql)
            for linha in cursor.fetchall():
                estoque.append(TrabalhoEstoque(linha[0], linha[3], linha[4], linha[5], linha[6], linha[7], linha[2]))
        except Exception as e:
            self.__erro = str(e)
        return estoque
    
    def insereTrabalhoEstoque(self, trabalhoEstoque):
        sql = """INSERT INTO Lista_estoque (id, idPersonagem, idTrabalho, nome, profissao, nivel, quantidade, raridade)
        VALUES (?,?,?,?,?,?,?,?)""", (trabalhoEstoque.pegaId(), self.__personagem.pegaId(), trabalhoEstoque.pegaTrabalhoId(), trabalhoEstoque.pegaNome(), trabalhoEstoque.pegaProfissao(), trabalhoEstoque.pegaNivel(), trabalhoEstoque.pegaQuantidade(), trabalhoEstoque.pegaRaridade())
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql)
            self.__conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            return False

    def modificaTrabalhoEstoque(self, trabalhoEstoque):
        sql = """UPDATE Lista_estoque SET idTrabalho = ?, nome = ?, profissao = ?, nivel = ?, quantidade = ?, raridade = ?""", (trabalhoEstoque.pegaTrabalhoId(), trabalhoEstoque.pegaNome(), trabalhoEstoque.pegaProfissao(), trabalhoEstoque.pegaNivel(), trabalhoEstoque.pegaQuantidade(), trabalhoEstoque.pegaRarirdade())
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql)
            self.__conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            return False
            
    def pegaErro(self):
        return self.__erro