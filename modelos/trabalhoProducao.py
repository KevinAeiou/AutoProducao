from constantes import CODIGO_PARA_PRODUZIR, CODIGO_PRODUZINDO, CODIGO_CONCLUIDO, CHAVE_RARIDADE_COMUM, CHAVE_RARIDADE_MELHORADO, CHAVE_RARIDADE_RARO, CHAVE_RARIDADE_ESPECIAL
from modelos.trabalho import Trabalho

class TrabalhoProducao(Trabalho):
    def __init__(self):
        super().__init__()
        self.idTrabalho = None
        self.recorrencia = False
        self.tipoLicenca = None
        self.estado = 0

    @property
    def ehParaProduzir(self):
        return self.estado == CODIGO_PARA_PRODUZIR
    
    @property
    def ehProduzindo(self):
        return self.estado == CODIGO_PRODUZINDO
    
    @property
    def ehConcluido(self):
        return self.estado == CODIGO_CONCLUIDO

    @property
    def ehEspecial(self):
        return self.raridade == CHAVE_RARIDADE_ESPECIAL
    
    @property
    def ehRaro(self):
        return self.raridade == CHAVE_RARIDADE_RARO
    
    @property
    def ehMelhorado(self):
        return self.raridade == CHAVE_RARIDADE_MELHORADO
    
    @property
    def ehComum(self):
        return self.raridade == CHAVE_RARIDADE_COMUM
    
    @property
    def ehRecorrente(self):
        return self.recorrencia
    
    @property
    def alternaRecorrencia(self):
        self.recorrencia = not self.recorrencia
    
    def __str__(self) -> str:
        id = 'Indefinido' if self.id == None else str(self.id)
        idTrabalho = 'Indefinido' if self.idTrabalho == None else str(self.idTrabalho)
        estado = 'Produzir' if self.estado == 0 else 'Produzindo' if self.estado == 1 else 'Feito'
        licenca = 'Indefinido' if self.tipoLicenca == None else str(self.tipoLicenca)
        recorrencia = 'Recorrente' if self.recorrencia else 'Único'
        return f'{id.ljust(36)} | {idTrabalho.ljust(36)} | {estado.ljust(10)} | {licenca.ljust(34)} | {recorrencia.ljust(10)}'