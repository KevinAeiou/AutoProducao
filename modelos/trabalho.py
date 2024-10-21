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

    def pegaId(self):
        return self.id
    
    def setId(self, id):
        self.id = id
    
    def pegaNome(self):
        return self.nome
    
    def setNome(self, nome):
        self.nome = nome
    
    def pegaNomeProducao(self):
        return self.nomeProducao
    
    def setNomeProducao(self, nomeProducao):
        self.nomeProducao = nomeProducao
    
    def pegaExperiencia(self):
        return self.experiencia
    
    def setExperiencia(self, experiencia):
        self.experiencia = int(experiencia)

    
    def pegaNivel(self):
        return self.nivel
    
    def setNivel(self, nivel):
        self.nivel = int(nivel)
    
    def pegaProfissao(self):
        return self.profissao

    def setProfissao(self, profissao):
        self.profissao = profissao

    def pegaRaridade(self):
        return self.raridade
    
    def setRaridade(self, raridade):
        self.raridade = raridade
    
    def pegaTrabalhoNecessario(self):
        return self.trabalhoNecessario
    
    def setTrabalhoNecessario(self, trabalhoNecessario):
        self.trabalhoNecessario = trabalhoNecessario

    def ehRaro(self):
        return self.raridade == CHAVE_RARIDADE_RARO
    
    def dicionarioParaObjeto(self, dicionario):
        if dicionario is None:
            return
        for chave in dicionario:
            setattr(self, chave, dicionario[chave])

    def __str__(self) -> str:
        return f'{(self.nome).ljust(44)} | {(self.profissao).ljust(22)} | {(self.raridade).ljust(9)} | {self.nivel}'