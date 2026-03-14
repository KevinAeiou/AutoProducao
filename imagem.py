from teclado import tira_screenshot
import cv2
import os
import numpy as np
from numpy import ndarray
import pytesseract
from time import sleep
from utilitarios import *
from pytesseract import Output
from utilitariosTexto import texto1_pertence_texto2, limpa_ruido_texto
from constantes import QTD_PIXEL_PRETO_REFERENCIA_MENU_PRINCIPAL


class ManipulaImagem:
	def __init__(self, debug: bool = False):
		self.debug = debug
		self.tela_inteira: ndarray | None = None
		self.frame_cinza: ndarray | None = None
		self.frame_binarizado: ndarray | None = None
		self.frame_invertido: ndarray | None = None
		self._configuraTesseract()

	def _configuraTesseract(self):
		caminho: str = r"C:\Users\kevin.amazonas\AppData\Local\Programs\Tesseract-OCR"
		pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"

	def _retorna_imagem_para_dicionario(self, imagem):
		return pytesseract.image_to_data(
			imagem, lang="por", config="--psm 6", output_type=Output.DICT
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

	def _retorna_imagem_cinza(self, imagem):
		self.frame_cinza = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)

	def _retorna_imagem_colorida(self, screenshot):
		return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

	def _retorna_imagem_invertida(self):
		if self.frame_cinza is None:
			return None

		self.frame_invertido = cv2.bitwise_not(self.frame_cinza)

	def _retorna_atualizacao_tela(self):
		self.tela_inteira = self._retorna_imagem_colorida(tira_screenshot())

	def _retorna_imagem_binarizada(
		self, nucleo: tuple = (1, 1), limite_minimo: int = 170
	) -> ndarray | None:
		if self.frame_cinza is None:
			return None

		blur = cv2.GaussianBlur(self.frame_cinza, nucleo, cv2.BORDER_DEFAULT)
		ret, thresh = cv2.threshold(blur, limite_minimo, 255, cv2.THRESH_BINARY_INV)
		self.frame_binarizado = thresh
		return thresh

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

	def abre_imagem(self, caminho_imagem: str) -> ndarray:
		return cv2.imread(caminho_imagem)

	def salva_nova_tela(
		self, nome_arquivo: str, caminho: str = r"tests\imagemTeste"
	):
		self._retorna_atualizacao_tela()
		if self.tela_inteira is None:
			return
		
		if os.path.isdir(caminho):
			cv2.imwrite("{}\\{}".format(caminho, nome_arquivo), self.tela_inteira)
			return
		os.makedirs(caminho)
		cv2.imwrite("{}\\{}".format(caminho, nome_arquivo), self.tela_inteira)

	def reconhece_nome_trabalho(
		self, y: int, identificador: int
	) -> str | None:
		altura: int = 70 if identificador == 1 else 34
		x, y, largura, altura = self.retorna_posicoes(
			x=233, y=y, largura=245, altura=altura
		)
		if self.tela_inteira is None:
			return None
		
		frame: ndarray = self.tela_inteira[y : y + altura, x : x + largura]
		self._retorna_imagem_cinza(
			np.array(frame)
		)
		self._retorna_imagem_binarizada()

		texto_reconhecido = self._reconhece_texto(self.frame_binarizado) if existePixelPreto(self.frame_binarizado) else None

		if self.debug:
			self._mostra_imagem(0, frame, "Frame normal")
			self._mostra_imagem(0, self.frame_binarizado, "Frame binarizado")
			print(f"Texto reconhecido: {texto_reconhecido}")

		return texto_reconhecido

	def retorna_nome_trabalho_reconhecido(self, yinicial_nome: int, identificador: int) -> str | None:
		"""
		Método para reconhecer o nome do trabalho atual.
		
		:param yinicial_nome: Posição inicial do nome do trabalho na tela.
		:type yinicial_nome: int
		:param identificador: Inteiro que representa a raridade do trabalho. 0 para trabalhos raros e especiais e 1 para trabalhos comuns e melhorados.
		:type identificador: int
		:return: String que contêm o nome do trabalho reconhecido.
		:rtype: str | None
		"""

		self._retorna_atualizacao_tela()
		return self.reconhece_nome_trabalho(yinicial_nome, identificador)

	def _reconhece_nome_confirmacao_trabalho_producao(
		self, tipo_trabalho: int
	) -> str | None:
		array_frames: tuple = ((169, 285, 303, 33), (183, 200, 318, 31))
		posicao: tuple = array_frames[tipo_trabalho]
		x, y, largura, altura = self.retorna_posicoes(
			x=posicao[0], y=posicao[1], largura=posicao[2], altura=posicao[3]
		)
		if self.tela_inteira is None:
			return None
		
		frame_nome_trabalho: ndarray = self.tela_inteira[y : y + altura, x : x + largura]
		self._retorna_imagem_cinza(
			imagem=np.array(frame_nome_trabalho)
		)
		self._retorna_imagem_binarizada(limite_minimo=115)
		return self._reconhece_texto(self.frame_binarizado, confianca=30)

	def retorna_nome_confirmacao_trabalho_producao_reconhecido(
		self, tipo_trabalho: int
	) -> str | None:
		"""
		Docstring para retorna_nome_confirmacao_trabalho_producao_reconhecido
		
		:param tipo_trabalho: Descrição
		:type tipo_trabalho: int
		:return: Descrição
		:rtype: str | None
		"""
		self._retorna_atualizacao_tela()
		return self._reconhece_nome_confirmacao_trabalho_producao(tipo_trabalho=tipo_trabalho)

	def reconhece_licenca(self) -> str | None:
		lista_licencas: list[str] = LISTA_LICENCAS
		lista_licencas.append("Nenhum item")

		if self.tela_inteira is None:
			return None
		
		self._retorna_imagem_cinza(
			np.array(self.tela_inteira[0 : self.tela_inteira.shape[0], 0 : self.tela_inteira.shape[1] // 2])
		)
		self._retorna_imagem_binarizada(limite_minimo=120)
		texto_reconhecido: str | None = self._reconhece_texto(self.frame_binarizado)
		if texto_reconhecido is None:
			return None
		
		for licenca in lista_licencas:
			if texto1_pertence_texto2(licenca, texto_reconhecido):
				return licenca
		return None

	def retorna_texto_licenca_reconhecida(self):
		self._retorna_atualizacao_tela()
		return self.reconhece_licenca()

	def reconhece_texto_nome_personagem(
		self, posicao: int
	) -> str | None:
		"""
		Método para reconhecimento do nome do personagem em uma posição específica.
		
		:param posicao: Posição específica na tela e que o texto deve ser reconhecido.
		:type posicao: int
		:return: String que contêm o texto reconhecido.
		:rtype: str | None
		"""
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
		texto_reconhecido = self._reconhece_texto(imagem=self.frame_binarizado, confianca=40)
		if self.debug:
			self._mostra_imagem(0, frame_nome_personagem, "Frame normal")
			self._mostra_imagem(0, self.frame_cinza, "Frame cinza")
			self._mostra_imagem(0, self.frame_binarizado, "Frame binarizado")
			print(f"Texto reconhecido: {texto_reconhecido}")

		return texto_reconhecido

	def retorna_texto_nome_personagem_reconhecido(self, posicao: int) -> str | None:
		"""
		Método responsável por reconhecer o nome do personagem atual.

		Args:
			posicao: Inteiro que representa a posição do texto a ser reconhecido.
			0 caso esteja no canto superior esquerdo da tela ou 1 caso esteja no centro.
			frame: Frame da tela inteira. None caso seja um reconhecimento real.
		"""

		titulo = "superior esquerda" if posicao == 0 else "central"
		print(f"Reconhecendo nome do personagem na posição {titulo}")
		return self.reconhece_texto_nome_personagem(posicao)

	def reconhece_texto_erro(self):
		if self.tela_inteira is None:
			return None
		
		tela = self.tela_inteira[318 : 318 + 120, 150:526]
		return self._reconhece_texto(tela)

	def retornaErroReconhecido(self):
		self._retorna_atualizacao_tela()
		return self.reconhece_texto_erro()

	def verifica_menu_referencia_inicial(self):
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

	def resolucao_eh_1366_768(self):
		if self.tela_inteira is None:
			return None

		return self.tela_inteira.shape[0] == 768 and self.tela_inteira.shape[1] == 1366

	def resolucao_eh_1600_2560(self):
		if self.tela_inteira is None:
			return None
		
		return self.tela_inteira.shape[0] == 1600 and self.tela_inteira.shape[1] == 2560

	def retornaRazaoEntreTelas(self, tela: ndarray) -> tuple:
		"""
		Função para encontrar as razões entre alturas e larguras da resolução de tela atual e resolução (1366x768)
		Args:
						tela (ndarray): Imagem da tela atual a ser encontrada as razões
		Returns:
						tuple: Tupla de valores encontrados (y, x)
		"""
		razaoX: float = tela.shape[1] / 1366
		razaoY: float = tela.shape[0] / 768
		return (razaoY, razaoX)

	def verificaMenuReferencia(self):
		self._retorna_atualizacao_tela()
		return self.verifica_menu_referencia_inicial()

	def reconhece_texto_menu(self) -> str | None:
		if self.tela_inteira is None:
			return None

		frame: ndarray = self.tela_inteira[0 : self.tela_inteira.shape[0], 0 : self.tela_inteira.shape[1] // 2]
		self._retorna_imagem_cinza(np.array(frame))
		self._retorna_imagem_binarizada(limite_minimo=155)
		texto_reconhecido = self._reconhece_texto(imagem=self.frame_binarizado, confianca=50)
		if self.debug:
			self._mostra_imagem(0, frame, "Frame")
			self._mostra_imagem(0, self.frame_binarizado, "Frame binarizado")
			print(f"Texto reconhecido: {texto_reconhecido}")

		return texto_reconhecido

	def retorna_texto_menu_reconhecido(self) -> str | None:
		self._retorna_atualizacao_tela()
		return self.reconhece_texto_menu()

	def reconhece_texto_sair(self):
		if self.tela_inteira is None:
			return None
		
		x, y, largura, _ = self.retorna_posicoes(
			x=50, y=700, largura=80, altura=55
		)
		if self.resolucao_eh_1366_768():
			x, y, largura, _ = self.retorna_posicoes(
				x=50, y=50, largura=80, altura=55
			)

		if self.resolucao_eh_1600_2560():
			x, y, largura, _ = self.retorna_posicoes(
				x=25, y=34, largura=80, altura=55
			)

		tela = self.tela_inteira
		self._retorna_imagem_cinza(
			np.array(tela[tela.shape[0] - y : tela.shape[0] - 15, x : x + largura])
		)
		self._retorna_imagem_binarizada()
		texto_reconhecido = self._reconhece_texto(self.frame_binarizado)

		if self.debug:
			self._mostra_imagem(0, self.frame_cinza, "Frame cinza")
			self._mostra_imagem(0, self.frame_binarizado, "Frame binarizado")
			print(f"Texto reconhecido: {texto_reconhecido}")

		return texto_reconhecido

	def retorna_texto_sair(self) -> str | None:
		return self.reconhece_texto_sair()

	def verifica_pixel_correspondencia(self):
		if self.tela_inteira is None:
			return None
		
		tela = self.tela_inteira
		x: int = int(tela.shape[1] // 2)
		_, y, largura, altura = self.retorna_posicoes(
			x=0, y=665, largura=36, altura=30
		)
		frameTela: ndarray = tela[y : y + altura, x - largura : x]
		contadorPixelCorrespondencia: int = np.sum(frameTela == (173, 239, 247))
		return True if contadorPixelCorrespondencia > 50 else False

	def retorna_existe_pixel_correspondencia(self):
		self._retorna_atualizacao_tela()
		return self.verifica_pixel_correspondencia()

	def existe_correspondencia(self):
		print(f"Verificando se possui correspondencia...")
		self._retorna_atualizacao_tela()
		return self.quantidadePixelBrancoEhMaiorQueZero()

	def quantidadePixelBrancoEhMaiorQueZero(self) -> bool:
		if self.tela_inteira is None:
			return False
		x, y, largura, altura = self.retorna_posicoes(
			x=235, y=233, largura=200, altura=30
		)
		frame: ndarray = self.tela_inteira[y : y + altura, x : x + largura]
		return np.sum(frame == 255) > 0

	def reconhece_texto_correspondencia(self):
		if self.tela_inteira is None:
			return None
		
		x, y, largura, altura = self.retorna_posicoes(
			x=168, y=231, largura=343, altura=130
		)
		frame_tela: ndarray = self.tela_inteira[y : y + altura, x : x + largura]
		texto_reconhecido = self._reconhece_texto(frame_tela)
		if self.debug:
			self._mostra_imagem(0, frame_tela, "Frame correspondencia")
			print(f'Correspondência reconhecida: {texto_reconhecido}')

		return texto_reconhecido

	def retorna_texto_correspondencia_reconhecido(self):
		self._retorna_atualizacao_tela()
		return self.reconhece_texto_correspondencia()

	def retorna_posicoes(
		self, x: int, y: int, largura: int, altura: int
	) -> tuple[int, int, int, int]:
		if self.tela_inteira is None:
			return x, y, largura, altura

		if not self.resolucao_eh_1366_768():
			razoes: tuple = self.retornaRazaoEntreTelas(self.tela_inteira)
			x = int(x * razoes[1])
			y = int(y * razoes[0])
			largura = int(largura * razoes[1])
			altura = int(altura * razoes[0])
		return x, y, largura, altura

	def reconhece_estado_trabalho(self) -> int | None:
		if self.tela_inteira is None:
			return None

		x, y, largura, altura = self.retorna_posicoes(
			x=233, y=311, largura=255, altura=43
		)
		tela = self.tela_inteira[y : y + altura, x : x + largura]
		texto: str | None = self._reconhece_texto(tela)
		if texto is None:
			print(f"Em produção...")
			return CODIGO_PRODUZINDO
		if texto1_pertence_texto2(texto1=STRING_PEDIDO_CONCLUIDO, texto2=texto):
			print(f"Pedido concluído!")
			return CODIGO_CONCLUIDO
		if texto1_pertence_texto2(texto1=STRING_ADICIONAR_NOVO_PEDIDO, texto2=texto):
			print(f"Nem um trabalho!")
			return CODIGO_PARA_PRODUZIR
		print(f"Em produção...")
		return CODIGO_PRODUZINDO

	def retornaEstadoTrabalho(self) -> int | None:
		self._retorna_atualizacao_tela()
		return self.reconhece_estado_trabalho()

	def reconheceNomeTrabalhoFrameProducao(self) -> str | None:
		"""
		Método para analise e reconhecimento do nome do trabalho para produção concluído.
		Args:
			tela (ndarray): Imagem que contêm os dados do trabalho para produção.
		Returns:
			str: String que contêm o nome do trabalho reconhecido.
		"""
		self._retorna_imagem_cinza(np.array(self.tela_inteira))
		self._retorna_imagem_invertida()
		x, y, largura, altura = self.retorna_posicoes(
			x=233, y=289, largura=253, altura=37
		)
		if self.frame_invertido is None:
			return None

		tela = self.frame_invertido[y : y + altura, x : x + largura]
		return self._reconhece_texto(tela)

	def retorna_nome_trabalho_frame_producao_reconhecido(self):
		self._retorna_atualizacao_tela()
		return self.reconheceNomeTrabalhoFrameProducao()

	def desenhaRetangulo(self, imagem, contorno, cor=(0, 255, 0)):
		x, y, l, a = cv2.boundingRect(contorno)
		area = l * a
		self.escreveTexto(str(area), imagem, contorno)
		return cv2.rectangle(imagem, (x, y), (x + l, y + a), cor, 2)

	def retonaImagemRedimensionada(self, imagem: ndarray, porcentagem: float):
		return (
			None
			if imagem is None
			else cv2.resize(imagem, (0, 0), fx=porcentagem, fy=porcentagem)
		)

	def retornaReferencia(self) -> tuple | None:
		print(f'Buscando referência "PEGAR"...')
		if self.tela_inteira is None:
			return None
		imagem = self.tela_inteira[0 : self.tela_inteira.shape[0], 0 : self.tela_inteira.shape[1] // 2]
		self._retorna_imagem_cinza(imagem=np.array(imagem))
		self._retorna_imagem_binarizada(limite_minimo=150)
		resultado: dict = self._retorna_imagem_para_dicionario(imagem=self.frame_binarizado)
		for i in range(len(resultado["text"])):
			if (
				not eh_vazia(limpa_ruido_texto(texto=resultado["text"][i]))
				and texto1_pertence_texto2(texto1=resultado["text"][i], texto2="Pegar")
				and resultado["conf"][i] > 90
			):
				x = resultado["left"][i]
				y = resultado["top"][i]
				l = resultado["width"][i]
				a = resultado["height"][i]
				centroX = x + (l / 2)
				centroY = y + (a / 2)
				return (centroX, centroY)
		return None

	def verifica_recompensa_disponivel(self):
		self._retorna_atualizacao_tela()
		return self.retornaReferencia()

	def verificaReferenciaLeiloeiro(self) -> tuple | None:
		if self.tela_inteira is None:
			return None
		imagem = self.tela_inteira[0 : self.tela_inteira.shape[0], 0 : self.tela_inteira.shape[1] // 2]
		self._retorna_imagem_cinza(imagem=np.array(imagem))
		self._retorna_imagem_binarizada(limite_minimo=130)
		resultado: dict = self._retorna_imagem_para_dicionario(imagem=self.frame_binarizado)
		for i in range(len(resultado["text"])):
			if resultado["conf"][i] > 0 and "iloei" in resultado["text"][i]:
				print(f'{resultado["text"][i]} | {resultado["conf"][i]}')
				x = resultado["left"][i]
				y = resultado["top"][i]
				l = resultado["width"][i]
				a = resultado["height"][i]
				centroX = x + (l / 2)
				centroY = y + (a / 2)
				return (centroX, centroY)
		return None

	def retornaReferenciaLeiloeiro(self):
		self._retorna_atualizacao_tela()
		return self.verificaReferenciaLeiloeiro()

	def escreveTexto(self, texto, frameTela, contorno):
		x, y, l, a = cv2.boundingRect(contorno)
		posicao = (x, y + 20)
		fonte = cv2.FONT_HERSHEY_SIMPLEX
		escala = 0.5
		cor = (0, 0, 0)
		thickness = 1
		return cv2.putText(
			frameTela, texto, posicao, fonte, escala, cor, thickness, cv2.LINE_AA
		)

	def reconheceNomePersonagemTeste(self):
		while True:
			self._retorna_atualizacao_tela()
			print(self.reconhece_texto_nome_personagem(0))
			sleep(1)
		return


if __name__ == "__main__":

	sleep(1)
	imagem = ManipulaImagem(debug=True)
	tela_teste: ndarray = imagem.abre_imagem(
		caminho_imagem=r"tests\imagemTeste\testeMenuPrincipal.png"
	)
	# imagem.retorna_texto_menu_reconhecido()
	imagem.retorna_texto_correspondencia_reconhecido()
	# frame_redimensionada = imagem.retonaImagemRedimensionada(tela_teste, 0.8)
	# if frame_redimensionada is not None:
	#     imagem.mostraImagem(0, frame_redimensionada)
	# while True:
	#     sleep(1)
	# print(imagem.reconheceNomeTrabalho(tela= telaMenuInicial, y= 524, identificador= 1))
	# print(imagem.retornaNomeTrabalhoReconhecido(yinicialNome= 524, identificador= 1))
	# print(imagem.existeCorrespondencia())
	# resultado = imagem.retornaReferenciaLeiloeiro()
	# print(resultado)
	# if resultado is None:
	#     continue
	# posicionaMouseEsquerdo(x_tela= resultado[0], y_tela= resultado[1]+ 100)
