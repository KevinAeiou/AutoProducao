__author__ = 'Kevin Amazonas'

from modelos.trabalhoVendido import TrabalhoVendido
from modelos.personagem import Personagem
from db.db import MeuBanco
from repositorio.repositorioVendas import RepositorioVendas
from constantes import CHAVE_LISTA_VENDAS, CHAVE_TRABALHOS, CHAVE_ID, CHAVE_NOME, CHAVE_NIVEL, CHAVE_PROFISSAO, CHAVE_RARIDADE, CHAVE_TRABALHO_NECESSARIO, CHAVE_DESCRICAO, CHAVE_DATA_VENDA, CHAVE_QUANTIDADE, CHAVE_VALOR, CHAVE_ID_TRABALHO, CHAVE_ID_PERSONAGEM, CHAVE_RARIDADE_RARO
from modelos.logger import MeuLogger

class VendaDaoSqlite:
    def __init__(self, banco: MeuBanco):
        self.__logger: MeuLogger= MeuLogger(nome= 'vendaDao')
        self.__meuBanco = banco
        self.__erro = None

    def pegaTrabalhosVendidos(self, personagem: Personagem) -> list[TrabalhoVendido] | None:
        try:
            vendas: list[TrabalhoVendido]= []
            sql = f"""SELECT {CHAVE_LISTA_VENDAS}.{CHAVE_ID}, {CHAVE_TRABALHOS}.{CHAVE_ID}, {CHAVE_TRABALHOS}.{CHAVE_NOME}, {CHAVE_TRABALHOS}.{CHAVE_NIVEL}, {CHAVE_TRABALHOS}.{CHAVE_PROFISSAO}, {CHAVE_TRABALHOS}.{CHAVE_RARIDADE}, {CHAVE_TRABALHOS}.{CHAVE_TRABALHO_NECESSARIO}, {CHAVE_LISTA_VENDAS}.{CHAVE_DESCRICAO}, {CHAVE_LISTA_VENDAS}.{CHAVE_DATA_VENDA}, {CHAVE_LISTA_VENDAS}.{CHAVE_QUANTIDADE}, {CHAVE_LISTA_VENDAS}.{CHAVE_VALOR} FROM {CHAVE_LISTA_VENDAS} INNER JOIN {CHAVE_TRABALHOS} ON {CHAVE_LISTA_VENDAS}.{CHAVE_ID_TRABALHO} == {CHAVE_TRABALHOS}.{CHAVE_ID} WHERE {CHAVE_ID_PERSONAGEM} == ?;"""
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute(sql, [personagem.id])
            for linha in cursor.fetchall():
                trabalho: TrabalhoVendido= TrabalhoVendido()
                trabalho.id = linha[0]
                trabalho.idTrabalho = linha[1]
                trabalho.nome = linha[2]
                trabalho.nivel = linha[3]
                trabalho.profissao = linha[4]
                trabalho.raridade = linha[5]
                trabalho.trabalhoNecessario = linha[6]
                trabalho.descricao = linha[7]
                trabalho.dataVenda = linha[8]
                trabalho.quantidade = linha[9]
                trabalho.valor = linha[10]
                vendas.append(trabalho)
            vendas = sorted(vendas, key=lambda trabalho: trabalho.dataVenda)
            return vendas
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None

    def pegaTrabalhoVendidoPorId(self, idBuscado: str) -> TrabalhoVendido | None:
        try:
            trabalho: TrabalhoVendido= TrabalhoVendido()
            sql = f"""SELECT * FROM {CHAVE_LISTA_VENDAS} WHERE {CHAVE_ID} == ? LIMIT 1;"""
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute(sql, [idBuscado])
            for linha in cursor.fetchall():
                trabalho.id = linha[0]
                trabalho.descricao = linha[1]
                trabalho.dataVenda = linha[2]
                trabalho.idPersonagem = linha[3]
                trabalho.quantidade = linha[4]
                trabalho.idTrabalho = linha[5]
                trabalho.valor = linha[6]
            return trabalho
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhosRarosVendidos(self, personagem: Personagem):
        try:
            vendas: list[TrabalhoVendido]= []
            sql = f"""
                SELECT 
                    {CHAVE_ID_TRABALHO},  
                    (
                    SELECT {CHAVE_NOME}
                    FROM {CHAVE_TRABALHOS}
                    WHERE {CHAVE_TRABALHOS}.{CHAVE_ID} == {CHAVE_ID_TRABALHO}
                    AND {CHAVE_TRABALHOS}.{CHAVE_RARIDADE} == '{CHAVE_RARIDADE_RARO}'
                    )
                    AS {CHAVE_NOME},
                    (
                    SELECT {CHAVE_NIVEL}
                    FROM {CHAVE_TRABALHOS}
                    WHERE {CHAVE_TRABALHOS}.{CHAVE_ID} == {CHAVE_ID_TRABALHO}
                    AND {CHAVE_TRABALHOS}.{CHAVE_RARIDADE} == '{CHAVE_RARIDADE_RARO}'
                    )
                    AS {CHAVE_NIVEL},
                    (
                    SELECT {CHAVE_PROFISSAO}
                    FROM {CHAVE_TRABALHOS}
                    WHERE {CHAVE_TRABALHOS}.{CHAVE_ID} == {CHAVE_ID_TRABALHO}
                    AND {CHAVE_TRABALHOS}.{CHAVE_RARIDADE} == '{CHAVE_RARIDADE_RARO}'
                    )
                    AS {CHAVE_NIVEL},
                    (
                    SELECT {CHAVE_TRABALHO_NECESSARIO}
                    FROM {CHAVE_TRABALHOS}
                    WHERE {CHAVE_TRABALHOS}.{CHAVE_ID} == {CHAVE_ID_TRABALHO}
                    AND {CHAVE_TRABALHOS}.{CHAVE_RARIDADE} == '{CHAVE_RARIDADE_RARO}'
                    )
                    AS {CHAVE_TRABALHO_NECESSARIO},
                    COUNT(*) AS {CHAVE_QUANTIDADE}
                FROM {CHAVE_LISTA_VENDAS}
                WHERE {CHAVE_ID_PERSONAGEM} == ? 
                AND {CHAVE_NOME} NOT NULL
                GROUP BY {CHAVE_ID_TRABALHO}
                ORDER BY {CHAVE_QUANTIDADE}
                ;"""
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute(sql, [personagem.id])
            for linha in cursor.fetchall():
                trabalhoVendido: TrabalhoVendido= TrabalhoVendido()
                trabalhoVendido.idTrabalho = linha[0]
                trabalhoVendido.nome = linha[1]
                trabalhoVendido.nivel = linha[2]
                trabalhoVendido.profissao = linha[3]
                trabalhoVendido.trabalhoNecessario = linha[4]
                trabalhoVendido.quantidade = linha[5]
                vendas.append(trabalhoVendido)
            vendas = sorted(vendas, key=lambda trabalhoVendido: (trabalhoVendido.quantidade, trabalhoVendido.nivel, trabalhoVendido.nome), reverse=True)
            return vendas
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def insereTrabalhoVendido(self, personagem: Personagem, trabalho: TrabalhoVendido, modificaServidor: bool = True) -> bool:
        try:
            sql = f"""INSERT INTO {CHAVE_LISTA_VENDAS} ({CHAVE_ID}, {CHAVE_DESCRICAO}, {CHAVE_DATA_VENDA}, {CHAVE_ID_PERSONAGEM}, {CHAVE_QUANTIDADE}, {CHAVE_ID_TRABALHO}, {CHAVE_VALOR})VALUES (?, ?, ?, ?, ?, ?, ?);"""
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, (trabalho.id, trabalho.descricao, trabalho.dataVenda, personagem.id, trabalho.quantidade, trabalho.idTrabalho, trabalho.valor))
            if modificaServidor:
                repositorioVendas: RepositorioVendas= RepositorioVendas(personagem= personagem)
                if repositorioVendas.insereTrabalhoVendido(trabalho= trabalho):
                    self.__logger.info(f'({trabalho}) inserido no servidor com sucesso!')
                    conexao.commit()
                    return True
                self.__logger.error(f'Erro ao inserir ({trabalho}) no servidor: {repositorioVendas.pegaErro()}')
                self.__erro= repositorioVendas.pegaErro()
                conexao.rollback()
                return False
            conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            conexao.rollback()
        finally:
            self.__meuBanco.desconecta()
        return False
    
    def removeTrabalhoVendido(self, personagem: Personagem, trabalho: TrabalhoVendido, modificaServidor: bool = True) -> bool:
        try:
            sql = f"""DELETE FROM {CHAVE_LISTA_VENDAS} WHERE {CHAVE_ID} == ?;"""
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, [trabalho.id])
            if modificaServidor:
                repositorioVendas: RepositorioVendas= RepositorioVendas(personagem= personagem)
                if repositorioVendas.removeTrabalhoVendido(trabalho= trabalho):
                    self.__logger.info(f'({trabalho}) removido do servidor com sucesso!')
                    conexao.commit()
                    return True
                self.__logger.error(f'Erro ao remover ({trabalho}) do servidor: {repositorioVendas.pegaErro()}')
                self.__erro= repositorioVendas.pegaErro()
                conexao.rollback()
                return False
            conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            conexao.rollback()
        finally:
            self.__meuBanco.desconecta()
        return False
    
    def modificaTrabalhoVendido(self, personagem: Personagem, trabalho: TrabalhoVendido, modificaServidor: bool = True):
        try:
            trabalhoModificado: TrabalhoVendido= TrabalhoVendido()
            trabalhoModificado.id = trabalho.id
            trabalhoModificado.idTrabalho = trabalho.idTrabalho
            trabalhoModificado.descricao = trabalho.descricao
            trabalhoModificado.dataVenda = trabalho.dataVenda
            trabalhoModificado.setQuantidade(trabalho.quantidade)
            trabalhoModificado.setValor(trabalho.valor)
            sql = f"""
                UPDATE {CHAVE_LISTA_VENDAS}
                SET {CHAVE_DESCRICAO} = ?, {CHAVE_DATA_VENDA} = ?, {CHAVE_QUANTIDADE} = ?, {CHAVE_ID_TRABALHO} = ?, {CHAVE_VALOR} = ?
                WHERE {CHAVE_ID} == ?;"""
            conexao = self.__meuBanco.pegaConexao()
            cursor = conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, (trabalhoModificado.descricao, trabalhoModificado.dataVenda, trabalhoModificado.quantidade, trabalhoModificado.idTrabalho, trabalhoModificado.valor, trabalhoModificado.id))
            if modificaServidor:
                repositorioVendas: RepositorioVendas= RepositorioVendas(personagem= personagem)
                if repositorioVendas.modificaTrabalhoVendido(trabalho= trabalhoModificado):
                    self.__logger.info(f'({trabalhoModificado}) modificado no servidor com sucesso!')
                    conexao.commit()
                    return True
                self.__logger.error(f'Erro ao modificar ({trabalhoModificado}) no servidor: {repositorioVendas.pegaErro()}')
                self.__erro= repositorioVendas.pegaErro()
                conexao.rollback()
                return False
            conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            conexao.rollback()
        finally:
            self.__meuBanco.desconecta()
        return False
    
    def sincronizaTrabalhosVendidos(self, personagem: Personagem):
        '''
            Função para sincronizar os trabalhos vendidos no servidor com o banco de dados local
            Returns:
                bool: Verdadeiro caso a sincronização seja concluída com sucesso
        '''
        try:
            self.__conexao = self.__meuBanco.pegaConexao()
            sql = f"""DELETE FROM {CHAVE_LISTA_VENDAS} WHERE {CHAVE_ID_PERSONAGEM} == ?;"""
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, [personagem.id])
            repositorioTrabalhoVendidos: RepositorioVendas= RepositorioVendas(personagem= personagem)
            trabalhosServidor: list[TrabalhoVendido]= repositorioTrabalhoVendidos.pegaTrabalhosVendidos()
            if trabalhosServidor is None:
                self.__logger.error(f'Erro ao buscar trabalhos vendidos no servidor: {repositorioTrabalhoVendidos.pegaErro()}')
                raise Exception(repositorioTrabalhoVendidos.pegaErro())
            for trabalho in trabalhosServidor:
                sql = f"""INSERT INTO {CHAVE_LISTA_VENDAS} ({CHAVE_ID}, {CHAVE_DESCRICAO}, {CHAVE_DATA_VENDA}, {CHAVE_ID_PERSONAGEM}, {CHAVE_QUANTIDADE}, {CHAVE_ID_TRABALHO}, {CHAVE_VALOR})VALUES (?, ?, ?, ?, ?, ?, ?);"""
                try:
                    cursor.execute(sql, (trabalho.id, trabalho.descricao, trabalho.dataVenda, personagem.id, trabalho.quantidade, trabalho.idTrabalho, trabalho.valor))
                    self.__logger.info(menssagem= f'Trabalho para produção ({trabalho.nome}) inserido com sucesso!')
                except Exception as e:
                    raise e
            self.__conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__conexao.rollback()
        finally:
            self.__meuBanco.desconecta()
        return False
        
    def pegaErro(self):
        return self.__erro