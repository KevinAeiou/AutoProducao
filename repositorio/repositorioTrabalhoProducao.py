from repositorio.firebaseDatabase import FirebaseDatabase
from modelos.trabalhoProducao import TrabalhoProducao
from constantes import *

class RepositorioTrabalhoProducao:
    _listaTrabalhosProducao = []
    def __init__(self, personagem) -> None:
        self._meuBanco = FirebaseDatabase()._dataBase
        self._personagem = personagem
        self._listaTrabalhosProducao = self.pegaTodosTrabalhosProducao()

    def limpaListaProducao(self):
        self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_TRABALHOS_PRODUCAO).remove()

    def pegaTodosTrabalhosProducao(self):
        listaTrabalhosProducao = []
        todosTrabalhosProducao = self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_TRABALHOS_PRODUCAO).get()
        if todosTrabalhosProducao.pyres != None:
            for trabalhoProducaoEncontrado in todosTrabalhosProducao.each():
                if CHAVE_TRABALHO_NECESSARIO in trabalhoProducaoEncontrado.val():
                    trabalhoNecessario = trabalhoProducaoEncontrado.val()[CHAVE_TRABALHO_NECESSARIO]
                else:
                    trabalhoNecessario = ''
                if CHAVE_TRABALHO_ID in trabalhoProducaoEncontrado.val():
                    trabalhoId = trabalhoProducaoEncontrado.val()[CHAVE_TRABALHO_ID]
                else:
                    trabalhoId = ''
                if  CHAVE_NOME_PRODUCAO in trabalhoProducaoEncontrado.val():
                    trabalhoProducao = TrabalhoProducao(trabalhoProducaoEncontrado.key(), trabalhoId, trabalhoProducaoEncontrado.val()[CHAVE_NOME], trabalhoProducaoEncontrado.val()[CHAVE_NOME_PRODUCAO], trabalhoProducaoEncontrado.val()[CHAVE_EXPERIENCIA], trabalhoProducaoEncontrado.val()[CHAVE_NIVEL], trabalhoProducaoEncontrado.val()[CHAVE_PROFISSAO], trabalhoProducaoEncontrado.val()[CHAVE_RARIDADE], trabalhoNecessario, trabalhoProducaoEncontrado.val()[CHAVE_RECORRENCIA], trabalhoProducaoEncontrado.val()[CHAVE_TIPO_LICENCA], trabalhoProducaoEncontrado.val()[CHAVE_ESTADO])
                    listaTrabalhosProducao.append(trabalhoProducao)
        listaTrabalhosProducao = sorted(listaTrabalhosProducao, key=lambda trabalhoProducao: trabalhoProducao.pegaEstado(), reverse=True)
        return listaTrabalhosProducao
    
    def pegaTrabalhoProducaoProId(self, trabalhoProducao):
        return self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_TRABALHOS_PRODUCAO).order_by_child(CHAVE_ID).equal_to(trabalhoProducao.pegaId()).get()
    
    def retornaListaTrabalhosProducaoParaProduzirProduzindo(self):
        listaTrabalhosParaProduzirProduzindo = []
        for trabalhoProducao in self._listaTrabalhosProducao:
            if trabalhoProducao.ehParaProduzir() or trabalhoProducao.ehProduzindo():
                listaTrabalhosParaProduzirProduzindo.append(trabalhoProducao)
        return listaTrabalhosParaProduzirProduzindo
    
    def removeTrabalhoProducao(self, trabalhoProducao):
        self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_TRABALHOS_PRODUCAO).child(trabalhoProducao.pegaId()).remove()
    
    def adicionaTrabalhoProducao(self, trabalhoProducao):
        resultado = self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_TRABALHOS_PRODUCAO).push(trabalhoProducao.__dict__)
        trabalhoProducao.setId(resultado['name'])
        return self.modificaTrabalhoProducao(trabalhoProducao)

    def modificaTrabalhoProducao(self, trabalhoProducao):
        trabalhoProducaoComId = self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_TRABALHOS_PRODUCAO).child(trabalhoProducao.pegaId()).update(trabalhoProducao.__dict__)
        return TrabalhoProducao(trabalhoProducaoComId[CHAVE_ID], trabalhoProducaoComId[CHAVE_TRABALHO_ID], trabalhoProducaoComId[CHAVE_NOME], trabalhoProducaoComId[CHAVE_NOME_PRODUCAO], trabalhoProducaoComId[CHAVE_EXPERIENCIA], trabalhoProducaoComId[CHAVE_NIVEL], trabalhoProducaoComId[CHAVE_PROFISSAO], trabalhoProducaoComId[CHAVE_RARIDADE], trabalhoProducaoComId[CHAVE_TRABALHO_NECESSARIO], trabalhoProducaoComId[CHAVE_RECORRENCIA], trabalhoProducaoComId[CHAVE_TIPO_LICENCA], trabalhoProducaoComId[CHAVE_ESTADO])
    
    def mostraListaTrabalhosProducao(self):
        for trabalhoProducao in self._listaTrabalhosProducao:
            print(trabalhoProducao)