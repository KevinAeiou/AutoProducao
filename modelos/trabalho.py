from uuid import uuid4
from constantes import CHAVE_RARIDADE_RARO

class Trabalho:
    def __init__(self):
        self.id = str(uuid4())
        self.nome = None
        self.nomeProducao = None
        self.experiencia : int = 0
        self.nivel : int = 0
        self.profissao = None
        self.raridade = None
        self.trabalhoNecessario = ''
    
    def setExperiencia(self, experiencia):
        self.experiencia = int(experiencia)

    def setNivel(self, nivel):
        self.nivel = int(nivel)

    def ehRaro(self):
        return self.raridade == CHAVE_RARIDADE_RARO
    
    def dicionarioParaObjeto(self, dicionario):
        if dicionario is None:
            return
        for chave in dicionario:
            setattr(self, chave, dicionario[chave])

    def __str__(self) -> str:
        return f'{(self.nome).ljust(44)} | {(self.profissao).ljust(22)} | {(self.raridade).ljust(9)} | {self.nivel}'