from uuid import uuid4

class Usuario:
    def __init__(self):
        self.id = str(uuid4())
        self.nome = None

    def dicionarioParaObjeto(self, dicionario: dict):
        if dicionario is None:
            return
        for chave in dicionario:
            setattr(self, chave, dicionario[chave])
    
    def __str__(self) -> str:
        id = 'Indefinido' if self.id == None else self.id
        nome = 'Indefinido' if self.nome == None else self.nome
        return f'{(id).ljust(36)} | {(nome).ljust(17)}'