__author__ = 'Kevin Amazonas'

from uuid import uuid4

class TrabalhoVendido:
    def __init__(self):
        self.id = str(uuid4())
        self.trabalhoId = None
        self.nome = None
        self.nivel = None
        self.profissao = None
        self.raridade = None
        self.trabalhoNecessario = None
        self.nomeProduto = None
        self.dataVenda = None
        self.quantidadeProduto = 0
        self.valorProduto = None
        self.nomePersonagem = None

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
        nome = 'Indefinido' if self.nome == None else self.nome
        data = 'Indefinido' if self.dataVenda == None else self.dataVenda
        valor = 'Indefinido' if self.valorProduto == None else str(self.valorProduto)
        quantidade = '0' if self.quantidadeProduto == None else str(self.quantidadeProduto)
        return f'{nome.ljust(44)} | {data.ljust(10)} | {valor.ljust(5)} | {quantidade}'