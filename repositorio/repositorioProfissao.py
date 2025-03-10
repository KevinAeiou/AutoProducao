from repositorio.firebaseDatabase import FirebaseDatabase
from repositorio.credenciais.firebaseCredenciais import CHAVE_ID_USUARIO
from repositorio.stream import Stream
from modelos.profissao import Profissao
from modelos.personagem import Personagem
from constantes import *
from requests.exceptions import HTTPError
from pyrebase import pyrebase

class RepositorioProfissao(Stream):
    listaProfissoes = []
    def __init__(self, personagem: Personagem= None):
        super().__init__(chave= CHAVE_PROFISSOES, nomeLogger= CHAVE_REPOSITORIO_PROFISSAO)
        self.__erro: str= None
        self.__meuBanco = FirebaseDatabase().pegaMeuBanco()
        self.__personagem: Personagem= personagem

    def streamHandler(self, menssagem: dict):
        super().streamHandler(menssagem= menssagem)
        if menssagem['event'] in ('put', 'path'):
            if menssagem['path'] == '/':
                return
            ids: list[str]= menssagem['path'].split('/')
            profissao: Profissao= Profissao()
            dicionarioProfissao: dict= {CHAVE_ID_PERSONAGEM: ids[1]}
            if menssagem['data'] is None:
                profissao.id= ids[2]
                profissao.experiencia= None
                dicionarioProfissao[CHAVE_TRABALHOS]= profissao
                super().insereDadosModificados(dado= dicionarioProfissao)
                return
            profissao.dicionarioParaObjeto(dicionario= menssagem['data'])
            dicionarioProfissao[CHAVE_TRABALHOS]= profissao
            super().insereDadosModificados(dado= dicionarioProfissao)

    def pegaProfissoesPersonagem(self) -> list[Profissao]:
        profissoes: list[Profissao]= []
        try:
            profissoesEncontradas = self.__meuBanco.child(CHAVE_PROFISSOES).child(self.__personagem.id).get()
            if profissoesEncontradas.pyres == None:
                return profissoes
            for profissaoEncontrada in profissoesEncontradas.each():
                profissao = Profissao()
                profissao.dicionarioParaObjeto(profissaoEncontrada.val())
                profissao.idPersonagem = self.__personagem.id
                profissaoEncontrada =self.__meuBanco.child(CHAVE_LISTA_PROFISSAO).child(profissao.id).get()
                if profissaoEncontrada.pyres is None:
                    raise Exception(f'({profissao.id}) não foi encontrado na lista de profissões!')
                profissao.nome= profissaoEncontrada.pyres[1].val()
                profissoes.append(profissao)
            profissoes = sorted(profissoes, key = lambda profissao: profissao.nome)
            profissoes = sorted(profissoes, key = lambda profissao: profissao.experiencia, reverse = True)
            return profissoes
        except Exception as e:
            self.__erro = str(e)
        return None
    
    def pegaListaProfissoes(self) -> list[Profissao]:
        profissoes: list[Profissao]= []
        try:
            profissoesEncontradas = self.__meuBanco.child(CHAVE_LISTA_PROFISSAO).get()
            if profissoesEncontradas.pyres == None:
                return profissoes
            for profissaoEncontrada in profissoesEncontradas.each():
                profissao = Profissao()
                profissao.dicionarioParaObjeto(profissaoEncontrada.val())
                profissoes.append(profissao)
            return profissoes
        except Exception as e:
            self.__erro = str(e)
        return None
    
    def insereProfissao(self, profissao: Profissao) -> bool:
        try:
            profissoes: pyrebase.PyreResponse= self.__meuBanco.child(CHAVE_LISTA_PROFISSAO).get()
            if profissoes.pyres is None:
                self.__meuBanco.child(CHAVE_LISTA_PROFISSAO).child(profissao.id).update({CHAVE_ID: profissao.id, CHAVE_NOME: profissao.nome})
            else:
                for profissaoRecebida in profissoes.each():
                    if profissaoRecebida.val()[CHAVE_NOME] == profissao.nome:
                        profissao.id= profissaoRecebida.key()
                        break
                else:
                    self.__meuBanco.child(CHAVE_LISTA_PROFISSAO).child(profissao.id).update({CHAVE_ID: profissao.id, CHAVE_NOME: profissao.nome})
            self.__meuBanco.child(CHAVE_PROFISSOES).child(self.__personagem.id).child(profissao.id).set({CHAVE_ID: profissao.id, CHAVE_EXPERIENCIA: profissao.experiencia, CHAVE_PRIORIDADE: profissao.prioridade})
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
        except Exception as e:
            self.__erro = str(e)
        return False

    def modificaProfissao(self, profissao: Profissao) -> bool:
        try:
            self.__meuBanco.child(CHAVE_PROFISSOES).child(self.__personagem.id).child(profissao.id).update({CHAVE_EXPERIENCIA: profissao.experiencia, CHAVE_PRIORIDADE: profissao.prioridade})
            self.__meuBanco.child(CHAVE_LISTA_PROFISSAO).child(profissao.id).update({CHAVE_NOME: profissao.nome})
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def removeProfissao(self, profissao: Profissao) -> bool:
        try:
            self.__meuBanco.child(CHAVE_PROFISSOES).child(self.__personagem.id).child(profissao.id).remove()
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def limpaProfissoes(self):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.__personagem.id).child(CHAVE_LISTA_PROFISSAO).remove()
            return True
        except Exception as e:
            self.__erro = str(e)
        return False

    def pegaErro(self):
        return self.__erro