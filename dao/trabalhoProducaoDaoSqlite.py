__author__ = 'Kevin Amazonas'

from modelos.trabalhoProducao import TrabalhoProducao
from modelos.personagem import Personagem
from db.db import MeuBanco
from modelos.logger import MeuLogger
from repositorio.repositorioTrabalhoProducao import RepositorioTrabalhoProducao
from constantes import *

class TrabalhoProducaoDaoSqlite:
    def __init__(self, banco: MeuBanco):
        self.__meuBanco: MeuBanco= banco
        self.__logger: MeuLogger= MeuLogger(nome= 'trabalhoProducaoDao')
        self.__erro = None
    
    def pegaTodosTrabalhosProducao(self):
        try:
            trabalhosProducao: list[TrabalhoProducao]= []
            sql = """SELECT Lista_desejo.id, trabalhos.id, trabalhos.nome, trabalhos.nomeProducao, trabalhos.experiencia, trabalhos.nivel, trabalhos.profissao, trabalhos.raridade, trabalhos.trabalhoNecessario, Lista_desejo.recorrencia, Lista_desejo.tipoLicenca, Lista_desejo.estado FROM Lista_desejo INNER JOIN trabalhos ON Lista_desejo.idTrabalho == trabalhos.id;"""
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute(sql)
            for linha in cursor.fetchall():
                recorrencia = True if linha[9] == 1 else False
                trabalhoProducao = TrabalhoProducao()
                trabalhoProducao.id = linha[0]
                trabalhoProducao.idTrabalho = linha[1]
                trabalhoProducao.nome = linha[2]
                trabalhoProducao.nomeProducao = linha[3]
                trabalhoProducao.experiencia = linha[4]
                trabalhoProducao.nivel = linha[5]
                trabalhoProducao.profissao = linha[6]
                trabalhoProducao.raridade = linha[7]
                trabalhoProducao.trabalhoNecessario = linha[8]
                trabalhoProducao.recorrencia = recorrencia
                trabalhoProducao.tipoLicenca = linha[10]
                trabalhoProducao.estado = linha[11]
                trabalhosProducao.append(trabalhoProducao)
            return trabalhosProducao
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhosProducao(self, personagem: Personagem):
        try:
            trabalhosProducao: list[TrabalhoProducao]= []
            sql = """SELECT Lista_desejo.id, trabalhos.id, trabalhos.nome, trabalhos.nomeProducao, trabalhos.experiencia, trabalhos.nivel, trabalhos.profissao, trabalhos.raridade, trabalhos.trabalhoNecessario, Lista_desejo.recorrencia, Lista_desejo.tipoLicenca, Lista_desejo.estado FROM Lista_desejo INNER JOIN trabalhos ON Lista_desejo.idTrabalho == trabalhos.id WHERE idPersonagem == ?;"""
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute(sql, [personagem.id])
            for linha in cursor.fetchall():
                recorrencia = True if linha[9] == 1 else False
                trabalhoProducao = TrabalhoProducao()
                trabalhoProducao.id = linha[0]
                trabalhoProducao.idTrabalho = linha[1]
                trabalhoProducao.nome = linha[2]
                trabalhoProducao.nomeProducao = linha[3]
                trabalhoProducao.experiencia = linha[4]
                trabalhoProducao.nivel = linha[5]
                trabalhoProducao.profissao = linha[6]
                trabalhoProducao.raridade = linha[7]
                trabalhoProducao.trabalhoNecessario = linha[8]
                trabalhoProducao.recorrencia = recorrencia
                trabalhoProducao.tipoLicenca = linha[10]
                trabalhoProducao.estado = linha[11]
                trabalhosProducao.append(trabalhoProducao)
            trabalhosProducao = sorted(trabalhosProducao, key = lambda trabalhoProducao: (trabalhoProducao.estado, trabalhoProducao.profissao, trabalhoProducao.nivel, trabalhoProducao.nome))
            return trabalhosProducao
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def recupera_trabalhos_producao_para_produzir_produzindo(self, personagem: Personagem) -> list[TrabalhoProducao] | None:
        '''
            Recupera os trabalhos para produção com estado igual a produzir (0) ou produzindo (1) de um personagem específico do banco de dados.
            Args:
                personagem(Personagem): Personagem específico para verificação.
            Returns:
                trabalhos_producao | None (list[TrabalhoProducao]): Lista de trabalhos para produção encontrados. None caso erro encontrado.
        '''
        try:
            trabalhos_producao: list[TrabalhoProducao] = []
            sql = """SELECT Lista_desejo.id, trabalhos.id, trabalhos.nome, trabalhos.nomeProducao, trabalhos.experiencia, trabalhos.nivel, trabalhos.profissao, trabalhos.raridade, trabalhos.trabalhoNecessario, Lista_desejo.recorrencia, Lista_desejo.tipoLicenca, Lista_desejo.estado FROM Lista_desejo INNER JOIN trabalhos ON Lista_desejo.idTrabalho == trabalhos.id WHERE idPersonagem == ? AND (estado == 0 OR estado == 1);"""
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute(sql, [personagem.id])
            for linha in cursor.fetchall():
                recorrencia = True if linha[9] == 1 else False
                trabalho_producao: TrabalhoProducao= TrabalhoProducao()
                trabalho_producao.id = linha[0]
                trabalho_producao.idTrabalho = linha[1]
                trabalho_producao.nome = linha[2]
                trabalho_producao.nomeProducao = linha[3]
                trabalho_producao.experiencia = linha[4]
                trabalho_producao.nivel = linha[5]
                trabalho_producao.profissao = linha[6]
                trabalho_producao.raridade = linha[7]
                trabalho_producao.trabalhoNecessario = linha[8]
                trabalho_producao.recorrencia = recorrencia
                trabalho_producao.tipoLicenca = linha[10]
                trabalho_producao.estado = linha[11]
                trabalhos_producao.append(trabalho_producao)
            return trabalhos_producao
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def recuperaTrabalhosProducaoEstadoProduzindo(self, personagem: Personagem) -> list[TrabalhoProducao]:
        try:
            trabalhosProducao: list[TrabalhoProducao]= []
            sql = """SELECT Lista_desejo.id, trabalhos.id, trabalhos.nome, trabalhos.nomeProducao, trabalhos.experiencia, trabalhos.nivel, trabalhos.profissao, trabalhos.raridade, trabalhos.trabalhoNecessario, Lista_desejo.recorrencia, Lista_desejo.tipoLicenca, Lista_desejo.estado FROM Lista_desejo INNER JOIN trabalhos ON Lista_desejo.idTrabalho == trabalhos.id WHERE idPersonagem == ? AND estado == 1;"""
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute(sql, [personagem.id])
            for linha in cursor.fetchall():
                recorrencia = True if linha[9] == 1 else False
                trabalhoProducao: TrabalhoProducao= TrabalhoProducao()
                trabalhoProducao.id = linha[0]
                trabalhoProducao.idTrabalho = linha[1]
                trabalhoProducao.nome = linha[2]
                trabalhoProducao.nomeProducao = linha[3]
                trabalhoProducao.experiencia = linha[4]
                trabalhoProducao.nivel = linha[5]
                trabalhoProducao.profissao = linha[6]
                trabalhoProducao.raridade = linha[7]
                trabalhoProducao.trabalhoNecessario = linha[8]
                trabalhoProducao.recorrencia = recorrencia
                trabalhoProducao.tipoLicenca = linha[10]
                trabalhoProducao.estado = linha[11]
                trabalhosProducao.append(trabalhoProducao)
            return trabalhosProducao
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhosParaProduzirPorProfissaoRaridade(self, personagem: Personagem, trabalho: TrabalhoProducao) -> list[TrabalhoProducao]:
        try:
            trabalhosProducao: list[TrabalhoProducao]= []
            sql= f"""SELECT {CHAVE_LISTA_TRABALHOS_PRODUCAO}.{CHAVE_ID}, {CHAVE_TRABALHOS}.{CHAVE_ID}, {CHAVE_TRABALHOS}.{CHAVE_NIVEL}, {CHAVE_TRABALHOS}.{CHAVE_PROFISSAO} FROM {CHAVE_LISTA_TRABALHOS_PRODUCAO} INNER JOIN {CHAVE_TRABALHOS} ON {CHAVE_LISTA_TRABALHOS_PRODUCAO}.{CHAVE_ID_TRABALHO} == {CHAVE_TRABALHOS}.{CHAVE_ID} WHERE {CHAVE_ID_PERSONAGEM} == ? AND {CHAVE_ESTADO} == {CODIGO_PARA_PRODUZIR} AND {CHAVE_TRABALHOS}.{CHAVE_RARIDADE} == ? AND {CHAVE_TRABALHOS}.{CHAVE_PROFISSAO} == ?;"""
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute(sql, (personagem.id, trabalho.raridade, trabalho.profissao))
            for linha in cursor.fetchall():
                trabalhoProducao = TrabalhoProducao()
                trabalhoProducao.id = linha[0]
                trabalhoProducao.idTrabalho = linha[1]
                trabalhoProducao.nivel = linha[2]
                trabalhoProducao.profissao = linha[3]
                trabalhosProducao.append(trabalhoProducao)
            return trabalhosProducao
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def pegaQuantidadeTrabalhoProducaoProduzindo(self, personagem: Personagem, trabalhoId: str):
        try:
            sql = """SELECT COUNT(*) AS quantidade FROM Lista_desejo WHERE idPersonagem == ? AND idTrabalho == ? AND estado == 1;"""
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute(sql, (personagem.id, trabalhoId))
            linha = cursor.fetchone()
            quantidade = 0 if linha is None else linha[0]
            return quantidade
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def recupera_quantidade_trabalho_producao_produzir_produzindo(self, personagem: Personagem, id_trabalho: str):
        '''
            Recupera a quantidade de trabalhos para produção com estado igual a produzir (0) ou produzindo (1) de um personagem específico do banco de dados.
            Args:
                personagem(Personagem): Personagem específico para verificação.
                id_trabalho(str): ID do trabalho para produção.
            Returns:
                quantidade | None (int): Quantidade de trabalhos para produção encontrados. None caso erro encontrado.
        '''
        try:
            sql = """SELECT COUNT(*) AS quantidade FROM Lista_desejo WHERE idPersonagem == ? AND idTrabalho == ? AND (estado == 0 OR estado == 1);"""
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute(sql, (personagem.id, id_trabalho))
            linha = cursor.fetchone()
            quantidade: int = 0 if linha is None else linha[0]
            return quantidade
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhoProducaoPorId(self, id: str):
        try:
            trabalhoProducao: TrabalhoProducao= TrabalhoProducao()
            sql = """SELECT id, idTrabalho, recorrencia, tipoLicenca, estado FROM Lista_desejo WHERE id == ?;"""
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute(sql, [id])
            for linha in cursor.fetchall():
                recorrencia = True if linha[2] == 1 else False
                trabalhoProducao.id = linha[0]
                trabalhoProducao.idTrabalho = linha[1]
                trabalhoProducao.recorrencia = recorrencia
                trabalhoProducao.tipoLicenca = linha[3]
                trabalhoProducao.estado = linha[4]
            return trabalhoProducao
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhosProducaoPorIdTrabalho(self, personagem: Personagem, id: str) -> list[TrabalhoProducao] | None:
        try:
            trabalhosProducaoEncontrados: list[TrabalhoProducao]= []
            sql = f"""SELECT {CHAVE_ID}, {CHAVE_ID_TRABALHO}, {CHAVE_RECORRENCIA}, {CHAVE_TIPO_LICENCA}, {CHAVE_ESTADO} FROM {CHAVE_LISTA_TRABALHOS_PRODUCAO} WHERE {CHAVE_ID_TRABALHO} == ? AND {CHAVE_ID_PERSONAGEM} == ?;"""
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute(sql, (id, personagem.id))
            for linha in cursor.fetchall():
                trabalhoProducao = TrabalhoProducao()
                recorrencia = True if linha[2] == 1 else False
                trabalhoProducao.id = linha[0]
                trabalhoProducao.idTrabalho = linha[1]
                trabalhoProducao.recorrencia = recorrencia
                trabalhoProducao.tipoLicenca = linha[3]
                trabalhoProducao.estado = linha[4]
                trabalhosProducaoEncontrados.append(trabalhoProducao)
            return trabalhosProducaoEncontrados
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def insere_trabalho_producao(self, personagem: Personagem, trabalhoProducao: TrabalhoProducao, modificaServidor: bool= True) -> bool:
        try:
            recorrencia = 1 if trabalhoProducao.recorrencia else 0
            sql = f"""INSERT INTO {CHAVE_LISTA_TRABALHOS_PRODUCAO} ({CHAVE_ID}, {CHAVE_ID_TRABALHO}, {CHAVE_ID_PERSONAGEM}, {CHAVE_RECORRENCIA}, {CHAVE_TIPO_LICENCA}, {CHAVE_ESTADO}) VALUES (?, ?, ?, ?, ?, ?);"""
            repositorioTrabalhoProducao: RepositorioTrabalhoProducao= RepositorioTrabalhoProducao(personagem= personagem)
            self.__conexao = self.__meuBanco.pegaConexao()
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, (trabalhoProducao.id, trabalhoProducao.idTrabalho, personagem.id, recorrencia, trabalhoProducao.tipoLicenca, trabalhoProducao.estado))
            if modificaServidor:
                if repositorioTrabalhoProducao.insereTrabalhoProducao(trabalho= trabalhoProducao):
                    self.__logger.info(f'({personagem.id.ljust(36)} | {trabalhoProducao}) inserido no servidor com sucesso!')
                    self.__conexao.commit()
                    return True
                self.__logger.error(f'Erro ao inserir ({personagem.id.ljust(36)} | {trabalhoProducao}) no servidor: {repositorioTrabalhoProducao.pegaErro}')
                self.__conexao.rollback()
                self.__erro= repositorioTrabalhoProducao.pegaErro
                return False
            self.__conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__conexao.rollback()
        finally:
            self.__meuBanco.desconecta()
        return False
    
    def removeTrabalhoProducao(self, personagem: Personagem, trabalhoProducao: TrabalhoProducao, modificaServidor: bool= True) -> bool:
        try:
            sql = f"""DELETE FROM {CHAVE_LISTA_TRABALHOS_PRODUCAO} WHERE {CHAVE_ID} == ?;"""
            repositorioTrabalhoProducao: RepositorioTrabalhoProducao= RepositorioTrabalhoProducao(personagem= personagem)
            self.__conexao = self.__meuBanco.pegaConexao()
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, [trabalhoProducao.id])
            if modificaServidor:
                if repositorioTrabalhoProducao.removeTrabalhoProducao(trabalho= trabalhoProducao):
                    self.__logger.info(f'({personagem.id.ljust(36)} | {trabalhoProducao}) removido do servidor com sucesso!')
                    self.__conexao.commit()
                    return True
                self.__logger.error(f'Erro ao remover ({personagem.id.ljust(36)} | {trabalhoProducao}) do servidor: {repositorioTrabalhoProducao.pegaErro}')
                self.__erro= repositorioTrabalhoProducao.pegaErro
                self.__conexao.rollback()
                return False
            self.__conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__conexao.rollback()
        finally:
            self.__meuBanco.desconecta()
        return False
    
    def removeProducoesPorIdPersonagem(self, personagem: Personagem) -> bool:
        try:
            self.__conexao = self.__meuBanco.pegaConexao()
            sql = f"""DELETE FROM {CHAVE_LISTA_TRABALHOS_PRODUCAO} WHERE {CHAVE_ID_PERSONAGEM} == ?;"""
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, [personagem.id])
            self.__conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__conexao.rollback()
        finally:
            self.__meuBanco.desconecta()
        return False
        
    def modifica_trabalho_producao(self, personagem: Personagem, trabalho: TrabalhoProducao, modifica_servidor: bool= True):
        self.__conexao = self.__meuBanco.pegaConexao()
        if self.__conexao is None:
            return False
        try:
            sql: str= f"""UPDATE {CHAVE_LISTA_TRABALHOS_PRODUCAO} SET {CHAVE_ID_TRABALHO} = ?, {CHAVE_RECORRENCIA} = ?, {CHAVE_TIPO_LICENCA} = ?, {CHAVE_ESTADO} = ? WHERE {CHAVE_ID} == ?;"""
            repositorio_trabalho_producao: RepositorioTrabalhoProducao= RepositorioTrabalhoProducao(personagem= personagem)
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            recorrencia: int= 1 if trabalho.recorrencia else 0
            cursor.execute(sql, (trabalho.idTrabalho, recorrencia, trabalho.tipoLicenca, trabalho.estado, trabalho.id))
            if modifica_servidor:
                if repositorio_trabalho_producao.modifica_trabalho_producao(trabalho= trabalho):
                    self.__logger.info(f'({personagem.id.ljust(36)} | {trabalho}) modificado no servidor com sucesso!')
                    self.__conexao.commit()
                    return True
                self.__logger.error(f'Erro ao modificar ({personagem.id.ljust(36)} | {trabalho}) no servidor: {repositorio_trabalho_producao.pegaErro}')
                self.__erro= repositorio_trabalho_producao.pegaErro
                self.__conexao.rollback()
                return False
            self.__conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__conexao.rollback()
        finally:
            self.__meuBanco.desconecta()
        return False
    
    def sincronizaTrabalhosProducao(self, personagem: Personagem):
        '''
            Função para sincronizar os trabalhos para produção no servidor com o banco de dados local
            Returns:
                bool: Verdadeiro caso a sincronização seja concluída com sucesso
        '''
        try:
            self.__conexao = self.__meuBanco.pegaConexao()
            sql = f"""DELETE FROM {CHAVE_LISTA_TRABALHOS_PRODUCAO} WHERE {CHAVE_ID_PERSONAGEM} == ?;"""
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, [personagem.id])
            repositorioTrabalhoProducao: RepositorioTrabalhoProducao= RepositorioTrabalhoProducao(personagem= personagem)
            trabalhosServidor: list[TrabalhoProducao]= repositorioTrabalhoProducao.pegaTodosTrabalhosProducao()
            if trabalhosServidor is None:
                self.__logger.error(f'Erro ao buscar trabalhos para produção no servidor: {repositorioTrabalhoProducao.pegaErro}')
                raise Exception(repositorioTrabalhoProducao.pegaErro)
            for trabalho in trabalhosServidor:
                sql = f"""INSERT INTO {CHAVE_LISTA_TRABALHOS_PRODUCAO} ({CHAVE_ID}, {CHAVE_ID_TRABALHO}, {CHAVE_ID_PERSONAGEM}, {CHAVE_RECORRENCIA}, {CHAVE_TIPO_LICENCA}, {CHAVE_ESTADO}) VALUES (?, ?, ?, ?, ?, ?);"""
                try:
                    recorrencia: int= 1 if trabalho.recorrencia else 0
                    licenca: str= '' if trabalho.tipoLicenca is None else trabalho.tipoLicenca
                    cursor.execute(sql, (trabalho.id, trabalho.idTrabalho, personagem.id, recorrencia, licenca, trabalho.estado))
                except Exception as e:
                    self.__logger.error(f'Erro ao inserir ({trabalho}) no banco: {e}')
                    continue
            self.__conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__conexao.rollback()
        finally:
            self.__meuBanco.desconecta()
        return False
    
    @property
    def pegaErro(self):
        '''
            Atributo que retorna o último erro registrado.
        '''
        return self.__erro