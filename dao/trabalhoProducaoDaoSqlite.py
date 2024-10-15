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
            SELECT Lista_desejo.id, trabalhos.id, trabalhos.nome, trabalhos.nomeProducao, trabalhos.experiencia, trabalhos.nivel, trabalhos.profissao, trabalhos.raridade, trabalhos.trabalhoNecessario, Lista_desejo.recorrencia, Lista_desejo.tipoLicenca, Lista_desejo.estado
            FROM Lista_desejo
            INNER JOIN trabalhos
            ON Lista_desejo.idTrabalho == trabalhos.id;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql)
            for linha in cursor.fetchall():
                recorrencia = True if linha[9] == 1 else False
                trabalhoProducao = TrabalhoProducao()
                trabalhoProducao.setId(linha[0])
                trabalhoProducao.setTrabalhoId([1])
                trabalhoProducao.setNome(linha[2])
                trabalhoProducao.setNomeProducao(linha[3])
                trabalhoProducao.setExperiencia(linha[4])
                trabalhoProducao.setNivel(linha[5])
                trabalhoProducao.setProfissao(linha[6])
                trabalhoProducao.setRaridade(linha[7])
                trabalhoProducao.setTrabalhoNecessario(linha[8])
                trabalhoProducao.setRecorrencia(recorrencia)
                trabalhoProducao.setLicenca(linha[10])
                trabalhoProducao.setEstado(linha[11])
                trabalhosProducao.append(trabalhoProducao)
            self.__meuBanco.desconecta()
            return trabalhosProducao
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhosProducao(self):
        trabalhosProducao = []
        sql = """
            SELECT Lista_desejo.id, trabalhos.id, trabalhos.nome, trabalhos.nomeProducao, trabalhos.experiencia, trabalhos.nivel, trabalhos.profissao, trabalhos.raridade, trabalhos.trabalhoNecessario, Lista_desejo.recorrencia, Lista_desejo.tipoLicenca, Lista_desejo.estado
            FROM Lista_desejo
            INNER JOIN trabalhos
            ON Lista_desejo.idTrabalho == trabalhos.id
            WHERE idPersonagem == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [self.__personagem.pegaId()])
            for linha in cursor.fetchall():
                recorrencia = True if linha[9] == 1 else False
                trabalhoProducao = TrabalhoProducao()
                trabalhoProducao.setId(linha[0])
                trabalhoProducao.setTrabalhoId(linha[1])
                trabalhoProducao.setNome(linha[2])
                trabalhoProducao.setNomeProducao(linha[3])
                trabalhoProducao.setExperiencia(linha[4])
                trabalhoProducao.setNivel(linha[5])
                trabalhoProducao.setProfissao(linha[6])
                trabalhoProducao.setRaridade(linha[7])
                trabalhoProducao.setTrabalhoNecessario(linha[8])
                trabalhoProducao.setRecorrencia(recorrencia)
                trabalhoProducao.setLicenca(linha[10])
                trabalhoProducao.setEstado(linha[11])
                trabalhosProducao.append(trabalhoProducao)
            self.__meuBanco.desconecta()
            return trabalhosProducao
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhosProducaoParaProduzirProduzindo(self):
        trabalhosProducao = []
        sql = """
            SELECT Lista_desejo.id, trabalhos.id, trabalhos.nome, trabalhos.nomeProducao, trabalhos.experiencia, trabalhos.nivel, trabalhos.profissao, trabalhos.raridade, trabalhos.trabalhoNecessario, Lista_desejo.recorrencia, Lista_desejo.tipoLicenca, Lista_desejo.estado
            FROM Lista_desejo
            INNER JOIN trabalhos
            ON Lista_desejo.idTrabalho == trabalhos.id
            WHERE idPersonagem == ? AND (estado == 0 OR estado == 1);"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [self.__personagem.pegaId()])
            for linha in cursor.fetchall():
                recorrencia = True if linha[9] == 1 else False
                trabalhoProducao = TrabalhoProducao()
                trabalhoProducao.setId(linha[0])
                trabalhoProducao.setTrabalhoId([1])
                trabalhoProducao.setNome(linha[2])
                trabalhoProducao.setNomeProducao(linha[3])
                trabalhoProducao.setExperiencia(linha[4])
                trabalhoProducao.setNivel(linha[5])
                trabalhoProducao.setProfissao(linha[6])
                trabalhoProducao.setRaridade(linha[7])
                trabalhoProducao.setTrabalhoNecessario(linha[8])
                trabalhoProducao.setRecorrencia(recorrencia)
                trabalhoProducao.setLicenca(linha[10])
                trabalhoProducao.setEstado(linha[11])
                trabalhosProducao.append(trabalhoProducao)
            self.__meuBanco.desconecta()
            return trabalhosProducao
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def insereTrabalhoProducao(self, trabalhoProducao):
        recorrencia = 1 if trabalhoProducao.pegaRecorrencia() else 0
        sql = """
            INSERT INTO Lista_desejo (id, idTrabalho, idPersonagem, recorrencia, tipoLicenca, estado) 
            VALUES (?, ?, ?, ?, ?, ?);
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalhoProducao.pegaId(), trabalhoProducao.pegaTrabalhoId(), self.__personagem.pegaId(), recorrencia, trabalhoProducao.pegaLicenca(), trabalhoProducao.pegaEstado()))
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
            SET idTrabalho = ?, recorrencia = ?, tipoLicenca = ?, estado = ? 
            WHERE id == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalhoProducao.pegaTrabalhoId(), recorrencia, trabalhoProducao.pegaLicenca(), trabalhoProducao.pegaEstado(), trabalhoProducao.pegaId()))
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
    
    
    def modificaIdPersonagemTrabalhoEmProducao(self, idPersonagemNovo, idPersonagemAntigo):
        sql = """
            UPDATE Lista_desejo 
            SET idPersonagem = ?
            WHERE idPersonagem == ?"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (idPersonagemNovo, idPersonagemAntigo))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
    
    def pegaErro(self):
        return self.__erro