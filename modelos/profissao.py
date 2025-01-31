from uuid import uuid4
from constantes import LISTA_EXPERIENCIAS_NIVEL

class Profissao:
    def __init__(self):
        self.id = str(uuid4())
        self.idPersonagem = None
        self.nome = None
        self.experiencia = 0
        self.prioridade = False

    def pegaExperienciaMaxima(self):
        return LISTA_EXPERIENCIAS_NIVEL[-1]
    
    def setExperiencia(self, experiencia):
        experiencia = self.pegaExperienciaMaxima() if int(experiencia) > self.pegaExperienciaMaxima() else int(experiencia)
        self.experiencia = experiencia

    def alternaPrioridade(self):
        self.prioridade = not self.prioridade

    def pegaNivel(self):
        for experiencia in LISTA_EXPERIENCIAS_NIVEL:
            if experiencia >= self.experiencia:
                if self.experiencia == experiencia:
                    return LISTA_EXPERIENCIAS_NIVEL.index(experiencia) + 2
                if experiencia > self.experiencia:
                    return LISTA_EXPERIENCIAS_NIVEL.index(experiencia) + 1
        return 0
    
    def pegaExperienciaMaximaPorNivel(self):
        for experiencia in LISTA_EXPERIENCIAS_NIVEL:
            if experiencia >= self.experiencia:
                if self.experiencia == experiencia:
                    if experiencia == self.pegaExperienciaMaxima():
                        return LISTA_EXPERIENCIAS_NIVEL[LISTA_EXPERIENCIAS_NIVEL.index(experiencia)]
                    return LISTA_EXPERIENCIAS_NIVEL[LISTA_EXPERIENCIAS_NIVEL.index(experiencia) + 1]
                if experiencia > self.experiencia:
                    return LISTA_EXPERIENCIAS_NIVEL[LISTA_EXPERIENCIAS_NIVEL.index(experiencia)]
        return 0

    def dicionarioParaObjeto(self, dicionario):
        for chave in dicionario:
            setattr(self, chave, dicionario[chave])

    def __str__(self) -> str:
        id = 'Indefinido' if self.id is None else self.id
        idPersonagem = 'Indefinido' if self.idPersonagem is None else self.idPersonagem
        nome = 'Indefinido' if self.nome is None else self.nome
        experiencia = 'Indefinido' if self.experiencia is None else str(self.experiencia)
        prioridade = 'Verdadeiro' if self.prioridade else 'Falso'
        return f'{(id).ljust(40)} | {(idPersonagem).ljust(40)} | {(nome).ljust(22)} | {experiencia.ljust(6)} | {prioridade.ljust(10)}'