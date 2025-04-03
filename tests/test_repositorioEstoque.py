import pytest
from unittest.mock import Mock, patch, MagicMock
from modelos.personagem import Personagem
from modelos.trabalhoEstoque import TrabalhoEstoque
from repositorio.repositorioEstoque import RepositorioEstoque
from constantes import *
from requests.exceptions import HTTPError
from firebase_admin import db

class TestRepositorioEstoque:
    """Classe de testes para RepositorioEstoque"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Configuração inicial para todos os testes"""
        # Mock do Personagem
        self.mock_personagem = Personagem()
        self.mock_personagem.id = "personagem123"
        
        # Mock da referência do Firebase
        self.mock_root_ref = MagicMock()
        self.mock_estoque_ref = MagicMock()
        self.mock_personagem_ref = MagicMock()
        
        # Configura a cadeia de chamadas
        self.mock_root_ref.child.return_value = self.mock_estoque_ref
        self.mock_estoque_ref.child.return_value = self.mock_personagem_ref
        
        # Mock do FirebaseDatabase
        self.firebase_patcher = patch('repositorio.firebaseDatabase.FirebaseDatabase')
        MockFirebaseDatabase = self.firebase_patcher.start()
        self.mock_firebase_instance = MockFirebaseDatabase.return_value
        self.mock_firebase_instance.banco.reference.return_value = self.mock_root_ref
        
        # Mock do Logger
        self.logger_patcher = patch('modelos.logger.MeuLogger')
        self.mock_logger_class = self.logger_patcher.start()
        self.mock_logger_instance = MagicMock()
        self.mock_logger_class.return_value = self.mock_firebase_instance
        
        # Mock do Stream
        self.stream_patcher = patch('repositorio.stream.Stream')
        self.mock_stream = self.stream_patcher.start()
        
        yield
        
        # Limpeza
        self.firebase_patcher.stop()
        self.logger_patcher.stop()
        self.stream_patcher.stop()

    def test_init_cria_referencia_correta(self):
        """Testa se a referência do Firebase é criada corretamente"""
        repositorio = RepositorioEstoque(personagem=self.mock_personagem)
        
        # Verifica a cadeia de chamadas
        self.mock_firebase_instance.banco.reference.assert_called_once()
        self.mock_root_ref.child.assert_called_once_with(CHAVE_ESTOQUE)
        self.mock_estoque_ref.child.assert_called_once_with(self.mock_personagem.id)
        
        # Verifica se a referência foi armazenada
        assert repositorio._RepositorioEstoque__minhaReferencia == self.mock_personagem_ref

    def test_init_com_erro(self):
        """Testa inicialização com erro no Firebase"""
        self.mock_firebase_instance.banco.reference.side_effect = Exception("Erro conexão")

        mock_logger_instance = MagicMock()
        self.mock_logger_class.return_value = mock_logger_instance
        
        repositorio = RepositorioEstoque(personagem=self.mock_personagem)
        
        mock_logger_instance.error.assert_called_once()
        assert repositorio._RepositorioEstoque__minhaReferencia is None
        assert repositorio._RepositorioEstoque__erro is not None

    def test_stream_handler_novo_trabalho(self):
        """Testa streamHandler para novo trabalho"""
        repositorio = RepositorioEstoque(personagem=self.mock_personagem)
        mensagem = {
            'event': 'put',
            'path': '/personagem123/trabalho456',
            'data': {
                CHAVE_ID: 'trabalho456',
                CHAVE_ID_TRABALHO: 'tipo789',
                CHAVE_QUANTIDADE: 5
            }
        }
        
        repositorio.streamHandler(mensagem)
        
        self.mock_stream.return_value.insereDadosModificados.assert_called_once()
        args = self.mock_stream.return_value.insereDadosModificados.call_args[0][0]
        assert args[CHAVE_ID_PERSONAGEM] == 'personagem123'
        assert isinstance(args[CHAVE_TRABALHOS], TrabalhoEstoque)

    def test_stream_handler_remove_trabalho(self):
        """Testa streamHandler para remoção de trabalho"""
        repositorio = RepositorioEstoque(personagem=self.mock_personagem)
        mensagem = {
            'event': 'put',
            'path': '/personagem123/trabalho456',
            'data': None
        }
        
        repositorio.streamHandler(mensagem)
        
        self.mock_stream.return_value.insereDadosModificados.assert_called_once()
        args = self.mock_stream.return_value.insereDadosModificados.call_args[0][0]
        assert args[CHAVE_ID_PERSONAGEM] == 'personagem123'
        assert args[CHAVE_TRABALHOS].id == 'trabalho456'

    def test_pega_todos_trabalhos_vazio(self):
        """Testa pegaTodosTrabalhosEstoque com estoque vazio"""
        repositorio = RepositorioEstoque(personagem=self.mock_personagem)
        self.mock_personagem_ref.get.return_value = None
        
        resultado = repositorio.pegaTodosTrabalhosEstoque()
        
        assert resultado == []
        assert repositorio._RepositorioEstoque__erro is None

    def test_pega_todos_trabalhos_com_dados(self):
        """Testa pegaTodosTrabalhosEstoque com dados"""
        repositorio = RepositorioEstoque(personagem=self.mock_personagem)
        dados_teste = {
            'trabalho1': {
                CHAVE_ID: 'trabalho1',
                CHAVE_ID_TRABALHO: 'tipo1',
                CHAVE_QUANTIDADE: 3
            }
        }
        self.mock_personagem_ref.get.return_value = dados_teste
        
        resultado = repositorio.pegaTodosTrabalhosEstoque()
        
        assert len(resultado) == 1
        assert isinstance(resultado[0], TrabalhoEstoque)
        assert resultado[0].id == 'trabalho1'

    def test_pega_todos_trabalhos_com_erro(self):
        """Testa pegaTodosTrabalhosEstoque com erro"""
        repositorio = RepositorioEstoque(personagem=self.mock_personagem)
        self.mock_personagem_ref.get.side_effect = HTTPError("Erro de conexão")
        
        resultado = repositorio.pegaTodosTrabalhosEstoque()
        
        assert resultado is None
        assert repositorio._RepositorioEstoque__erro is not None

    def test_insere_trabalho_novo(self):
        """Testa insereTrabalhoEstoque para novo trabalho"""
        repositorio = RepositorioEstoque(personagem=self.mock_personagem)
        self.mock_personagem_ref.get.return_value = None
        
        trabalho = TrabalhoEstoque()
        trabalho.id = "novo_trabalho"
        trabalho.idTrabalho = "tipo1"
        trabalho.quantidade = 5
        
        resultado = repositorio.insereTrabalhoEstoque(trabalho)
        
        assert resultado is True
        self.mock_personagem_ref.child.assert_called_with("novo_trabalho")
        self.mock_personagem_ref.child.return_value.set.assert_called_once()

    def test_modifica_trabalho(self):
        """Testa modificaTrabalhoEstoque"""
        repositorio = RepositorioEstoque(personagem=self.mock_personagem)
        
        trabalho = TrabalhoEstoque()
        trabalho.id = "trabalho1"
        trabalho.idTrabalho = "tipo1"
        trabalho.quantidade = 10
        
        resultado = repositorio.modificaTrabalhoEstoque(trabalho)
        
        assert resultado is True
        self.mock_personagem_ref.child.assert_called_with("trabalho1")
        self.mock_personagem_ref.child.return_value.update.assert_called_once()

    def test_remove_trabalho(self):
        """Testa removeTrabalho"""
        repositorio = RepositorioEstoque(personagem=self.mock_personagem)
        
        trabalho = TrabalhoEstoque()
        trabalho.id = "trabalho1"
        
        resultado = repositorio.removeTrabalho(trabalho)
        
        assert resultado is True
        self.mock_personagem_ref.child.assert_called_with("trabalho1")
        self.mock_personagem_ref.child.return_value.delete.assert_called_once()

    def test_pega_erro(self):
        """Testa pegaErro"""
        repositorio = RepositorioEstoque(personagem=self.mock_personagem)
        repositorio._RepositorioEstoque__erro = "erro_teste"
        
        assert repositorio.pegaErro() == "erro_teste"