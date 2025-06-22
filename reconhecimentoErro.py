from constantes import (
    CODIGO_ERRO_OUTRA_CONEXAO,
    CODIGO_ERRO_PRECISA_LICENCA,
    CODIGO_ERRO_FALHA_CONECTAR,
    CODIGO_ERRO_CONEXAO_INTERROMPIDA,
    CODIGO_ERRO_MANUTENCAO_SERVIDOR,
    CODIGO_ERRO_REINO_INDISPONIVEL,
    CODIGO_ERRO_RECURSOS_INSUFICIENTES,
    CODIGO_ERRO_TEMPO_PRODUCAO_EXPIRADA,
    CODIGO_ERRO_EXPERIENCIA_INSUFICIENTE,
    CODIGO_ERRO_ESPACO_PRODUCAO_INSUFICIENTE,
    CODIGO_FALHA_AO_INICIAR_CONEXAO,
    CODIGO_ERRO_ESCOLHA_ITEM_NECESSARIA,
    CODIGO_CONECTANDO,
    CODIGO_RESTAURA_CONEXAO,
    CODIGO_RECEBER_RECOMPENSA,
    CODIGO_ERRO_ATUALIZACAO_JOGO,
    CODIGO_ERRO_CONCLUIR_TRABALHO,
    CODIGO_ERRO_ESPACO_BOLSA_INSUFICIENTE,
    CODIGO_ERRO_MOEDAS_MILAGROSAS_INSUFICIENTES,
    CODIGO_ITEM_A_VENDA,
    CODIGO_ERRO_USUARIO_SENHA_INVALIDA,
    CODIGO_SAIR_JOGO,
    CODIGO_ERRO_USA_OBJETO_PARA_PRODUZIR
)
from teclado import click_especifico, preciona_tecla
from time import sleep
from utilitarios import retorna_codigo_erro_reconhecido
from modelos.logger import MeuLogger

class ReconhecimentoErro():
    """Classe base para reconhecimento de erros."""
    def __init__(self, texto_erro_encontrado: str = ''):
        self.__logger_verifica_erro: MeuLogger= MeuLogger(nome= 'reconhecimentoErro')
        self._erro = texto_erro_encontrado

    def get_codigo_erro(self) -> int:
        """Retorna o erro reconhecido a partir do texto de erro encontrado."""
        return retorna_codigo_erro_reconhecido(self._erro)
    
    def atualiza_texto_erro(self, texto_erro_encontrado: str):
        """Atualiza o texto de erro encontrado."""
        self._erro = texto_erro_encontrado

    @property
    def eh_erro_outra_conexao(self) -> bool:
        '''
            Verifica se o erro é Outra Conexão Encontrada.    
            Returns:
                bool: True se o código de erro corresponder a CODIGO_ERRO_OUTRA_CONEXAO,
                    False caso contrário.
            Side Effects:
                Registra uma mensagem de debug no logger quando detectado o erro é Outra Conexão Encontrada.
        '''
        eh_outra_conexao: bool = self.get_codigo_erro() == CODIGO_ERRO_OUTRA_CONEXAO
        if eh_outra_conexao:
            self.__logger_verifica_erro.debug(mensagem= 'Reconhecido erro Outra Conexão.')
        return eh_outra_conexao

    @property
    def eh_erro_licenca_necessaria(self):
        """Verifica se o erro é de licença necessária."""
        eh_licenca_necessaria: bool = self.get_codigo_erro() == CODIGO_ERRO_PRECISA_LICENCA
        if eh_licenca_necessaria:
            self.__logger_verifica_erro.debug(mensagem= 'Reconhecido erro Licença necessária.')
        return eh_licenca_necessaria
    
    @property
    def eh_erro_falha_conexao(self):
        """Verifica se o erro é de falha de conexão."""
        eh_falha_conexao: bool = self.get_codigo_erro() == CODIGO_ERRO_FALHA_CONECTAR
        if eh_falha_conexao:
            self.__logger_verifica_erro.debug(mensagem= 'Reconhecido erro Falha na conexão.')
        return eh_falha_conexao
    
    @property
    def eh_erro_conexao_interrompida(self):
        """Verifica se o erro é de conexão interrompida."""
        eh_conexao_interrompida: bool = self.get_codigo_erro() == CODIGO_ERRO_CONEXAO_INTERROMPIDA
        if eh_conexao_interrompida:
            self.__logger_verifica_erro.debug(mensagem= 'Reconhecido erro Falha na conexão.')
        return eh_conexao_interrompida
    
    @property
    def eh_erro_servidor_manutencao(self):
        """Verifica se o erro é de servidor em manutenção."""
        eh_servidor_manutencao: bool = self.get_codigo_erro() == CODIGO_ERRO_MANUTENCAO_SERVIDOR
        if eh_servidor_manutencao:
            self.__logger_verifica_erro.debug(mensagem= 'Reconhecido erro Servidor em manutenção.')
        return eh_servidor_manutencao
    
    @property
    def eh_erro_reino_indisponivel(self):
        """Verifica se o erro é de reino indisponível."""
        eh_reino_indisponivel: bool = self.get_codigo_erro() == CODIGO_ERRO_REINO_INDISPONIVEL
        if eh_reino_indisponivel:
            self.__logger_verifica_erro.debug(mensagem= 'Reconhecido erro Reino indisponível.')
        return eh_reino_indisponivel
    
    @property
    def eh_erro_recursos_insuficientes(self):
        """Verifica se o erro é de recursos insuficientes."""
        eh_recursos_insuficientes: bool = self.get_codigo_erro() == CODIGO_ERRO_RECURSOS_INSUFICIENTES
        if eh_recursos_insuficientes:
            self.__logger_verifica_erro.debug(mensagem= 'Reconhecido erro Recursos insuficientes.')
        return eh_recursos_insuficientes
    
    @property
    def eh_erro_tempo_producao_expirado(self):
        """Verifica se o erro é de tempo de produção expirado."""
        eh_tempo_expirado: bool = self.get_codigo_erro() == CODIGO_ERRO_TEMPO_PRODUCAO_EXPIRADA
        if eh_tempo_expirado:
            self.__logger_verifica_erro.debug(mensagem= 'Reconhecido erro Tempo de produção expirou.')
        return eh_tempo_expirado
    
    @property
    def eh_erro_experiencia_insuficiente(self):
        """Verifica se o erro é de experiência insuficiente."""
        eh_experiencia_insuficiente: bool = self.get_codigo_erro() == CODIGO_ERRO_EXPERIENCIA_INSUFICIENTE
        if eh_experiencia_insuficiente:
            self.__logger_verifica_erro.debug(mensagem= 'Reconhecido erro Experiência insuficiente.')
        return eh_experiencia_insuficiente
    
    @property
    def eh_erro_espaco_producao_insuficiente(self):
        """Verifica se o erro é de espaço de produção insuficiente."""
        eh_espaco_producao_insuficiente: bool = self.get_codigo_erro() == CODIGO_ERRO_ESPACO_PRODUCAO_INSUFICIENTE
        if eh_espaco_producao_insuficiente:
            self.__logger_verifica_erro.debug(mensagem= 'Reconhecido erro Espaço de produção insuficiente.')
        return eh_espaco_producao_insuficiente
    
    @property
    def eh_erro_falha_iniciar_conexao(self):
        """Verifica se o erro é de falha ao iniciar a conexão."""
        eh_falha_iniciar_conexao: bool = self.get_codigo_erro() == CODIGO_FALHA_AO_INICIAR_CONEXAO
        if eh_falha_iniciar_conexao:
            self.__logger_verifica_erro.debug(mensagem= 'Reconhecido erro Falha ao iniciar a conexão.')
        return eh_falha_iniciar_conexao
    
    @property
    def eh_erro_escolha_item_necessaria(self):
        """Verifica se o erro é de escolha de item necessária."""
        eh_escolha_item_necessaria: bool = self.get_codigo_erro() == CODIGO_ERRO_ESCOLHA_ITEM_NECESSARIA
        if eh_escolha_item_necessaria:
            self.__logger_verifica_erro.debug(mensagem= 'Reconhecido erro Escolha de item necessária.')
        return eh_escolha_item_necessaria
    
    @property
    def eh_erro_conectando(self):
        """Verifica se o erro é de conectando."""
        eh_conectando: bool = self.get_codigo_erro() == CODIGO_CONECTANDO
        if eh_conectando:
            self.__logger_verifica_erro.debug(mensagem= 'Reconhecido erro Conectando.')
        return eh_conectando
    
    @property
    def eh_erro_restaura_conexao(self):
        """Verifica se o erro é de restauração de conexão."""
        eh_restaurando_conexao: bool = self.get_codigo_erro() == CODIGO_RESTAURA_CONEXAO
        if eh_restaurando_conexao:
            self.__logger_verifica_erro.debug(mensagem= 'Reconhecido erro Restaurando conexão.')
        return eh_restaurando_conexao
    
    @property
    def eh_erro_receber_recompensa_diaria(self):
        """Verifica se o erro é de receber recompensa diária."""
        eh_recompensa_diaria: bool = self.get_codigo_erro() == CODIGO_RECEBER_RECOMPENSA
        if eh_recompensa_diaria:
            self.__logger_verifica_erro.debug(mensagem= 'Reconhecido erro Receber recompensa diária.')
        return eh_recompensa_diaria
    
    @property
    def eh_erro_versao_jogo_desatualizada(self):
        """Verifica se o erro é de versão do jogo desatualizada."""
        eh_versao_desatualizada: bool = self.get_codigo_erro() == CODIGO_ERRO_ATUALIZACAO_JOGO
        if eh_versao_desatualizada:
            self.__logger_verifica_erro.debug(mensagem= 'Reconhecido erro Versão do jogo está desatualizada.')
        return eh_versao_desatualizada
    
    @property
    def eh_erro_trabalho_nao_concluido(self):
        """Verifica se o erro é de trabalho não concluído."""
        eh_trabalho_nao_concluido: bool = self.get_codigo_erro() == CODIGO_ERRO_CONCLUIR_TRABALHO
        if eh_trabalho_nao_concluido:
            self.__logger_verifica_erro.debug(mensagem= 'Reconhecido erro Trabalho não concluído.')
        return eh_trabalho_nao_concluido
    
    @property
    def eh_erro_espaco_bolsa_insuficiente(self):
        """Verifica se o erro é de espaço na bolsa insuficiente."""
        eh_espaco_bolsa_insuficiente: bool = self.get_codigo_erro() == CODIGO_ERRO_ESPACO_BOLSA_INSUFICIENTE
        if eh_espaco_bolsa_insuficiente:
            self.__logger_verifica_erro.debug(mensagem= 'Reconhecido erro Espaço na bolsa insuficiente.')
        return eh_espaco_bolsa_insuficiente
    
    @property
    def eh_erro_moedas_milagrosas_insuficientes(self):
        """Verifica se o erro é de moedas milagrosas insuficientes."""
        eh_moedas_insuficientes: bool = self.get_codigo_erro() == CODIGO_ERRO_MOEDAS_MILAGROSAS_INSUFICIENTES
        if eh_moedas_insuficientes:
            self.__logger_verifica_erro.debug(mensagem= 'Reconhecido erro Moedas milagrosas insuficientes.')
        return eh_moedas_insuficientes
    
    @property
    def eh_erro_item_avenda(self):
        """Verifica se o erro é de item à venda."""
        eh_item_venda: bool = self.get_codigo_erro() == CODIGO_ITEM_A_VENDA
        if eh_item_venda:
            self.__logger_verifica_erro.debug(mensagem= 'Reconhecido erro Item à venda.')
        return eh_item_venda
    
    @property
    def eh_erro_usuario_ou_senha_invalida(self):
        """Verifica se o erro é de usuário ou senha inválida."""
        eh_usuario_senha_invalida: bool = self.get_codigo_erro() == CODIGO_ERRO_USUARIO_SENHA_INVALIDA
        if eh_usuario_senha_invalida:
            self.__logger_verifica_erro.debug(mensagem= 'Reconhecido erro Usuário ou senha inválidos.')
        return eh_usuario_senha_invalida
    
    @property
    def eh_erro_sair_jogo(self):
        """Verifica se o erro é de sair do jogo."""
        eh_sair_jogo: bool = self.get_codigo_erro() == CODIGO_SAIR_JOGO
        if eh_sair_jogo:
            self.__logger_verifica_erro.debug(mensagem= 'Reconhecido erro Sair do jogo.')
        return eh_sair_jogo
    
    @property
    def eh_erro_usa_objeto_produzir(self):
        """Verifica se o erro é de usar objeto para produzir."""
        eh_usa_objeto: bool = self.get_codigo_erro() == CODIGO_ERRO_USA_OBJETO_PARA_PRODUZIR
        if eh_usa_objeto:
            self.__logger_verifica_erro.debug(mensagem= 'Reconhecido erro Usa ojeto para produzir.')
        return eh_usa_objeto
    
class VerificacaoErro(ReconhecimentoErro):
    """Classe para verificar erros específicos."""
    def __init__(self, texto_erro_encontrado: str = ''):
        super().__init__(texto_erro_encontrado)
    
    def verifica_erro(self) -> bool:
        '''
            Verifica se existe algum tipo de erro na tela.
            Returns:
                bool: Verdadeiro caso seja reconhecido pelo menos um erro em tela. Falso caso contrário.
        '''
        if self.eh_erro_licenca_necessaria or self.eh_erro_falha_conexao or self.eh_erro_conexao_interrompida or self.eh_erro_servidor_manutencao or self.eh_erro_reino_indisponivel:
            click_especifico(cliques= 2, tecla_especifica= 'enter')
            return True
        if self.eh_erro_outra_conexao or self.eh_erro_recursos_insuficientes or self.eh_erro_tempo_producao_expirado or self.eh_erro_experiencia_insuficiente or self.eh_erro_espaco_producao_insuficiente or self.eh_erro_falha_iniciar_conexao:
            click_especifico(cliques= 1, tecla_especifica= 'enter')
            if self.eh_erro_outra_conexao or self.eh_erro_falha_iniciar_conexao:
                return True
            click_especifico(cliques= 2, tecla_especifica= 'f1')
            preciona_tecla(cliques= 9, teclaEspecifica= 'up')
            click_especifico(cliques= 1, tecla_especifica= 'left')
            return True
        if self.eh_erro_escolha_item_necessaria:
            click_especifico(cliques= 1, tecla_especifica= 'enter')
            click_especifico(cliques= 1, tecla_especifica= 'f2')
            preciona_tecla(cliques= 9, teclaEspecifica= 'up')
            return True
        if self.eh_erro_conectando or self.eh_erro_restaura_conexao:
            sleep(1)
            return True
        if self.eh_erro_receber_recompensa_diaria or self.eh_erro_versao_jogo_desatualizada or self.eh_erro_usa_objeto_produzir or self.eh_erro_sair_jogo:
            click_especifico(cliques= 1, tecla_especifica= 'f2')
            if self.eh_erro_versao_jogo_desatualizada:
                click_especifico(cliques= 1, tecla_especifica= 'f1')
                exit()
                return True
            return True
        if self.eh_erro_trabalho_nao_concluido:
            click_especifico(cliques= 1, tecla_especifica= 'f1')
            preciona_tecla(cliques= 8, teclaEspecifica= 'up')
            return True
        if self.eh_erro_espaco_bolsa_insuficiente:
            click_especifico(cliques= 1, tecla_especifica= 'f1')
            preciona_tecla(cliques= 8, teclaEspecifica= 'up')
            return True
        if self.eh_erro_moedas_milagrosas_insuficientes or self.eh_erro_item_avenda:
            click_especifico(cliques= 1, tecla_especifica= 'f1')
            return True
        if self.eh_erro_usuario_ou_senha_invalida:
            click_especifico(cliques= 1, tecla_especifica= 'enter')
            click_especifico(cliques= 1, tecla_especifica= 'f1')
            return True
        return False