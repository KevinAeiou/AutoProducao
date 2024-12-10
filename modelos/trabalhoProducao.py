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
        id = 'Indefinido' if self.id == None else str(self.id)
        idTrabalho = 'Indefinido' if self.idTrabalho == None else str(self.idTrabalho)
        estado = 'Produzir' if self.estado == 0 else 'Produzindo' if self.estado == 1 else 'Feito'
        licenca = 'Indefinido' if self.tipo_licenca == None else str(self.tipo_licenca)
        recorrencia = 'Recorrente' if self.recorrencia else 'Único'
        return f'{id.ljust(36)} | {idTrabalho.ljust(36)} | {estado.ljust(10)} | {licenca.ljust(34)} | {recorrencia}'