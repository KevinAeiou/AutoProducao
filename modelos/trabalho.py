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
        nome = 'Indefinido' if self.nome == None else self.nome
        profissao = 'Indefinido' if self.profissao == None else self.profissao
        raridade = 'Indefinido' if self.raridade == None else self.raridade
        nivel = 'Indefinido' if self.nivel == None else str(self.nivel)
        return f'{nome.ljust(44)} | {profissao.ljust(22)} | {raridade.ljust(9)} | {nivel}'