from services.recompensa_service import RecompensaService
from modelos.personagem import Personagem

class RecompensaWorkFlow():

	def __init__(self) -> None:
		self.verificado: bool = False
		self.service: RecompensaService = RecompensaService()

	def executar(self):
		personagem: Personagem | None = self.service.buscar_personagem_disponivel()

		if not personagem:
			return
		
		while personagem:
			self.service.inicia_coleta(personagem)
			personagem = self.service.buscar_personagem_disponivel()

		self.verificado = True

	def precisa_coletar(self):

		return not self.verificado