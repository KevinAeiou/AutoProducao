__author__ = 'Kevin Amazonas'

from modelos.personagem import Personagem
from db.db import MeuBanco

class PersonagemDaoSqlite():
    def __init__(self):
        self.__conexao = None
        self.__erro = None
        self.__fabrica = None
        try:
            self.__meuBanco = MeuBanco()
            self.__conexao = self.__meuBanco.pegaConexao(1)
            self.__fabrica = self.__meuBanco.pegaFabrica()
            self.__meuBanco.criaTabelas()
        except Exception as e:
            self.__erro = str(e)

    def pegaPersonagens(self):
        personagens = []
        sql = """SELECT * FROM personagens;"""
        try:
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql)
                for linha in cursor.fetchall():
                    estado = True if linha[5] else False
                    uso = True if linha[6] else False
                    autoProducao = True if linha[7] else False
                    personagens.append(Personagem(linha[0], linha[1], linha[2],linha[3],linha[4],estado,uso,autoProducao))
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return personagens
    
    def modificaPersonagem(self, personagem):
        estado = 1 if personagem.pegaEstado() else 0
        uso = 1 if personagem.pegaUso() else 0
        autoProducao = 1 if personagem.pegaAutoProducao() else 0
        sql = """
            UPDATE personagens SET nome = ?, email = ?, senha = ?, espacoProducao = ?, estado = ?, uso = ?, autoProducao = ?
            WHERE id == ?"""
        try:
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql, (personagem.pegaNome(), personagem.pegaEmail(), personagem.pegaSenha(), personagem.pegaEspacoProducao(), estado, uso, autoProducao, personagem.pegaId()))
                self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
    
    def inserePersonagem(self, personagem):
        estado = 1 if personagem.pegaEstado() else 0
        uso = 1 if personagem.pegaUso() else 0
        autoProducao = 1 if personagem.pegaAutoProducao() else 0
        sql = """
            INSERT INTO personagens (id, nome, email, senha, espacoProducao, estado, uso, autoProducao)
            VALUES (?,?,?,?,?,?,?,?)
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (personagem.pegaId(), personagem.pegaNome(), personagem.pegaEmail(), personagem.pegaSenha(), personagem.pegaEspacoProducao(), estado, uso, autoProducao))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
    
    def removePersonagem(self, personagem):
        sql = """DELETE FROM personagens WHERE id == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [personagem.pegaId()])
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
        
    def insereColunaAutoProducaoTabelaPesonagem(self):
        sql = """
            ALTER TABLE personagens
            ADD COLUMN autoProducao TINYINT;
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql)
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False

    def pegaErro(self):
        return self.__erro