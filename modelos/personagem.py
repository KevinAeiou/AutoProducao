class Personagem:
    def __init__(self, id, nome, email, senha, espacoProducao, estado, uso):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.espacoProducao = espacoProducao
        self.estado = estado
        self.uso = uso

    def __str__(self) -> str:
        return f'{(self.nome).ljust(20)} | {self.email}'
    
    def pegaId(self):
        return self.id

    def pegaNome(self):
        return self.nome
    
    def pegaEmail(self):
        return self.email
    
    def pegaSenha(self):
        return self.senha
    
    def pegaEspacoProducao(self):
        return self.espacoProducao
    
    def pegaEstado(self):
        return self.estado
    
    def pegaUso(self):
        return self.uso
    
    def setEstado(self, estado):
        self.estado = estado
    
    def setEspacoProducao(self, espacoProducao):
        self.espacoProducao = espacoProducao
    
    def ehAtivo(self):
        return True if self.estado else False

    def alternaUso(self):
        self.uso = not self.uso

    def alternaEstado(self):
        self.estado = not self.estado