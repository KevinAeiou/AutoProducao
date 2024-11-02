from constantes import CODIGO_PARA_PRODUZIR, CODIGO_PRODUZINDO, CODIGO_CONCLUIDO, CHAVE_RARIDADE_COMUM, CHAVE_RARIDADE_MELHORADO, CHAVE_RARIDADE_RARO, CHAVE_RARIDADE_ESPECIAL
from uuid import uuid4
from modelos.trabalho import Trabalho

class TrabalhoProducao(Trabalho):
    def __init__(self):
        super().__init__()
        self.idTrabalho = None
        self.recorrencia = None
        self.tipo_licenca = None
        self.estado = None

    def ehParaProduzir(self):
        return self.estado == CODIGO_PARA_PRODUZIR
    
    def ehProduzindo(self):
        return self.estado == CODIGO_PRODUZINDO
    
    def ehConcluido(self):
        return self.estado == CODIGO_CONCLUIDO

    def ehEspecial(self):
        return self.raridade == CHAVE_RARIDADE_ESPECIAL
    
    def ehRaro(self):
        return self.raridade == CHAVE_RARIDADE_RARO
    
    def ehMelhorado(self):
        return self.raridade == CHAVE_RARIDADE_MELHORADO
    
    def ehComum(self):
        return self.raridade == CHAVE_RARIDADE_COMUM
    
    def ehRecorrente(self):
        return self.recorrencia
    
    def alternaRecorrencia(self):
        self.recorrencia = not self.recorrencia
    
    def dicionarioParaObjeto(self, dicionario):
        for chave in dicionario:
            setattr(self, chave, dicionario[chave])
    
    def __str__(self) -> str:
        nome = 'Indefinido' if self.nome == None else self.nome
        profissao = 'Indefinido' if self.profissao == None else self.profissao
        nivel = 'Indefinido' if self.nivel == None else str(self.nivel)
        estado = 'Produzir' if self.estado == 0 else 'Produzindo' if self.estado == 1 else 'Feito'
        licenca = 'Indefinido' if self.tipo_licenca == None else self.tipo_licenca
        recorrencia = 'Recorrente' if self.recorrencia else 'Único'
        return f'{nome.ljust(44)} | {profissao.ljust(22)} | {nivel.ljust(5)} | {estado.ljust(10)} | {licenca.ljust(34)} | {recorrencia}'