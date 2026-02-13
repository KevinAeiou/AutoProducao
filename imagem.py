from teclado import tira_screenshot
import cv2
import os
import numpy as np
from numpy import ndarray
import pytesseract
from time import sleep
from utilitarios import *
from pytesseract import Output
from utilitariosTexto import texto1_pertence_texto2, limpaRuidoTexto
from constantes import QTD_PIXEL_PRETO_REFERENCIA_MENU_PRINCIPAL


class ManipulaImagem:
	def __init__(self, debug: bool = False):
		self.debug = debug
		self.configuraTesseract()

	def configuraTesseract(self):
		caminho: str = r"C:\Users\kevin.amazonas\AppData\Local\Programs\Tesseract-OCR"
		pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"

	def retornaImagemParaDicionario(self, imagem):
		return pytesseract.image_to_data(
			imagem, lang="por", config="--psm 6", output_type=Output.DICT
		)

	def reconheceDigito(self, imagem):
		caminho: str = r"C:\Program Files\Tesseract-OCR"
		pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"
		digitoReconhecido: str = pytesseract.image_to_string(
			imagem, config="--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789"
		)
		return digitoReconhecido.strip()

	def reconhece_texto(self, imagem: ndarray, confianca: int = 80) -> str | None:
		resultado: dict = self.retornaImagemParaDicionario(imagem)
		listaPalavras: list[str] = []
		for i in range(len(resultado["text"])):
			if resultado["conf"][i] > confianca:
				listaPalavras.append(resultado["text"][i])
		stringPalavras: str = "".join(listaPalavras)
		return (
			None
			if ehVazia(lista=stringPalavras)
			else limpaRuidoTexto(texto=stringPalavras)
		)

	def retornaImagemBinarizadaOtsu(
		self, imagem, limiarMinimo: int = 0, limiarMaximo: int = 255
	):
		ret, imagemBinarizada = cv2.threshold(
			imagem, limiarMinimo, limiarMaximo, cv2.THRESH_BINARY | cv2.THRESH_OTSU
		)
		return imagemBinarizada

	def retornaImagemEqualizada(self, img):
		clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
		return clahe.apply(img)

	def retorna_imagem_cinza(self, imagem):
		return cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)

	def retorna_imagem_colorida(self, screenshot):
		return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

	def retornaImagemInvertida(self, telaCinza):
		return cv2.bitwise_not(telaCinza)

	def retorna_atualizacao_tela(self):
		return self.retorna_imagem_colorida(tira_screenshot())

	def retorna_imagem_binarizada(
		self, imagem, nucleo: tuple = (1, 1), limiteMinimo: int = 170
	) -> np.ndarray:
		blur = cv2.GaussianBlur(imagem, nucleo, cv2.BORDER_DEFAULT)
		ret, thresh = cv2.threshold(blur, limiteMinimo, 255, cv2.THRESH_BINARY_INV)
		return thresh

	def retornaImagemDitalata(self, imagem, kernel, iteracoes):
		return cv2.dilate(imagem, kernel, iterations=iteracoes)

	def retornaImagemErodida(self, imagem, kernel, iteracoes):
		return cv2.erode(imagem, kernel, iterations=iteracoes)

	def mostra_imagem(self, indice, imagem: ndarray, nomeFrame: str = "Janela teste"):
		if cv2.getWindowProperty(nomeFrame, cv2.WND_PROP_VISIBLE) < 0:
			cv2.imshow(nomeFrame, imagem)
			cv2.waitKey(indice)
			cv2.destroyAllWindows()
			return
		cv2.imshow(nomeFrame, imagem)
		cv2.waitKey(indice)

	def abreImagem(self, caminhoImagem):
		return cv2.imread(caminhoImagem)

	def salvaNovaTela(self, nomeArquivo: str):
		imagem: ndarray = self.retorna_imagem_colorida()
		return self.salvaImagemCaminhoEspecifico(nomeArquivo, imagem)

	def salvaImagemCaminhoEspecifico(
		self, nomeArquivo: str, imagem: ndarray, caminho: str = "tests\imagemTeste"
	):
		if os.path.isdir(caminho):
			cv2.imwrite("{}\\{}".format(caminho, nomeArquivo), imagem)
			return
		os.makedirs(caminho)
		cv2.imwrite("{}\\{}".format(caminho, nomeArquivo), imagem)

	def reconheceNomeTrabalho(
		self, tela: ndarray, y: int, identificador: int
	) -> str | None:
		if tela is None:
			return None
		altura: int = 70 if identificador == 1 else 34
		x, y, largura, altura = self.retorna_posicoes(
			tela, x=233, y=y, largura=245, altura=altura
		)
		frameTrabalho: ndarray = tela[y : y + altura, x : x + largura]
		frameNomeTrabalhoTratado: ndarray = self.retorna_imagem_cinza(
			np.array(frameTrabalho)
		)
		frameNomeTrabalhoTratado = self.retorna_imagem_binarizada(
			frameNomeTrabalhoTratado
		)
		return (
			self.reconhece_texto(frameNomeTrabalhoTratado)
			if existePixelPreto(frameNomeTrabalhoTratado)
			else None
		)

	def retornaNomeTrabalhoReconhecido(self, yinicialNome: int, identificador: int):
		return self.reconheceNomeTrabalho(
			self.retorna_atualizacao_tela(), yinicialNome, identificador
		)

	def reconheceNomeConfirmacaoTrabalhoProducao(
		self, tela: np.ndarray, tipoTrabalho: int
	) -> str | None:
		arrayFrames: tuple = ((169, 285, 303, 33), (183, 200, 318, 31))
		posicao: int = arrayFrames[tipoTrabalho]
		x, y, largura, altura = self.retorna_posicoes(
			tela, x=posicao[0], y=posicao[1], largura=posicao[2], altura=posicao[3]
		)
		frameNomeTrabalho: ndarray = tela[y : y + altura, x : x + largura]
		frameNomeTrabalhoCinza: ndarray = self.retorna_imagem_cinza(
			imagem=np.array(frameNomeTrabalho)
		)
		frameNomeTrabalhoBinarizado: ndarray = self.retorna_imagem_binarizada(
			imagem=frameNomeTrabalhoCinza, limiteMinimo=115
		)
		return self.reconhece_texto(frameNomeTrabalhoBinarizado, confianca=30)

	def retornaNomeConfirmacaoTrabalhoProducaoReconhecido(
		self, tipoTrabalho: int
	) -> str | None:
		return self.reconheceNomeConfirmacaoTrabalhoProducao(
			self.retorna_atualizacao_tela(), tipoTrabalho=tipoTrabalho
		)

	def reconheceLicenca(self, tela: ndarray) -> str | None:
		listaLicencas: list[str] = LISTA_LICENCAS
		listaLicencas.append("Nenhum item")
		frameTelaCinza: ndarray = self.retorna_imagem_cinza(
			np.array(tela[0 : tela.shape[0], 0 : tela.shape[1] // 2])
		)
		fremaTelaBinarizada: ndarray = self.retorna_imagem_binarizada(
			imagem=frameTelaCinza, limiteMinimo=120
		)
		textoReconhecido: str = self.reconhece_texto(fremaTelaBinarizada)
		if textoReconhecido is None:
			return None
		for licenca in listaLicencas:
			if texto1_pertence_texto2(licenca, textoReconhecido):
				return licenca
		return None

	def retornaTextoLicencaReconhecida(self):
		return self.reconheceLicenca(self.retorna_atualizacao_tela())

	def reconhece_texto_nome_personagem(
		self, tela: ndarray, posicao: int
	) -> str | None:
		"""
		Método para reconhecimento do nome do personagem em uma posição específica.
		Args:
						tela (ndarray): Imagem da tela atual inteira.
						posicao (int): Posição específica na tela e que o texto deve ser reconhecido.
		Returns:
						str: String que contêm o texto reconhecido.
		"""
		if self.resolucao_eh_1600_2560(tela):
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
		frame_cinza: ndarray = self.retorna_imagem_cinza(np.array(frame_nome_personagem))
		frame_binarizado: ndarray = self.retorna_imagem_binarizada(
			imagem=frame_cinza, limiteMinimo=100
		)
		texto_reconhecido = self.reconhece_texto(imagem=frame_binarizado, confianca=40)
		if self.debug:
			self.mostra_imagem(0, frame_nome_personagem, "Frame normal")
			self.mostra_imagem(0, frame_cinza, "Frame cinza")
			self.mostra_imagem(0, frame_binarizado, "Frame binarizado")
			print(f"Texto reconhecido: {texto_reconhecido}")
		return texto_reconhecido

	def retorna_texto_nome_personagem_reconhecido(
		self, posicao: int, frame: ndarray | None = None
	) -> str | None:
		"""
		Método responsável por reconhecer o nome do personagem atual.

		Args:
						posicao: Inteiro que representa a posição do texto a ser reconhecido.
						0 caso esteja no canto superior esquerdo da tela ou 1 caso esteja no centro.
						frame: Frame da tela inteira. None caso seja um reconhecimento real.
		"""

		titulo = "superior esquerda" if posicao == 0 else "central"
		print(f"Reconhecendo nome do personagem na posição {titulo}")
		if frame is None:
			return self.reconhece_texto_nome_personagem(
				self.retorna_atualizacao_tela(), posicao
			)
		return self.reconhece_texto_nome_personagem(frame, posicao)

	def reconheceTextoErro(self, tela):
		return self.reconhece_texto(tela[318 : 318 + 120, 150:526])

	def retornaErroReconhecido(self):
		return self.reconheceTextoErro(self.retorna_atualizacao_tela())

	def verifica_menu_referencia_inicial(self, tela: ndarray):
		posicao_menu: tuple = (
			[tela.shape[0], int(tela.shape[1] // 2)],
			[tela.shape[0], tela.shape[1]],
		)
		_, _, largura, altura = self.retorna_posicoes(
			tela, x=233, y=311, largura=55, altura=55
		)
		for posicao in posicao_menu:
			frame_tela: ndarray = tela[
				posicao[0] - altura : posicao[0], posicao[1] - largura : posicao[1]
			]
			contador_pixel_preto = np.sum(frame_tela == (85, 204, 255))
			if self.debug:
				self.mostra_imagem(0, frame_tela)
				print(f"CONTADOR PIXEL PRETO: {contador_pixel_preto}")

			if contador_pixel_preto >= QTD_PIXEL_PRETO_REFERENCIA_MENU_PRINCIPAL:
				return True
		return False

	def resolucao_eh_1366_768(self, tela: ndarray):
		return tela.shape[0] == 768 and tela.shape[1] == 1366

	def resolucao_eh_1600_2560(self, tela: ndarray):
		return tela.shape[0] == 1600 and tela.shape[1] == 2560

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

	def verificaMenuReferencia(self, frame=None):
		if frame is None:
			return self.verifica_menu_referencia_inicial(self.retorna_atualizacao_tela())
		return self.verifica_menu_referencia_inicial(frame)

	def reconhece_texto_menu(self, tela: ndarray) -> str | None:
		frame: ndarray = tela[0 : tela.shape[0], 0 : tela.shape[1] // 2]
		frame_cinza: ndarray = self.retorna_imagem_cinza(np.array(frame))
		frame_binarizado = self.retorna_imagem_binarizada(
			imagem=frame_cinza, limiteMinimo=155
		)
		texto_reconhecido = self.reconhece_texto(imagem=frame_binarizado, confianca=50)
		if self.debug:
			self.mostra_imagem(0, frame, "Frame")
			self.mostra_imagem(0, frame_binarizado, "Frame binarizado")
			print(f"Texto reconhecido: {texto_reconhecido}")

		return texto_reconhecido

	def retorna_texto_menu_reconhecido(self, frame: ndarray | None = None) -> str | None:
		if frame:
			return self.reconhece_texto_menu(frame)
		return self.reconhece_texto_menu(self.retorna_atualizacao_tela())

	def reconheceTextoSair(self, tela: np.ndarray):
		x, _, largura, _ = self.retorna_posicoes(
			tela, x=50, y=665, largura=80, altura=55
		)
		frameTelaTratado: ndarray = self.retorna_imagem_cinza(
			np.array(tela[tela.shape[0] - 55 : tela.shape[0] - 15, x : x + largura])
		)
		frameTelaTratado = self.retorna_imagem_binarizada(frameTelaTratado)
		return self.reconhece_texto(frameTelaTratado)

	def retornaTextoSair(self):
		return self.reconheceTextoSair(self.retorna_atualizacao_tela())

	def verificaPixelCorrespondencia(self, tela: ndarray):
		x: int = int(tela.shape[1] // 2)
		_, y, largura, altura = self.retorna_posicoes(
			tela, x=0, y=665, largura=36, altura=30
		)
		frameTela: ndarray = tela[y : y + altura, x - largura : x]
		contadorPixelCorrespondencia: int = np.sum(frameTela == (173, 239, 247))
		return True if contadorPixelCorrespondencia > 50 else False

	def retornaExistePixelCorrespondencia(self):
		return self.verificaPixelCorrespondencia(self.retorna_atualizacao_tela())

	def existeCorrespondencia(self):
		print(f"Verificando se possui correspondencia...")
		return self.quantidadePixelBrancoEhMaiorQueZero(self.retorna_atualizacao_tela())

	def quantidadePixelBrancoEhMaiorQueZero(self, tela: ndarray) -> bool:
		x, y, largura, altura = self.retorna_posicoes(
			tela, x=235, y=233, largura=200, altura=30
		)
		frame: ndarray = tela[y : y + altura, x : x + largura]
		return np.sum(frame == 255) > 0

	def reconheceTextoCorrespondencia(self, tela: ndarray):
		x, y, largura, altura = self.retorna_posicoes(
			tela, x=168, y=231, largura=343, altura=130
		)
		frameTela: ndarray = tela[y : y + altura, x : x + largura]
		return self.reconhece_texto(frameTela)

	def retornaTextoCorrespondenciaReconhecido(self):
		return self.reconheceTextoCorrespondencia(self.retorna_atualizacao_tela())

	def retorna_posicoes(
		self, tela: ndarray, x: int, y: int, largura: int, altura: int
	) -> tuple[int, int, int, int]:
		if not self.resolucao_eh_1366_768(tela):
			razoes: tuple = self.retornaRazaoEntreTelas(tela)
			x = int(x * razoes[1])
			y = int(y * razoes[0])
			largura = int(largura * razoes[1])
			altura = int(altura * razoes[0])
		return x, y, largura, altura

	def reconheceEstadoTrabalho(self, tela: ndarray) -> int:
		x, y, largura, altura = self.retorna_posicoes(
			tela, x=233, y=311, largura=255, altura=43
		)
		texto: str = self.reconhece_texto(tela[y : y + altura, x : x + largura])
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

	def retornaEstadoTrabalho(self) -> int:
		return self.reconheceEstadoTrabalho(tela=self.retorna_atualizacao_tela())

	def reconheceNomeTrabalhoFrameProducao(self, tela: ndarray) -> str | None:
		"""
		Método para analise e reconhecimento do nome do trabalho para produção concluído.
		Args:
						tela (ndarray): Imagem que contêm os dados do trabalho para produção.
		Returns:
						str: String que contêm o nome do trabalho reconhecido.
		"""
		telaCinza: ndarray = self.retorna_imagem_cinza(np.array(tela))
		telaInvertida: ndarray = self.retornaImagemInvertida(telaCinza)
		x, y, largura, altura = self.retorna_posicoes(
			tela, x=233, y=289, largura=253, altura=37
		)
		tela = telaInvertida[y : y + altura, x : x + largura]
		return self.reconhece_texto(tela)

	def retorna_nome_trabalho_frame_producao_reconhecido(self):
		return self.reconheceNomeTrabalhoFrameProducao(self.retorna_atualizacao_tela())

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

	def retornaReferencia(self, imagem: np.ndarray) -> tuple | None:
		print(f'Buscando referência "PEGAR"...')
		imagem = imagem[0 : imagem.shape[0], 0 : imagem.shape[1] // 2]
		imagemTratada = self.retorna_imagem_cinza(imagem=np.array(imagem))
		imagemTratada = self.retorna_imagem_binarizada(
			imagem=imagemTratada, limiteMinimo=150
		)
		resultado: dict = self.retornaImagemParaDicionario(imagem=imagemTratada)
		for i in range(len(resultado["text"])):
			if (
				not ehVazia(limpaRuidoTexto(texto=resultado["text"][i]))
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
		return self.retornaReferencia(self.retorna_atualizacao_tela())

	def verificaReferenciaLeiloeiro(self, imagem: np.ndarray) -> tuple | None:
		imagem = imagem[0 : imagem.shape[0], 0 : imagem.shape[1] // 2]
		imagemTratada = self.retorna_imagem_cinza(imagem=np.array(imagem))
		imagemTratada = self.retorna_imagem_binarizada(
			imagem=imagemTratada, limiteMinimo=130
		)
		resultado: dict = self.retornaImagemParaDicionario(imagem=imagemTratada)
		for i in range(len(resultado["text"])):
			# if resultado["conf"][i] > 0:
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
		return self.verificaReferenciaLeiloeiro(self.retorna_atualizacao_tela())

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
			copiaTela = self.retorna_atualizacao_tela()
			print(self.reconhece_texto_nome_personagem(copiaTela, 0))
			sleep(1)
		return


if __name__ == "__main__":

	sleep(1)
	imagem = ManipulaImagem(debug=True)
	tela_teste: ndarray = imagem.abreImagem(
		caminhoImagem=r"tests\imagemTeste\teste_tela_inicial_resolucao_2560_1600.png"
	)
	imagem.retorna_texto_menu_reconhecido()
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
