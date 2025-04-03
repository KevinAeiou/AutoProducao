import pytest
from unittest.mock import patch, MagicMock, call
import firebase_admin
from firebase_admin import credentials, db
from modelos.logger import MeuLogger
from repositorio.firebaseDatabase import FirebaseDatabase

class TestFirebaseDatabase:
    """Testes para a classe FirebaseDatabase"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Configuração inicial para todos os testes"""
        # Mocks para as dependências externas
        self.firebase_patcher = patch('firebase_admin.initialize_app')
        self.cred_patcher = patch('firebase_admin.credentials.Certificate')
        self.logger_patcher = patch('modelos.logger.MeuLogger')
        
        self.mock_firebase_init = self.firebase_patcher.start()
        self.mock_cred = self.cred_patcher.start()
        self.mock_logger_class = self.logger_patcher.start()
        
        # Mock da instância do logger
        self.mock_logger_instance = MagicMock()
        self.mock_logger_class.return_value = self.mock_logger_instance
        
        # Mock para db (simulando o módulo)
        self.db_patcher = patch('firebase_admin.db', autospec=True)
        self.mock_db = self.db_patcher.start()
        
        # Reset do singleton entre testes
        FirebaseDatabase._FirebaseDatabase__instancia = None
        
        yield
        
        # Limpeza dos patches
        self.firebase_patcher.stop()
        self.cred_patcher.stop()
        self.logger_patcher.stop()
        self.db_patcher.stop()

    def test_singleton(self):
        """Testa se o padrão Singleton está funcionando corretamente"""
        instance1 = FirebaseDatabase()
        instance2 = FirebaseDatabase()
        
        assert instance1 is instance2

    def test_inicializacao_sucesso(self):
        """Testa inicialização bem-sucedida do Firebase"""
        instance = FirebaseDatabase()
        
        # Verifica chamadas de inicialização
        self.mock_cred.assert_called_once_with(
            r'repositorio\credenciais\bootwarspear-firebase-adminsdk-it84w-3832600b85.json'
        )
        self.mock_firebase_init.assert_called_once_with(
            credential=self.mock_cred.return_value,
            options={'databaseURL': 'https://bootwarspear-default-rtdb.firebaseio.com/'}
        )
        
        # Verifica logs
        self.mock_logger_instance.info.assert_called_once_with(
            menssagem='Conexão com Firebase estabelecida com sucesso.'
        )
        assert instance.banco is not None

    def test_inicializacao_falha(self):
        """Testa inicialização com falha"""
        # Configura para lançar exceção
        self.mock_firebase_init.side_effect = Exception("Erro de conexão")
        
        with pytest.raises(Exception):
            instance = FirebaseDatabase()
        
        # Verifica log de erro
        self.mock_logger_instance.error.assert_called_once_with(
            menssagem='Falha na inicialização do Firebase: Erro de conexão'
        )
        assert instance._FirebaseDatabase__erro is not None

    def test_propriedade_banco(self):
        """Testa a propriedade banco"""
        instance = FirebaseDatabase()
        
        # Primeira chamada
        result = instance.banco
        assert result == self.mock_db
        
        # Verifica log
        self.mock_logger_instance.info.assert_called_with(
            menssagem='Conexão com Firebase estabelecida com sucesso.'
        )
        
        # Segunda chamada (deve usar cache)
        result2 = instance.banco
        assert result2 == self.mock_db
        assert self.mock_logger_instance.info.call_count == 2

    def test_propriedade_banco_com_erro(self):
        """Testa propriedade banco quando há erro"""
        # Configura para lançar exceção
        self.mock_db.side_effect = Exception("Erro de banco")
        
        instance = FirebaseDatabase()
        with pytest.raises(Exception) as exc_info:
            _ = instance.banco
    
        # Verifica a mensagem de erro
        assert str(exc_info.value) == "Erro de banco"
        
        # Verifica se o erro foi registrado
        self.mock_logger_instance.error.assert_called_once_with(
            menssagem='Erro ao obter referência do banco: Erro de banco'
        )
        
        # Verifica se o erro foi armazenado
        assert instance.pegaErro() is not None

    def test_pega_erro(self):
        """Testa o método pegaErro"""
        instance = FirebaseDatabase()
        
        # Sem erro
        assert instance.pegaErro() is None
        
        # Com erro
        test_error = Exception("Erro teste")
        instance._FirebaseDatabase__erro = test_error
        assert instance.pegaErro() is test_error