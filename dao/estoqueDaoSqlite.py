__author__ = 'Kevin Amazonas'

from modelos.trabalhoEstoque import TrabalhoEstoque
from db.db import MeuBanco
from repositorio.repositorioEstoque import RepositorioEstoque

class EstoqueDaoSqlite:
    def __init__(self, personagem = None):
        self.__conexao = None
        self.__erro = None
        self.__personagem = personagem
        self.__repositorioEstoque = RepositorioEstoque(personagem)
        try:
            self.__meuBanco = MeuBanco()
            self.__conexao = self.__meuBanco.pegaConexao(1)
            self.__meuBanco.criaTabelas()
        except Exception as e:
            self.__erro = str(e)

    def pegaEstoque(self):
        estoque = []
        sql = """
            SELECT Lista_estoque.id, trabalhos.nome, trabalhos.profissao, trabalhos.nivel, Lista_estoque.quantidade, trabalhos.raridade, Lista_estoque.idTrabalho
            FROM Lista_estoque
            INNER JOIN trabalhos
            ON Lista_estoque.idTrabalho == trabalhos.id
            WHERE idPersonagem = ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [self.__personagem.pegaId()])
            for linha in cursor.fetchall():
                trabalhoEstoque = TrabalhoEstoque()
                trabalhoEstoque.setId(linha[0])
                trabalhoEstoque.setNome(linha[1])
                trabalhoEstoque.setProfissao(linha[2])
                trabalhoEstoque.setNivel(linha[3])
                trabalhoEstoque.setQuantidade(linha[4])
                trabalhoEstoque.setRaridade(linha[5])
                trabalhoEstoque.setIdTrabalho(linha[6])
                estoque.append(trabalhoEstoque)
            self.__meuBanco.desconecta()
            return estoque
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None

    def pegaTodosTrabalhosEstoque(self):
        estoque = []
        sql = """
            SELECT Lista_estoque.id, trabalhos.nome, trabalhos.profissao, trabalhos.nivel, Lista_estoque.quantidade, trabalhos.raridade, Lista_estoque.idTrabalho
            FROM Lista_estoque
            INNER JOIN trabalhos
            ON Lista_estoque.idTrabalho == trabalhos.id;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql)
            for linha in cursor.fetchall():
                trabalhoEstoque = TrabalhoEstoque()
                trabalhoEstoque.setId(linha[0])
                trabalhoEstoque.setNome(linha[1])
                trabalhoEstoque.setProfissao(linha[2])
                trabalhoEstoque.setNivel(linha[3])
                trabalhoEstoque.setQuantidade(linha[4])
                trabalhoEstoque.setRaridade(linha[5])
                trabalhoEstoque.setIdTrabalho(linha[6])
                estoque.append(trabalhoEstoque)
            self.__meuBanco.desconecta()
            return estoque
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def insereTrabalhoEstoque(self, trabalhoEstoque):
        sql = """
            INSERT INTO Lista_estoque (id, idPersonagem, idTrabalho, quantidade)
            VALUES (?,?,?,?)"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalhoEstoque.pegaId(), self.__personagem.pegaId(), trabalhoEstoque.pegaTrabalhoId(), trabalhoEstoque.pegaQuantidade()))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if self.__repositorioEstoque.insereTrabalhoEstoque(trabalhoEstoque):
                print(f'{trabalhoEstoque.pegaNome()} inserido com sucesso no servidor!')
            else:
                print(f'Erro ao inserir trabalho no estoque!')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False

    def modificaTrabalhoEstoque(self, trabalhoEstoque):
        sql = """
            UPDATE Lista_estoque 
            SET idTrabalho = ?, quantidade = ?
            WHERE id == ?"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalhoEstoque.pegaTrabalhoId(), trabalhoEstoque.pegaQuantidade(), trabalhoEstoque.pegaId()))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if self.__repositorioEstoque.modificaTrabalhoEstoque(trabalhoEstoque):
                print(f'{trabalhoEstoque.pegaNome()} modificado com sucesso no servidor!')
            else:
                print(f'Erro ao modificar estoque no servidor: {self.__repositorioEstoque.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False

    def modificaIdTrabalhoEstoque(self, idTrabalhoNovo, idTrabalhoAntigo):
        sql = """
            UPDATE Lista_estoque 
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

    def modificaIdPersonagemTrabalhoEstoque(self, idPersonagemNovo, idPersonagemAntigo):
        sql = """
            UPDATE Lista_estoque 
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
    
    def removeTrabalhoEstoque(self, trabalhoEstoque):
        sql = """
            DELETE FROM Lista_estoque
            WHERE id == ?;
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [trabalhoEstoque.pegaId()])
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if self.__repositorioEstoque.removeTrabalho(trabalhoEstoque):
                print(f'{trabalhoEstoque.pegaNome()} removido com sucesso do servidor!')
            else:
                print(f'Erro ao remover trabalho do estoque no servidor: {self.__repositorioEstoque.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False

    def pegaErro(self):
        return self.__erro