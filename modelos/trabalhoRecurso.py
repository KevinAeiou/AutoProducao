class TrabalhoRecurso:
    def __init__(self, profissao, nivel, primario, secundario, terciario, quantidade):
        self.profissao = profissao
        self.nivel = nivel
        self.primario = primario
        self.secundario = secundario
        self.terciario = terciario
        self.quantidade = quantidade
        
    def pegaProfissao(self):
        return self.profissao
    
    def pegaNivel(self):
        return self.nivel
    
    def pegaPrimario(self):
        return self.primario
    
    def pegaSecundario(self):
        return self.secundario
    
    def pegaTerciario(self):
        return self.terciario
    
    def pegaQuantidadeTerciario(self):
        return self.quantidade
    
    def pegaQuantidadeSecundario(self):
        return self.quantidade + 1
    
    def pegaQuantidadePrimario(self):
        return self.quantidade + 2
    
    def __str__(self) -> str:
        return f'{(self.profissao).ljust(23)} | {str(self.nivel).ljust(2)} | {(self.terciario).ljust(20)} | {(self.secundario).ljust(20)} | {(self.primario).ljust(20)} | {self.quantidade}'