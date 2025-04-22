from uuid import uuid4
from constantes import CHAVE_RARIDADE_RARO, CHAVE_RARIDADE_COMUM, CHAVE_RARIDADE_MELHORADO, CHAVE_PROFISSAO_ARMA_DE_LONGO_ALCANCE, CHAVE_LISTA_PRODUCAO_RECURSO
from utilitariosTexto import textoEhIgual

class Trabalho:
    def __init__(self):
        self.id: str = str(uuid4())
        self.nome: str = None
        self.nomeProducao: str = None
        self.experiencia: int = None
        self.nivel: int = None
        self.profissao: str = None
        self.raridade: str = None
        self.trabalhoNecessario: str = None

    def pegaNivel(self, nivelProfissao: int) -> int:
        '''
            Método para encontrar o nível do trabalho atual com base no nível da prpofissão.
            Args:
                nivelProfissao (int): Número inteiro que representa o nível atual da Profissão.
            Returns:
                int: Número inteiro que representa o nível do trabalho.
        '''
        dicionarioNiveis: dict = {
            2: 10, 3: 10,
            4: 12, 5: 12,
            6: 14, 7: 14,
            8: 8,
            9: 16, 10: 16,
            11: 18, 12: 18,
            13: 20, 14: 20,
            15: 22, 16: 22,
            17: 24, 18: 24,
            19: 26, 20: 26,
            21: 28, 22: 28,
            23: 30, 24: 30,
            25: 32, 26: 32,
            27: 34, 28: 34
        }
        return dicionarioNiveis.get(nivelProfissao, 1)
    
    def pegaQuantidadeRecursosNecessarios(self) -> int:
        '''
            Função que retorna a quantidade de recursos terciários necessários para produção de trabalhos comuns
            Input: int
        '''
        x = 0
        if self.profissao == CHAVE_PROFISSAO_ARMA_DE_LONGO_ALCANCE:
            x = 1
        if self.nivel == 10 or self.nivel == 16:
            return x + 2
        if self.nivel == 12 or self.nivel == 18:
            return x + 4
        if self.nivel == 14 or self.nivel == 20:
            return x + 6
        if self.nivel == 22:
            return x + 8
        if self.nivel == 24:
            return x + 10
        if self.nivel == 26:
            return x + 12
        if self.nivel == 28:
            return x + 14
        if self.nivel == 30:
            return x + 16
        if self.nivel == 32:
            return x + 18
        return 0

    @property
    def ehComum(self) -> bool:
        return self.raridade == CHAVE_RARIDADE_COMUM
    
    @property
    def ehMelhorado(self) -> bool:
        return self.raridade == CHAVE_RARIDADE_MELHORADO

    @property
    def ehRaro(self) -> bool:
        return self.raridade == CHAVE_RARIDADE_RARO
    
    @property
    def ehProducaoRecursos(self) -> bool:
        return any(textoEhIgual(recurso, self.nomeProducao) for recurso in CHAVE_LISTA_PRODUCAO_RECURSO)
    
    def dicionarioParaObjeto(self, dicionario: dict):
        '''
            Método para transformar um dicionário em um objeto de classe.
            Args:
                dicionario (dict): Dicionário a ser transformado em classe.
        '''
        if dicionario is None:
            return
        for chave in dicionario:
            setattr(self, chave, dicionario[chave])

    def __str__(self) -> str:
        nome = 'Indefinido' if self.nome == None else self.nome
        profissao = 'Indefinido' if self.profissao == None else self.profissao
        raridade = 'Indefinido' if self.raridade == None else self.raridade
        nivel = 'Indefinido' if self.nivel == None else str(self.nivel)
        return f'{nome.ljust(44)} | {profissao.ljust(22)} | {raridade.ljust(9)} | {nivel.ljust(5)}'