class Trabalho:
    def __init__(self, id, nome, nomeProducao, experiencia, nivel, profissao, raridade, trabalhoNecessario) -> None:
        self.id = id
        self.nome = nome
        self.nomeProducao = nomeProducao
        self.experiencia : int = experiencia
        self.nivel : int = nivel
        self.profissao = profissao
        self.raridade = raridade
        self.trabalhoNecessario = trabalhoNecessario

    def pegaId(self):
        return self.id
    
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

    def __str__(self) -> str:
        return f'{(self.nome).ljust(44)} | {(self.profissao).ljust(22)} | {(self.raridade).ljust(9)} | {self.nivel}'