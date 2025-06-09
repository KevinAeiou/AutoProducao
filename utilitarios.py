from constantes import *
from modelos.trabalhoEstoque import TrabalhoEstoque
from utilitariosTexto import textoEhIgual, limpaRuidoTexto
import numpy as np
import os

def ehVazia(lista: list) -> bool:
    '''
        Função para verificar se uma lista está vazia
        Args:
            lista (list): Lista a ser verificada
        Returns:
            bool: Verdadeiro caso a lista esteja vazia
    '''
    return len(lista) == 0

def variavelExiste(variavel):
    return variavel != None

def retiraDigitos(texto):
    listaDigitos = ['0','1','2','3','4','5','6','7','8','9']
    for digito in listaDigitos:
        texto = texto.replace(digito,'')
    return texto

def existePixelPreto(frameTela):
    return np.sum(frameTela == 0) > 0

def existePixelPretoSuficiente(frameTela):
    return np.sum(frameTela==0) > 250 and np.sum(frameTela==0) < 3000

def ehMenuInicial(menu: int) -> bool:
    return menu == MENU_INICIAL

def ehMenuProduzir(menu):
    return menu == MENU_PROFISSOES

def ehMenuJogar(menu):
    return menu == MENU_JOGAR

def ehMenuEscolhaPersonagem(menu):
    return menu == MENU_ESCOLHA_PERSONAGEM

def ehMenuTrabalhosDisponiveis(menu):
    return menu == MENU_TRABALHOS_DISPONIVEIS
    
def ehMenuNoticias(menu: int) -> bool:
    return menu == MENU_NOTICIAS

def ehMenuDesconhecido(menu: int) -> bool:
    return menu == MENU_DESCONHECIDO

def haMaisQueUmPersonagemAtivo(listaPersonagemAtivo):
    return not len(listaPersonagemAtivo) == 1

def trabalhoEhColecaoRecursosAvancados(trabalhoProducao):
    return textoEhIgual(trabalhoProducao.nome, 'grandecoleçãoderecursosavançados') or textoEhIgual(trabalhoProducao.nome, 'coletaemmassaderecursosavançados')

def trabalhoEhColecaoRecursosComuns(trabalhoProducao):
    return textoEhIgual(trabalhoProducao.nome, 'grandecoleçãoderecursoscomuns')

def trabalhoEhMelhoriaCatalisadorComposto(trabalhoProducao):
    return textoEhIgual(trabalhoProducao.nome, 'melhoriadocatalizadoramplificado')

def trabalhoEhMelhoriaCatalisadorComum(trabalhoProducao):
    return textoEhIgual(trabalhoProducao.nome, 'melhoriadocatalizadorcomum')

def trabalhoEhMelhoriaSubstanciaComposta(trabalhoProducao):
    return textoEhIgual(trabalhoProducao.nome, 'melhoriadasubstânciacomposta')

def trabalhoEhMelhoriaSubstanciaComum(trabalhoProducao):
    return textoEhIgual(trabalhoProducao.nome, 'melhoriadasubstânciacomum')

def trabalhoEhMelhoriaEssenciaComposta(trabalhoProducao):
    return textoEhIgual(trabalhoProducao.nome, 'melhoriadaessênciacomposta')

def trabalhoEhProducaoLicenca(trabalhoProducao):
    return textoEhIgual(trabalhoProducao.nome,'melhorarlicençacomum') or textoEhIgual(trabalhoProducao.nome,'licençadeproduçãodoaprendiz')

def trabalhoEhMelhoriaEssenciaComum(dicionarioTrabalho):
    return textoEhIgual(dicionarioTrabalho.nome, 'melhoriadaessênciacomum')

def nao_fizer_quatro_verificacoes(dicionarioTrabalho):
    return dicionarioTrabalho[CHAVE_POSICAO] < 4

def chave_dicionario_trabalho_desejado_existe(dicionarioTrabalho):
    return dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] != None

def primeira_busca(dicionarioTrabalho):
    return dicionarioTrabalho[CHAVE_POSICAO] == -1

def ehMenuTrabalhosAtuais(menu: int) -> bool:
    return menu == MENU_TRABALHOS_ATUAIS

def ehMenuTrabalhoEspecifico(menu: int) -> bool:
    return menu == MENU_TRABALHO_ESPECIFICO

def ehMenuLicenca(menu: int) -> bool:
    return menu == MENU_LICENSAS

def ehMenuEscolhaEquipamento(menu: int) -> bool:
    return menu == MENU_ESCOLHA_EQUIPAMENTO

def ehMenuAtributosEquipamento(menu: int) -> bool:
    return menu == MENU_TRABALHOS_ATRIBUTOS

def ehMenuMercado(menu: int) -> bool:
    return menu == MENU_MERCADO

def ehMenuAnuncio(menu: int) -> bool:
    return menu == MENU_ANUNCIO

def ehMenuMeusAnuncios(menu: int) -> bool:
    return menu == MENU_MEUS_ANUNCIOS

def ehMenuOfertaDiaria(menu: int) -> bool:
    return menu == MENU_OFERTA_DIARIA

def ehMenuPersonagem(menu: int) -> bool:
    return menu == MENU_PERSONAGEM

def ehMenuPrincipal(menu: int) -> bool:
    return menu == MENU_PRINCIPAL

def ehMenuRecompensasDiarias(menu: int) -> bool:
    return menu == MENU_RECOMPENSAS_DIARIAS

def ehMenuLojaMilagrosa(menu: int) -> bool:
    return menu == MENU_LOJA_MILAGROSA

def retornaListaDicionarioProfissaoRecursos(nivel: int) -> list[dict[str, list[str]]]:
    listaDicionarioProfissaoRecursos: list[dict[str, list[str]]] = []
    if nivel == 1:
        listaDicionarioProfissaoRecursos = [
                {CHAVE_PROFISSAO_BRACELETES:['Fibra de Bronze','Prata','Pin de Estudante']},
                {CHAVE_PROFISSAO_CAPOTES:['Furador do aprendiz','Tecido delicado','Substância instável']},
                {CHAVE_PROFISSAO_AMULETOS:['Pinça do aprendiz','Jade bruta','Energia inicial']},
                {CHAVE_PROFISSAO_ANEIS:['Molde do aprendiz','Pepita de cobre','Pedra de sombras']},
                {CHAVE_PROFISSAO_ARMADURAS_PESADAS:['Marretão do aprendiz','Placas de cobre','Anéis de bronze']},
                {CHAVE_PROFISSAO_ARMADURA_LEVE:['Faca do aprendiz','Escamas da serpente','Couro resistente']},
                {CHAVE_PROFISSAO_ARMADURAS_DE_TECIDO:['Tesoura do aprendiz','Fio grosseiro','Tecido de linho']},
                {CHAVE_PROFISSAO_ARMAS_CORPO_A_CORPO:['Lascas','Minério de cobre','Mó do aprendiz']},
                {CHAVE_PROFISSAO_ARMA_DE_LONGO_ALCANCE:['Esfera do aprendiz','Varinha de madeira','Cabeça do cajado de jade']}]
        return listaDicionarioProfissaoRecursos
    if nivel == 8:    
        listaDicionarioProfissaoRecursos = [
                {CHAVE_PROFISSAO_BRACELETES:['Fibra de Platina','Âmbarito','Pino do Aprendiz']},
                {CHAVE_PROFISSAO_CAPOTES:['Furador do principiante','Tecido espesso','Substância estável']},
                {CHAVE_PROFISSAO_AMULETOS:['Pinça do principiante','Ônix extraordinária','Éter inicial']},
                {CHAVE_PROFISSAO_ANEIS:['Molde do principiante','Pepita de prata','Pedra da luz']},
                {CHAVE_PROFISSAO_ARMADURAS_PESADAS:['Marretão do principiante','Placas de ferro','Anéis de aço']},
                {CHAVE_PROFISSAO_ARMADURA_LEVE:['Faca do principiante','Escamas do lagarto','Couro grosso']},
                {CHAVE_PROFISSAO_ARMADURAS_DE_TECIDO:['Tesoura do principiante','Fio grosso','Tecido de cetim']},
                {CHAVE_PROFISSAO_ARMAS_CORPO_A_CORPO:['Lascas de quartzo','Minério de ferro','Mó do principiante']},
                {CHAVE_PROFISSAO_ARMA_DE_LONGO_ALCANCE:['Esfera do neófito','Varinha de aço','Cabeça do cajado de ônix']}]
    return listaDicionarioProfissaoRecursos

def retornaChaveTipoRecurso(recursoProducao: TrabalhoEstoque) -> str | None:
    '''
        Função para encontrar a chave correspondente ao recurso de produção
        Args:
            recursoProducao (TrabalhoEstoque): Objeto da classe TrabalhoEstoque que contêm os atributos do trabalho de produção de recursos.
        Returns:
            str: String que contêm a chave correspondente ao trabalho de produção de recursos.
    '''
    listaDicionarioProfissaoRecursos = retornaListaDicionarioProfissaoRecursos(recursoProducao.nivel)
    # chaveProfissao = limpaRuidoTexto(recursoProducao.profissao)
    chaveProfissao = recursoProducao.profissao
    for dicionarioProfissaoRecursos in listaDicionarioProfissaoRecursos:
        if chaveProfissao in dicionarioProfissaoRecursos:
            for x in range(len(dicionarioProfissaoRecursos[chaveProfissao])):
                if textoEhIgual(dicionarioProfissaoRecursos[chaveProfissao][x], recursoProducao.nome):
                    if x == 0 and recursoProducao.nivel == 1:
                        return CHAVE_RCP
                    if x == 0 and recursoProducao.nivel == 8:
                        return CHAVE_RAP
                    if x == 1 and recursoProducao.nivel == 1:
                        return CHAVE_RCS
                    if x == 1 and recursoProducao.nivel == 8:
                        return CHAVE_RAS
                    if x == 2 and recursoProducao.nivel == 1:
                        return CHAVE_RCT
                    if x == 2 and recursoProducao.nivel == 8:
                        return CHAVE_RAT
                    break
    return None

def retornaListaTrabalhosParaProduzirProduzindo(dicionarioPersonagemAtributos):
    listaTrabalhosParaProduzirProduzindo = []
    for trabalhoProducao in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS_PRODUCAO]:
        if trabalhoProducao.ehParaProduzir() or trabalhoProducao.ehProduzindo():
            listaTrabalhosParaProduzirProduzindo.append(trabalhoProducao)
    return listaTrabalhosParaProduzirProduzindo

def limpaTela():
    print("\n" * os.get_terminal_size().lines)

def retorna_codigo_erro_reconhecido(texto_erro_encontrado: str) -> int:
    '''
    Função que retorna o código do erro reconhecido a partir do texto de erro encontrado.
    Args:
        texto_erro_encontrado (str): Texto de erro encontrado.
    Returns:
        int: Código do erro reconhecido, ou zero(0) caso não seja reconhecido.
    '''
    if texto_erro_encontrado is None:
        return 0
    for posicao_tipo_erro in range(len(CHAVE_LISTA_ERROS)):
        texto_erro: str = limpaRuidoTexto(CHAVE_LISTA_ERROS[posicao_tipo_erro])
        if texto_erro in texto_erro_encontrado:
            return posicao_tipo_erro + 1
    return 0