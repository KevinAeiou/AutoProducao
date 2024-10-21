__author__ = 'Kevin Amazonas'

from modelos.personagem import Personagem
from db.db import MeuBanco
from repositorio.repositorioPersonagem import RepositorioPersonagem

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
            self.__repositorioPersonagem = RepositorioPersonagem()
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
                    personagem = Personagem()
                    personagem.id = linha[0]
                    personagem.nome = linha[1]
                    personagem.email = linha[2]
                    personagem.senha = linha[3]
                    personagem.espacoProducao = linha[4]
                    personagem.estado = estado
                    personagem.uso = uso
                    personagem.autoProducao = autoProducao
                    personagens.append(personagem)
                self.__meuBanco.desconecta()
                return personagens
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def pegaPersonagemEspecificoPorId(self, personagem):
        sql = """
            SELECT * 
            FROM personagens
            WHERE id == ?;"""
        try:
            personagemEncontrado = Personagem()
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql, [personagem.id])
                for linha in cursor.fetchall():
                    estado = True if linha[5] else False
                    uso = True if linha[6] else False
                    autoProducao = True if linha[7] else False
                    personagemEncontrado.id = linha[0]
                    personagemEncontrado.nome = linha[1]
                    personagemEncontrado.email = linha[2]
                    personagemEncontrado.senha = linha[3]
                    personagemEncontrado.espacoProducao = linha[4]
                    personagemEncontrado.estado = estado
                    personagemEncontrado.uso = uso
                    personagemEncontrado.autoProducao = autoProducao
                self.__meuBanco.desconecta()
                return personagemEncontrado            
        except Exception as e:
            self.__erro = str(e)
        return None
    
    def pegaPersonagemEspecificoPorNome(self, personagem):
        nome = '' if personagem.nome == None else personagem.nome
        sql = """
            SELECT * 
            FROM personagens
            WHERE nome == ?;"""
        try:
            personagemEncontrado = Personagem()
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql, [nome])
                for linha in cursor.fetchall():
                    estado = True if linha[5] else False
                    uso = True if linha[6] else False
                    autoProducao = True if linha[7] else False
                    personagemEncontrado.id = linha[0]
                    personagemEncontrado.nome = linha[1]
                    personagemEncontrado.email = linha[2]
                    personagemEncontrado.senha = linha[3]
                    personagemEncontrado.espacoProducao = linha[4]
                    personagemEncontrado.estado = estado
                    personagemEncontrado.uso = uso
                    personagemEncontrado.autoProducao = autoProducao
                self.__meuBanco.desconecta()
                return personagemEncontrado            
        except Exception as e:
            self.__erro = str(e)
        return None
    
    def modificaPersonagem(self, personagem, modificaServidor = True):
        estado = 1 if personagem.estado else 0
        uso = 1 if personagem.uso else 0
        autoProducao = 1 if personagem.autoProducao else 0
        sql = """
            UPDATE personagens SET id = ?, nome = ?, email = ?, senha = ?, espacoProducao = ?, estado = ?, uso = ?, autoProducao = ?
            WHERE id == ?"""
        try:
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql, (personagem.id, personagem.nome, personagem.email, personagem.senha, personagem.espacoProducao, estado, uso, autoProducao, personagem.id))
                self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaServidor:
                if self.__repositorioPersonagem.modificaPersonagem(personagem):
                    print(f'{personagem.nome} modificado com sucesso no servidor!')
                else:
                    print(f'Erro ao modificar personagem no servidor: {self.__repositorioPersonagem.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
    
    def modificaPersonagemPorNome(self, personagem):
        estado = 1 if personagem.estado else 0
        uso = 1 if personagem.uso else 0
        autoProducao = 1 if personagem.autoProducao else 0
        sql = """
            UPDATE personagens SET id = ?, nome = ?, email = ?, senha = ?, espacoProducao = ?, estado = ?, uso = ?, autoProducao = ?
            WHERE nome == ?"""
        try:
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql, (personagem.id, personagem.nome, personagem.email, personagem.senha, personagem.espacoProducao, estado, uso, autoProducao, personagem.nome))
                self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
    
    def inserePersonagem(self, personagem, modificaServidor = True):
        estado = 1 if personagem.estado else 0
        uso = 1 if personagem.uso else 0
        autoProducao = 1 if personagem.autoProducao else 0
        sql = """
            INSERT INTO personagens (id, nome, email, senha, espacoProducao, estado, uso, autoProducao)
            VALUES (?,?,?,?,?,?,?,?)
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (personagem.id, personagem.nome, personagem.email, personagem.senha, personagem.espacoProducao, estado, uso, autoProducao))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaServidor:
                if self.__repositorioPersonagem.inserePersonagem(personagem):
                    print(f'{personagem.nome} inserido com sucesso no servidor!')
                else:
                    print(f'Erro ao inserir trabalho no servidor: {self.__repositorioPersonagem.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
    
    def removePersonagem(self, personagem, modificaServidor = True):
        sql = """DELETE FROM personagens WHERE id == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [personagem.id])
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaServidor:
                if self.__repositorioPersonagem.removePersonagem(personagem):
                    print(f'{personagem.nome} removido com sucesso no servidor!')
                else:
                    print(f'Erro ao remover personagem do servidor: {self.__repositorioPersonagem.pegaErro()}')
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

    def deletaTabelaPersonagens(self):
        sql = """
            DROP TABLE personagens;            
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql)
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
    
    def pegaErro(self):
        return self.__erro