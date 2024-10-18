__author__ = 'Kevin Amazonas'

from uuid import uuid4

class TrabalhoVendido:
    def __init__(self):
        self.id = str(uuid4())
        self.nomeProduto = None
        self.dataVenda = None
        self.nomePersonagem = None
        self.quantidadeProduto = 0
        self.trabalhoId = None
        self.valorProduto = None

    def pegaId(self):
        return self.id
    
    def pegaNome(self):
        return self.nomeProduto
    
    def pegaDataVenda(self):
        return self.dataVenda
    
    def pegaNomePersonagem(self):
        return self.nomePersonagem
    
    def pegaQuantidadeProduto(self):
        return self.quantidadeProduto
    
    def pegaTrabalhoId(self):
        return self.trabalhoId
    
    def pegaValorProduto(self):
        return self.valorProduto
    
    def setId(self, id):
        self.id = id

    def setNome(self, nome):
        self.nomeProduto = nome

    def setData(self, data):
        self.dataVenda = data

    def setQuantidade(self, quantidade):
        quantidade = 0 if int(quantidade) < 0 else int(quantidade)
        self.quantidadeProduto = quantidade

    def setValor(self, valor):
        valor = 0 if int(valor) < 0 else int(valor)
        self.valorProduto = valor

    def dicionarioParaObjeto(self, dicionario):
        for chave in dicionario:
            setattr(self, chave, dicionario[chave])
            
    def __str__(self) -> str:
        return f'{(self.nomeProduto).ljust(113)} | {(self.dataVenda).ljust(10)} | {(self.trabalhoId).ljust(36)} | {str(self.valorProduto).ljust(5)} | {self.quantidadeProduto}'