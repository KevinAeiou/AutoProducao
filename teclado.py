from time import sleep
import pyautogui as tecla
from constantes import *

def clickAtalhoEspecifico(tecla1, tecla2):
    sleep(1)
    tecla.hotkey(tecla1,tecla2)
    sleep(1)
    
def clickEspecifico(cliques: int, teclaEspecifica: str):
    '''
        Função para realizar cliques em teclas específicas.
        Args:
            cliques (int): Inteiro que contêm a quantidade de cliques a serem realizados.
            teclaEspecifica (str): String que contêm a tecla a ser clicada.
    '''
    sleep(0.5)
    for x in range(cliques):
        if isinstance(teclaEspecifica, int):
            teclaEspecifica += 1
            teclaNumerica = f'num{teclaEspecifica}'
        else:
            teclaNumerica = teclaEspecifica
        tecla.hotkey(teclaNumerica)
        print(f'{teclaEspecifica}.')
        sleep(0.5)

def precionaTecla(cliques: int, teclaEspecifica: str):
    '''
        Função para clicar continuamente uma tela específica.
        Args:
            cliques (int): Inteiro que contêm a quantidade de cliques a serem realizados.
            teclaEspecifica (str): String que contêm a tecla a ser precionada.
    '''
    for _ in range(cliques):
        tecla.press(teclaEspecifica)

def tiraScreenshot():
    return tecla.screenshot()

def cliqueMouseEsquerdo(cliques: int, xTela: int, yTela: int):
    '''
        Função para clicar na tela com o botão esquerdo do mouse.
        Args:
            cliques (int): Inteiro que contêm a quantidade de cliques a serem realizados.
            xTela (int): Inteiro que contêm a posição 'x' da tela.
            yTela (int): Inteiro que contêm a posição 'y' da tela.
    '''
    sleep(0.5)
    for x in range(cliques):
        tecla.leftClick(xTela, yTela)
        print(f'Click em x:{xTela} - y:{yTela}.')
        sleep(1)

def clickAtalhoEspecifico(tecla1, tecla2):
    tecla.hotkey(tecla1, tecla2)
    sleep(1)

def vaiParaMenuCorrespondencia():
    clickEspecifico(1,'f2')
    clickEspecifico(1,'1')
    clickEspecifico(1,'9')

def posicionaMouseEsquerdo(xTela: int, yTela: int):
    '''
        Função para posicionar o ponteiro do mouse em coordenadas específicas.
        Args:
            xTela (int): Inteiro que contêm a coordenada 'x' da tela.
            yTela (int): Inteiro que contêm a coordenada 'y' da tela.
    '''
    tecla.moveTo(xTela, yTela)
    print(f'Posicionado em {xTela}:{yTela}.')

def encerraSecao() -> None:
    print(f'Encerrando seção...')
    clickEspecifico(1,'f2')
    clickEspecifico(1,8)
    clickEspecifico(1,5)
    clickEspecifico(1,'f2')

def entraProfissaoEspecifica(posicao: int) -> None:
    sleep(1)
    for x in range(posicao):
        tecla.hotkey('down')
        print('Baixo.')
        sleep(0.5)
    tecla.hotkey('enter')
    print('Enter.')
    sleep(2)
    tecla.hotkey('up')
    print('Cima.')
    sleep(0.5)
    
def entraTrabalhoEncontrado(dicionarioTrabalho: dict) -> None:
    posicao: int = dicionarioTrabalho[CHAVE_POSICAO] if dicionarioTrabalho[CHAVE_POSICAO] > 0 else 0
    print(f'Entra trabalho na posição: {posicao + 1}.')
    precionaTecla(3, 'up')
    clickEspecifico(posicao + 1, 'down')
    clickEspecifico(1, 'enter')

def vaiParaMenuTrabalhoEmProducao():
    clickEspecifico(1,'f1')
    precionaTecla(9,'up')
    clickEspecifico(1,'left')

def vaiParaOTopoDaListaDeTrabalhosComunsEMelhorados(dicionarioTrabalho):
    print(f'Voltando para o topo da lista!')
    precionaTecla(dicionarioTrabalho[CHAVE_POSICAO] + 5, 'up')

def saiProfissaoVerificada(dicionario):
    print(f'Nem um trabalho disponível está na lista de desejos.')
    clickEspecifico(1, 'f1')
    precionaTecla(dicionario[CHAVE_POSICAO] + 10, 'up')
    clickEspecifico(1, 'left')
    sleep(1)

def preencheCamposLogin(email: str, senha: str) -> None:
    clickEspecifico(1,'f2')
    clickEspecifico(1,0)
    clickEspecifico(1,'f2')
    clickEspecifico(1,'down')
    precionaTecla(30,'backspace')
    tecla.write(email)
    clickEspecifico(1,'down')
    tecla.write(senha)
    clickEspecifico(2,'down')
    clickEspecifico(1,'enter')
    sleep(5)