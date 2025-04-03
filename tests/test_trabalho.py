import pytest
from uuid import UUID
from modelos.trabalho import Trabalho
from constantes import (
    CHAVE_ID,
    CHAVE_NOME,
    CHAVE_NOME_PRODUCAO,
    CHAVE_EXPERIENCIA,
    CHAVE_NIVEL,
    CHAVE_PROFISSAO,
    CHAVE_RARIDADE,
    CHAVE_TRABALHO_NECESSARIO,
    CHAVE_PROFISSAO_ANEIS,
    CHAVE_RARIDADE_RARO,
    CHAVE_RARIDADE_COMUM,
    CHAVE_RARIDADE_MELHORADO,
    CHAVE_PROFISSAO_ARMA_DE_LONGO_ALCANCE
)

class TestTrabalho:
    @pytest.fixture
    def trabalho(self):
        '''
            Fixture para criar uma instância limpa de Trabalho para cada teste
        '''
        return Trabalho()

    @pytest.fixture
    def dados_trabalho(self):
        '''
            Dados completos para teste de carregamento
        '''
        return {
            CHAVE_NOME: 'Ferraria Avançada',
            CHAVE_NOME_PRODUCAO: 'Espada Longa',
            CHAVE_EXPERIENCIA: 1500,
            CHAVE_NIVEL: 10,
            CHAVE_PROFISSAO: CHAVE_PROFISSAO_ANEIS,
            CHAVE_RARIDADE: CHAVE_RARIDADE_MELHORADO,
            CHAVE_TRABALHO_NECESSARIO: 'Forja Básica'
        }

    def test_init_deve_criar_trabalho_com_valores_padrao(self, trabalho):
        '''
            Testa a inicialização com valores padrão
        '''
        assert trabalho.nome is None
        assert trabalho.nomeProducao is None
        assert trabalho.experiencia is None
        assert trabalho.nivel is None
        assert trabalho.profissao is None
        assert trabalho.raridade is None
        assert trabalho.trabalhoNecessario is None
        # Verifica se o ID é um UUID válido
        UUID(trabalho.id, version=4)

    @pytest.mark.parametrize("nivel_profissao,nivel_esperado", [
        (1, 1), (2, 10), (3, 10), (4, 12), (5, 12), (6, 14), (7, 14),
        (8, 8), (9, 16), (10, 16), (11, 18), (12, 18), (13, 20), (14, 20),
        (15, 22), (16, 22), (17, 24), (18, 24), (19, 26), (20, 26),
        (21, 28), (22, 28), (23, 30), (24, 30), (25, 32), (26, 32),
        (27, 1), (100, 1)  # Testa valores fora do range definido
    ])
    def test_pegaNivel_deve_retornar_nivel_correto(self, trabalho, nivel_profissao, nivel_esperado):
        '''
            Testa o cálculo do nível baseado no nível da profissão
        '''
        assert trabalho.pegaNivel(nivel_profissao) == nivel_esperado

    @pytest.mark.parametrize("nivel,profissao,quantidade_esperada", [
        (9, "Outra Profissão", 0),
        (10, "Outra Profissão", 2), (16, "Outra Profissão", 2),
        (12, "Outra Profissão", 4), (18, "Outra Profissão", 4),
        (14, "Outra Profissão", 6), (20, "Outra Profissão", 6),
        (22, "Outra Profissão", 8), (24, "Outra Profissão", 10),
        (26, "Outra Profissão", 12), (28, "Outra Profissão", 14),
        (30, "Outra Profissão", 16), (32, "Outra Profissão", 18),
        (10, CHAVE_PROFISSAO_ARMA_DE_LONGO_ALCANCE, 3),
        (16, CHAVE_PROFISSAO_ARMA_DE_LONGO_ALCANCE, 3),
        (32, CHAVE_PROFISSAO_ARMA_DE_LONGO_ALCANCE, 19)
    ])
    def test_pegaQuantidadeRecursosNecessarios(self, trabalho, nivel, profissao, quantidade_esperada):
        '''
            Testa o cálculo de recursos necessários
        '''
        trabalho.nivel = nivel
        trabalho.profissao = profissao
        assert trabalho.pegaQuantidadeRecursosNecessarios() == quantidade_esperada

    @pytest.mark.parametrize("raridade,eh_comum,eh_melhorado,eh_raro", [
        (CHAVE_RARIDADE_COMUM, True, False, False),
        (CHAVE_RARIDADE_MELHORADO, False, True, False),
        (CHAVE_RARIDADE_RARO, False, False, True),
        ("Outra Raridade", False, False, False),
        (None, False, False, False)
    ])
    def test_metodos_raridade(self, trabalho, raridade, eh_comum, eh_melhorado, eh_raro):
        '''
            Testa os métodos que verificam a raridade
        '''
        trabalho.raridade = raridade
        assert trabalho.ehComum() == eh_comum
        assert trabalho.ehMelhorado() == eh_melhorado
        assert trabalho.ehRaro() == eh_raro

    def test_dicionarioParaObjeto_deve_carregar_todos_os_campos(self, trabalho, dados_trabalho):
        '''
            Testa o carregamento de dados a partir de um dicionário
        '''
        trabalho.dicionarioParaObjeto(dados_trabalho)
        assert trabalho.nome == dados_trabalho[CHAVE_NOME]
        assert trabalho.nomeProducao == dados_trabalho[CHAVE_NOME_PRODUCAO]
        assert trabalho.experiencia == dados_trabalho[CHAVE_EXPERIENCIA]
        assert trabalho.nivel == dados_trabalho[CHAVE_NIVEL]
        assert trabalho.profissao == dados_trabalho[CHAVE_PROFISSAO]
        assert trabalho.raridade == dados_trabalho[CHAVE_RARIDADE]
        assert trabalho.trabalhoNecessario == dados_trabalho[CHAVE_TRABALHO_NECESSARIO]
        assert hasattr(trabalho, CHAVE_ID)

    def test_dicionarioParaObjeto_com_none_nao_deve_alterar_objeto(self, trabalho):
        '''
            Testa o comportamento quando o dicionário é None
        '''
        trabalho.nome = "Original"
        trabalho.dicionarioParaObjeto(None)
        assert trabalho.nome == "Original"

    def test_str_deve_retornar_representacao_formatada(self, trabalho, dados_trabalho):
        '''
            Testa a representação em string do trabalho
        '''
        trabalho.dicionarioParaObjeto(dados_trabalho)
        output = str(trabalho)
        assert dados_trabalho[CHAVE_NOME] in output
        assert dados_trabalho[CHAVE_PROFISSAO] in output
        assert dados_trabalho[CHAVE_RARIDADE] in output
        assert str(dados_trabalho[CHAVE_NIVEL]) in output
        trabalho2 = Trabalho()
        output2 = str(trabalho2)
        assert "Indefinido" in output2
        assert "Indefinido" in output2