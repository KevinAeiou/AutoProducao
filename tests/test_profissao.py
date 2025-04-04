import pytest
from uuid import UUID
from modelos.profissao import Profissao
from constantes import LISTA_EXPERIENCIAS_NIVEL

class TestProfissao:
    @pytest.fixture
    def profissao(self):
        """Fixture para criar uma instância limpa de Profissao para cada teste"""
        return Profissao()

    @pytest.fixture
    def dados_profissao(self):
        """Dados completos para teste de carregamento"""
        return {
            'idPersonagem': 'personagem123',
            'nome': 'Guerreiro',
            'experiencia': 1500,
            'prioridade': True
        }

    def test_init_deve_criar_profissao_com_valores_padrao(self, profissao):
        """Testa a inicialização com valores padrão"""
        assert profissao.idPersonagem is None
        assert profissao.nome is None
        assert profissao.experiencia == 0
        assert profissao.prioridade is False
        # Verifica se o ID é um UUID válido
        UUID(profissao.id, version=4)

    def test_pegaExperienciaMaxima_deve_retornar_ultimo_item_da_lista(self):
        """Testa o método que retorna a experiência máxima"""
        profissao = Profissao()
        assert profissao.pegaExperienciaMaxima == LISTA_EXPERIENCIAS_NIVEL[-1]

    @pytest.mark.parametrize("exp_input,exp_expected", [
        (100, 100),
        ("500", 500),
        (999999, LISTA_EXPERIENCIAS_NIVEL[-1]),  # Testa valor acima do máximo
        (0, 0),
        (-100, 0)  # Testa valor negativo
    ])
    def test_setExperiencia_deve_configurar_valor_corretamente(self, profissao, exp_input, exp_expected):
        """Testa a configuração da experiência com diferentes valores"""
        profissao.setExperiencia(exp_input)
        assert profissao.experiencia == exp_expected

    def test_alternaPrioridade_deve_inverter_valor_atual(self, profissao):
        """Testa a alternância da prioridade"""
        estado_inicial = profissao.prioridade
        profissao.alternaPrioridade()
        assert profissao.prioridade is not estado_inicial
        profissao.alternaPrioridade()
        assert profissao.prioridade is estado_inicial

    @pytest.mark.parametrize("exp,nivel_esperado", [
        (0, 1),
        (LISTA_EXPERIENCIAS_NIVEL[0] - 1, 1),
        (LISTA_EXPERIENCIAS_NIVEL[0], 2),
        (LISTA_EXPERIENCIAS_NIVEL[1] - 1, 2),
        (LISTA_EXPERIENCIAS_NIVEL[1], 3),
        (LISTA_EXPERIENCIAS_NIVEL[-1], len(LISTA_EXPERIENCIAS_NIVEL) + 1),
        (LISTA_EXPERIENCIAS_NIVEL[-1] + 1000, len(LISTA_EXPERIENCIAS_NIVEL) + 1)
    ])
    def test_pegaNivel_deve_retornar_nivel_correto(self, profissao, exp, nivel_esperado):
        """Testa o cálculo do nível baseado na experiência"""
        profissao.experiencia = exp
        assert profissao.pegaNivel() == nivel_esperado

    @pytest.mark.parametrize("exp,exp_max_esperada", [
        (0, LISTA_EXPERIENCIAS_NIVEL[0]),
        (LISTA_EXPERIENCIAS_NIVEL[0] - 1, LISTA_EXPERIENCIAS_NIVEL[0]),
        (LISTA_EXPERIENCIAS_NIVEL[0], LISTA_EXPERIENCIAS_NIVEL[1]),
        (LISTA_EXPERIENCIAS_NIVEL[1] - 1, LISTA_EXPERIENCIAS_NIVEL[1]),
        (LISTA_EXPERIENCIAS_NIVEL[-1], LISTA_EXPERIENCIAS_NIVEL[-1]),
        (LISTA_EXPERIENCIAS_NIVEL[-1] + 1000, LISTA_EXPERIENCIAS_NIVEL[-1])
    ])
    def test_pegaExperienciaMaximaPorNivel_deve_retornar_valor_correto(self, profissao, exp, exp_max_esperada):
        """Testa o cálculo da experiência máxima para o nível atual"""
        profissao.experiencia = exp
        assert profissao.pegaExperienciaMaximaPorNivel() == exp_max_esperada

    def test_dicionarioParaObjeto_deve_carregar_todos_os_campos(self, profissao, dados_profissao):
        """Testa o carregamento de dados a partir de um dicionário"""
        profissao.dicionarioParaObjeto(dados_profissao)
        
        assert profissao.idPersonagem == dados_profissao['idPersonagem']
        assert profissao.nome == dados_profissao['nome']
        assert profissao.experiencia == dados_profissao['experiencia']
        assert profissao.prioridade == dados_profissao['prioridade']
        # O ID original deve permanecer (não deve ser sobrescrito)
        assert hasattr(profissao, 'id')

    def test_str_deve_retornar_representacao_formatada(self, profissao, dados_profissao):
        """Testa a representação em string da profissão"""
        profissao.dicionarioParaObjeto(dados_profissao)
        output = str(profissao)
        
        assert dados_profissao['idPersonagem'] in output
        assert dados_profissao['nome'] in output
        assert str(dados_profissao['experiencia']) in output
        assert "Verdadeiro" in output  # Prioridade é True nos dados

        # Teste com valores padrão
        profissao2 = Profissao()
        output2 = str(profissao2)
        
        assert "Indefinido" in output2  # Para idPersonagem e nome
        assert "0" in output2  # Experiência padrão
        assert "Falso" in output2  # Prioridade padrão