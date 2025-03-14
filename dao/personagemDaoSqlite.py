__author__ = 'Kevin Amazonas'

from modelos.personagem import Personagem
from modelos.logger import MeuLogger
from db.db import MeuBanco
from repositorio.repositorioPersonagem import RepositorioPersonagem
from constantes import CHAVE_ID, CHAVE_NOME, CHAVE_EMAIL, CHAVE_SENHA, CHAVE_AUTO_PRODUCAO, CHAVE_ESPACO_PRODUCAO, CHAVE_ESTADO, CHAVE_USO, CHAVE_PERSONAGENS, CHAVE_LISTA_ESTOQUE, CHAVE_ID_PERSONAGEM, CHAVE_PROFISSOES, CHAVE_LISTA_TRABALHOS_PRODUCAO, CHAVE_LISTA_VENDAS

class PersonagemDaoSqlite():
    def __init__(self, banco: MeuBanco):
        self.__meuBanco: MeuBanco= banco
        self.__conexao = None
        self.__erro = None
        self.__fabrica = None
        self.__logger: MeuLogger= MeuLogger(nome= 'personagemDao')
        self.__logger.debug(menssagem= f'Inicializando PersonagemDaoSqlite')
        try:
            self.__repositorioPersonagem = RepositorioPersonagem()
        except Exception as e:
            self.__erro= str(e)

    def pegaPersonagens(self) -> list[Personagem]:
        try:
            self.__conexao = self.__meuBanco.pegaConexao()
            self.__fabrica = self.__meuBanco.pegaFabrica()
            personagens: list[Personagem]= []
            sql = f"""SELECT * FROM {CHAVE_PERSONAGENS.lower()};"""
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql)
                for linha in cursor.fetchall():
                    estado = True if linha[5] else False
                    uso = True if linha[6] else False
                    autoProducao = True if linha[7] else False
                    personagem = Personagem()
                    personagem.id = linha[0]
                    personagem.nome = linha[1]
                    personagem.email = linha[2]
                    personagem.senha = linha[3]
                    personagem.espacoProducao = linha[4]
                    personagem.estado = estado
                    personagem.uso = uso
                    personagem.autoProducao = autoProducao
                    personagens.append(personagem)
                personagens = sorted(personagens,  key= lambda personagem: personagem.email)
                return personagens
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def pegaPersonagemPorId(self, id : str) -> Personagem:
        try:
            self.__conexao = self.__meuBanco.pegaConexao()
            self.__fabrica = self.__meuBanco.pegaFabrica()
            sql = f"""SELECT * FROM {CHAVE_PERSONAGENS.lower()} WHERE {CHAVE_ID} == ?;"""
            personagemEncontrado: Personagem= Personagem()
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql, [id])
                for linha in cursor.fetchall():
                    estado = True if linha[5] else False
                    uso = True if linha[6] else False
                    autoProducao = True if linha[7] else False
                    personagemEncontrado.id = linha[0]
                    personagemEncontrado.nome = linha[1]
                    personagemEncontrado.email = linha[2]
                    personagemEncontrado.senha = linha[3]
                    personagemEncontrado.espacoProducao = linha[4]
                    personagemEncontrado.estado = estado
                    personagemEncontrado.uso = uso
                    personagemEncontrado.autoProducao = autoProducao
                return personagemEncontrado            
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def modificaPersonagem(self, personagem: Personagem, modificaServidor: bool= True) -> bool:
        try:
            self.__conexao = self.__meuBanco.pegaConexao()
            self.__fabrica = self.__meuBanco.pegaFabrica()
            estado: int = 1 if personagem.estado else 0
            uso: int= 1 if personagem.uso else 0
            autoProducao: int= 1 if personagem.autoProducao else 0
            sql = f"""UPDATE {CHAVE_PERSONAGENS.lower()} SET {CHAVE_ID} = ?, {CHAVE_NOME} = ?, {CHAVE_EMAIL} = ?, {CHAVE_SENHA} = ?, {CHAVE_ESPACO_PRODUCAO} = ?, {CHAVE_ESTADO} = ?, {CHAVE_USO} = ?, {CHAVE_AUTO_PRODUCAO} = ? WHERE {CHAVE_ID} == ?"""
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute('BEGIN')
                cursor.execute(sql, (personagem.id, personagem.nome, personagem.email, personagem.senha, personagem.espacoProducao, estado, uso, autoProducao, personagem.id))
            if modificaServidor:
                if self.__repositorioPersonagem.modificaPersonagem(personagem= personagem):
                    self.__logger.info(f'({personagem}) modificado no servidor com sucesso!')
                    self.__conexao.commit()
                    return True
                self.__logger.error(f'Erro ao modificar ({personagem}) no servidor: {self.__repositorioPersonagem.pegaErro()}')
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
    
    def inserePersonagem(self, personagem: Personagem, modificaServidor: bool = True) -> bool:
        try:
            self.__conexao = self.__meuBanco.pegaConexao()
            self.__fabrica = self.__meuBanco.pegaFabrica()
            estado: int = 1 if personagem.estado else 0
            uso: int = 1 if personagem.uso else 0
            autoProducao: int = 1 if personagem.autoProducao else 0
            sql = f"""INSERT INTO {CHAVE_PERSONAGENS.lower()} ({CHAVE_ID}, {CHAVE_NOME}, {CHAVE_EMAIL}, {CHAVE_SENHA}, {CHAVE_ESPACO_PRODUCAO}, {CHAVE_ESTADO}, {CHAVE_USO}, {CHAVE_AUTO_PRODUCAO}) VALUES (?,?,?,?,?,?,?,?)"""
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, (personagem.id, personagem.nome, personagem.email, personagem.senha, personagem.espacoProducao, estado, uso, autoProducao))
            if modificaServidor:
                if self.__repositorioPersonagem.inserePersonagem(personagem= personagem):
                    self.__logger.info(f'({personagem}) inserido com sucesso no servidor!')
                    self.__conexao.commit()
                    return True
                self.__erro= self.__repositorioPersonagem.pegaErro()
                self.__logger.error(f'Erro ao inserir ({personagem}) no servidor: {self.__repositorioPersonagem.pegaErro()}')
                self.__conexao.rollback()
                return False
            self.__conexao.commit()
            return True
        except Exception as e:
            self.__conexao.rollback()
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return False
    
    def removePersonagem(self, personagem: Personagem, modificaServidor: bool = True) -> bool:
        try:
            self.__conexao = self.__meuBanco.pegaConexao()
            sqlRemovePersonagem = f"""DELETE FROM {CHAVE_PERSONAGENS.lower()} WHERE {CHAVE_ID} == ?;"""
            sqlRemoveEstoque= f"""DELETE FROM {CHAVE_LISTA_ESTOQUE} WHERE {CHAVE_ID_PERSONAGEM} == ?;"""
            sqlRemoveProfissoes= f"""DELETE FROM {CHAVE_PROFISSOES.lower()} WHERE {CHAVE_ID_PERSONAGEM} == ?;"""
            sqlRemoveProducao= f"""DELETE FROM {CHAVE_LISTA_TRABALHOS_PRODUCAO} WHERE {CHAVE_ID_PERSONAGEM} == ?;"""
            sqlRemoveVendas=f"""DELETE FROM {CHAVE_LISTA_VENDAS} WHERE {CHAVE_ID_PERSONAGEM} == ?;"""
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sqlRemovePersonagem, [personagem.id])
            cursor.execute(sqlRemoveEstoque, [personagem.id])
            cursor.execute(sqlRemoveProducao, [personagem.id])
            cursor.execute(sqlRemoveProfissoes, [personagem.id])
            cursor.execute(sqlRemoveVendas, [personagem.id])
            if modificaServidor:
                if self.__repositorioPersonagem.removePersonagem(personagem= personagem):
                    self.__logger.info(f'({personagem}) removido do servidor com sucesso!')
                    self.__conexao.commit()
                    return True
                self.__conexao.rollback()
                self.__logger.error(f'Erro ao remover ({personagem}) do servidor: {self.__repositorioPersonagem.pegaErro()}')
                self.__erro = self.__repositorioPersonagem.pegaErro()
                return False
            self.__conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__conexao.rollback()
        finally:
            self.__meuBanco.desconecta()
        return False
    
    def sinconizaPersonagens(self) -> bool:
        '''
            Função para sincronizar personagens no servidor com o banco de dados local
            Returns:
                bool: Verdadeiro caso a sincronização seja concluída com sucesso
        '''
        try:
            personagensBanco: list[Personagem]= self.pegaPersonagens()
            if personagensBanco is None:
                return False
            self.__conexao = self.__meuBanco.pegaConexao()
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            for persoangemBanco in personagensBanco:
                sqlRemovePersonagem = f"""
                    DELETE FROM {CHAVE_PERSONAGENS.lower()}
                    WHERE {CHAVE_ID} == ?;"""
                sqlRemoveEstoque= f"""
                    DELETE FROM {CHAVE_LISTA_ESTOQUE}
                    WHERE {CHAVE_ID_PERSONAGEM} == ?;"""
                sqlRemoveProfissoes= f"""
                    DELETE FROM {CHAVE_PROFISSOES.lower()}
                    WHERE {CHAVE_ID_PERSONAGEM} == ?;"""
                sqlRemoveProducao= f"""
                    DELETE FROM {CHAVE_LISTA_TRABALHOS_PRODUCAO}
                    WHERE {CHAVE_ID_PERSONAGEM} == ?;"""
                sqlRemoveVendas=f"""
                    DELETE FROM {CHAVE_LISTA_VENDAS}
                    WHERE {CHAVE_ID_PERSONAGEM} == ?;
                    """
                try:
                    cursor.execute(sqlRemovePersonagem, [persoangemBanco.id])
                    cursor.execute(sqlRemoveEstoque, [persoangemBanco.id])
                    cursor.execute(sqlRemoveProducao, [persoangemBanco.id])
                    cursor.execute(sqlRemoveProfissoes, [persoangemBanco.id])
                    cursor.execute(sqlRemoveVendas, [persoangemBanco.id])
                    continue
                except Exception as e:
                    raise e
            repositorioPersonagem: RepositorioPersonagem= RepositorioPersonagem()
            personagensServidor: list[Personagem]= repositorioPersonagem.pegaTodosPersonagens()
            if personagensServidor is None:
                raise Exception(repositorioPersonagem.pegaErro())
            for personagemServidor in personagensServidor:
                estado: int = 1 if personagemServidor.estado else 0
                uso: int = 1 if personagemServidor.uso else 0
                autoProducao: int = 1 if personagemServidor.autoProducao else 0
                sql = f"""
                    INSERT INTO {CHAVE_PERSONAGENS.lower()} ({CHAVE_ID}, {CHAVE_NOME}, {CHAVE_EMAIL}, {CHAVE_SENHA}, {CHAVE_ESPACO_PRODUCAO}, {CHAVE_ESTADO}, {CHAVE_USO}, {CHAVE_AUTO_PRODUCAO})
                    VALUES (?,?,?,?,?,?,?,?);
                    """
                try:
                    cursor.execute(sql, (personagemServidor.id, personagemServidor.nome, personagemServidor.email, personagemServidor.senha, personagemServidor.espacoProducao, estado, uso, autoProducao))
                    self.__logger.info(menssagem= f'Personagem ({personagemServidor.nome}) inserido no banco com sucesso!')
                except Exception as e:
                    raise e
            self.__conexao.commit()
            return True
        except Exception as e:
            self.__erro= str(e)
            self.__conexao.rollback()
        finally:
            self.__meuBanco.desconecta()
        return False
    
    def pegaErro(self):
        return self.__erro