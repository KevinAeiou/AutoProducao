from numpy import ndarray

from visao.reconhecimento_texto import ReconhecimentoTexto
from visao.manipulador_imagem import ManipuladorImagem
from utilitarios import eh_vazia, retorna_codigo_erro_reconhecido
from utilitariosTexto import limpa_ruido_texto, texto1_pertence_texto2
from constantes import (
	MENU_RECOMPENSAS_DIARIAS,
	MENU_PRINCIPAL,
	MENU_PERSONAGEM,
)
class ReconhecimentoTela():

	def __init__(self) -> None:
		self._reconhecimento_texto: ReconhecimentoTexto = ReconhecimentoTexto()
		self._manipulador_imagem: ManipuladorImagem = ManipuladorImagem(debug=True)
		self.menu_atual: int | None = None
		self.erro_atual: int | None = None

	def reconhece_menu_atual(self):
		self._manipulador_imagem.retorna_atualizacao_tela()
		frame_menu: ndarray | None = self._manipulador_imagem.retorna_frame_menu()

		texto_menu: str | None = self._reconhecimento_texto._reconhece_texto(frame_menu)

		if texto_menu is None:
			return
		
		if 'recompensasdiarias' in texto_menu:
			self.menu_atual = MENU_RECOMPENSAS_DIARIAS
			return
		
		if texto1_pertence_texto2('interagir', texto_menu):
			self.menu_atual = MENU_PRINCIPAL
			return 
		
		if texto1_pertence_texto2('conquistas', texto_menu):
			self.menu_atual = MENU_PERSONAGEM
			return 
		
	def retorna_coordenadas_botao_pegar(self) -> tuple | None:
		self._manipulador_imagem.retorna_atualizacao_tela()
		frame_referencia_pegar: ndarray | None = self._manipulador_imagem.retorna_frame_menu()

		resultado: dict = self._reconhecimento_texto._retorna_imagem_para_dicionario(frame_referencia_pegar)

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
	
	def verifica_erro(self):
		self._manipulador_imagem.retorna_atualizacao_tela()
		
		frame_erro: ndarray | None = self._manipulador_imagem.retorna_frame_menu()
		texto_erro: str | None = self._reconhecimento_texto._reconhece_texto(frame_erro)

		if texto_erro is None:
			return
		
		self.erro_atual = retorna_codigo_erro_reconhecido(texto_erro)
		
	@property
	def erro_encontrado(self):
		return self.erro_atual != None

	@property
	def eh_menu_recompensas_diarias(self) -> bool:
		if self.menu_atual is None:
			return False
		
		return self.menu_atual == MENU_RECOMPENSAS_DIARIAS