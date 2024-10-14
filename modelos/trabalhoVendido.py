class TrabalhoVendido:
    def __init__(self, id, nomeProduto, dataVenda, nomePersonagem, quantidadeProduto, trabalhoId, valorProduto):
        self.id = id
        self.nomeProduto = nomeProduto
        self.dataVenda = dataVenda
        self.nomePersonagem = nomePersonagem
        self.quantidadeProduto = int(quantidadeProduto)
        self.trabalhoId = trabalhoId
        self.valorProduto = int(valorProduto)

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

    def __str__(self) -> str:
        return f'{(self.nomeProduto).ljust(113)} | {(self.dataVenda).ljust(10)} | {(self.trabalhoId).ljust(36)} | {str(self.valorProduto).ljust(5)} | {self.quantidadeProduto}'