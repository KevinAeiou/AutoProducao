from teclado import tiraScreenshot
import cv2
import numpy as np
import pytesseract

def reconheceDigito(imagem):
    caminho = r"C:\Program Files\Tesseract-OCR"
    pytesseract.pytesseract.tesseract_cmd = caminho +r"\tesseract.exe"
    digitoReconhecido=pytesseract.image_to_string(imagem, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
    return digitoReconhecido

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

def retornaImagemBinarizada(image):
    blur = cv2.GaussianBlur(image, (1, 1), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(blur, 180, 255, cv2.THRESH_BINARY_INV)
    return thresh

def retornaImagemDitalata(imagem,kernel,iteracoes):
    return cv2.dilate(imagem,kernel,iterations=iteracoes)

def retornaImagemErodida(imagem,kernel,iteracoes):
    return cv2.erode(imagem,kernel,iterations=iteracoes)