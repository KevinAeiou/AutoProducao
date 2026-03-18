from modelos.personagem import Personagem
from dao.personagemDaoSqlite import PersonagemDaoSqlite
from db.db import MeuBanco
from modelos.logger import MeuLogger
from visao.reconhecimento_texto import ReconhecimentoTexto
from visao.reconhecimento_tela import ReconhecimentoTela
from automacao.teclado import ManipulaTeclado
from automacao.mouse import ManipulaMouse
from utilitarios import ehMenuRecompensasDiarias, limpa_tela

logger: MeuLogger = MeuLogger(nome='recompensa_service')
class RecompensaService():

	def __init__(self) -> None:
		banco_ref: MeuBanco = MeuBanco()
		banco_ref.pega_conexao()
		banco_ref.cria_tabelas()
		self.personagem_dao: PersonagemDaoSqlite = PersonagemDaoSqlite(banco_ref)
		self.personagens_verificados: list[Personagem] = []
		self.reconhecimento_texto: ReconhecimentoTexto = ReconhecimentoTexto()
		self.reconhecimento_tela: ReconhecimentoTela = ReconhecimentoTela()
		self.manipula_teclado: ManipulaTeclado = ManipulaTeclado()
		self.manipula_mouse: ManipulaMouse = ManipulaMouse()

	def buscar_personagem_disponivel(self) -> Personagem | None:
		personagens_ativos: list[Personagem] = self.personagem_dao.pegaPersonagens()
		emails_verificados = {p.email for p in self.personagens_verificados}

		personagens_disponiveis = [
			p for p in personagens_ativos
			if p.email not in emails_verificados
		]

		if not personagens_disponiveis:
			return None

		personagem = personagens_disponiveis[0]
		self.personagens_verificados.append(personagem)

		return personagem

	def inicia_coleta(self, personagem: Personagem):
		limpa_tela()

		logger.info(f'Iniciando coleta para {personagem.nome} | {personagem.email}')

		nome_personagem: str | None = self.reconhecimento_texto.reconhecer_nome_personagem()

		if not nome_personagem:
			logger.warning('Não foi possível reconhecer o personagem atual.')
			return
		
		logger.debug(f'NOME_RECONHECIDO: {nome_personagem}')

		if nome_personagem == str(personagem.nome).lower():
			self.reconhecimento_tela.reconhece_menu_atual()

			if self.reconhecimento_tela.eh_menu_recompensas_diarias:		
				for _ in range(2):
					logger.debug(f'Buscando botão "Pegar".')

					referencia: tuple | None = self.reconhecimento_tela.retorna_coordenadas_botao_pegar()
					if referencia is not None:
						self.manipula_mouse.clica(x=referencia[0], y=referencia[1])

					self.manipula_teclado.preciona_tecla(tecla='up', cliques=10)
					self.manipula_teclado.clica_tecla(tecla='left')

				self.manipula_teclado.clica_tecla(tecla='f1', cliques=2)