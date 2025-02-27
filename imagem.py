from teclado import tiraScreenshot
import cv2
import os
import numpy as np
import pytesseract
from time import sleep
from utilitarios import *
from pytesseract import Output

class ManipulaImagem:
    def __init__(self):
        self.configuraTesseract()
        
    def configuraTesseract(self):
        caminho: str = r"C:\Program Files\Tesseract-OCR"
        pytesseract.pytesseract.tesseract_cmd = caminho +r"\tesseract.exe"

    def retornaImagemParaDicionario(self, imagem):
        return pytesseract.image_to_data(imagem, lang="por", config='--psm 6', output_type= Output.DICT)
        
    def reconheceDigito(self, imagem):
        caminho = r"C:\Program Files\Tesseract-OCR"
        pytesseract.pytesseract.tesseract_cmd = caminho +r"\tesseract.exe"
        digitoReconhecido=pytesseract.image_to_string(imagem, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
        return digitoReconhecido.strip()

    def reconheceTexto(self, imagem: tuple, confianca: int = 80) -> str | None:
        resultado: dict = self.retornaImagemParaDicionario(imagem)
        listaPalavras: list[str] = []
        for i in range(len(resultado['text'])):
            if resultado['conf'][i] > confianca:
                listaPalavras.append(resultado['text'][i])
        stringPalavras: str = ''.join(listaPalavras)
        return None if tamanhoIgualZero(lista= stringPalavras) else limpaRuidoTexto(texto= stringPalavras)

    def retornaImagemBinarizadaOtsu(self, imagemDesfocada):
        ret, thresh = cv2.threshold(imagemDesfocada, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        return thresh

    def retornaImagemEqualizada(self, img):
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        return clahe.apply(img)

    def retornaImagemCinza(self, imagem):
        return cv2.cvtColor(np.array(imagem), cv2.COLOR_RGB2GRAY)

    def retornaImagemColorida(self, screenshot):
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

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
    
    def mostraImagem(self, indice, imagem, nomeFrame = 'Janela teste'):
        cv2.imshow(nomeFrame, imagem)
        cv2.waitKey(indice)
        cv2.destroyAllWindows()

    def abreImagem(self, caminhoImagem):
        return cv2.imread(caminhoImagem)
    
    def salvaNovaTela(self, nomeImagem):
        imagem = cv2.cvtColor(np.array(tiraScreenshot()), cv2.COLOR_RGB2BGR)
        if os.path.isdir('tests/imagemTeste'):
            cv2.imwrite('tests/imagemTeste/{}'.format(nomeImagem),imagem)
        else:
            os.makedirs('tests/imagemTeste')
            cv2.imwrite('tests/imagemTeste/{}'.format(nomeImagem),imagem)

    def reconheceNomeTrabalho(self, tela: np.ndarray, y: int, identificador: int) -> str | None:
        altura: int = 68 if identificador == 1 else 34
        frameTrabalho: np.ndarray = tela[y : y + altura, 233 : 478]
        frameNomeTrabalhoTratado: np.ndarray = self.retornaImagemCinza(frameTrabalho)
        frameNomeTrabalhoTratado = self.retornaImagemBinarizada(frameNomeTrabalhoTratado)
        return self.reconheceTexto(frameNomeTrabalhoTratado) if existePixelPreto(frameNomeTrabalhoTratado) else None
    
    def retornaNomeTrabalhoReconhecido(self, yinicialNome, identificador):
        return self.reconheceNomeTrabalho(self.retornaAtualizacaoTela(), yinicialNome, identificador)

    def reconheceNomeConfirmacaoTrabalhoProducao(self, tela: np.ndarray, tipoTrabalho: int) -> str | None:
        arrayFrames: tuple = ((169, 285, 303, 33), (183, 200, 318, 31)) # [x, y, altura, largura]
        posicao: int = arrayFrames[tipoTrabalho]
        frameNomeTrabalho: np.ndarray = tela[posicao[1]:posicao[1] + posicao[3], posicao[0]:posicao[0] + posicao[2]]
        frameNomeTrabalhoCinza: np.ndarray = self.retornaImagemCinza(imagem= frameNomeTrabalho)
        frameNomeTrabalhoBinarizado: np.ndarray = self.retornaImagemBinarizada(imagem= frameNomeTrabalhoCinza, limiteMinimo= 115)
        return self.reconheceTexto(frameNomeTrabalhoBinarizado, confianca=50)

    def retornaNomeConfirmacaoTrabalhoProducaoReconhecido(self, tipoTrabalho: int) -> str | None:
        return self.reconheceNomeConfirmacaoTrabalhoProducao(self.retornaAtualizacaoTela(), tipoTrabalho= tipoTrabalho)

    def reconheceLicenca(self, telaInteira) -> str | None:
        listaLicencas = LISTA_LICENCAS
        listaLicencas.append('Nenhum item')
        frameTelaCinza = self.retornaImagemCinza(telaInteira[0 : telaInteira.shape[0], 0 : telaInteira.shape[1] // 2])
        fremaTelaBinarizada = self.retornaImagemBinarizada(imagem= frameTelaCinza, limiteMinimo= 120)
        textoReconhecido: str = self.reconheceTexto(fremaTelaBinarizada)
        if textoReconhecido is None: return None
        for licenca in listaLicencas:
            if texto1PertenceTexto2(licenca, textoReconhecido): return licenca
        return None
    
    def retornaTextoLicencaReconhecida(self):
        return self.reconheceLicenca(self.retornaAtualizacaoTela())
    
    def reconheceTextoNomePersonagem(self, tela, posicao: int) -> str | None:
        x: int = tela.shape[1]//7
        y: int = 14*(tela.shape[0]//30)
        posicaoNome = [[2,33,210,45], [x,y,200,40]] # [x, y, altura, largura]
        frameNomePersonagem = tela[posicaoNome[posicao][1]:posicaoNome[posicao][1]+posicaoNome[posicao][3], posicaoNome[posicao][0]:posicaoNome[posicao][0]+posicaoNome[posicao][2]]
        frameCinza = self.retornaImagemCinza(frameNomePersonagem)
        frameBinarizado = self.retornaImagemBinarizada(imagem= frameCinza, limiteMinimo= 150)
        return self.reconheceTexto(imagem= frameBinarizado, confianca= 40)
    
    def retornaTextoNomePersonagemReconhecido(self, posicao: int) -> str | None:
        print(f'Verificando nome personagem...')
        return self.reconheceTextoNomePersonagem(self.retornaAtualizacaoTela(), posicao)
    
    def reconheceTextoErro(self, tela):
        return self.reconheceTexto(tela[318:318+120,150:526])

    def retornaErroReconhecido(self):
        return self.reconheceTextoErro(self.retornaAtualizacaoTela())
    
    def verificaMenuReferenciaInicial(self, tela):
        posicaoMenu = [[703,627],[712,1312]]
        for posicao in posicaoMenu:
            frameTela = tela[posicao[0]:posicao[0] + 53, posicao[1]:posicao[1] + 53]
            contadorPixelPreto = np.sum(frameTela == (85,204,255))
            if contadorPixelPreto == 1720:
                return True
        return False
    
    def verificaMenuReferencia(self):
        return self.verificaMenuReferenciaInicial(self.retornaAtualizacaoTela())
    
    def reconheceTextoMenu(self, tela) -> str | None:
        frameTela = tela[0 : tela.shape[0], 0 : tela.shape[1]//2]
        frameTelaTratado = self.retornaImagemCinza(frameTela)
        frameTelaTratado = self.retornaImagemBinarizada(imagem= frameTelaTratado, limiteMinimo= 155)
        return self.reconheceTexto(imagem= frameTelaTratado, confianca= 50)

    def retornaTextoMenuReconhecido(self) -> str | None:        
        return self.reconheceTextoMenu(self.retornaAtualizacaoTela())
    
    def reconheceTextoSair(self, tela: np.ndarray):
        frameTelaTratado = self.retornaImagemCinza(tela[tela.shape[0]-55:tela.shape[0]-15,50:50+80])
        frameTelaTratado = self.retornaImagemBinarizada(frameTelaTratado)
        return self.reconheceTexto(frameTelaTratado)
    
    def retornaTextoSair(self):
        return self.reconheceTextoSair(self.retornaAtualizacaoTela())
        
    def verificaPixelCorrespondencia(self, tela):
        frameTela = tela[665:690, 644:675]
        contadorPixelCorrespondencia = np.sum(frameTela==(173,239,247))
        if contadorPixelCorrespondencia > 50:
            print(f'Há correspondencia!')
            return True
        print(f'Não há correspondencia!')
        return False

    def retornaExistePixelCorrespondencia(self):
        return self.verificaPixelCorrespondencia(self.retornaAtualizacaoTela())
        
    def existeCorrespondencia(self):
        print(f'Verificando se possui correspondencia...')
        return self.quantidadePixelBrancoEhMaiorQueZero(self.retornaAtualizacaoTela())

    def quantidadePixelBrancoEhMaiorQueZero(self, imagem):
        return np.sum(imagem[233:233+30, 235:235+200] == 255) > 0
    
    def reconheceTextoCorrespondencia(self, tela):
        return self.reconheceTexto(tela[231:231+100, 168:168+343])

    def retornaTextoCorrespondenciaReconhecido(self):
        return self.reconheceTextoCorrespondencia(self.retornaAtualizacaoTela())
    
    def reconheceEstadoTrabalho(self, tela) -> int:
        texto: str = self.reconheceTexto(tela[311:311+43, 233:486])
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

    def reconheceNomeTrabalhoFrameProducao(self, tela):
        tela = self.retornaImagemBinarizada(tela[285:285+37, 233:486])
        return self.reconheceTexto(tela)
    
    def retornaNomeTrabalhoFrameProducaoReconhecido(self):
        return self.reconheceNomeTrabalhoFrameProducao(self.retornaAtualizacaoTela())
    
    def desenhaRetangulo(self, imagem, contorno, cor = (0,255,0)):
        x,y,l,a=cv2.boundingRect(contorno)
        area = l * a
        self.escreveTexto(str(area), imagem, contorno)
        return cv2.rectangle(imagem,(x,y),(x+l,y+a), cor ,2)

    def retonaImagemRedimensionada(self, imagem, porcentagem):
        return cv2.resize(imagem,(0,0),fx=porcentagem,fy=porcentagem)

    def retornaReferencia(self, imagem: np.ndarray) -> tuple | None:
        print(f'Buscando referência "PEGAR"...')
        imagem = imagem[0:imagem.shape[0], 0:imagem.shape[1]//2]
        imagemTratada = self.retornaImagemCinza(imagem= imagem)
        imagemTratada = self.retornaImagemBinarizada(imagem= imagemTratada, limiteMinimo=150)
        resultado: dict = self.retornaImagemParaDicionario(imagem= imagemTratada)
        for i in range(len(resultado['text'])):
            if not tamanhoIgualZero(limpaRuidoTexto(texto= resultado["text"][i])) and texto1PertenceTexto2(texto1= resultado["text"][i], texto2= 'Pegar') and resultado["conf"][i] > 90:
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
        imagemTratada = self.retornaImagemCinza(imagem= imagem)
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
        # self.mostraImagem(0, imagemTratada)
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
    clickAtalhoEspecifico(tecla1='alt', tecla2='tab')
    sleep(1)
    imagem = ManipulaImagem()
    while True:
        sleep(1)
        print(imagem.retornaNomeConfirmacaoTrabalhoProducaoReconhecido(tipoTrabalho= 0))
        # resultado = imagem.retornaReferenciaLeiloeiro()
        # print(resultado)
        # if resultado is None:
        #     continue
        # posicionaMouseEsquerdo(x_tela= resultado[0], y_tela= resultado[1]+ 100)