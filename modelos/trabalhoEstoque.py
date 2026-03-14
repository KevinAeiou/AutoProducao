from modelos.trabalho import Trabalho

class TrabalhoEstoque(Trabalho):
	def __init__(self):
		super().__init__()
		self.idTrabalho = None
		self.quantidade = 0
	
	def setQuantidade(self, quantidade: int):
		quantidade = 0 if int(quantidade) < 0 else int(quantidade)
		self.quantidade = quantidade
	
	def dicionarioParaObjeto(self, dicionario):
		for chave in dicionario:
			setattr(self, chave, dicionario[chave])
			
	def decrementa_quantidade(self, quantidade: int):
		self.quantidade = 0 if self.quantidade - quantidade < 0 else self.quantidade - quantidade

	def __str__(self) -> str:
		id: str= 'Indefinido' if self.id == None else str(self.id)
		trabalhoId: str= 'Indefinido' if self.idTrabalho == None else str(self.idTrabalho)
		quantidade: str= str(self.quantidade)
		return f'{id.ljust(36)} | {trabalhoId.ljust(36)} | {quantidade.ljust(3)}'