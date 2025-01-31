from uuid import uuid4
from modelos.trabalho import Trabalho

class TrabalhoEstoque(Trabalho):
    def __init__(self):
        super().__init__()
        self.id = str(uuid4())
        self.trabalhoId = None
        self.quantidade = 0
    
    def setQuantidade(self, quantidade):
        quantidade = 0 if int(quantidade) < 0 else int(quantidade)
        self.quantidade = quantidade
    
    def dicionarioParaObjeto(self, dicionario):
        for chave in dicionario:
            setattr(self, chave, dicionario[chave])
            
    def __str__(self) -> str:
        id = 'Indefinido' if self.id == None else str(self.id)
        trabalhoId = 'Indefinido' if self.trabalhoId == None else str(self.trabalhoId)
        quantidade = str(self.quantidade)
        return f'{id.ljust(36)} | {trabalhoId.ljust(36)} | {quantidade.ljust(3)}'