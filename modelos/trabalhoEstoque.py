class TrabalhoEstoque:
    def __init__(self, id, nome, profissao, nivel, quantidade, raridade, trabalhoId) -> None:
        self.id = id
        self.nome = nome
        self.profissao = profissao
        self.nivel = int(nivel)
        self.quantidade = int(quantidade)
        self.raridade = raridade
        self.trabalhoId = trabalhoId

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
    
    def setQuantidade(self, quantidade):
        quantidade = 0 if int(quantidade) < 0 else int(quantidade)
        self.quantidade = quantidade
    
    def __str__(self) -> str:
        return f'{(self.nome).ljust(40)} | {(self.profissao).ljust(25)} | {str(self.quantidade).ljust(3)} | {str(self.nivel).ljust(5)} | {(self.raridade).ljust(10)} | {self.trabalhoId}'