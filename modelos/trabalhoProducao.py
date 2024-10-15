from constantes import *

class TrabalhoProducao:
    def __init__(self, id, trabalhoId, nome, nomeProducao, experiencia, nivel, profissao, raridade, trabalhoNecessario, recorrencia, tipoLicenca, estado):
        self.id = id
        self.trabalhoId = trabalhoId
        self.nome = nome
        self.nomeProducao = nomeProducao
        self.experiencia = experiencia
        self.nivel = nivel
        self.profissao = profissao
        self.raridade = raridade
        self.trabalhoNecessario = trabalhoNecessario
        self.recorrencia = recorrencia
        self.tipo_licenca = tipoLicenca
        self.estado = estado

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