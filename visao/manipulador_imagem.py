
import cv2
import pytesseract
import numpy as np

from numpy import ndarray
from automacao.teclado import ManipulaTeclado
from constantes import QTD_PIXEL_PRETO_REFERENCIA_MENU_PRINCIPAL

class ManipuladorImagem():

	def __init__(self, debug: bool = False) -> None:
		self.tela_inteira: ndarray | None = None
		self.altura_cabecalho: int = 0
		self.altura_rodape: int = 0
		self.debug: bool = debug
		self.frame_binarizado = None
		self.frame_cinza = None
		self.manipula_teclado: ManipulaTeclado = ManipulaTeclado()
		self._configuraTesseract()

	def _configuraTesseract(self):
		caminho: str = r"C:\Users\kevin.amazonas\AppData\Local\Programs\Tesseract-OCR"
		pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"

	def _retorna_imagem_colorida(self, screenshot):
		return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
	
	def retorna_atualizacao_tela(self):
		self.tela_inteira = self._retorna_imagem_colorida(self.manipula_teclado.tira_screenshot())

		if self.debug:
			self._mostra_imagem(
				indice=0, 
				imagem=self._retona_imagem_redimensionada(self.tela_inteira, 0.5), 
				nome_frame='Tela inteira'
			)
		
		return self.tela_inteira

	def _mostra_imagem(self, indice, imagem: ndarray | None, nome_frame: str = "Janela teste"):
		if imagem is None:
			return
	
		if cv2.getWindowProperty(nome_frame, cv2.WND_PROP_VISIBLE) < 0:
			cv2.imshow(nome_frame, imagem)
			cv2.waitKey(indice)
			cv2.destroyAllWindows()
			return

		cv2.imshow(nome_frame, imagem)
		cv2.waitKey(indice)

	def _retona_imagem_redimensionada(self, imagem: ndarray, porcentagem: float) -> ndarray | None:
		return (
			None
			if imagem is None
			else cv2.resize(imagem, (0, 0), fx=porcentagem, fy=porcentagem)
		)

	def resolucao_eh_1600_2560(self):
		if self.tela_inteira is None:
			return None
		
		return self.tela_inteira.shape[0] == 1600 and self.tela_inteira.shape[1] == 2560
	
	def _retorna_imagem_cinza(self, imagem):
		self.frame_cinza = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)

	def _retorna_imagem_binarizada(
		self, nucleo: tuple = (1, 1), limite_minimo: int = 170
	) -> ndarray | None:
		if self.frame_cinza is None:
			return None

		blur = cv2.GaussianBlur(self.frame_cinza, nucleo, cv2.BORDER_DEFAULT)
		ret, thresh = cv2.threshold(blur, limite_minimo, 255, cv2.THRESH_BINARY_INV)
		self.frame_binarizado = thresh
		return thresh
	
	def retorna_frame_nome_personagem(
		self, posicao: int
	) -> ndarray | None:
		"""
		Método para reconhecimento do nome do personagem em uma posição específica.
		
		:param posicao: Posição específica na tela e que o texto deve ser reconhecido.
		:type posicao: int
		:return: Frame da tela binarizada que contêm o texto reconhecido.
		:rtype: ndarray | None
		"""

		self.retorna_atualizacao_tela()
		if self.tela_inteira is None:
			return None
		
		tela = self.tela_inteira
		if self.resolucao_eh_1600_2560():
			x: int = tela.shape[1] // 6
			y: int = 19 * (tela.shape[0] // 40)
		else:
			x: int = tela.shape[1] // 7
			y: int = 14 * (tela.shape[0] // 30)
		posicao_nome: list[tuple] = [
			(2, 33, 210, 45),
			(x, y, 200, 40),
		]  # [x, y, altura, largura]

		frame_nome_personagem: ndarray = tela[
			posicao_nome[posicao][1] : posicao_nome[posicao][1]
			+ posicao_nome[posicao][3],
			posicao_nome[posicao][0] : posicao_nome[posicao][0]
			+ posicao_nome[posicao][2],
		]

		self._retorna_imagem_cinza(np.array(frame_nome_personagem))
		self._retorna_imagem_binarizada(limite_minimo=100)

		if self.debug:
			self._mostra_imagem(0, frame_nome_personagem)
			self._mostra_imagem(0, self.frame_binarizado)

		return self.frame_binarizado
	
	def retorna_frame_menu(self):
		if self.tela_inteira is None:
			return None
		
		frame: ndarray = (
			self.tela_inteira[0 : self.tela_inteira.shape[0], 
			0 : self.tela_inteira.shape[1] // 2]
		)
		self._retorna_imagem_cinza(np.array(frame))
		self._retorna_imagem_binarizada(limite_minimo=155)

		if self.debug:
			self._mostra_imagem(0, frame)
			self._mostra_imagem(0, self.frame_binarizado)
		
		return self.frame_binarizado
	
	def retorna_posicoes(
		self, x: int, y: int, largura: int, altura: int
	) -> tuple[int, int, int, int]:
		if self.tela_inteira is None:
			return x, y, largura, altura

		# if not self.resolucao_eh_1366_768():
		# 	razoes: tuple = self.retornaRazaoEntreTelas(self.tela_inteira)
		# 	x = int(x * razoes[1])
		# 	y = int(y * razoes[0])
		# 	largura = int(largura * razoes[1])
		# 	altura = int(altura * razoes[0])
		return x, y, largura, altura
	
	def verifica_menu_referencia(self):
		if self.tela_inteira is None:
			return None

		posicao_menu: tuple = (
			[self.tela_inteira.shape[0], int(self.tela_inteira.shape[1] // 2)],
			[self.tela_inteira.shape[0], self.tela_inteira.shape[1]],
		)
		_, _, largura, altura = self.retorna_posicoes(
			x=233, y=311, largura=55, altura=55
		)
		for posicao in posicao_menu:
			frame_tela: ndarray = self.tela_inteira[
				posicao[0] - altura : posicao[0], posicao[1] - largura : posicao[1]
			]
			contador_pixel_preto = np.sum(frame_tela == (85, 204, 255))

			if self.debug:
				self._mostra_imagem(0, frame_tela)
				print(f"CONTADOR PIXEL PRETO: {contador_pixel_preto}")

			if contador_pixel_preto >= QTD_PIXEL_PRETO_REFERENCIA_MENU_PRINCIPAL:
				return True
			
		return False