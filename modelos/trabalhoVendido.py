__author__ = 'Kevin Amazonas'

from modelos.trabalho import Trabalho

class TrabalhoVendidoVelho(Trabalho):
    def __init__(self):
        super().__init__()
        self.trabalhoId = None
        self.nomeProduto = None
        self.dataVenda = None
        self.quantidadeProduto = None
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
        id = 'Indefinido' if self.id == None else self.id
        idTrabalho = 'Indefinido' if self.trabalhoId == None else self.trabalhoId
        data = 'Indefinido' if self.dataVenda == None else self.dataVenda
        valor = 'Indefinido' if self.valorProduto == None else str(self.valorProduto)
        quantidade = '0' if self.quantidadeProduto == None else str(self.quantidadeProduto)
        return f'{id.ljust(36)} | {idTrabalho.ljust(36)} | {data.ljust(10)} | {valor.ljust(5)} | {quantidade.ljust(3)}'

class TrabalhoVendido(Trabalho):
    def __init__(self):
        super().__init__()
        self.idTrabalho = None
        self.idPersonagem = None
        self.descricao = None
        self.dataVenda = None
        self.quantidade = None
        self.valor = None

    def setQuantidade(self, quantidade):
        quantidade = 0 if int(quantidade) < 0 else int(quantidade)
        self.quantidade = quantidade

    def setValor(self, valor):
        valor = 0 if int(valor) < 0 else int(valor)
        self.valor = valor

    def dicionarioParaObjeto(self, dicionario):
        for chave in dicionario:
            setattr(self, chave, dicionario[chave])
            
    def __str__(self) -> str:
        id = 'Indefinido' if self.id == None else self.id
        nome = 'Indefinido' if self.nome == None else self.nome
        data = 'Indefinido' if self.dataVenda == None else self.dataVenda
        valor = 'Indefinido' if self.valor == None else str(self.valor)
        quantidade = '0' if self.quantidade == None else str(self.quantidade)
        return f'{id.ljust(36)} | {nome.ljust(36)} | {data.ljust(10)} | {valor.ljust(5)} | {quantidade.ljust(3)}'