from time import sleep
import pyautogui as tecla
from constantes import *

def clickAtalhoEspecifico(tecla1, tecla2):
    sleep(1)
    tecla.hotkey(tecla1,tecla2)
    sleep(1)
    
def click_especifico(cliques: int, tecla_especifica: str):
    '''
        Função para realizar cliques em teclas específicas.
        Args:
            cliques (int): Inteiro que contêm a quantidade de cliques a serem realizados.
            teclaEspecifica (str): String que contêm a tecla a ser clicada.
    '''
    sleep(0.5)
    for x in range(cliques):
        if isinstance(tecla_especifica, int):
            tecla_especifica += 1
            teclaNumerica = f'num{tecla_especifica}'
        else:
            teclaNumerica = tecla_especifica
        tecla.hotkey(teclaNumerica)
        print(f'{tecla_especifica}.')
        sleep(0.5)

def preciona_tecla(cliques: int, teclaEspecifica: str):
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

def clique_mouse_esquerdo(cliques: int = 1, xTela: int = 45, yTela: int = 45):
    '''
        Função para clicar na tela com o botão esquerdo do mouse.
        Args:
            cliques (int): Inteiro que contêm a quantidade de cliques a serem realizados. Um (1) como padrão.
            xTela (int): Inteiro que contêm a posição 'x' da tela. Um (45) como padrão.
            yTela (int): Inteiro que contêm a posição 'y' da tela. Um (45) como padrão.
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
    click_especifico(1,'f2')
    click_especifico(1,'1')
    click_especifico(1,'9')

def posiciona_mouse_esquerdo(xTela: int= None, yTela: int= None):
    '''
        Função para posicionar o ponteiro do mouse em coordenadas específicas da tela.
        Posiciona ao centro caso não seja passado nem um parâmetro.
        Args:
            xTela (int): Inteiro que contêm a coordenada 'x' da tela.
            yTela (int): Inteiro que contêm a coordenada 'y' da tela.
    '''
    if xTela is None or yTela is None:
        tela = tecla.screenshot()
        xTela, yTela = tela.width // 2, tela.height // 2
    tecla.moveTo(xTela, yTela)
    print(f'Posicionado em {xTela}:{yTela}.')

def encerraSecao() -> None:
    print(f'Encerrando seção...')
    click_especifico(1,'f2')
    click_especifico(1,8)
    click_especifico(1,5)
    click_especifico(1,'f2')

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
    
def entra_trabalho_encontrado(dicionarioTrabalho: dict) -> None:
    posicao: int = dicionarioTrabalho[CHAVE_POSICAO] if dicionarioTrabalho[CHAVE_POSICAO] > 0 else 0
    print(f'Entra trabalho na posição: {posicao + 1}.')
    preciona_tecla(3, 'up')
    click_especifico(posicao + 1, 'down')
    click_especifico(1, 'enter')

def vai_para_menu_trabalho_em_producao():
    click_especifico(1,'f1')
    preciona_tecla(9,'up')
    click_especifico(1,'left')

def vai_para_topo_da_lista_de_trabalhos_comuns_e_melhorados(dicionarioTrabalho):
    print(f'Voltando para o topo da lista!')
    preciona_tecla(dicionarioTrabalho[CHAVE_POSICAO] + 5, 'up')

def saiProfissaoVerificada(dicionario):
    print(f'Nem um trabalho disponível está na lista de desejos.')
    click_especifico(1, 'f1')
    preciona_tecla(dicionario[CHAVE_POSICAO] + 10, 'up')
    click_especifico(1, 'left')
    sleep(1)

def preencheCamposLogin(email: str, senha: str) -> None:
    click_especifico(1,'f2')
    click_especifico(1,0)
    click_especifico(1,'f2')
    click_especifico(1,'down')
    preciona_tecla(30,'backspace')
    tecla.write(email)
    click_especifico(1,'down')
    tecla.write(senha)
    click_especifico(2,'down')
    click_especifico(1,'enter')
    sleep(5)