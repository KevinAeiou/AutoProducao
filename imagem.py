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
        # self.mostraImagem(0, frameNomeTrabalho, None)
        # frameNomeTrabalhoCinza = self.retornaImagemCinza(frameNomeTrabalho)
        frameNomeTrabalhoBinarizado = self.retornaImagemBinarizada(frameNomeTrabalho)
        # self.mostraImagem(0, frameNomeTrabalhoBinarizado, None)
        return self.reconheceTexto(frameNomeTrabalhoBinarizado)

    def retornaNomeConfirmacaoTrabalhoProducaoReconhecido(self, tipoTrabalho):
        return self.reconheceNomeConfirmacaoTrabalhoProducao(self.retornaAtualizacaoTela(), tipoTrabalho)

    def reconheceTextoLicenca(self, telaInteira):
        listaLicencas = ['novato','iniciante','aprendiz','mestre','nenhumitem']
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
        return np.sum(self.retornaAtualizacaoTela()[233:233+30, 235:235+200] == 255) > 0
    
    def reconheceTextoCorrespondencia(self, tela):
        return self.reconheceTexto(tela[231:231+100, 168:168+343])

    def retornaTextoCorrespondenciaReconhecido(self):
        return self.reconheceTextoCorrespondencia(self.retornaAtualizacaoTela())
    
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
    
    def desenhaRetangulo(self, imagem, contorno):
        x,y,l,a=cv2.boundingRect(contorno)
        return cv2.rectangle(imagem,(x,y),(x+l,y+a),(0,255,0),2)

    def retonaImagemRedimensionada(self, imagem, porcentagem):
        return cv2.resize(imagem,(0,0),fx=porcentagem,fy=porcentagem)

    def retornaReferencia(self, imagem):
        print(f'Buscando referência "PEGAR"...')
        imagem = imagem[0:imagem.shape[0],330:488]
        imagem = imagem[0:imagem.shape[0],0:imagem.shape[1]//2]
        imagemCinza = self.retornaImagemCinza(imagem)
        imagemLimiarizada = cv2.Canny(imagemCinza,143,255)
        kernel = np.ones((2,2),np.uint8)
        imagemDilatada = self.retornaImagemDitalata(imagemLimiarizada,kernel, 1)
        contornos, h1 = cv2.findContours(imagemDilatada,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for contorno in contornos:
            area = cv2.contourArea(contorno)
            epsilon = 0.02 * cv2.arcLength(contorno, True)
            aproximacao = cv2.approxPolyDP(contorno, epsilon, True)
            if cv2.isContourConvex(aproximacao) and len(aproximacao) == 4 and area >= 3000 and area <= 3800:
                x, y, l, a = cv2.boundingRect(contorno)
                if l > a:
                    centroX = x+(l/2)
                    centroY = y+(a/2)
                    return [centroX, centroY]
        return None
    
    def verificaRecompensaDisponivel(self):
        telaInteira = self.retornaAtualizacaoTela()
        return self.retornaReferencia(telaInteira)

    def escreveTexto(self, frameTela, contorno):
        area = cv2.contourArea(contorno)
        texto = f'Area: {area}'
        x,y,l,a=cv2.boundingRect(contorno)
        posicao = (x, y)
        fonte = cv2.FONT_HERSHEY_SIMPLEX
        escala = 0.5
        cor = (255, 255, 255)
        thickness = 1
        return cv2.putText(frameTela, texto, posicao, fonte, escala, cor, thickness, cv2.LINE_AA)
    
    def retornaReferenciaTeste(self):
        telaInteira = self.abreImagem('tests/imagemTeste/testeMenuRecompensasDiarias2.png')
        telaInteira = self.retonaImagemRedimensionada(telaInteira, 0.8)
        frameTela = telaInteira[0:telaInteira.shape[0],0:telaInteira.shape[1]//2]
        imagemCinza = self.retornaImagemCinza(frameTela)
        # self.mostraImagem(0, imagemCinza, 'TELA_CINZA')
        # imagemDesfocada = cv2.GaussianBlur(imagemCinza,(15,15), 1)
        # self.mostraImagem(0, imagemDesfocada, 'TELA_DESFOCADA')
        imagemLimiarizada = cv2.Canny(imagemCinza,143,255)
        # self.mostraImagem(0, imagemLimiarizada, 'TELA_LIMIARIZADA')
        kernel = np.ones((2,2),np.uint8)
        imagemDilatada = self.retornaImagemDitalata(imagemLimiarizada,kernel, 1)
        # imagemErodida = self.retornaImagemErodida(imagemDilatada,kernel, 1)
        # saida2 = cv2.hconcat([imagemDilatada, imagemErodida])
        # saida3 = cv2.vconcat([saida1, saida2])
        # saida3 = self.retonaImagemRedimensionada(saida3, 0.6)
        # self.mostraImagem(0, saida3, 'SAIDA')
        contornos, h1 = cv2.findContours(imagemDilatada,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for contorno in contornos:
            area = cv2.contourArea(contorno)
            epsilon = 0.02 * cv2.arcLength(contorno, True)
            aproximacao = cv2.approxPolyDP(contorno, epsilon, True)
            if cv2.isContourConvex(aproximacao) and len(aproximacao) == 4 and area >= 3000 and area <= 3800:
                x, y, l, a = cv2.boundingRect(contorno)
                if l > a:
                    frameTela = self.desenhaRetangulo(frameTela, contorno)
                    frameTela = self.escreveTexto(frameTela, contorno)
                    centroX = 330+x+(l/2)
                    centroY = y+(a/2)
                    print(f'Centro da forma: {centroX} - {centroY} - {area}')
        # saida1 = cv2.hconcat([imagemLimiarizada, frameTela])
        # self.mostraImagem(0, imagemLimiarizada, 'IMAGEM_LIMIARIZADA')
        self.mostraImagem(0, imagemDilatada, 'TELA_DILATADA')
        # self.mostraImagem(0, imagemErodida, 'TELA_ERODIDA')
        self.mostraImagem(0, frameTela, 'BORDAS_RECONHECIDAS')

if __name__=='__main__':
    imagem = ManipulaImagem()
    imagem.retornaReferenciaTeste()
