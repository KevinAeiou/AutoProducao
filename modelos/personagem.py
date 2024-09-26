class Personagem:
    def __init__(self, id, nome, email, senha, espacoProducao, estado, uso, autoProducao):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.espacoProducao = espacoProducao
        self.estado = estado
        self.uso = uso
        self.autoProducao = autoProducao

    def __str__(self) -> str:
        estado = 'Verdadeiro' if self.estado else 'Falso'
        uso = 'Verdadeiro' if self.uso else 'Falso'
        autoProducao = 'Verdadeiro' if self.autoProducao else 'Falso'
        return f'{(self.id).ljust(20)} | {(self.nome).ljust(17)} | {str(self.espacoProducao).ljust(6)} | {(estado).ljust(10)} | {uso.ljust(10)} | {autoProducao}'
    
    def pegaId(self):
        return self.id
    
    def setId(self, id):
        self.id = id

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
    
    def pegaAutoProducao(self):
        return self.autoProducao
    
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

    def alternaAutoProducao(self):
        self.autoProducao = not self.autoProducao

    def dicionarioParaObjeto(self, dicionario):
        for chave in dicionario:
            setattr(self, chave, dicionario[chave])