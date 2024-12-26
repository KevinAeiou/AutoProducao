from uuid import uuid4
from modelos.trabalho import Trabalho

class TrabalhoEstoque(Trabalho):
    def __init__(self):
        super().__init__()
        self.id = str(uuid4())
        self.trabalhoId = None
        self.quantidade = 0
    
    def setQuantidade(self, quantidade):
        self.quantidade = int(quantidade)
    
    def dicionarioParaObjeto(self, dicionario):
        for chave in dicionario:
            setattr(self, chave, dicionario[chave])
            
    def __str__(self) -> str:
        id = 'Indefinido' if self.id == None else str(self.id)
        idTrabalho = 'Indefinido' if self.idTrabalho == None else str(self.idTrabalho)
        quantidade = str(self.quantidade)
        return f'{id.ljust(36)} | {idTrabalho.ljust(36)} | {quantidade}'