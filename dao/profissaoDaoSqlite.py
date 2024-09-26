__author__ = 'Kevin Amazonas'

from modelos.profissao import Profissao
from db.db import MeuBanco

class ProfissaoDaoSqlite:
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
    
    def pegaProfissoes(self):
        profissoes = []
        sql = f"""
        SELECT * FROM profissoes 
        WHERE idPersonagem == {self.__personagem.pegaId()};"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql)
            for linha in cursor.fetchall():
                prioridade = True if linha[4] == 1 else False
                profissoes.append(Profissao(linha[0], linha[2], linha[3], prioridade))
            profissoes = sorted(profissoes, key=lambda profissao:(profissao.pegaExperiencia()), reverse=True)
        except Exception as e:
            self.__erro = str(e)
        return profissoes
    
    def modificaProfissao(self, profissao):
        prioridade = 1 if profissao.pegaPrioridade() else 0
        sql = """UPDATE profissoes SET nome = ?, experiencia = ?, prioridade = ?""", (profissao.pegaNome(), profissao.pegaExperiencia(), prioridade)
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