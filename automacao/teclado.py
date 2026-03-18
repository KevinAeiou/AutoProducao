import pyautogui


class ManipulaTeclado():

	def __init__(self) -> None:
		
		pass

	def tira_screenshot(self):
		return pyautogui.screenshot()
	
	def preciona_tecla(self, tecla: str, cliques: int = 1):
		for _ in range(cliques):
			pyautogui.press(tecla)

	def clica_tecla(self, tecla: str | int, cliques: int = 1):
		for _ in range(cliques):
			if isinstance(tecla, int):
				string_tela: str = f'num{tecla}'
			
			else:
				string_tela = tecla

			pyautogui.hotkey(string_tela)