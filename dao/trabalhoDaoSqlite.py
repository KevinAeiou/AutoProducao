__author__ = 'Kevin Amazonas'

from modelos.trabalho import Trabalho
from db.db import MeuBanco

class TrabalhoDaoSqlite():
    def __init__(self):
        self.__conexao = None
        self.__erro = None
        self.__fabrica = None
        try:
            meuBanco = MeuBanco()
            self.__conexao = meuBanco.pegaConexao(1)
            self.__fabrica = meuBanco.pegaFabrica()
            meuBanco.criaTabelas()
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
        except Exception as e:
            self.__erro = str(e)
        return todosTrabalhos
    
    def insereTrabalho(self, trabalho):
        sql = """INSERT INTO trabalhos (id, nome, nomeProducao, experiencia, nivel, profissao, raridade, trabalhoNecessario)
        VALUES (?,?,?,?,?,?,?,?)"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalho.pegaId(), trabalho.pegaNome(), trabalho.pegaNomeProducao(), trabalho.pegaExperiencia(), trabalho.pegaNivel(), trabalho.pegaProfissao(), trabalho.pegaRaridade(), trabalho.pegaTrabalhoNecessario()))
            self.__conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            return False

    def modificaTrabalho(self, trabalho):
        sql = """
            UPDATE trabalhos SET nome = ?, nomeProducao = ?, experiencia = ?, nivel = ?, profissao = ?, raridade = ?, trabalhoNecessario = ?
            WHERE id = ?"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalho.pegaNome(), trabalho.pegaNomeProducao(), trabalho.pegaExperiencia(), trabalho.pegaNivel(), trabalho.pegaProfissao(), trabalho.pegaRaridade(), trabalho.pegaTrabalhoNecessario(), trabalho.pegaId()))
            self.__conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            return False
        
    def removeTrabalho(self, trabalho):
        sql = """DELETE FROM trabalhos WHERE id == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [trabalho.pegaId()])
            self.__conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            return False
    
    def pegaErro(self):
        return self.__erro