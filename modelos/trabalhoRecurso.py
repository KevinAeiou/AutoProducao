class TrabalhoRecurso:
    def __init__(self, profissao, nivel, primario, secundario, terciario, quantidade):
        self.profissao = profissao
        self.nivel = nivel
        self.primario = primario
        self.secundario = secundario
        self.terciario = terciario
        self.quantidade = quantidade
    
    @property
    def pegaQuantidadeTerciario(self):
        return self.quantidade
    
    property
    def pegaQuantidadeSecundario(self):
        return self.quantidade + 1
    
    @property
    def pegaQuantidadePrimario(self):
        return self.quantidade + 2
    
    def __str__(self) -> str:
        profissao: str = 'Indefinido' if self.profissao is None else self.profissao
        nivel: str = 'Indefinido' if self.nivel is None else str(self.nivel)
        terciario: str = 'Indefinido' if self.terciario is None else self.terciario
        secundario: str = 'Indefinido' if self.secundario is None else self.secundario
        primario: str = 'Indefinido' if self.primario is None else self.primario
        quantidade: str = 'Indefinido' if self.quantidade is None else str(self.quantidade)
        return f'{profissao.ljust(23)} | {nivel.ljust(2)} | {terciario.ljust(20)} | {secundario.ljust(20)} | {primario.ljust(20)} | {quantidade}'