from constantes import *
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

    def pegaId(self):
        return self.id

    def pegaNome(self):
        return self.nome
    
    def pegaNomeProducao(self):
        return self.nomeProducao
    
    def pegaEstado(self):
        return self.estado
    
    def pegaExperiencia(self):
        return self.experiencia
    
    def pegaNivel(self):
        return self.nivel
    
    def pegaProfissao(self):
        return self.profissao
    
    def pegaRaridade(self):
        return self.raridade
    
    def pegaRecorrencia(self):
        return self.recorrencia
    
    def pegaLicenca(self):
        return self.tipo_licenca
    
    def pegaTrabalhoId(self):
        return self.trabalhoId
    
    def pegaTrabalhoNecessario(self):
        return self.trabalhoNecessario
    
    def setId(self, id):
        self.id = id

    def setNome(self, nome):
        self.nome = nome

    def setExperiencia(self, experiencia):
        experiencia = int(experiencia)
        self.experiencia = experiencia

    def setNivel(self, nivel):
        nivel = int(nivel)
        self.nivel = nivel

    def setProfissao(self, profissao):
        self.profissao = profissao

    def setRaridade(self, raridade):
        self.raridade = raridade

    def setTrabalhoNecessario(self, trabalhoNecessario):
        self.trabalhoNecessario = trabalhoNecessario

    def setEstado(self, estado):
        self.estado = estado

    def setTrabalhoId(self, trabalhoId):
        self.trabalhoId = trabalhoId

    def setNomeProducao(self, nomeProducao):
        self.nomeProducao = nomeProducao

    def setRecorrencia(self, recorrencia):
        self.recorrencia = recorrencia

    def setLicenca(self, licenca):
        self.tipo_licenca = licenca

    def ehParaProduzir(self):
        return self.pegaEstado() == CODIGO_PARA_PRODUZIR
    
    def ehProduzindo(self):
        return self.pegaEstado() == CODIGO_PRODUZINDO
    
    def ehConcluido(self):
        return self.pegaEstado() == CODIGO_CONCLUIDO

    def ehEspecial(self):
        return self.raridade == CHAVE_RARIDADE_ESPECIAL
    
    def ehRaro(self):
        return self.raridade == CHAVE_RARIDADE_RARO
    
    def ehMelhorado(self):
        return self.raridade == CHAVE_RARIDADE_MELHORADO
    
    def ehComum(self):
        return self.raridade == CHAVE_RARIDADE_COMUM
    
    def ehRecorrente(self):
        return self.pegaRecorrencia()
    
    def alternaRecorrencia(self):
        self.recorrencia = not self.recorrencia
    
    def dicionarioParaObjeto(self, dicionario):
        for chave in dicionario:
            setattr(self, chave, dicionario[chave])
    
    def __str__(self) -> str:
        estado = 'Produzir' if self.estado == 0 else 'Produzindo' if self.estado == 1 else 'Feito'
        recorrencia = 'Recorrente' if self.recorrencia else 'Único'
        return f'{self.nome.ljust(44)} | {self.profissao.ljust(22)} | {str(self.nivel).ljust(5)} | {estado.ljust(10)} | {self.tipo_licenca.ljust(34)} | {recorrencia}'