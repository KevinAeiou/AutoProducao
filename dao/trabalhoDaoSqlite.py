__author__ = 'Kevin Amazonas'

from modelos.trabalho import Trabalho
from db.db import MeuBanco
from repositorio.repositorioTrabalho import RepositorioTrabalho
from modelos.logger import MeuLogger
from constantes import CHAVE_ID, CHAVE_PROFISSAO, CHAVE_NIVEL, CHAVE_TRABALHOS, CHAVE_RARIDADE, CHAVE_NOME, CHAVE_NOME_PRODUCAO, CHAVE_EXPERIENCIA, CHAVE_TRABALHO_NECESSARIO

class TrabalhoDaoSqlite:
    def __init__(self, banco: MeuBanco):
        self.__meuBanco: MeuBanco= banco
        self.__conexao = None
        self.__erro = None
        self.__fabrica = None
        self.__logger: MeuLogger= MeuLogger(nome= 'trabalhoDao')
        try:
            self.__repositorioTrabalho = RepositorioTrabalho()
        except Exception as e:
            self.__erro = str(e)

    def pegaTrabalhos(self) -> list[Trabalho]:
        '''
            Método para recuperar uma lista de objetos da classe Trabalho no banco de dados local.
            Returns:
                trabalhos (list[Trabalho]): Lista de objetos da classe Trabalho recuperados no banco de dados.    
        '''
        try:
            trabalhos: list[Trabalho]= []
            sql = f"""SELECT * FROM {CHAVE_TRABALHOS};"""
            self.__conexao = self.__meuBanco.pegaConexao()
            self.__fabrica = self.__meuBanco.pegaFabrica()
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql)
                for linha in cursor.fetchall():
                    trabalho: Trabalho= Trabalho()
                    trabalho.id = linha[0]
                    trabalho.nome = linha[1]
                    trabalho.nomeProducao = linha[2]
                    trabalho.experiencia = linha[3]
                    trabalho.nivel = linha[4]
                    trabalho.profissao = linha[5]
                    trabalho.raridade = linha[6]
                    trabalho.trabalhoNecessario = linha[7]
                    if trabalho.profissao is None:
                        trabalho.profissao= ''
                    trabalhos.append(trabalho)
                trabalhos = sorted(trabalhos, key= lambda trabalho: (trabalho.profissao, trabalho.raridade, trabalho.nivel))
                return trabalhos            
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhosPorProfissaoRaridadeNivel(self, trabalhoBuscado: Trabalho) -> list[Trabalho] | None:
        try:
            trabalhos: list[Trabalho] = []
            sql = f"""SELECT * FROM {CHAVE_TRABALHOS} WHERE {CHAVE_PROFISSAO} = ? AND {CHAVE_RARIDADE} == ? AND {CHAVE_NIVEL} == ?;"""
            self.__conexao = self.__meuBanco.pegaConexao()
            self.__fabrica = self.__meuBanco.pegaFabrica()
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql, (trabalhoBuscado.profissao, trabalhoBuscado.raridade, str(trabalhoBuscado.nivel)))
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
                trabalhos = sorted(trabalhos, key= lambda trabalho: trabalho.nome)
                return trabalhos            
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhosPorProfissaoRaridade(self, trabalhoBuscado: Trabalho):
        try:
            trabalhos: list[Trabalho]= []
            sql = """
                SELECT * 
                FROM trabalhos
                WHERE profissao = ? 
                AND raridade == ?;
                """
            self.__conexao = self.__meuBanco.pegaConexao()
            self.__fabrica = self.__meuBanco.pegaFabrica()
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql, (trabalhoBuscado.profissao, trabalhoBuscado.raridade))
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
                trabalhos = sorted(trabalhos, key= lambda trabalho: (trabalho.nivel, trabalho.nome))
                return trabalhos            
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None

    def pegaTrabalhoPorId(self, idBuscado: str) -> Trabalho | None:
        trabalho: Trabalho= Trabalho()
        sql = f"""SELECT * FROM {CHAVE_TRABALHOS} WHERE {CHAVE_ID} == ?;"""
        try:
            self.__conexao = self.__meuBanco.pegaConexao()
            self.__fabrica = self.__meuBanco.pegaFabrica()
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql, [idBuscado])
                for linha in cursor.fetchall():
                    trabalho.id = linha[0]
                    trabalho.nome = linha[1]
                    trabalho.nomeProducao = linha[2]
                    trabalho.experiencia = linha[3]
                    trabalho.nivel = linha[4]
                    trabalho.profissao = linha[5]
                    trabalho.raridade = linha[6]
                    trabalho.trabalhoNecessario = linha[7]
                return trabalho            
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def retornaListaIdsRecursosNecessarios(self, trabalho: Trabalho) -> list[str] | None:
        try:
            idsTrabalhos: list[str]= []
            sql = f"""SELECT {CHAVE_ID} FROM {CHAVE_TRABALHOS} WHERE {CHAVE_PROFISSAO} == ? AND {CHAVE_NIVEL} == ?;"""
            self.__conexao = self.__meuBanco.pegaConexao()
            self.__fabrica = self.__meuBanco.pegaFabrica()
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql, (trabalho.profissao, trabalho.nivel))
                for linha in cursor.fetchall():
                    idsTrabalhos.append(linha[0])
                return idsTrabalhos            
        except Exception as e:
            self.__erro= str(e)
        finally:
            self.__meuBanco.desconecta()
        return None

    def pegaTrabalhoPorNomeProfissaoRaridade(self, trabalhoBuscado: Trabalho):
        try:
            trabalho: Trabalho= Trabalho()
            sql= f"""SELECT * FROM {CHAVE_TRABALHOS} WHERE {CHAVE_NOME} == ? AND {CHAVE_PROFISSAO} = ? AND {CHAVE_RARIDADE} == ?;"""
            self.__conexao = self.__meuBanco.pegaConexao()
            self.__fabrica = self.__meuBanco.pegaFabrica()
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql, (trabalhoBuscado.nome, trabalhoBuscado.profissao, trabalhoBuscado.raridade))
                for linha in cursor.fetchall():
                    trabalho.id = linha[0]
                    trabalho.nome = linha[1]
                    trabalho.nomeProducao = linha[2]
                    trabalho.experiencia = linha[3]
                    trabalho.nivel = linha[4]
                    trabalho.profissao = linha[5]
                    trabalho.raridade = linha[6]
                    trabalho.trabalhoNecessario = linha[7]
                return trabalho            
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None

    def pegaTrabalhoPorNome(self, nomeTrabalho : str) -> Trabalho | None:
        try:
            trabalho: Trabalho= Trabalho()
            sql= f"""SELECT * FROM {CHAVE_TRABALHOS} WHERE {CHAVE_NOME} == ? LIMIT 1;"""
            self.__conexao = self.__meuBanco.pegaConexao()
            self.__fabrica = self.__meuBanco.pegaFabrica()
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql, [nomeTrabalho])
                for linha in cursor.fetchall():
                    trabalho.id = linha[0]
                    trabalho.nome = linha[1]
                    trabalho.nomeProducao = linha[2]
                    trabalho.experiencia = linha[3]
                    trabalho.nivel = linha[4]
                    trabalho.profissao = linha[5]
                    trabalho.raridade = linha[6]
                    trabalho.trabalhoNecessario = linha[7]
                return trabalho            
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def insereTrabalho(self, trabalho: Trabalho, modificaServidor: bool= True) -> bool:
        try:
            sql= f"""INSERT INTO {CHAVE_TRABALHOS} ({CHAVE_ID}, {CHAVE_NOME}, {CHAVE_NOME_PRODUCAO}, {CHAVE_EXPERIENCIA}, {CHAVE_NIVEL}, {CHAVE_PROFISSAO}, {CHAVE_RARIDADE}, {CHAVE_TRABALHO_NECESSARIO}) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
            self.__conexao = self.__meuBanco.pegaConexao()
            self.__fabrica = self.__meuBanco.pegaFabrica()
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, (trabalho.id, trabalho.nome, trabalho.nomeProducao, trabalho.experiencia, trabalho.nivel, trabalho.profissao, trabalho.raridade, trabalho.trabalhoNecessario))
            if modificaServidor:
                if self.__repositorioTrabalho.insereTrabalho(trabalho):
                    self.__logger.info(f'({trabalho.id.ljust(36)} | {trabalho}) inserido no servidor com sucesso!')
                    self.__conexao.commit()
                    return True
                self.__logger.error(f'Erro ao inserir ({trabalho.id.ljust(36)} | {trabalho}) no servidor: {self.__repositorioTrabalho.pegaErro}')
                self.__erro= self.__repositorioTrabalho.pegaErro
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

    def modificaTrabalho(self, trabalho : Trabalho, modificaServidor: bool= True) -> bool:
        try:
            sql= f"""UPDATE {CHAVE_TRABALHOS} SET {CHAVE_NOME} = ?, {CHAVE_NOME_PRODUCAO} = ?, {CHAVE_EXPERIENCIA} = ?, {CHAVE_NIVEL} = ?, {CHAVE_PROFISSAO} = ?, {CHAVE_RARIDADE} = ?, {CHAVE_TRABALHO_NECESSARIO} = ? WHERE {CHAVE_ID} = ?;"""
            self.__conexao= self.__meuBanco.pegaConexao()
            self.__fabrica= self.__meuBanco.pegaFabrica()
            cursor= self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, (trabalho.nome, trabalho.nomeProducao, trabalho.experiencia, trabalho.nivel, trabalho.profissao, trabalho.raridade, trabalho.trabalhoNecessario, trabalho.id))
            if modificaServidor:
                if self.__repositorioTrabalho.modificaTrabalho(trabalho):
                    self.__logger.info(f'({trabalho.id.ljust(36)} | {trabalho}) modificado no servidor com sucesso!')
                    self.__conexao.commit()
                    return True
                self.__logger.error(f'Erro ao modificar ({trabalho.id.ljust(36)} | {trabalho}) no servidor: {self.__repositorioTrabalho.pegaErro}')
                self.__erro= self.__repositorioTrabalho.pegaErro
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
        
    def removeTrabalho(self, trabalho: Trabalho, modificaServidor: bool= True) -> bool:
        try:
            sql= f"""DELETE FROM {CHAVE_TRABALHOS} WHERE {CHAVE_ID} == ?;"""
            self.__conexao = self.__meuBanco.pegaConexao()
            self.__fabrica = self.__meuBanco.pegaFabrica()
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, [trabalho.id])
            if modificaServidor:
                if self.__repositorioTrabalho.removeTrabalho(trabalho= trabalho):
                    self.__logger.info(f'({trabalho.id.ljust(36)} | {trabalho}) removido do servidor com sucesso!')
                    self.__conexao.commit()
                    return True
                self.__logger.error(f'Erro ao remover ({trabalho.id.ljust(36)} | {trabalho}) do servidor: {self.__repositorioTrabalho.pegaErro}')
                self.__erro= self.__repositorioTrabalho.pegaErro
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
    
    def sincronizaTrabalhos(self) -> bool:
        '''
            Função para sincronizar os trabalhos no servidor com o banco de dados local
            Returns:
                bool: Verdadeiro caso a sincronização seja concluída com sucesso
        '''
        try:
            self.__conexao = self.__meuBanco.pegaConexao()
            sql = f"""DELETE FROM {CHAVE_TRABALHOS};"""
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql)
            repositorioTrabalho: RepositorioTrabalho= RepositorioTrabalho()
            trabalhosServidor: list[Trabalho]= repositorioTrabalho.pegaTodosTrabalhos()
            if trabalhosServidor is None:
                self.__logger.error(f'Erro ao buscar trabalhos no servidor: {repositorioTrabalho.pegaErro}')
                raise Exception(repositorioTrabalho.pegaErro)
            for trabalho in trabalhosServidor:
                sql= f"""INSERT INTO {CHAVE_TRABALHOS} ({CHAVE_ID}, {CHAVE_NOME}, {CHAVE_NOME_PRODUCAO}, {CHAVE_EXPERIENCIA}, {CHAVE_NIVEL}, {CHAVE_PROFISSAO}, {CHAVE_RARIDADE}, {CHAVE_TRABALHO_NECESSARIO}) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
                try:
                    cursor.execute(sql, (trabalho.id, trabalho.nome, trabalho.nomeProducao, trabalho.experiencia, trabalho.nivel, trabalho.profissao, trabalho.raridade, trabalho.trabalhoNecessario))
                except Exception as e:
                    self.__logger.error(f'Erro ao inserir trabalho no banco ({trabalho.id}, {trabalho.nome}, {trabalho.nomeProducao}, {trabalho.experiencia}, {trabalho.nivel}, {trabalho.profissao}, {trabalho.raridade}, {trabalho.trabalhoNecessario}): {repositorioTrabalho.pegaErro}')
                    raise e
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