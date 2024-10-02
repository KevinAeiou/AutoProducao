class TrabalhoVendido:
    def __init__(self, id, nomeProduto, dataVenda, nomePersonagem, quantidadeProduto, trabalhoId, valorProduto) -> None:
        self.id = id
        self.nomeProduto = nomeProduto
        self.dataVenda = dataVenda
        self.nomePersonagem = nomePersonagem
        self.quantidadeProduto = quantidadeProduto
        self.trabalhoId = trabalhoId
        self.valorProduto = valorProduto

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

    def __str__(self) -> str:
        return f'{(self.nomeProduto).ljust(113)} | {(self.dataVenda).ljust(10)} | {(self.trabalhoId).ljust(36)} | {str(self.valorProduto).ljust(5)} | {self.quantidadeProduto}'