from teclado import tiraScreenshot
import cv2
import os
import numpy as np
from numpy import ndarray
import pytesseract
from time import sleep
from utilitarios import *
from pytesseract import Output
from utilitariosTexto import texto1PertenceTexto2, limpaRuidoTexto

class ManipulaImagem:
    def __init__(self):
        self.configuraTesseract()
        
    def configuraTesseract(self):
        caminho: str = r"C:\Program Files\Tesseract-OCR"
        pytesseract.pytesseract.tesseract_cmd = caminho +r"\tesseract.exe"

    def retornaImagemParaDicionario(self, imagem):
        return pytesseract.image_to_data(imagem, lang="por", config='--psm 6', output_type= Output.DICT)
        
    def reconheceDigito(self, imagem):
        caminho: str = r"C:\Program Files\Tesseract-OCR"
        pytesseract.pytesseract.tesseract_cmd = caminho +r"\tesseract.exe"
        digitoReconhecido: str = pytesseract.image_to_string(imagem, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
        return digitoReconhecido.strip()

    def reconheceTexto(self, imagem: tuple, confianca: int = 80) -> str | None:
        resultado: dict = self.retornaImagemParaDicionario(imagem)
        listaPalavras: list[str] = []
        for i in range(len(resultado['text'])):
            if resultado['conf'][i] > confianca:
                listaPalavras.append(resultado['text'][i])
        stringPalavras: str = ''.join(listaPalavras)
        return None if ehVazia(lista= stringPalavras) else limpaRuidoTexto(texto= stringPalavras)

    def retornaImagemBinarizadaOtsu(self, imagem, limiarMinimo: int = 0, limiarMaximo: int = 255):
        ret, imagemBinarizada = cv2.threshold(imagem, limiarMinimo, limiarMaximo, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        return imagemBinarizada

    def retornaImagemEqualizada(self, img):
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        return clahe.apply(img)

    def retornaImagemCinza(self, imagem):
        return cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)

    def retornaImagemColorida(self, screenshot):
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    def retornaImagemInvertida(self, telaCinza):
        return cv2.bitwise_not(telaCinza)

    def retornaAtualizacaoTela(self):
        return self.retornaImagemColorida(tiraScreenshot())

    def retornaImagemBinarizada(self, imagem, nucleo: tuple = (1, 1), limiteMinimo: int = 170) -> np.ndarray:
        blur = cv2.GaussianBlur(imagem, nucleo, cv2.BORDER_DEFAULT)
        ret, thresh = cv2.threshold(blur, limiteMinimo, 255, cv2.THRESH_BINARY_INV)
        return thresh

    def retornaImagemDitalata(self, imagem, kernel, iteracoes):
        return cv2.dilate(imagem, kernel, iterations = iteracoes)

    def retornaImagemErodida(self,imagem, kernel, iteracoes):
        return cv2.erode(imagem, kernel, iterations = iteracoes)
    
    def mostraImagem(self, indice, imagem: ndarray, nomeFrame: str = 'Janela teste'):
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
        imagem: ndarray = self.retornaImagemColorida()
        return self.salvaImagemCaminhoEspecifico(nomeArquivo, imagem)

    def salvaImagemCaminhoEspecifico(self, nomeArquivo: str, imagem: ndarray, caminho: str = 'tests\imagemTeste'):
        if os.path.isdir(caminho):
            cv2.imwrite('{}\\{}'.format(caminho, nomeArquivo), imagem)
            return
        os.makedirs(caminho)
        cv2.imwrite('{}\\{}'.format(caminho, nomeArquivo),imagem)

    def reconheceNomeTrabalho(self, tela: ndarray, y: int, identificador: int) -> str | None:
        if tela:
            altura: int = 70 if identificador == 1 else 34
            x, y, largura, altura = self.retornaPosicoes(tela, x= 233, y= y, largura= 245, altura= altura)
            frameTrabalho: ndarray = tela[y : y + altura, x : x + largura]
            frameNomeTrabalhoTratado: ndarray = self.retornaImagemCinza(np.array(frameTrabalho))
            frameNomeTrabalhoTratado = self.retornaImagemBinarizada(frameNomeTrabalhoTratado)
            return self.reconheceTexto(frameNomeTrabalhoTratado) if existePixelPreto(frameNomeTrabalhoTratado) else None
        return None
    
    def retornaNomeTrabalhoReconhecido(self, yinicialNome: int, identificador: int):
        return self.reconheceNomeTrabalho(self.retornaAtualizacaoTela(), yinicialNome, identificador)

    def reconheceNomeConfirmacaoTrabalhoProducao(self, tela: np.ndarray, tipoTrabalho: int) -> str | None:
        arrayFrames: tuple = ((169, 285, 303, 33), (183, 200, 318, 31))
        posicao: int = arrayFrames[tipoTrabalho]
        x, y, largura, altura = self.retornaPosicoes(tela, x= posicao[0], y= posicao[1], largura= posicao[2], altura= posicao[3])
        frameNomeTrabalho: ndarray = tela[y : y + altura, x : x + largura]
        frameNomeTrabalhoCinza: ndarray = self.retornaImagemCinza(imagem= np.array(frameNomeTrabalho))
        frameNomeTrabalhoBinarizado: ndarray = self.retornaImagemBinarizada(imagem= frameNomeTrabalhoCinza, limiteMinimo= 115)
        return self.reconheceTexto(frameNomeTrabalhoBinarizado, confianca=30)

    def retornaNomeConfirmacaoTrabalhoProducaoReconhecido(self, tipoTrabalho: int) -> str | None:
        return self.reconheceNomeConfirmacaoTrabalhoProducao(self.retornaAtualizacaoTela(), tipoTrabalho= tipoTrabalho)

    def reconheceLicenca(self, tela: ndarray) -> str | None:
        listaLicencas: list[str] = LISTA_LICENCAS
        listaLicencas.append('Nenhum item')
        frameTelaCinza: ndarray = self.retornaImagemCinza(np.array(tela[0 : tela.shape[0], 0 : tela.shape[1] // 2]))
        fremaTelaBinarizada: ndarray = self.retornaImagemBinarizada(imagem= frameTelaCinza, limiteMinimo= 120)
        textoReconhecido: str = self.reconheceTexto(fremaTelaBinarizada)
        if textoReconhecido is None: return None
        for licenca in listaLicencas:
            if texto1PertenceTexto2(licenca, textoReconhecido): return licenca
        return None
    
    def retornaTextoLicencaReconhecida(self):
        return self.reconheceLicenca(self.retornaAtualizacaoTela())
    
    def reconheceTextoNomePersonagem(self, tela: ndarray, posicao: int) -> str | None:
        '''
            Método para reconhecimento do nome do personagem em uma posição específica.
            Args:
                tela (ndarray): Imagem da tela atual inteira.
                posicao (int): Posição específica na tela e que o texto deve ser reconhecido.
            Returns:
                str: String que contêm o texto reconhecido.
        '''
        x: int = tela.shape[1]//7
        y: int = 14*(tela.shape[0]//30)
        posicaoNome: list[tuple] = [(2, 33, 210, 45), (x, y, 200, 40)] # [x, y, altura, largura]
        frameNomePersonagem: ndarray = tela[
            posicaoNome[posicao][1] : posicaoNome[posicao][1]+posicaoNome[posicao][3], 
            posicaoNome[posicao][0] : posicaoNome[posicao][0]+posicaoNome[posicao][2]]
        frameCinza: ndarray = self.retornaImagemCinza(np.array(frameNomePersonagem))
        frameBinarizado: ndarray = self.retornaImagemBinarizada(imagem= frameCinza, limiteMinimo= 100)
        return self.reconheceTexto(imagem= frameBinarizado, confianca= 40)
    
    def retornaTextoNomePersonagemReconhecido(self, posicao: int) -> str | None:
        print(f'Reconhecendo nome do personagem na posição {posicao}')
        return self.reconheceTextoNomePersonagem(self.retornaAtualizacaoTela(), posicao)
    
    def reconheceTextoErro(self, tela):
        return self.reconheceTexto(tela[318:318+120,150:526])

    def retornaErroReconhecido(self):
        return self.reconheceTextoErro(self.retornaAtualizacaoTela())
    
    def verificaMenuReferenciaInicial(self, tela: ndarray):
        posicaoMenu: tuple= ([tela.shape[0], int(tela.shape[1]//2)], [tela.shape[0], tela.shape[1]])
        for posicao in posicaoMenu:
            _, _, largura, altura = self.retornaPosicoes(tela, x= 233, y= 311, largura= 55, altura= 55)
            frameTela: ndarray= tela[posicao[0] - altura:posicao[0], posicao[1] - largura:posicao[1]]
            contadorPixelPreto = np.sum(frameTela == (85,204,255))
            if contadorPixelPreto >= 1720:
                return True
        return False

    def resolucaoEh1366x768(self, tela: ndarray):
        return tela.shape[0] == 768 and tela.shape[1] == 1366

    def retornaRazaoEntreTelas(self, tela: ndarray) -> tuple:
        '''
            Função para encontrar as razões entre alturas e larguras da resolução de tela atual e resolução (1366x768)
            Args:
                tela (ndarray): Imagem da tela atual a ser encontrada as razões
            Returns:
                tuple: Tupla de valores encontrados (y, x)
        '''
        razaoX: float= tela.shape[1] / 1366
        razaoY: float= tela.shape[0] / 768
        return (razaoY, razaoX)
    
    def verificaMenuReferencia(self):
        return self.verificaMenuReferenciaInicial(self.retornaAtualizacaoTela())
    
    def reconheceTextoMenu(self, tela: ndarray) -> str | None:
        frameTela: ndarray = tela[0 : tela.shape[0], 0 : tela.shape[1]//2]
        frameTelaTratado: ndarray = self.retornaImagemCinza(np.array(frameTela))
        frameTelaTratado = self.retornaImagemBinarizada(imagem= frameTelaTratado, limiteMinimo= 155)
        return self.reconheceTexto(imagem= frameTelaTratado, confianca= 50)

    def retornaTextoMenuReconhecido(self) -> str | None:        
        return self.reconheceTextoMenu(self.retornaAtualizacaoTela())
    
    def reconheceTextoSair(self, tela: np.ndarray):
        x, _, largura, _ = self.retornaPosicoes(tela, x= 50, y= 665, largura= 80, altura= 55)
        frameTelaTratado: ndarray = self.retornaImagemCinza(np.array(tela[tela.shape[0] - 55 : tela.shape[0] - 15 , x : x + largura]))
        frameTelaTratado = self.retornaImagemBinarizada(frameTelaTratado)
        return self.reconheceTexto(frameTelaTratado)
    
    def retornaTextoSair(self):
        return self.reconheceTextoSair(self.retornaAtualizacaoTela())
        
    def verificaPixelCorrespondencia(self, tela: ndarray):
        x: int = int(tela.shape[1]//2)
        _, y, largura, altura = self.retornaPosicoes(tela, x= 0, y= 665, largura= 36, altura= 30)
        frameTela: ndarray = tela[y : y + altura, x - largura : x]
        contadorPixelCorrespondencia: int = np.sum(frameTela==(173,239,247))
        return True if contadorPixelCorrespondencia > 50 else False

    def retornaExistePixelCorrespondencia(self):
        return self.verificaPixelCorrespondencia(self.retornaAtualizacaoTela())
        
    def existeCorrespondencia(self):
        print(f'Verificando se possui correspondencia...')
        return self.quantidadePixelBrancoEhMaiorQueZero(self.retornaAtualizacaoTela())

    def quantidadePixelBrancoEhMaiorQueZero(self, tela: ndarray) -> bool:
        x, y, largura, altura = self.retornaPosicoes(tela, x= 235, y= 233, largura= 200, altura= 30)
        frame: ndarray = tela[y : y + altura, x : x + largura]
        self.mostraImagem(1, frame)
        return np.sum(frame == 255) > 0
    
    def reconheceTextoCorrespondencia(self, tela: ndarray):
        x, y, largura, altura = self.retornaPosicoes(tela, x= 168, y= 231, largura= 343, altura= 130)
        frameTela: ndarray = tela[y : y + altura, x : x + largura]
        return self.reconheceTexto(frameTela)

    def retornaTextoCorrespondenciaReconhecido(self):
        return self.reconheceTextoCorrespondencia(self.retornaAtualizacaoTela())
    
    def retornaPosicoes(self, tela: ndarray, x: int, y: int, largura: int, altura: int) -> int:
        if not self.resolucaoEh1366x768(tela):
            razoes: tuple = self.retornaRazaoEntreTelas(tela)
            x = int(x * razoes[1])
            y = int(y * razoes[0])
            largura = int(largura * razoes[1])
            altura = int(altura * razoes[0])
        return x, y, largura, altura


    def reconheceEstadoTrabalho(self, tela: ndarray) -> int:
        x, y, largura, altura = self.retornaPosicoes(tela, x= 233, y= 311, largura= 255, altura= 43)
        texto: str = self.reconheceTexto(tela[y : y + altura, x : x + largura])
        if texto is None:
            print(f'Em produção...')
            return CODIGO_PRODUZINDO
        if texto1PertenceTexto2(texto1= STRING_PEDIDO_CONCLUIDO, texto2= texto):
            print(f'Pedido concluído!')
            return CODIGO_CONCLUIDO
        if texto1PertenceTexto2(texto1= STRING_ADICIONAR_NOVO_PEDIDO, texto2= texto):
            print(f'Nem um trabalho!')
            return CODIGO_PARA_PRODUZIR
        print(f'Em produção...')
        return CODIGO_PRODUZINDO
    
    def retornaEstadoTrabalho(self) -> int:
        return self.reconheceEstadoTrabalho(tela= self.retornaAtualizacaoTela())

    def reconheceNomeTrabalhoFrameProducao(self, tela: ndarray) -> str | None:
        '''
            Método para analise e reconhecimento do nome do trabalho para produção concluído.
            Args:
                tela (ndarray): Imagem que contêm os dados do trabalho para produção.
            Returns:
                str: String que contêm o nome do trabalho reconhecido.
        '''
        telaCinza: ndarray = self.retornaImagemCinza(np.array(tela))
        telaInvertida: ndarray = self.retornaImagemInvertida(telaCinza)
        x, y, largura, altura = self.retornaPosicoes(tela, x= 233, y= 289, largura= 253, altura= 37)
        tela = telaInvertida[y : y + altura, x : x + largura]
        return self.reconheceTexto(tela)
    
    def retornaNomeTrabalhoFrameProducaoReconhecido(self):
        return self.reconheceNomeTrabalhoFrameProducao(self.retornaAtualizacaoTela())
    
    def desenhaRetangulo(self, imagem, contorno, cor = (0,255,0)):
        x,y,l,a=cv2.boundingRect(contorno)
        area = l * a
        self.escreveTexto(str(area), imagem, contorno)
        return cv2.rectangle(imagem,(x,y),(x+l,y+a), cor ,2)

    def retonaImagemRedimensionada(self, imagem: ndarray, porcentagem: float):
        return None if imagem is None else cv2.resize(imagem,(0,0),fx=porcentagem,fy=porcentagem)

    def retornaReferencia(self, imagem: np.ndarray) -> tuple | None:
        print(f'Buscando referência "PEGAR"...')
        imagem = imagem[0:imagem.shape[0], 0:imagem.shape[1]//2]
        imagemTratada = self.retornaImagemCinza(imagem= np.array(imagem))
        imagemTratada = self.retornaImagemBinarizada(imagem= imagemTratada, limiteMinimo=150)
        resultado: dict = self.retornaImagemParaDicionario(imagem= imagemTratada)
        for i in range(len(resultado['text'])):
            if not ehVazia(limpaRuidoTexto(texto= resultado["text"][i])) and texto1PertenceTexto2(texto1= resultado["text"][i], texto2= 'Pegar') and resultado["conf"][i] > 90:
                x = resultado["left"][i]
                y = resultado["top"][i]
                l = resultado["width"][i]
                a = resultado["height"][i]
                centroX = x+(l/2)
                centroY = y+(a/2)
                return (centroX, centroY)
        return None
    
    def verificaRecompensaDisponivel(self):
        return self.retornaReferencia(self.retornaAtualizacaoTela())

    def verificaReferenciaLeiloeiro(self, imagem: np.ndarray) -> tuple | None:
        imagem = imagem[0:imagem.shape[0], 0:imagem.shape[1]//2]
        imagemTratada = self.retornaImagemCinza(imagem= np.array(imagem))
        imagemTratada = self.retornaImagemBinarizada(imagem= imagemTratada, limiteMinimo=130)
        resultado: dict = self.retornaImagemParaDicionario(imagem= imagemTratada)
        for i in range(len(resultado['text'])):
            # if resultado["conf"][i] > 0:
            if resultado["conf"][i] > 0 and 'iloei' in resultado["text"][i]:
                print(f'{resultado["text"][i]} | {resultado["conf"][i]}')
                x = resultado["left"][i]
                y = resultado["top"][i]
                l = resultado["width"][i]
                a = resultado["height"][i]
                centroX = x+(l/2)
                centroY = y+(a/2)
                return (centroX, centroY)
        return None
    
    def retornaReferenciaLeiloeiro(self):
        return self.verificaReferenciaLeiloeiro(self.retornaAtualizacaoTela())

    def escreveTexto(self, texto, frameTela, contorno):
        x,y,l,a=cv2.boundingRect(contorno)
        posicao = (x, y+20)
        fonte = cv2.FONT_HERSHEY_SIMPLEX
        escala = 0.5
        cor = (0, 0, 0)
        thickness = 1
        return cv2.putText(frameTela, texto, posicao, fonte, escala, cor, thickness, cv2.LINE_AA)
    
    def reconheceNomePersonagemTeste(self):
        while True:
            copiaTela = self.retornaAtualizacaoTela()
            print(self.reconheceTextoNomePersonagem(copiaTela, 0))
            sleep(1)
        return

if __name__=='__main__':
    from teclado import clickAtalhoEspecifico, posicionaMouseEsquerdo
    # clickAtalhoEspecifico(tecla1='alt', tecla2='tab')
    sleep(1)
    imagem = ManipulaImagem()
    # telaTeste: ndarray= imagem.abreImagem(caminhoImagem= r'tests\imagemTeste\testeEstadoTrabalhoConcluidoGrandeColecao.png')
    # else:
    #     imagem.mostraImagem(0, frame)
    while True:
        sleep(1)
        frame: ndarray = imagem.retornaImagemColorida()
        frame = imagem.retonaImagemRedimensionada(frame, 0.8)
        imagem.mostraImagem(0, frame)
        # print(imagem.reconheceNomeTrabalho(tela= telaMenuInicial, y= 524, identificador= 1))
        # print(imagem.retornaNomeTrabalhoReconhecido(yinicialNome= 524, identificador= 1))
        # print(imagem.existeCorrespondencia())
        # resultado = imagem.retornaReferenciaLeiloeiro()
        # print(resultado)
        # if resultado is None:
        #     continue
        # posicionaMouseEsquerdo(x_tela= resultado[0], y_tela= resultado[1]+ 100)