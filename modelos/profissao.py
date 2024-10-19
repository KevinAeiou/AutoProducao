from uuid import uuid4

class Profissao:
    def __init__(self):
        self.id = str(uuid4())
        self.idPersonagem = None
        self.nome = None
        self.experiencia = 0
        self.prioridade = False
    
    def setExperiencia(self, experiencia):
        experiencia = 830000 if experiencia > 830000 else int(experiencia)
        self.experiencia = experiencia

    def alternaPrioridade(self):
        self.prioridade = not self.prioridade

    def pegaNivel(self):
        listaXPMaximo = [0, 20, 200, 540, 1250, 2550, 4700, 7990, 12770, 19440, 28440, 40270, 55450, 74570, 98250, 127180, 156110, 185040, 215000, 245000, 300000, 375000, 470000, 585000, 706825, 830000]
        for experiencia in listaXPMaximo:
            if experiencia >= self.experiencia:
                if self.experiencia == experiencia:
                    return listaXPMaximo.index(experiencia) + 1
                if experiencia > self.experiencia:
                    return listaXPMaximo.index(experiencia)
        return 0
    
    def dicionarioParaObjeto(self, dicionario):
        for chave in dicionario:
            setattr(self, chave, dicionario[chave])

    def __str__(self) -> str:
        prioridade = 'Verdadeiro' if self.prioridade else 'Falso'
        return f'{(self.id).ljust(40)} | {(self.idPersonagem).ljust(40)} | {(self.nome).ljust(22)} | {str(self.experiencia).ljust(6)} | {prioridade}'