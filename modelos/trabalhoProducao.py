from constantes import CODIGO_PARA_PRODUZIR, CODIGO_PRODUZINDO, CODIGO_CONCLUIDO, CHAVE_RARIDADE_COMUM, CHAVE_RARIDADE_MELHORADO, CHAVE_RARIDADE_RARO, CHAVE_RARIDADE_ESPECIAL
from uuid import uuid4

class TrabalhoProducao:
    def __init__(self):
        self.id = str(uuid4())
        self.trabalhoId = None
        self.nome = None
        self.nomeProducao = None
        self.experiencia = 0
        self.nivel = 0
        self.profissao = None
        self.raridade = None
        self.trabalhoNecessario = ''
        self.recorrencia = None
        self.tipo_licenca = None
        self.estado = None
    
    @property
    def pegaExperiencia(self):
        return self.experiencia
    
    @property
    def pegaNivel(self):
        return self.nivel

    @pegaExperiencia.setter
    def setExperiencia(self, experiencia):
        experiencia = int(experiencia)
        self.experiencia = experiencia

    @pegaNivel.setter
    def setNivel(self, nivel):
        nivel = int(nivel)
        self.nivel = nivel

    def ehParaProduzir(self):
        return self.estado == CODIGO_PARA_PRODUZIR
    
    def ehProduzindo(self):
        return self.estado == CODIGO_PRODUZINDO
    
    def ehConcluido(self):
        return self.estado == CODIGO_CONCLUIDO

    def ehEspecial(self):
        return self.raridade == CHAVE_RARIDADE_ESPECIAL
    
    def ehRaro(self):
        return self.raridade == CHAVE_RARIDADE_RARO
    
    def ehMelhorado(self):
        return self.raridade == CHAVE_RARIDADE_MELHORADO
    
    def ehComum(self):
        return self.raridade == CHAVE_RARIDADE_COMUM
    
    def ehRecorrente(self):
        return self.recorrencia
    
    def alternaRecorrencia(self):
        self.recorrencia = not self.recorrencia
    
    def dicionarioParaObjeto(self, dicionario):
        for chave in dicionario:
            setattr(self, chave, dicionario[chave])
    
    def __str__(self) -> str:
        estado = 'Produzir' if self.estado == 0 else 'Produzindo' if self.estado == 1 else 'Feito'
        recorrencia = 'Recorrente' if self.recorrencia else 'Único'
        return f'{self.nome.ljust(44)} | {self.profissao.ljust(22)} | {str(self.nivel).ljust(5)} | {estado.ljust(10)} | {self.tipo_licenca.ljust(34)} | {recorrencia}'