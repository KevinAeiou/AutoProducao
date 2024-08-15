from teclado import tiraScreenshot
import cv2
import numpy as np
import pytesseract


def reconheceTexto(imagem):
    texto = None
    caminho = r"C:\Program Files\Tesseract-OCR"
    pytesseract.pytesseract.tesseract_cmd = caminho +r"\tesseract.exe"
    textoReconhecido = pytesseract.image_to_string(imagem, lang="por")
    if len(textoReconhecido) != 0:
        listaCaracteresEspeciais = ['"','',',','.','|','!','@','$','%','¨','&','*','(',')','_','-','+','=','§','[',']','{','}','ª','º','^','~','?','/','°',':',';','>','<','\'','\n']
        for especial in listaCaracteresEspeciais:
            textoReconhecido = textoReconhecido.replace(especial,'')
        texto = textoReconhecido
    return texto

def retornaImagemBinarizadaOtsu(imagemDesfocada):
    ret, thresh = cv2.threshold(imagemDesfocada, 0, 255,
                            cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return thresh

def retornaImagemEqualizada(img):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    return clahe.apply(img)

def retornaImagemCinza(screenshot):
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

def retornaImagemColorida(screenshot):
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def retornaAtualizacaoTela():
    screenshot = tiraScreenshot()
    return retornaImagemColorida(screenshot)