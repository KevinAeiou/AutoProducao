from uuid import uuid4

class Personagem:
    def __init__(self):
        self.id = str(uuid4())
        self.nome = None
        self.email = None
        self.senha = None
        self.espacoProducao = 1
        self.estado = False
        self.uso = False
        self.autoProducao = False

    def __str__(self) -> str:
        estado = 'Verdadeiro' if self.estado else 'Falso'
        uso = 'Verdadeiro' if self.uso else 'Falso'
        autoProducao = 'Verdadeiro' if self.autoProducao else 'Falso'
        id = 'Indefinido' if self.id == None else self.id
        nome = 'Indefinido' if self.nome == None else self.nome
        espaco = 'Indefinido' if self.espacoProducao == None else self.espacoProducao
        return f'{(id).ljust(36)} | {(nome).ljust(17)} | {str(espaco).ljust(6)} | {(estado).ljust(10)} | {uso.ljust(10)} | {autoProducao}'
    
    def pegaId(self):
        return self.id
    
    def setId(self, id):
        self.id = id

    def pegaNome(self):
        return self.nome
    
    def setNome(self, nome):
        self.nome = nome
    
    def pegaEmail(self):
        return self.email
    
    def setEmail(self, email):
        self.email = email
    
    def pegaSenha(self):
        return self.senha
    
    def setSenha(self, senha):
        self.senha = senha
    
    def pegaEspacoProducao(self):
        return self.espacoProducao
    
    def setEspacoProducao(self, espacoProducao):
        self.espacoProducao = int(espacoProducao)
    
    def pegaEstado(self):
        return self.estado
    
    def setEstado(self, estado):
        self.estado = estado
    
    def pegaUso(self):
        return self.uso
    
    def setUso(self, uso):
        self.uso = uso
    
    def pegaAutoProducao(self):
        return self.autoProducao
    
    def setAutoProducao(self, autoProducao):
        self.autoProducao = autoProducao
    
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