class Trabalho:
    def __init__(self, id, nome, nomeProducao, experiencia, nivel, profissao, raridade, trabalhoNecessario) -> None:
        self.id = id
        self.nome = nome
        self.nomeProducao = nomeProducao
        self.experiencia = experiencia
        self.nivel = nivel
        self.profissao = profissao
        self.raridade = raridade
        self.trabalhoNecessario = trabalhoNecessario

    def pegaId(self):
        return self.id
    
    def pegaNome(self):
        return self.nome
    
    def pegaNomeProducao(self):
        return self.nomeProducao
    
    def pegaExperiencia(self):
        return self.experiencia
    
    def pegaNivel(self):
        return self.nivel
    
    def pegaProfissao(self):
        return self.profissao
    
    def pegaRaridade(self):
        return self.raridade
    
    def pegaTrabalhoNecessario(self):
        return self.trabalhoNecessario

    def __str__(self) -> str:
        return f'{(self.nome).ljust(44)} | {(self.profissao).ljust(22)} | {(self.raridade).ljust(9)} | {self.nivel}'