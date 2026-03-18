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

	def move_cursor_para(self, x: int | None = None, y: int | None = None):
		if x is None:
			tela = pyautogui.screenshot()
			x = tela.width // 2

		if y is None:
			tela = pyautogui.screenshot()
			y = tela.height // 2
			
		pyautogui.moveTo(x, y)
