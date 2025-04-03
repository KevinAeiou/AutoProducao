import pytest
from modelos.usuario import Usuario
from modelos.personagem import Personagem

class TestPersonagem:
    def test_init(self):
        personagem = Personagem()
        assert personagem.email is None
        assert personagem.senha is None
        assert personagem.espacoProducao == 1
        assert personagem.estado is False
        assert personagem.uso is False
        assert personagem.autoProducao is False
    
    def test_setEspacoProducao(self):
        personagem = Personagem()
        personagem.setEspacoProducao(5)
        assert personagem.espacoProducao == 5
        personagem.setEspacoProducao("10")
        assert personagem.espacoProducao == 10
    
    def test_ehAtivo(self):
        personagem = Personagem()
        assert personagem.ehAtivo is False
        personagem.estado = True
        assert personagem.ehAtivo is True
    
    def test_alternaUso(self):
        personagem = Personagem()
        assert personagem.uso is False
        personagem.alternaUso
        assert personagem.uso is True
        personagem.alternaUso
        assert personagem.uso is False
    
    def test_alternaEstado(self):
        personagem = Personagem()
        assert personagem.estado is False
        personagem.alternaEstado
        assert personagem.estado is True
        personagem.alternaEstado
        assert personagem.estado is False
    
    def test_alternaAutoProducao(self):
        personagem = Personagem()
        assert personagem.autoProducao is False
        personagem.alternaAutoProducao
        assert personagem.autoProducao is True
        personagem.alternaAutoProducao
        assert personagem.autoProducao is False
    
    def test_dicionarioParaObjeto(self):
        personagem = Personagem()
        dados = {
            'email': 'teste@teste.com',
            'senha': '123456',
            'espacoProducao': 3,
            'estado': True,
            'uso': True,
            'autoProducao': True,
            'nome': 'Personagem Teste',
            'id': 1
        }
        personagem.dicionarioParaObjeto(dados)
        assert personagem.email == 'teste@teste.com'
        assert personagem.senha == '123456'
        assert personagem.espacoProducao == 3
        assert personagem.estado is True
        assert personagem.uso is True
        assert personagem.autoProducao is True
        assert personagem.nome == 'Personagem Teste'
        assert personagem.id == 1
    
    def test_str(self):
        personagem = Personagem()
        personagem.id = "abc"
        personagem.nome = "Teste"
        personagem.espacoProducao = 2
        personagem.estado = True
        personagem.uso = False
        personagem.autoProducao = True
        
        expected_output = "abc                                  | Teste             | 2      | Verdadeiro | Falso      | Verdadeiro"
        assert str(personagem) == expected_output
        
        personagem2 = Personagem()
        personagem2.id = None
        expected_output2 = "Indefinido                           | Indefinido        | 1      | Falso      | Falso      | Falso     "
        assert str(personagem2) == expected_output2