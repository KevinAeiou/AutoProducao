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
        todosTrabalhos = []
        sql = """SELECT * FROM trabalhos;"""
        try:
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql)
                for linha in cursor.fetchall():
                    todosTrabalhos.append(Trabalho(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], linha[6], linha[7]))
                todosTrabalhos = sorted(todosTrabalhos, key= lambda trabalho: (trabalho.pegaProfissao(), trabalho.pegaRaridade(), trabalho.pegaNivel()))
                self.__meuBanco.desconecta()
                return todosTrabalhos            
        except Exception as e:
            self.__erro = str(e)
        return None
    
    def insereTrabalho(self, trabalho):
        sql = """INSERT INTO trabalhos (id, nome, nomeProducao, experiencia, nivel, profissao, raridade, trabalhoNecessario)
        VALUES (?,?,?,?,?,?,?,?)"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalho.pegaId(), trabalho.pegaNome(), trabalho.pegaNomeProducao(), trabalho.pegaExperiencia(), trabalho.pegaNivel(), trabalho.pegaProfissao(), trabalho.pegaRaridade(), trabalho.pegaTrabalhoNecessario()))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if self.__repositorioTrabalho.insereTrabalho(trabalho):
                print(f'{trabalho.pegaNome()} inserido no servidor com sucesso!')
            else:
                print(f'Erro ao inserir trabalho no servidor: {self.__repositorioTrabalho.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False

    def modificaTrabalho(self, trabalho):
        sql = """
            UPDATE trabalhos SET nome = ?, nomeProducao = ?, experiencia = ?, nivel = ?, profissao = ?, raridade = ?, trabalhoNecessario = ?
            WHERE id = ?"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalho.pegaNome(), trabalho.pegaNomeProducao(), trabalho.pegaExperiencia(), trabalho.pegaNivel(), trabalho.pegaProfissao(), trabalho.pegaRaridade(), trabalho.pegaTrabalhoNecessario(), trabalho.pegaId()))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if self.__repositorioTrabalho.modificaTrabalho(trabalho):
                print(f'{trabalho.pegaNome()} modificado no servidor com sucesso!')
            else:
                print(f'Erro ao modificar trabalho no servidor: {self.__repositorioTrabalho.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
        
    def removeTrabalho(self, trabalho):
        sql = """DELETE FROM trabalhos WHERE id == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [trabalho.pegaId()])
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if self.__repositorioTrabalho.removeTrabalho(trabalho):
                print(f'{trabalho.pegaNome()} removido do servidor com sucesso!')
            else:
                print(f'Erro ao remover trabalho do servidor: {self.__repositorioTrabalho.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
    
    def pegaErro(self):
        return self.__erro