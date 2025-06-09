import re
from unidecode import unidecode

def textoEhIgual(texto1: str, texto2: str) -> bool:
    '''
        Função para verificar se dois textos são iguais.
        Args:
            texto1 (str): String que contêm o primeiro texto.
            texto2 (str): String que contêm o segundo texto.
        Returns:
            bool: Verdadeiro caso os dois textos sejam iguais.
    '''
    return limpaRuidoTexto(texto1) == limpaRuidoTexto(texto2)

def texto1_pertence_texto2(texto1: str, texto2: str) -> bool:
    '''
        Função para verificar caso texto1 está contido no texto2
        Args:
            texto1 (str): String que contêm o texto a ser verificado
            texto2 (str): String que contêm o texto a ser verificado
        Returns:
            bool: Verdadeiro caso o texto1 está contido no texto2
    '''
    return limpaRuidoTexto(texto= texto1) in limpaRuidoTexto(texto= texto2)

def limpaRuidoTexto(texto: str) -> str:
    '''
        Função para retirar caracteres especiais do texto recebido por parâmetro.
        Args:
            texto (str): String que contêm o texto a ser higienizado.
        Returns:
            str: String que contêm o texto higienizado.
    '''
    texto = '' if texto is None else texto
    padrao: str = '[^a-zA-Z0-9àáãâéêíîóõôúûç_]'
    expressao = re.compile(padrao)
    novaStringPalavras: str = expressao.sub('', texto)
    return unidecode(novaStringPalavras).lower()