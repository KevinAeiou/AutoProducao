class Profissao:
    def __init__(self, id, nome, experiencia, prioridade):
        self.id = id
        self.nome = nome
        self.experiencia = experiencia
        self.prioridade = prioridade
    
    def __str__(self) -> str:
        return f'{(self.nome).ljust(20)} | {(self.experiencia).ljust(6)} | {self.prioridade}'
    
    def pegaId(self):
        return self.id

    def pegaNome(self):
        return self.nome
    
    def pegaExperiencia(self):
        return self.experiencia
    
    def pegaPrioridade(self):
        return self.prioridade
    
    def setExperiencia(self, experiencia):
        self.experiencia = experiencia

    def setPrioridade(self, prioridade):
        self.prioridade = prioridade