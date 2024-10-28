from uuid import uuid4

class TrabalhoEstoque:
    def __init__(self,):
        self.id = str(uuid4())
        self.nome = None
        self.profissao = None
        self.nivel = 0
        self.quantidade = 0
        self.raridade = None
        self.trabalhoId = None

    def setNivel(self, nivel):
        self.nivel = int(nivel)
    
    def setQuantidade(self, quantidade):
        quantidade = 0 if int(quantidade) < 0 else int(quantidade)
        self.quantidade = quantidade
    
    def dicionarioParaObjeto(self, dicionario):
        for chave in dicionario:
            setattr(self, chave, dicionario[chave])
            
    def __str__(self) -> str:
        return f'{(self.nome).ljust(40)} | {(self.profissao).ljust(25)} | {str(self.quantidade).ljust(3)} | {str(self.nivel).ljust(5)} | {(self.raridade).ljust(10)} | {self.trabalhoId}'