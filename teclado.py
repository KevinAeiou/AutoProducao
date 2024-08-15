from time import sleep
import pyautogui as tecla

def clickAtalhoEspecifico(tecla1, tecla2):
    sleep(1)
    tecla.hotkey(tecla1,tecla2)
    sleep(1)

def tiraScreenshot():
    return tecla.screenshot()