from constantes import *
from modelos.personagem import Personagem
from repositorio.firebaseDatabase import FirebaseDatabase
from repositorio.credenciais.firebaseCredenciais import CHAVE_ID_USUARIO
from requests.exceptions import HTTPError
from repositorio.stream import Stream
from modelos.logger import MeuLogger
from firebase_admin import db
from firebase_admin.db import Event

from time import time

class RepositorioPersonagem(Stream):
    def __init__(self):
        super().__init__(chave=CHAVE_PERSONAGENS, nomeLogger= CHAVE_REPOSITORIO_PERSONAGEM)
        self.__logger: MeuLogger= MeuLogger(nome= CHAVE_REPOSITORIO_PERSONAGEM, arquivoLogger= f'{CHAVE_REPOSITORIO_PERSONAGEM}.log')
        self.__erro = None
        firebaseDb: FirebaseDatabase = FirebaseDatabase()
        try:
            meuBanco: db = firebaseDb.banco
            self.__minhaReferenciaUsuarios: db.Reference = meuBanco.reference(CHAVE_USUARIOS2).child(CHAVE_ID_USUARIO).child(CHAVE_PERSONAGENS)
            self.__minhaReferenciaPersonagens: db.Reference = meuBanco.reference(CHAVE_PERSONAGENS)
            self.__minhaReferenciaProfissoes: db.Reference = meuBanco.reference(CHAVE_PROFISSOES)
            self.__minhaReferenciaProducoes: db.Reference = meuBanco.reference(CHAVE_PRODUCAO)
            self.__minhaReferenciaEstoque: db.Reference = meuBanco.reference(CHAVE_ESTOQUE)
            self.__minhaReferenciaVendas: db.Reference = meuBanco.reference(CHAVE_VENDAS)
        except Exception as e:
            self.__logger.error(menssagem= f'Erro: {e}')
    
    def streamHandler(self, evento: Event):
        super().streamHandler(evento= evento)
        if evento.event_type in (STRING_PUT, STRING_PATCH):
            if evento.path == "/":
                return
            self.__logger.debug(menssagem= evento.path)
            self.__logger.debug(menssagem= evento.data)
            caminho: str= evento.path
            idPersonagem: str= caminho.replace('/', '').strip()
            dicionarioPersonagem: dict= {CHAVE_ID: idPersonagem}
            if evento.data is None:
                super().insereDadosModificados(dado= dicionarioPersonagem)
                return
            dicionarioPersonagem = evento.data
            dicionarioPersonagem[CHAVE_ID] = idPersonagem
            super().insereDadosModificados(dado= dicionarioPersonagem)
            return
    
    def pegaTodosPersonagens(self) -> list[Personagem] | None:
        personagens: list[Personagem]= []
        try:
            idPersonagensEncontrados: dict= self.__minhaReferenciaUsuarios.get()
            if idPersonagensEncontrados is None:
                return personagens
            for chave, valor in idPersonagensEncontrados.items():
                resultadoPersonagem: dict= self.__minhaReferenciaPersonagens.order_by_key().equal_to(chave).get()
                if resultadoPersonagem is None:
                    continue
                for chave2, valor2 in resultadoPersonagem.items():
                    personagem: Personagem= Personagem()
                    personagem.dicionarioParaObjeto(valor2)
                    break
                personagens.append(personagem)
            self.__logger.debug(menssagem= f'Personagens recuperados com sucesso!')
            return personagens
        except HTTPError as e:
            self.__erro = str(e.errno)
            self.__logger.error(menssagem= f'Erro ao pegar personagens: {e.errno}')
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(menssagem= f'Erro ao pegar personagens: {e}')
        return None
    
    def inserePersonagem(self, personagem: Personagem) -> bool:
        try:
            self.__minhaReferenciaUsuarios.update({personagem.id: True})
            self.__minhaReferenciaPersonagens.child(personagem.id).set(personagem.__dict__)
            self.__logger.debug(menssagem= f'Personagem ({personagem}) inserido com sucesso!')
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
            self.__logger.error(menssagem= f'Erro ao inserir personagem: {e.errno}')
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(menssagem= f'Erro ao inserir personagem: {e}')
        return False
    
    def modificaPersonagem(self, personagem: Personagem) -> bool:
        try:
            self.__minhaReferenciaPersonagens.child(personagem.id).update(personagem.__dict__)
            self.__logger.debug(menssagem= f'Personagem ({personagem}) modificado com sucesso!')
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
            self.__logger.error(menssagem= f'Erro ao modificar personagem: {e.errno}')
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(menssagem= f'Erro ao modificar personagem: {e}')
        return False
    
    def removePersonagem(self, personagem: Personagem) -> bool:
        try:
            self.__minhaReferenciaPersonagens.child(personagem.id).delete()
            self.__logger.debug(menssagem= f'Referência de personagem ({personagem.id}) removida da lista de personagens.')
            self.__minhaReferenciaUsuarios.child(personagem.id).delete()
            self.__logger.debug(menssagem= f'Referência de personagem ({personagem.id}) removida da lista de usuários.')
            self.__minhaReferenciaProfissoes.child(personagem.id).delete()
            self.__logger.debug(menssagem= f'Referência de personagem ({personagem.id}) removida da lista de profissões.')
            self.__minhaReferenciaProducoes.child(personagem.id).delete()
            self.__logger.debug(menssagem= f'Referência de personagem ({personagem.id}) removida da lista de produções.')
            self.__minhaReferenciaEstoque.child(personagem.id).delete()
            self.__logger.debug(menssagem= f'Referência de personagem ({personagem.id}) removida da lista de estoque.')
            self.__minhaReferenciaVendas.child(personagem.id).delete()
            self.__logger.debug(menssagem= f'Referência de personagem ({personagem.id}) removida da lista de vendas.')
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
            self.__logger.error(menssagem= f'Erro ao remover personagem: {e.errno}')
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(menssagem= f'Erro ao remover personagem: {e}')
        return False

    @property
    def pegaErro(self):
        return self.__erro