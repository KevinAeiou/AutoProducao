__author__ = 'Kevin Amazonas'

from modelos.trabalhoVendido import TrabalhoVendido
from modelos.personagem import Personagem
from db.db import MeuBanco
from repositorio.repositorioVendas import RepositorioVendas
from constantes import CHAVE_LISTA_VENDAS, CHAVE_TRABALHOS, CHAVE_ID, CHAVE_NOME, CHAVE_NIVEL, CHAVE_PROFISSAO, CHAVE_RARIDADE, CHAVE_TRABALHO_NECESSARIO, CHAVE_DESCRICAO, CHAVE_DATA_VENDA, CHAVE_QUANTIDADE, CHAVE_VALOR, CHAVE_ID_TRABALHO, CHAVE_ID_PERSONAGEM, CHAVE_RARIDADE_RARO
import logging

class VendaDaoSqlite:
    logging.basicConfig(level = logging.INFO, filename = 'logs/aplicacao.log', encoding='utf-8', format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt = '%d/%m/%Y %I:%M:%S %p')
    def __init__(self, personagem = None):
        self.__conexao = None
        self.__erro = None
        self.__personagem: Personagem = personagem
        self.__repositorioVendas = RepositorioVendas(personagem)
        self.__logger = logging.getLogger('vendaDao')
        try:
            self.__meuBanco = MeuBanco()
            self.__conexao = self.__meuBanco.pegaConexao(1)
            self.__meuBanco.criaTabelas()
        except Exception as e:
            self.__erro = str(e)

    def pegaTrabalhosVendidos(self) -> list[TrabalhoVendido] | None:
        vendas: list[TrabalhoVendido]= []
        sql = f"""
            SELECT {CHAVE_LISTA_VENDAS}.{CHAVE_ID}, {CHAVE_TRABALHOS}.{CHAVE_ID}, {CHAVE_TRABALHOS}.{CHAVE_NOME}, {CHAVE_TRABALHOS}.{CHAVE_NIVEL}, {CHAVE_TRABALHOS}.{CHAVE_PROFISSAO}, {CHAVE_TRABALHOS}.{CHAVE_RARIDADE}, {CHAVE_TRABALHOS}.{CHAVE_TRABALHO_NECESSARIO}, {CHAVE_LISTA_VENDAS}.{CHAVE_DESCRICAO}, {CHAVE_LISTA_VENDAS}.{CHAVE_DATA_VENDA}, {CHAVE_LISTA_VENDAS}.{CHAVE_QUANTIDADE}, {CHAVE_LISTA_VENDAS}.{CHAVE_VALOR}
            FROM {CHAVE_LISTA_VENDAS}
            INNER JOIN {CHAVE_TRABALHOS}
            ON {CHAVE_LISTA_VENDAS}.{CHAVE_ID_TRABALHO} == {CHAVE_TRABALHOS}.{CHAVE_ID}
            WHERE {CHAVE_ID_PERSONAGEM} == ?;
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [self.__personagem.id])
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
            self.__meuBanco.desconecta()
            return vendas
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None

    def pegaTrabalhoVendidoPorId(self, idBuscado: str) -> TrabalhoVendido | None:
        trabalho: TrabalhoVendido= TrabalhoVendido()
        sql = f"""
            SELECT * 
            FROM {CHAVE_LISTA_VENDAS} 
            WHERE {CHAVE_ID} == ?
            LIMIT 1;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [idBuscado])
            for linha in cursor.fetchall():
                trabalho.id = linha[0]
                trabalho.descricao = linha[1]
                trabalho.dataVenda = linha[2]
                trabalho.idPersonagem = linha[3]
                trabalho.quantidade = linha[4]
                trabalho.idTrabalho = linha[5]
                trabalho.valor = linha[6]
            self.__meuBanco.desconecta()
            return trabalho
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def pegaTrabalhosRarosVendidos(self):
        vendas = []
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
            ;
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [self.__personagem.id])
            for linha in cursor.fetchall():
                trabalhoVendido = TrabalhoVendido()
                trabalhoVendido.idTrabalho = linha[0]
                trabalhoVendido.nome = linha[1]
                trabalhoVendido.nivel = linha[2]
                trabalhoVendido.profissao = linha[3]
                trabalhoVendido.trabalhoNecessario = linha[4]
                trabalhoVendido.quantidade = linha[5]
                vendas.append(trabalhoVendido)
            self.__meuBanco.desconecta()
            vendas = sorted(vendas, key=lambda trabalhoVendido: (trabalhoVendido.quantidade, trabalhoVendido.nivel, trabalhoVendido.nome), reverse=True)
            return vendas
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def insereTrabalhoVendido(self, trabalho: TrabalhoVendido, modificaServidor: bool = True) -> bool:
        sql = f"""
            INSERT INTO {CHAVE_LISTA_VENDAS} ({CHAVE_ID}, {CHAVE_DESCRICAO}, {CHAVE_DATA_VENDA}, {CHAVE_ID_PERSONAGEM}, {CHAVE_QUANTIDADE}, {CHAVE_ID_TRABALHO}, {CHAVE_VALOR})
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, (trabalho.id, trabalho.descricao, trabalho.dataVenda, self.__personagem.id, trabalho.quantidade, trabalho.idTrabalho, trabalho.valor))
            if modificaServidor:
                if self.__repositorioVendas.insereTrabalhoVendido(trabalho= trabalho):
                    self.__logger.info(f'({trabalho}) inserido no servidor com sucesso!')
                    self.__conexao.commit()
                    self.__meuBanco.desconecta()
                    return True
                self.__logger.error(f'Erro ao inserir ({trabalho}) no servidor: {self.__repositorioVendas.pegaErro()}')
                self.__erro= self.__repositorioVendas.pegaErro()
                self.__conexao.rollback()
                self.__meuBanco.desconecta()
                return False
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__conexao.rollback()
        self.__meuBanco.desconecta()
        return False
    
    def removeTrabalhoVendido(self, trabalho: TrabalhoVendido, modificaServidor: bool = True) -> bool:
        sql = f"""
            DELETE FROM {CHAVE_LISTA_VENDAS}
            WHERE {CHAVE_ID} == ?;
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, [trabalho.id])
            if modificaServidor:
                if self.__repositorioVendas.removeTrabalhoVendido(trabalho= trabalho):
                    self.__logger.info(f'({trabalho}) removido do servidor com sucesso!')
                    self.__conexao.commit()
                    self.__meuBanco.desconecta()
                    return True
                self.__logger.error(f'Erro ao remover ({trabalho}) do servidor: {self.__repositorioVendas.pegaErro()}')
                self.__erro= self.__repositorioVendas.pegaErro()
                self.__conexao.rollback()
                self.__meuBanco.desconecta()
                return False
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__conexao.rollback()
        self.__meuBanco.desconecta()
        return False
    
    def modificaTrabalhoVendido(self, trabalho: TrabalhoVendido, modificaServidor: bool = True):
        trabalhoModificado = TrabalhoVendido()
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
        try:
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, (trabalhoModificado.descricao, trabalhoModificado.dataVenda, trabalhoModificado.quantidade, trabalhoModificado.idTrabalho, trabalhoModificado.valor, trabalhoModificado.id))
            if modificaServidor:
                if self.__repositorioVendas.modificaTrabalhoVendido(trabalho= trabalhoModificado):
                    self.__logger.info(f'({trabalhoModificado}) modificado no servidor com sucesso!')
                    self.__conexao.commit()
                    self.__meuBanco.desconecta()
                    return True
                self.__logger.error(f'Erro ao modificar ({trabalhoModificado}) no servidor: {self.__repositorioVendas.pegaErro()}')
                self.__erro= self.__repositorioVendas.pegaErro()
                self.__conexao.rollback()
                self.__meuBanco.desconecta()
                return False
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__conexao.rollback()
        self.__meuBanco.desconecta()
        return False
    
    def modificaIdTrabalhoVendido(self, idTrabalhoNovo, idTrabalhoAntigo):
        sql = f"""
            UPDATE {CHAVE_LISTA_VENDAS} 
            SET {CHAVE_ID_TRABALHO} = ?
            WHERE {CHAVE_ID_TRABALHO} == ?"""
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
    
    def modificaIdPersonagemTrabalhoVendido(self, idTrabalhoNovo, idTrabalhoAntigo):
        sql = f"""
            UPDATE {CHAVE_LISTA_VENDAS} 
            SET {CHAVE_ID_PERSONAGEM} = ?
            WHERE {CHAVE_ID_PERSONAGEM} == ?"""
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
    
        
    def pegaTodosTrabalhosVendidos(self):
        vendas = []
        sql = f"""
            SELECT * 
            FROM {CHAVE_LISTA_VENDAS}"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql)
            for linha in cursor.fetchall():
                trabalhoVendido = TrabalhoVendido()
                trabalhoVendido.id = linha[0]
                trabalhoVendido.descricao = linha[1]
                trabalhoVendido.dataVenda = linha[2]
                trabalhoVendido.idPersonagem = linha[3]
                trabalhoVendido.quantidade = linha[4]
                trabalhoVendido.idTrabalho = linha[5]
                trabalhoVendido.valor = linha[6]
                vendas.append(trabalhoVendido)
            return vendas
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
            
    def pegaErro(self):
        return self.__erro