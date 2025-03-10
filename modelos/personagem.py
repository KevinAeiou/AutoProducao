from modelos.usuario import Usuario

class Personagem(Usuario):
    def __init__(self):
        super().__init__()
        self.email = None
        self.senha = None
        self.espacoProducao = 1
        self.estado = False
        self.uso = False
        self.autoProducao = False

    def setEspacoProducao(self, espacoProducao):
        self.espacoProducao = int(espacoProducao)
    
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
    
    def __str__(self) -> str:
        estado = 'Verdadeiro' if self.estado else 'Falso'
        uso = 'Verdadeiro' if self.uso else 'Falso'
        autoProducao = 'Verdadeiro' if self.autoProducao else 'Falso'
        id = 'Indefinido' if self.id == None else self.id
        nome = 'Indefinido' if self.nome == None else self.nome
        espaco = 'Indefinido' if self.espacoProducao == None else self.espacoProducao
        return f'{(id).ljust(36)} | {(nome).ljust(17)} | {str(espaco).ljust(6)} | {(estado).ljust(10)} | {uso.ljust(10)} | {autoProducao.ljust(10)}'