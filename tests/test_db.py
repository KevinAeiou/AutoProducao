from db.db import MeuBanco
from modelos.trabalho import Trabalho
import uuid

class TesteBancoDeDados:
    _meuBanco = MeuBanco()
    def testDeveInserirUmTrabalhoNaTabelaTrabalhos(self):
        self._meuBanco.pegaConexao()
        trabalhosAtuais = self._meuBanco.pegaTodosTrabalhos()
        esperado = len(trabalhosAtuais) + 1
        self._meuBanco.insereTrabalho(Trabalho(str(uuid.uuid4()), 'Nome teste', 'Nome produção teste', 999, 99, 'Profissao teste', 'Raridade teste', 'Trabalho necessario teste'))
        trabalhosAtuais = self._meuBanco.pegaTodosTrabalhos()
        for trabalho in trabalhosAtuais:
            print(trabalho)
        recebido = len(trabalhosAtuais)
        assert esperado == recebido
