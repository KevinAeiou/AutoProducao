__author__ = 'Kevin Amazonas'

from modelos.trabalhoProducao import TrabalhoProducao
from db.db import MeuBanco
from repositorio.repositorioTrabalhoProducao import RepositorioTrabalhoProducao

class TrabalhoProducaoDaoSqlite:
    def __init__(self, personagem = None):
        self.__conexao = None
        self.__erro = None
        self.__personagem = personagem
        try:
            self.__meuBanco = MeuBanco()
            self.__conexao = self.__meuBanco.pegaConexao(1)
            self.__meuBanco.criaTabelas()
            self.__repositorioTrabalhoProducao = RepositorioTrabalhoProducao(personagem)
        except Exception as e:
            self.__erro = str(e)
    
    def pegaTodosTrabalhosProducao(self):
        trabalhosProducao = []
        sql = """
            SELECT * 
            FROM Lista_desejo;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql)
            for linha in cursor.fetchall():
                recorrencia = True if linha[10] == 1 else False
                trabalhosProducao.append(TrabalhoProducao(linha[0], linha[1], linha[3], linha[4], linha[5], linha[6], linha[7], linha[8], linha[9], recorrencia, linha[11], linha[12]))
            self.__meuBanco.desconecta()
            return trabalhosProducao
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhosProducao(self):
        trabalhosProducao = []
        sql = """SELECT * FROM Lista_desejo WHERE idPersonagem == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [self.__personagem.pegaId()])
            for linha in cursor.fetchall():
                recorrencia = True if linha[10] == 1 else False
                trabalhosProducao.append(TrabalhoProducao(linha[0], linha[1], linha[3], linha[4], linha[5], linha[6], linha[7], linha[8], linha[9], recorrencia, linha[11], linha[12]))
            self.__meuBanco.desconecta()
            return trabalhosProducao
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhosProducaoParaProduzirProduzindo(self):
        trabalhosProducao = []
        sql = """SELECT * FROM Lista_desejo WHERE idPersonagem == ? AND (estado == 0 OR estado == 1);"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [self.__personagem.pegaId()])
            for linha in cursor.fetchall():
                recorrencia = True if linha[10] == 1 else False
                trabalhosProducao.append(TrabalhoProducao(linha[0], linha[1], linha[3], linha[4], linha[5], linha[6], linha[7], linha[8], linha[9], recorrencia, linha[11], linha[12]))
            self.__meuBanco.desconecta()
            return trabalhosProducao
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def insereTrabalhoProducao(self, trabalhoProducao):
        recorrencia = 1 if trabalhoProducao.pegaRecorrencia() else 0
        sql = """INSERT INTO Lista_desejo (id, idTrabalho, idPersonagem, nome, nomeProducao, experiencia, nivel, profissao, raridade, trabalhoNecessario, recorrencia, tipoLicenca, estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalhoProducao.pegaId(), trabalhoProducao.pegaTrabalhoId(), self.__personagem.pegaId(), trabalhoProducao.pegaNome(), trabalhoProducao.pegaNomeProducao(), trabalhoProducao.pegaExperiencia(), trabalhoProducao.pegaNivel(), trabalhoProducao.pegaProfissao(), trabalhoProducao.pegaRaridade(), trabalhoProducao.pegaTrabalhoNecessario(), recorrencia, trabalhoProducao.pegaLicenca(), trabalhoProducao.pegaEstado()))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if self.__repositorioTrabalhoProducao.insereTrabalhoProducao(trabalhoProducao):
                print(f'{trabalhoProducao.pegaNome()} inserido com sucesso no servidor!')
            else:
                print(f'Erro ao inserir trabalho produção no servidor: {self.__repositorioTrabalhoProducao.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
        
    def removeTrabalhoProducao(self, trabalhoProducao):
        sql = """
            DELETE FROM Lista_desejo
            WHERE id == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [trabalhoProducao.pegaId()])
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if self.__repositorioTrabalhoProducao.removeTrabalhoProducao(trabalhoProducao):
                print(f'{trabalhoProducao.pegaNome()} removido com sucesso no servidor!')
            else:
                print(f'Erro ao remover trabalho produção no servidor: {self.__repositorioTrabalhoProducao.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
        
    def modificaTrabalhoProducao(self, trabalhoProducao):
        recorrencia = 1 if trabalhoProducao.pegaRecorrencia() else 0
        sql = """
            UPDATE Lista_desejo 
            SET idTrabalho = ?, nome = ?, nomeProducao = ?, experiencia = ?, nivel = ?, profissao = ?, raridade = ?, trabalhoNecessario = ?, recorrencia = ?, tipoLicenca = ?, estado = ? 
            WHERE id == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalhoProducao.pegaTrabalhoId(), trabalhoProducao.pegaNome(), trabalhoProducao.pegaNomeProducao(), trabalhoProducao.pegaExperiencia(), trabalhoProducao.pegaNivel(), trabalhoProducao.pegaProfissao(), trabalhoProducao.pegaRaridade(), trabalhoProducao.pegaTrabalhoNecessario(), recorrencia, trabalhoProducao.pegaLicenca(), trabalhoProducao.pegaEstado(), trabalhoProducao.pegaId()))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if self.__repositorioTrabalhoProducao.modificaTrabalhoProducao(trabalhoProducao):
                print(f'{trabalhoProducao.pegaNome()} modificado com sucesso no servidor!')
            else:
                print(f'Erro ao modificar trabalho produção no servidor: {self.__repositorioTrabalhoProducao.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
    
    def modificaIdTrabalhoEmProducao(self, idTrabalhoNovo, idTrabalhoAntigo):
        sql = """
            UPDATE Lista_desejo 
            SET idTrabalho = ?
            WHERE idTrabalho == ?"""
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
    
    def pegaErro(self):
        return self.__erro