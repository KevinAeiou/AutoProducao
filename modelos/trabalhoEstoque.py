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

    def pegaId(self):
        return self.id
    
    def pegaNome(self):
        return self.nome
    
    def pegaProfissao(self):
        return self.profissao
    
    def pegaNivel(self):
        return self.nivel
    
    def pegaQuantidade(self):
        return self.quantidade
    
    def pegaRaridade(self):
        return self.raridade
    
    def pegaTrabalhoId(self):
        return self.trabalhoId
    
    def setId(self, id):
        self.id = id

    def setNome(self, nome):
        self.nome = nome

    def setProfissao(self, profissao):
        self.profissao = profissao

    def setNivel(self, nivel):
        self.nivel = int(nivel)

    def setQuantidade(self, quantidade):
        quantidade = 1 if int(quantidade) < 0 else int(quantidade)
        self.quantidade = quantidade

    def setRaridade(self, raridade):
        self.raridade = raridade

    def setIdTrabalho(self, idTrabalho):
        self.trabalhoId = idTrabalho
    
    def setQuantidade(self, quantidade):
        quantidade = 0 if int(quantidade) < 0 else int(quantidade)
        self.quantidade = quantidade
    
    def dicionarioParaObjeto(self, dicionario):
        for chave in dicionario:
            setattr(self, chave, dicionario[chave])
            
    def __str__(self) -> str:
        return f'{(self.nome).ljust(40)} | {(self.profissao).ljust(25)} | {str(self.quantidade).ljust(3)} | {str(self.nivel).ljust(5)} | {(self.raridade).ljust(10)} | {self.trabalhoId}'