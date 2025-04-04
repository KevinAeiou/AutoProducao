from uuid import uuid4
from constantes import LISTA_EXPERIENCIAS_NIVEL

class Profissao:
    def __init__(self):
        self.id = str(uuid4())
        self.idPersonagem = None
        self.nome = None
        self.experiencia = 0
        self.prioridade = False

    @property
    def pegaExperienciaMaxima(self):
        return LISTA_EXPERIENCIAS_NIVEL[-1]
    
    def setExperiencia(self, experiencia: int):
        experiencia = self.pegaExperienciaMaxima if int(experiencia) > self.pegaExperienciaMaxima else int(experiencia) if int(experiencia) > 0 else 0
        self.experiencia = experiencia

    @property
    def alternaPrioridade(self):
        self.prioridade = not self.prioridade

    def pegaNivel(self):
        if self.experiencia >= self.pegaExperienciaMaxima:
            return len(LISTA_EXPERIENCIAS_NIVEL) + 1
        for i, experiencia in enumerate(LISTA_EXPERIENCIAS_NIVEL):
            if self.experiencia < experiencia:
                return i + 1
            if self.experiencia == experiencia:
                return i + 2
        return 0

    @property
    def pegaExperienciaMaximaPorNivel(self):
        if self.experiencia >= self.pegaExperienciaMaxima:
            return self.pegaExperienciaMaxima
        for i, exp in enumerate(LISTA_EXPERIENCIAS_NIVEL):
            if self.experiencia < exp:
                return exp
            if self.experiencia == exp:
                if i == len(LISTA_EXPERIENCIAS_NIVEL) - 1:
                    return exp
                return LISTA_EXPERIENCIAS_NIVEL[i + 1]
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
        return f'{(idPersonagem).ljust(40)} | {(id).ljust(40)} | {(nome).ljust(22)} | {experiencia.ljust(6)} | {prioridade.ljust(10)}'