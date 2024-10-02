__author__ = 'Kevin Amazonas'

from modelos.profissao import Profissao
from db.db import MeuBanco
from uuid import uuid4
from constantes import CHAVE_PROFISSAO_ARMA_DE_LONGO_ALCANCE, CHAVE_PROFISSAO_ARMA_CORPO_A_CORPO, CHAVE_PROFISSAO_ARMADURA_DE_TECIDO, CHAVE_PROFISSAO_ARMADURA_LEVE, CHAVE_PROFISSAO_ARMADURA_PESADA, CHAVE_PROFISSAO_ANEIS, CHAVE_PROFISSAO_AMULETOS, CHAVE_PROFISSAO_CAPOTES, CHAVE_PROFISSAO_BRACELETES

class ProfissaoDaoSqlite:
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
    
    def pegaProfissoes(self):
        profissoes = []
        sql = f"""
        SELECT * FROM profissoes 
        WHERE idPersonagem == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [self.__personagem.pegaId()])
            for linha in cursor.fetchall():
                prioridade = True if linha[4] == 1 else False
                profissoes.append(Profissao(linha[0], linha[2], linha[3], prioridade))
            profissoes = sorted(profissoes, key=lambda profissao:(profissao.pegaExperiencia()), reverse=True)
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return profissoes
    
    def modificaProfissao(self, profissao):
        prioridade = 1 if profissao.pegaPrioridade() else 0
        sql = """
            UPDATE profissoes 
            SET nome = ?, experiencia = ?, prioridade = ?
            WHERE id = ?"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (profissao.pegaNome(), profissao.pegaExperiencia(), prioridade, profissao.pegaId()))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
    
    def insereListaProfissoes(self):
        profissoes = [CHAVE_PROFISSAO_ARMA_DE_LONGO_ALCANCE, CHAVE_PROFISSAO_ARMA_CORPO_A_CORPO, CHAVE_PROFISSAO_ARMADURA_DE_TECIDO, CHAVE_PROFISSAO_ARMADURA_LEVE, CHAVE_PROFISSAO_ARMADURA_PESADA, CHAVE_PROFISSAO_ANEIS, CHAVE_PROFISSAO_AMULETOS, CHAVE_PROFISSAO_CAPOTES, CHAVE_PROFISSAO_BRACELETES]
        for profissao in profissoes:
            self.__conexao = self.__meuBanco.pegaConexao(1)
            if self.insereProfissao(Profissao(str(profissoes.index(profissao)) + str(uuid4()), profissao, 0, False)):
                print(f'Profissão {profissao} inserida com sucesso!')
                continue
            print(f'Erro ao inserir profissão: {self.pegaErro()}')
    
    def insereProfissao(self, profissao):
        prioridade = 1 if profissao.pegaPrioridade() else 0
        sql = """
            INSERT INTO profissoes (id, idPersonagem, nome, experiencia, prioridade)
            VALUES (?, ?, ?, ?, ?)"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (profissao.pegaId(), self.__personagem.pegaId(), profissao.pegaNome(), profissao.pegaExperiencia(), prioridade))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
    
    def deletaTabelaProfissoes(self):
        sql = """
            DROP TABLE profissoes;            
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