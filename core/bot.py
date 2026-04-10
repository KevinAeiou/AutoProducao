from workflows.workflow_recompensa import RecompensaWorkFlow
from automacao.teclado import ManipulaTeclado
from modelos.logger import MeuLogger

logger: MeuLogger = MeuLogger(nome="bot")


class Bot:

	def __init__(self) -> None:
		self.recompensa: RecompensaWorkFlow = RecompensaWorkFlow()
		self.manipula_teclado: ManipulaTeclado = ManipulaTeclado()

		self.alternar_janela()

	def alternar_janela(self):
		logger.debug(f"CLIQUE_ALT_TAB")
		self.manipula_teclado.clica_atalho(tecla1="alt", tecla2="tab")

	def executar(self):

		if self.recompensa.precisa_coletar():
			self.recompensa.executar()
		pass
