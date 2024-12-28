from uuid import uuid4
from constantes import CHAVE_RARIDADE_RARO

class Trabalho:
    def __init__(self):
        self.id = str(uuid4())
        self.nome = None
        self.nomeProducao = None
        self.experiencia = None
        self.nivel = None
        self.profissao = None
        self.raridade = None
        self.trabalhoNecessario = None

    def pegaNivel(self, nivelProfissao):
        if nivelProfissao == 2 or nivelProfissao == 3:
            return 10
        if nivelProfissao == 4 or nivelProfissao == 5:
            return 12
        if nivelProfissao == 6 or nivelProfissao == 7:
            return 14
        if nivelProfissao == 8:
            return 8
        if nivelProfissao == 9 or nivelProfissao == 10:
            return 16
        if nivelProfissao == 11 or nivelProfissao == 12:
            return 18
        if nivelProfissao == 13 or nivelProfissao == 14:
            return 20
        if nivelProfissao == 15 or nivelProfissao == 16:
            return 22
        if nivelProfissao == 17 or nivelProfissao == 18:
            return 24
        if nivelProfissao == 19 or nivelProfissao == 20:
            return 26
        if nivelProfissao == 21 or nivelProfissao == 22:
            return 28
        if nivelProfissao == 23 or nivelProfissao == 24:
            return 30
        if nivelProfissao == 25 or nivelProfissao == 26:
            return 32
        return 1

    def ehRaro(self):
        return self.raridade == CHAVE_RARIDADE_RARO
    
    def dicionarioParaObjeto(self, dicionario):
        if dicionario is None:
            return
        for chave in dicionario:
            setattr(self, chave, dicionario[chave])

    def __str__(self) -> str:
        nome = 'Indefinido' if self.nome == None else self.nome
        profissao = 'Indefinido' if self.profissao == None else self.profissao
        raridade = 'Indefinido' if self.raridade == None else self.raridade
        nivel = 'Indefinido' if self.nivel == None else str(self.nivel)
        return f'{nome.ljust(44)} | {profissao.ljust(22)} | {raridade.ljust(9)} | {nivel}'