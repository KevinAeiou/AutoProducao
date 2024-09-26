class Profissao:
    def __init__(self, id, nome, experiencia, prioridade):
        self.id = id
        self.nome = nome
        self.experiencia = experiencia
        self.prioridade = prioridade
    
    def pegaId(self):
        return self.id
    
    def setId(self, id):
        self.id = id

    def pegaNome(self):
        return self.nome
    
    def setNome(self, nome):
        self.nome = nome
    
    def pegaExperiencia(self):
        return self.experiencia
    
    def pegaPrioridade(self):
        return self.prioridade
    
    def setExperiencia(self, experiencia):
        if experiencia > 830000:
            experiencia = 830000
        self.experiencia = experiencia

    def setPrioridade(self, prioridade):
        self.prioridade = prioridade

    def alternaPrioridade(self):
        self.prioridade = not self.pegaPrioridade()

    def pegaNivel(self):
        listaXPMaximo = [0, 20, 200, 540, 1250, 2550, 4700, 7990, 12770, 19440, 28440, 40270, 55450, 74570, 98250, 127180, 156110, 185040, 215000, 245000, 300000, 375000, 470000, 585000, 706825, 830000]
        for experiencia in listaXPMaximo:
            if experiencia >= self.pegaExperiencia():
                if self.pegaExperiencia() == experiencia:
                    return listaXPMaximo.index(experiencia) + 1
                if experiencia > self.pegaExperiencia():
                    return listaXPMaximo.index(experiencia)
        return 0

    def __str__(self) -> str:
        prioridade = 'Verdadeiro' if self.pegaPrioridade() else 'Falso'
        return f'{(self.id).ljust(40)} | {(self.nome).ljust(22)} | {str(self.experiencia).ljust(6)} | {prioridade}'