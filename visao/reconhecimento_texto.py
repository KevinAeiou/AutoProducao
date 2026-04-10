import pytesseract

from numpy import ndarray

from visao.manipulador_imagem import ManipuladorImagem
from modelos.logger import MeuLogger
from utilitarios import eh_vazia
from utilitariosTexto import limpa_ruido_texto


logger: MeuLogger = MeuLogger(nome='reconhecimento_texto')

class ReconhecimentoTexto():

	def __init__(self) -> None:
		self.manipulador_imagem: ManipuladorImagem = ManipuladorImagem()
		self._configuraTesseract()

	def _configuraTesseract(self):
		caminho: str = r"C:\Users\kevin.amazonas\AppData\Local\Programs\Tesseract-OCR"
		pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"

	def _retorna_imagem_para_dicionario(self, imagem):
		return pytesseract.image_to_data(
			imagem, lang="por", config="--psm 6", output_type=pytesseract.Output.DICT
		)
	
	def _reconhece_texto(self, imagem: ndarray | None, confianca: int = 80) -> str | None:
		resultado: dict = self._retorna_imagem_para_dicionario(imagem)

		lista_palavras: list[str] = []

		for i in range(len(resultado["text"])):
			if resultado["conf"][i] > confianca:
				lista_palavras.append(resultado["text"][i])

		string_palavras: str = "".join(lista_palavras)

		return (
			None
			if eh_vazia(lista=string_palavras)
			else limpa_ruido_texto(texto=string_palavras)
		)
	
	def reconhecer_nome_personagem(self, posicao: int | None = None) -> list[str]:
		frame_nome = None
		nome_reconhecido: str | None = None
		nomes_reconhecidos: list[str] = []

		if posicao is None:
			for indice in range(0, 2):
				frame_nome: ndarray | None = self.manipulador_imagem.retorna_frame_nome_personagem(posicao=indice)

				nome_reconhecido = self._reconhece_texto(imagem=frame_nome, confianca=40)
				if nome_reconhecido is None:
					continue

				nomes_reconhecidos.append(nome_reconhecido)
			
			return nomes_reconhecidos
		
		frame_nome: ndarray | None = self.manipulador_imagem.retorna_frame_nome_personagem(posicao=posicao)

		nome_reconhecido = self._reconhece_texto(imagem=frame_nome, confianca=40)
		
		if nome_reconhecido is not None:
			nomes_reconhecidos.append(nome_reconhecido)
	
		return nomes_reconhecidos
