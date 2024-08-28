from time import sleep
import pyautogui as tecla

def clickAtalhoEspecifico(tecla1, tecla2):
    sleep(1)
    tecla.hotkey(tecla1,tecla2)
    sleep(1)
    
def clickEspecifico(cliques, tecla):
    sleep(0.5)
    for x in range(cliques):
        if isinstance(tecla, int):
            tecla += 1
            teclaNumerica = f'num{tecla}'
        else:
            teclaNumerica = tecla
        tecla.hotkey(teclaNumerica)
        print(f'{tecla}.')
        sleep(0.5)

def clickContinuo(cliques, tecla):
    for x in range(cliques):
        tecla.press(tecla)

def tiraScreenshot():
    return tecla.screenshot()

def clickMouseEsquerdo(clicks, xTela,yTela):
    sleep(0.5)
    for x in range(clicks):
        tecla.leftClick(xTela, yTela)
        print(f'Click em {xTela}:{yTela}.')
        sleep(1)

def clickAtalhoEspecifico(tecla1, tecla2):
    tecla.hotkey(tecla1, tecla2)
    sleep(1)

def vaiParaMenuCorrespondencia():
    clickEspecifico(1,'f2')
    clickEspecifico(1,'1')
    clickEspecifico(1,'9')

def posicionaMouseEsquerdo(x_tela,y_tela):
    tecla.moveTo(x_tela,y_tela)
    print(f'Posicionado em {x_tela}:{y_tela}.')

def encerraSecao():
    print(f'Encerrando seção...')
    clickEspecifico(1,'f2')
    clickEspecifico(1,8)
    clickEspecifico(1,5)
    clickEspecifico(1,'f2')