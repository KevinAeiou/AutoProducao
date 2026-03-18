import pyautogui

class ManipulaMouse():

	def	__init__(self) -> None:
		pass

	def clica(self, x: int, y: int, cliques: int = 1, intervalo: int = 1, botao: str = 'esquerdo'):

		for _ in range(cliques):
			if botao == 'esquerdo':
				pyautogui.leftClick(x, y, interval=intervalo)
				continue

			if botao == 'direito':
				pyautogui.rightClick(x, y, interval=intervalo)

		pass