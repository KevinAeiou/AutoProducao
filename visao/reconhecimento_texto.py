from visao.manipulador_imagem import ManipuladorImagem
from modelos.logger import MeuLogger

logger: MeuLogger = MeuLogger(nome='reconhecimento_texto')

class ReconhecimentoTexto():

	def __init__(self) -> None:
		self.manipulador_imagem: ManipuladorImagem = ManipuladorImagem(debug=True)
		
	def reconhecer_nome_personagem(self) -> str | None:
		nome_reconhecido = None

		for indice in range(0, 2):
			nome_reconhecido: str | None = self.manipulador_imagem.reconhece_texto_nome_personagem(posicao=indice)
			if nome_reconhecido:
				break
			
		return nome_reconhecido