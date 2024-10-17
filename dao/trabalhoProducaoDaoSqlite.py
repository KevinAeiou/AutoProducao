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
                trabalhoProducao.id = linha[0]
                trabalhoProducao.trabalhoId = linha[1]
                trabalhoProducao.nome = linha[2]
                trabalhoProducao.nomeProducao = linha[3]
                trabalhoProducao.experiencia = linha[4]
                trabalhoProducao.nivel = linha[5]
                trabalhoProducao.profissao = linha[6]
                trabalhoProducao.raridade = linha[7]
                trabalhoProducao.trabalhoNecessario = linha[8]
                trabalhoProducao.recorrencia = recorrencia
                trabalhoProducao.tipo_licenca = linha[10]
                trabalhoProducao.estado = linha[11]
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
            cursor.execute(sql, [self.__personagem.id])
            for linha in cursor.fetchall():
                recorrencia = True if linha[9] == 1 else False
                trabalhoProducao = TrabalhoProducao()
                trabalhoProducao.id = linha[0]
                trabalhoProducao.trabalhoId = linha[1]
                trabalhoProducao.nome = linha[2]
                trabalhoProducao.nomeProducao = linha[3]
                trabalhoProducao.experiencia = linha[4]
                trabalhoProducao.nivel = linha[5]
                trabalhoProducao.profissao = linha[6]
                trabalhoProducao.raridade = linha[7]
                trabalhoProducao.trabalhoNecessario = linha[8]
                trabalhoProducao.recorrencia = recorrencia
                trabalhoProducao.tipo_licenca = linha[10]
                trabalhoProducao.estado = linha[11]
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
            cursor.execute(sql, [self.__personagem.id])
            for linha in cursor.fetchall():
                recorrencia = True if linha[9] == 1 else False
                trabalhoProducao = TrabalhoProducao()
                trabalhoProducao.id = linha[0]
                trabalhoProducao.trabalhoId = linha[1]
                trabalhoProducao.nome = linha[2]
                trabalhoProducao.nomeProducao = linha[3]
                trabalhoProducao.experiencia = linha[4]
                trabalhoProducao.nivel = linha[5]
                trabalhoProducao.profissao = linha[6]
                trabalhoProducao.raridade = linha[7]
                trabalhoProducao.trabalhoNecessario = linha[8]
                trabalhoProducao.recorrencia = recorrencia
                trabalhoProducao.tipo_licenca = linha[10]
                trabalhoProducao.estado = linha[11]
                trabalhosProducao.append(trabalhoProducao)
            self.__meuBanco.desconecta()
            return trabalhosProducao
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhoProducaoPorId(self, trabalhoProducao):
        trabalhoProducao = TrabalhoProducao()
        sql = """
            SELECT Lista_desejo.id, trabalhos.id, trabalhos.nome, trabalhos.nomeProducao, trabalhos.experiencia, trabalhos.nivel, trabalhos.profissao, trabalhos.raridade, trabalhos.trabalhoNecessario, Lista_desejo.recorrencia, Lista_desejo.tipoLicenca, Lista_desejo.estado
            FROM Lista_desejo
            INNER JOIN trabalhos
            ON Lista_desejo.idTrabalho == trabalhos.id
            WHERE Lista_desejo.id == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [trabalhoProducao.id])
            for linha in cursor.fetchall():
                recorrencia = True if linha[9] == 1 else False
                trabalhoProducao.id = linha[0]
                trabalhoProducao.trabalhoId = linha[1]
                trabalhoProducao.nome = linha[2]
                trabalhoProducao.nomeProducao = linha[3]
                trabalhoProducao.experiencia = linha[4]
                trabalhoProducao.nivel = linha[5]
                trabalhoProducao.profissao = linha[6]
                trabalhoProducao.raridade = linha[7]
                trabalhoProducao.trabalhoNecessario = linha[8]
                trabalhoProducao.recorrencia = recorrencia
                trabalhoProducao.tipo_licenca = linha[10]
                trabalhoProducao.estado = linha[11]
            self.__meuBanco.desconecta()
            return trabalhoProducao
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def insereTrabalhoProducao(self, trabalhoProducao, modificaServidor = True):
        recorrencia = 1 if trabalhoProducao.recorrencia else 0
        sql = """
            INSERT INTO Lista_desejo (id, idTrabalho, idPersonagem, recorrencia, tipoLicenca, estado) 
            VALUES (?, ?, ?, ?, ?, ?);
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalhoProducao.id, trabalhoProducao.trabalhoId, self.__personagem.id, recorrencia, trabalhoProducao.tipo_licenca, trabalhoProducao.estado))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaServidor:
                if self.__repositorioTrabalhoProducao.insereTrabalhoProducao(trabalhoProducao):
                    print(f'{trabalhoProducao.nome} inserido com sucesso no servidor!')
                else:
                    print(f'Erro ao inserir trabalho produção no servidor: {self.__repositorioTrabalhoProducao.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
        
    def removeTrabalhoProducao(self, trabalhoProducao, modificaServidor = True):
        sql = """
            DELETE FROM Lista_desejo
            WHERE id == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [trabalhoProducao.id])
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaServidor:
                if self.__repositorioTrabalhoProducao.removeTrabalhoProducao(trabalhoProducao):
                    print(f'{trabalhoProducao.nome} removido com sucesso no servidor!')
                else:
                    print(f'Erro ao remover trabalho produção no servidor: {self.__repositorioTrabalhoProducao.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
        
    def modificaTrabalhoProducao(self, trabalhoProducao, modificaServidor = True):
        recorrencia = 1 if trabalhoProducao.recorrencia else 0
        sql = """
            UPDATE Lista_desejo 
            SET idTrabalho = ?, recorrencia = ?, tipoLicenca = ?, estado = ? 
            WHERE id == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalhoProducao.trabalhoId, recorrencia, trabalhoProducao.tipo_licenca, trabalhoProducao.estado, trabalhoProducao.id))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaServidor:
                if self.__repositorioTrabalhoProducao.modificaTrabalhoProducao(trabalhoProducao):
                    print(f'{trabalhoProducao.nome} modificado com sucesso no servidor!')
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