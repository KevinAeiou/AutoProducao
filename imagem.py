from teclado import tiraScreenshot
import cv2
import re
import os
import numpy as np
import pytesseract
from time import sleep
from utilitarios import *

class ManipulaImagem:
    def reconheceDigito(self, imagem):
        caminho = r"C:\Program Files\Tesseract-OCR"
        pytesseract.pytesseract.tesseract_cmd = caminho +r"\tesseract.exe"
        digitoReconhecido=pytesseract.image_to_string(imagem, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
        return digitoReconhecido.strip()

    def reconheceTexto(self, imagem):
        caminho = r"C:\Program Files\Tesseract-OCR"
        pytesseract.pytesseract.tesseract_cmd = caminho +r"\tesseract.exe"
        textoReconhecido = pytesseract.image_to_string(imagem, lang="por")
        if len(textoReconhecido) != 0:
            listaCaracteresEspeciais = ['"','',',','.','|','!','@','$','%','¨','&','*','(',')','_','-','+','=','§','[',']','{','}','ª','º','^','~','?','/','°',':',';','>','<','\'','\n']
            for especial in listaCaracteresEspeciais:
                textoReconhecido = textoReconhecido.replace(especial,'')
            return textoReconhecido.strip()
        return None

    def retornaImagemBinarizadaOtsu(self, imagemDesfocada):
        ret, thresh = cv2.threshold(imagemDesfocada, 0, 255,
                                cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        return thresh

    def retornaImagemEqualizada(self, img):
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        return clahe.apply(img)

    def retornaImagemCinza(self, screenshot):
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    def retornaImagemColorida(self, screenshot):
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    def retornaAtualizacaoTela(self):
        return self.retornaImagemColorida(tiraScreenshot())

    def retornaImagemBinarizada(self, image):
        blur = cv2.GaussianBlur(image, (1, 1), cv2.BORDER_DEFAULT)
        ret, thresh = cv2.threshold(blur, 180, 255, cv2.THRESH_BINARY_INV)
        return thresh

    def retornaImagemDitalata(self, imagem, kernel, iteracoes):
        return cv2.dilate(imagem, kernel, iterations = iteracoes)

    def retornaImagemErodida(self,imagem, kernel, iteracoes):
        return cv2.erode(imagem, kernel, iterations = iteracoes)
    
    def mostraImagem(self, indice, imagem, nomeFrame):
        if nomeFrame == None:
            nomeFrame = 'Janela teste'
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

    def reconheceNomeTrabalho(self, tela, y, identificador):
        altura = 34
        if identificador == 1:
            altura = 68
        frameTelaInteira = tela[y:y + altura, 233:478]
        frameNomeTrabalhoTratado = self.retornaImagemCinza(frameTelaInteira)
        frameNomeTrabalhoTratado = self.retornaImagemBinarizada(frameNomeTrabalhoTratado)
        if existePixelPreto(frameNomeTrabalhoTratado):
            return self.reconheceTexto(frameNomeTrabalhoTratado)
        return None
    
    def retornaNomeTrabalhoReconhecido(self, yinicialNome, identificador):
        sleep(1.5)
        return self.reconheceNomeTrabalho(self.retornaAtualizacaoTela(), yinicialNome, identificador)

    def reconheceNomeConfirmacaoTrabalhoProducao(self, tela, tipoTrabalho):
        listaFrames = [[169, 285, 303, 33], [183, 200, 318, 31]] # [x, y, altura, largura]
        posicao = listaFrames[tipoTrabalho]
        frameNomeTrabalho = tela[posicao[1]:posicao[1] + posicao[3], posicao[0]:posicao[0] + posicao[2]]
        frameNomeTrabalhoCinza = self.retornaImagemCinza(frameNomeTrabalho)
        frameNomeTrabalhoBinarizado = self.retornaImagemBinarizada(frameNomeTrabalhoCinza)
        return self.reconheceTexto(frameNomeTrabalhoBinarizado)

    def retornaNomeConfirmacaoTrabalhoProducaoReconhecido(self, tipoTrabalho):
        return self.reconheceNomeConfirmacaoTrabalhoProducao(self.retornaAtualizacaoTela(), tipoTrabalho)

    def reconheceTextoLicenca(self, telaInteira):
        listaLicencas = ['iniciante','principiante','aprendiz','mestre','nenhumitem']
        frameTelaCinza = self.retornaImagemCinza(telaInteira[275:317,169:512])
        frameTelaEqualizado = self.retornaImagemEqualizada(frameTelaCinza)
        textoReconhecido = self.reconheceTexto(frameTelaEqualizado)
        if variavelExiste(textoReconhecido):
            for licenca in listaLicencas:
                if texto1PertenceTexto2(licenca, textoReconhecido):
                    return textoReconhecido
        return None
    
    def retornaTextoLicencaReconhecida(self):
        return self.reconheceTextoLicenca(self.retornaAtualizacaoTela())
    
    def reconheceTextoNomePersonagem(self, tela, posicao):
        posicaoNome = [[2,33,169,27], [190,355,177,30]] # [x, y, altura, largura]
        frameNomePersonagem = tela[posicaoNome[posicao][1]:posicaoNome[posicao][1]+posicaoNome[posicao][3], posicaoNome[posicao][0]:posicaoNome[posicao][0]+posicaoNome[posicao][2]]
        frameNomePersonagemCinza = self.retornaImagemCinza(frameNomePersonagem)
        frameNomePersonagemEqualizada = self.retornaImagemEqualizada(frameNomePersonagemCinza)
        frameNomePersonagemBinarizado = self.retornaImagemBinarizada(frameNomePersonagemEqualizada)
        print(np.sum(frameNomePersonagemBinarizado == 0))
        contadorPixelPretoEhMaiorQueCinquenta = np.sum(frameNomePersonagemBinarizado == 0) > 50
        if contadorPixelPretoEhMaiorQueCinquenta:
            nomePersonagemReconhecido = self.reconheceTexto(frameNomePersonagemBinarizado)
            if variavelExiste(nomePersonagemReconhecido):
                nome = limpaRuidoTexto(nomePersonagemReconhecido)
                print(f'Personagem reconhecido: {nome}.')
                return nome
            if np.sum(frameNomePersonagemBinarizado == 0) >= 170 and np.sum(frameNomePersonagemBinarizado == 0) <= 320:
                return 'provisorioatecair'
        return None
    
    def retornaTextoNomePersonagemReconhecido(self, posicao):
        print(f'Verificando nome personagem...')
        return self.reconheceTextoNomePersonagem(self.retornaAtualizacaoTela(), posicao)
    
    def reconheceTextoErro(self, tela):
        return self.reconheceTexto(tela[318:318+120,150:526])

    def retornaErroReconhecido(self):
        return self.reconheceTextoErro(self.retornaAtualizacaoTela())
    
    def reconheceTextoMenu(self, tela, x, y, largura):
        alturaFrame = 30
        frameTela = tela[y:y+alturaFrame,x:x+largura]
        if y > alturaFrame:
            frameTela = self.retornaImagemCinza(frameTela)
            frameTela = self.retornaImagemEqualizada(frameTela)
            frameTela = self.retornaImagemBinarizada(frameTela)
        if existePixelPretoSuficiente(frameTela):
            texto = self.reconheceTexto(frameTela)
            if variavelExiste(texto):
                return limpaRuidoTexto(texto)
        return None

    def retornaTextoMenuReconhecido(self, x, y, largura):        
        return self.reconheceTextoMenu(self.retornaAtualizacaoTela(), x, y, largura)
    
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
    
    def reconheceTextoSair(self, tela):
        frameTelaTratado = self.retornaImagemCinza(tela[tela.shape[0]-50:tela.shape[0]-15,50:50+60])
        frameTelaTratado = self.retornaImagemBinarizada(frameTelaTratado)
        contadorPixelPreto = np.sum(frameTelaTratado==0)
        if contadorPixelPreto > 100 and contadorPixelPreto < 400:
            texto = self.reconheceTexto(frameTelaTratado)
            if variavelExiste(texto):
                return limpaRuidoTexto(texto)
        return None
    
    def retornaTextoSair(self):
        return self.reconheceTextoSair(self.retornaAtualizacaoTela())
        
    def existePixelCorrespondencia(self):
        confirmacao = False
        tela = self.retornaAtualizacaoTela()
        frameTela = tela[665:690, 644:675]
        contadorPixelCorrespondencia = np.sum(frameTela==(173,239,247))
        if contadorPixelCorrespondencia > 50:
            print(f'Há correspondencia!')
            confirmacao = True
        else:
            print(f'Não há correspondencia!')
        return confirmacao
    
    def existeCorrespondencia(self):
        print(f'Verificando se possui correspondencia...')
        return np.sum(self.retornaAtualizacaoTela()[233:233+30, 235:235+200] == 255) > 0
    
    def retornaTextoCorrespondenciaReconhecido(self, telaInteira):
        return self.reconheceTexto(telaInteira[231:231+50, 168:168+343])
    
    def retornaValorDoTrabalhoVendido(self, telaInteira):
        frameTelaTratado = self.retornaImagemCinza(telaInteira[490:490+30,410:410+100])
        frameTelaTratado = self.retornaImagemBinarizada(frameTelaTratado)
        ouro = re.sub('[^0-9]','', self.reconheceDigito(frameTelaTratado))
        if ouro.isdigit():
            return int(ouro)
        return 0
    
    def reconheceEstadoTrabalho(self, tela):
        texto = self.reconheceTexto(tela[311:311+43, 233:486])
        if variavelExiste(texto):
            if texto1PertenceTexto2("pedidoconcluido", texto):
                print(f'Pedido concluído!')
                return CODIGO_CONCLUIDO
            if texto1PertenceTexto2('adicionarumnovopedido', texto):
                print(f'Nem um trabalho!')
                return CODIGO_PARA_PRODUZIR
        print(f'Em produção...')
        return CODIGO_PRODUZINDO
    
    def retornaEstadoTrabalho(self):
        return self.reconheceEstadoTrabalho(self.retornaAtualizacaoTela())

    def reconheceNomeTrabalhoFrameProducao(self, tela):
        tela = self.retornaImagemBinarizada(tela[285:285+37, 233:486])
        return self.reconheceTexto(tela)
    
    def retornaNomeTrabalhoFrameProducaoReconhecido(self):
        return self.reconheceNomeTrabalhoFrameProducao(self.retornaAtualizacaoTela())
    
    def retornaReferencia(self):
        print(f'Buscando referência "PEGAR"...')
        telaInteira = self.retornaAtualizacaoTela()
        frameTela = telaInteira[0:telaInteira.shape[0],330:488]
        imagem = self.retornaImagemCinza(frameTela)
        imagem = cv2.GaussianBlur(imagem,(1,1),0)
        imagem = cv2.Canny(imagem,150,180)
        kernel = np.ones((2,2),np.uint8)
        imagem = self.retornaImagemDitalata(imagem,kernel,1)
        imagem = self.retornaImagemErodida(imagem,kernel,1)
        contornos,h1 = cv2.findContours(imagem,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for cnt in contornos:
            area = cv2.contourArea(cnt)
            if area > 4500 and area < 5700:
                x, y, l, a = cv2.boundingRect(cnt)
                print(f'Area:{area}, x:{x}, y:{y}.')
                cv2.rectangle(frameTela,(x,y),(x+l,y+a),(0,255,0),2)
                centroX = 330+x+(l/2)
                centroY = y+(a/2)
                return [centroX, centroY]
        return None