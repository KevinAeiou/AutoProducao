__author__ = 'Kevin Amazonas'

from modelos.trabalho import Trabalho
from db.db import MeuBanco
from repositorio.repositorioTrabalho import RepositorioTrabalho

class TrabalhoDaoSqlite():
    def __init__(self):
        self.__conexao = None
        self.__erro = None
        self.__fabrica = None
        try:
            self.__meuBanco = MeuBanco()
            self.__conexao = self.__meuBanco.pegaConexao(1)
            self.__fabrica = self.__meuBanco.pegaFabrica()
            self.__meuBanco.criaTabelas()
            self.__repositorioTrabalho = RepositorioTrabalho()
        except Exception as e:
            self.__erro = str(e)

    def pegaTrabalhos(self):
        trabalhos = []
        sql = """SELECT * FROM trabalhos;"""
        try:
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql)
                for linha in cursor.fetchall():
                    trabalho = Trabalho()
                    trabalho.id = linha[0]
                    trabalho.nome = linha[1]
                    trabalho.nomeProducao = linha[2]
                    trabalho.experiencia = linha[3]
                    trabalho.nivel = linha[4]
                    trabalho.profissao = linha[5]
                    trabalho.raridade = linha[6]
                    trabalho.trabalhoNecessario = linha[7]
                    trabalhos.append(trabalho)
                trabalhos = sorted(trabalhos, key= lambda trabalho: (trabalho.profissao, trabalho.raridade, trabalho.nivel))
                self.__meuBanco.desconecta()
                return trabalhos            
        except Exception as e:
            self.__erro = str(e)
        return None

    def pegaTrabalhoEspecificoPorId(self, trabalho):
        trabalho = Trabalho()
        sql = """
            SELECT * 
            FROM trabalhos
            WHERE id == ?;"""
        try:
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql, [trabalho.id])
                for linha in cursor.fetchall():
                    trabalho.id = linha[0]
                    trabalho.nome = linha[1]
                    trabalho.nomeProducao = linha[2]
                    trabalho.experiencia = linha[3]
                    trabalho.nivel = linha[4]
                    trabalho.profissao = linha[5]
                    trabalho.raridade = linha[6]
                    trabalho.trabalhoNecessario = linha[7]
                self.__meuBanco.desconecta()
                return trabalho            
        except Exception as e:
            self.__erro = str(e)
        return None

    def pegaTrabalhoEspecificoPorNomeProfissao(self, trabalho):
        trabalho = Trabalho()
        sql = """
            SELECT * 
            FROM trabalhos
            WHERE nome == ? AND profissao = ? AND raridade == ?;"""
        try:
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql, (trabalho.nome, trabalho.profissao, trabalho.raridade))
                for linha in cursor.fetchall():
                    trabalho.id = linha[0]
                    trabalho.nome = linha[1]
                    trabalho.nomeProducao = linha[2]
                    trabalho.experiencia = linha[3]
                    trabalho.nivel = linha[4]
                    trabalho.profissao = linha[5]
                    trabalho.raridade = linha[6]
                    trabalho.trabalhoNecessario = linha[7]
                self.__meuBanco.desconecta()
                return trabalho            
        except Exception as e:
            self.__erro = str(e)
        return None
    
    def insereTrabalho(self, trabalho, modificaServidor = True):
        sql = """INSERT INTO trabalhos (id, nome, nomeProducao, experiencia, nivel, profissao, raridade, trabalhoNecessario)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalho.id, trabalho.nome, trabalho.nomeProducao, trabalho.experiencia, trabalho.nivel, trabalho.profissao, trabalho.raridade, trabalho.trabalhoNecessario))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaServidor:
                if self.__repositorioTrabalho.insereTrabalho(trabalho):
                    print(f'{trabalho.nome} inserido no servidor com sucesso!')
                else:
                    print(f'Erro ao inserir trabalho no servidor: {self.__repositorioTrabalho.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False

    def modificaTrabalhoPorId(self, trabalho, modificaServidor = True):
        sql = """
            UPDATE trabalhos SET nome = ?, nomeProducao = ?, experiencia = ?, nivel = ?, profissao = ?, raridade = ?, trabalhoNecessario = ?
            WHERE id = ?"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalho.nome, trabalho.nomeProducao, trabalho.experiencia, trabalho.nivel, trabalho.profissao, trabalho.raridade, trabalho.trabalhoNecessario, trabalho.id))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaServidor:
                if self.__repositorioTrabalho.modificaTrabalho(trabalho):
                    print(f'{trabalho.nome} modificado no servidor com sucesso!')
                else:
                    print(f'Erro ao modificar trabalho no servidor: {self.__repositorioTrabalho.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False

    def modificaTrabalhoPorNomeProfissaoRaridade(self, trabalho):
        sql = """
            UPDATE trabalhos SET id = ?, nome = ?, nomeProducao = ?, experiencia = ?, nivel = ?, profissao = ?, raridade = ?, trabalhoNecessario = ?
            WHERE nome = ? AND profissao = ? AND raridade = ?"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalho.id, trabalho.nome, trabalho.nomeProducao, trabalho.experiencia, trabalho.nivel, trabalho.profissao, trabalho.raridade, trabalho.trabalhoNecessario, trabalho.nome, trabalho.profissao, trabalho.raridade))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
        
    def removeTrabalho(self, trabalho, modificaServidor = True):
        sql = """DELETE FROM trabalhos WHERE id == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [trabalho.id])
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaServidor:
                if self.__repositorioTrabalho.removeTrabalho(trabalho):
                    print(f'{trabalho.nome} removido do servidor com sucesso!')
                else:
                    print(f'Erro ao remover trabalho do servidor: {self.__repositorioTrabalho.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
    
    def pegaErro(self):
        return self.__erro