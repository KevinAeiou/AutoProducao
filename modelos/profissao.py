from uuid import uuid4
from constantes import LISTA_EXPERIENCIAS_NIVEL

class Profissao:
    def __init__(self):
        self.id: str = str(uuid4())
        self.idPersonagem: str = None
        self.nome: str = None
        self.experiencia: int = 0
        self.prioridade: bool = False

    @property
    def pegaExperienciaMaxima(self):
        return LISTA_EXPERIENCIAS_NIVEL[-1]
    
    def setExperiencia(self, experiencia: int):
        experiencia = self.pegaExperienciaMaxima if int(experiencia) > self.pegaExperienciaMaxima else int(experiencia) if int(experiencia) > 0 else 0
        self.experiencia = experiencia

    @property
    def alternaPrioridade(self):
        self.prioridade = not self.prioridade

    def nivel(self):
        if self.experiencia >= self.pegaExperienciaMaxima:
            return len(LISTA_EXPERIENCIAS_NIVEL) + 1
        for i, experiencia in enumerate(LISTA_EXPERIENCIAS_NIVEL):
            if self.experiencia < experiencia:
                return i + 1
            if self.experiencia == experiencia:
                return i + 2
        return 0
    
    @property
    def nivel_trabalho_produzido(self) -> int:
        '''
            Retorna o nível do trabalho produzido baseado no nível atual da profissão.
            Returns:
                int: Inteiro que contém o nível do trabalho produzido. É zero por padrão.
        '''
        match self.nivel():
            case 2 | 3: return 10
            case 4 | 5: return 12
            case 6 | 7: return 14
            case 9 | 10: return 16
            case 11 | 12: return 18
            case 13 | 14: return 20
            case 15 | 16: return 22
            case 17 | 18: return 24
            case 19 | 20: return 26
            case 21 | 22: return 28
            case 23 | 24: return 30
            case 25 | 26: return 32
            case 27 | 28: return 34
            case _: return 0

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
    
    @property
    def eh_nivel_producao_melhorada(self) -> bool:
        '''
            Atributo que verifica se o nível de produção é 'melhorado'.
            Returns:
                bool: Verdadeiro se o nível da profissão for melhorado, false caso contrário.
        '''
        if self.nivel() > 7:
            return self.nivel() % 2 == 0
        return self.nivel() % 2 != 0
    
    @property
    def eh_nivel_anterior_ao_maximo(self) -> bool:
        '''
            Verifica se o nível atual é o nível máximo.
            Returns:
                bool: Verdadeiro caso o nível atual seja o máximo. Falso caso contrário.
        '''
        return self.nivel() == LISTA_EXPERIENCIAS_NIVEL[-2]
    
    def ha_experiencia_suficiente(self, experiencia: int) -> bool:
        '''
            Verifica se há experiência sucifiente para avançar de nível.
            Args:
                experiencia (int): Experiência para somar à experiência atual da profissão.
            Returns:
                bool: Verdadeiro caso a soma da experiência atual mais a experiência passada por parâmetro seja igual ou superior a experiência máxima atual.
        '''
        return self.experiencia + experiencia >= self.pegaExperienciaMaximaPorNivel

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