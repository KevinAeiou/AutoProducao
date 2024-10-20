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
        nome = '' if self.nomeProduto == None else self.nomeProduto
        return f'{(nome).ljust(113)} | {(self.dataVenda).ljust(10)} | {(self.trabalhoId).ljust(36)} | {str(self.valorProduto).ljust(5)} | {self.quantidadeProduto}'