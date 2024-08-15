from unidecode import unidecode


def textoEhIgual(texto1, texto2):
    return limpaRuidoTexto(texto1) == limpaRuidoTexto(texto2)

def tamanhoIgualZero(lista):
    return len(lista) == 0

def variavelExiste(variavel):
    return variavel != None

def limpaRuidoTexto(texto):
    return unidecode(texto).replace(' ','').replace('-','').lower()