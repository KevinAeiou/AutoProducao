from workflows.workflow_recompensa import RecompensaWorkFlow

class Bot:

	def __init__(self) -> None:
		self.recompensa: RecompensaWorkFlow = RecompensaWorkFlow()
		pass

	def executar(self):

		if self.recompensa.precisa_coletar():
			self.recompensa.executar()
		pass