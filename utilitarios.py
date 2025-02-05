from unidecode import unidecode
from constantes import *
from modelos.trabalho import Trabalho
import numpy as np
import os
import re

def textoEhIgual(texto1, texto2):
    return limpaRuidoTexto(texto1) == limpaRuidoTexto(texto2)

def texto1PertenceTexto2(texto1, texto2):
    return limpaRuidoTexto(texto1) in limpaRuidoTexto(texto2)

def tamanhoIgualZero(lista):
    return len(lista) == 0

def variavelExiste(variavel):
    return variavel != None

def limpaRuidoTexto(texto: str) -> str:
    texto = '' if texto is None else texto
    padrao: str = '[^a-zA-Z0-9àáãâéêíîóõôúûç_]'
    expressao = re.compile(padrao)
    novaStringPalavras: str = expressao.sub('', texto)
    return unidecode(novaStringPalavras).lower()

def retiraDigitos(texto):
    listaDigitos = ['0','1','2','3','4','5','6','7','8','9']
    for digito in listaDigitos:
        texto = texto.replace(digito,'')
    return texto

def erroEncontrado(erro):
    return erro != 0

def nenhumErroEncontrado(erro):
    return not erroEncontrado(erro)

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

def ehErroOutraConexao(erro):
    return erro == CODIGO_ERRO_OUTRA_CONEXAO

def ehErroRestauraConexao(erro: int) -> bool:
    return erro == CODIGO_RESTAURA_CONEXAO

def ehErroConectando(erro: int) -> bool:
    return erro == CODIGO_CONECTANDO

def ehErroRecursosInsuficiente(erro):
    return erro == CODIGO_ERRO_RECURSOS_INSUFICIENTES

def ehErroEspacoProducaoInsuficiente(erro):
    return erro == CODIGO_ERRO_ESPACO_PRODUCAO_INSUFICIENTE

def ehErroEspacoBolsaInsuficiente(erro):
    return erro == CODIGO_ERRO_ESPACO_BOLSA_INSUFICIENTE

def ehErroLicencaNecessaria(erro):
    return erro == CODIGO_ERRO_PRECISA_LICENCA

def ehErroFalhaConexao(erro):
    return erro == CODIGO_ERRO_FALHA_CONECTAR

def ehErroConexaoInterrompida(erro):
    return erro == CODIGO_ERRO_CONEXAO_INTERROMPIDA

def ehErroServidorEmManutencao(erro):
    return erro == CODIGO_ERRO_MANUTENCAO_SERVIDOR

def ehErroReinoIndisponivel(erro):
    return erro == CODIGO_ERRO_REINO_INDISPONIVEL

def ehErroOutraConexao(erro):
    return erro == CODIGO_ERRO_OUTRA_CONEXAO

def ehErroExperienciaInsuficiente(erro):
    return erro == CODIGO_ERRO_EXPERIENCIA_INSUFICIENTE

def ehErroTempoDeProducaoExpirada(erro):
    return erro == CODIGO_ERRO_TEMPO_PRODUCAO_EXPIRADA

def ehErroEscolhaItemNecessaria(erro):
    return erro == CODIGO_ERRO_ESCOLHA_ITEM_NECESSARIA

def ehErroReceberRecompensaDiaria(erro):
    return erro == CODIGO_RECEBER_RECOMPENSA

def ehErroVersaoJogoDesatualizada(erro):
    return erro == CODIGO_ERRO_ATUALIZACAO_JOGO

def ehErroSairDoJogo(erro):
    return erro == CODIGO_SAIR_JOGO

def ehErroTrabalhoNaoConcluido(erro):
    return erro == CODIGO_ERRO_CONCLUIR_TRABALHO

def ehErroEspacoBolsaInsuficiente(erro):
    return erro == CODIGO_ERRO_ESPACO_BOLSA_INSUFICIENTE

def ehErroUsuarioOuSenhaInvalida(erro: int) -> bool:
    return erro == CODIGO_ERRO_USUARIO_SENHA_INVALIDA

def ehErroMoedasMilagrosasInsuficientes(erro):
    return erro == CODIGO_ERRO_MOEDAS_MILAGROSAS_INSUFICIENTES

def ehErroItemAVenda(erro: int) -> bool:
    return erro == CODIGO_ITEM_A_VENDA

def chaveEspacoBolsaForVerdadeira(dicionarioPersonagem):
    return dicionarioPersonagem[CHAVE_ESPACO_BOLSA]

def haMaisQueUmPersonagemAtivo(listaPersonagemAtivo):
    return not len(listaPersonagemAtivo) == 1

def trabalhoEhProducaoRecursos(trabalho: Trabalho) -> bool:
    if variavelExiste(trabalho):
        for recurso in CHAVE_LISTA_PRODUCAO_RECURSO:
            if textoEhIgual(recurso, trabalho.nomeProducao):
                print(f'Trabalho produção é recurso')
                return True
    print(f'Trabalho produção não é recurso')
    return False

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

def naoFizerQuatroVerificacoes(dicionarioTrabalho):
    return dicionarioTrabalho[CHAVE_POSICAO] < 4

def chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
    return dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] != None

def primeiraBusca(dicionarioTrabalho):
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

def retornaListaDicionarioProfissaoRecursos(nivelProduzTrabalhoComum):
    listaDicionarioProfissaoRecursos = []
    if nivelProduzTrabalhoComum == 1:
        listaDicionarioProfissaoRecursos=[
                {'braceletes':['Fibra de Bronze','Prata','Pin de Estudante']},
                {'capotes':['Furador do aprendiz','Tecido delicado','Substância instável']},
                {'amuletos':['Pinça do aprendiz','Jade bruta','Energia inicial']},
                {'aneis':['Molde do aprendiz','Pepita de cobre','Pedra de sombras']},
                {'armadurapesada':['Marretão do aprendiz','Placas de cobre','Anéis de bronze']},
                {'armaduraleve':['Faca do aprendiz','Escamas da serpente','Couro resistente']},
                {'armaduradetecido':['Tesoura do aprendiz','Fio grosseiro','Tecido de linho']},
                {'armacorpoacorpo':['Lascas','Minério de cobre','Mó do aprendiz']},
                {'armadelongoalcance':['Esfera do aprendiz','Varinha de madeira','Cabeça do cajado de jade']}]
    elif nivelProduzTrabalhoComum == 8:    
        listaDicionarioProfissaoRecursos=[
                {'braceletes':['Fibra de Platina','Âmbarito','Pino do Aprendiz']},
                {'capotes':['Furador do principiante','Tecido espesso','Substância estável']},
                {'amuletos':['Pinça do principiante','Ônix extraordinária','Éter inicial']},
                {'aneis':['Molde do principiante','Pepita de prata','Pedra da luz']},
                {'armadurapesada':['Marretão do principiante','Placas de ferro','Anéis de aço']},
                {'armaduraleve':['Faca do principiante','Escamas do lagarto','Couro grosso']},
                {'armaduradetecido':['Tesoura do principiante','Fio grosso','Tecido de cetim']},
                {'armacorpoacorpo':['Lascas de quartzo','Minério de ferro','Mó do principiante']},
                {'armadelongoalcance':['Esfera do neófito','Varinha de aço','Cabeça do cajado de ônix']}]
    return listaDicionarioProfissaoRecursos

def retornaChaveTipoRecurso(trabalhoEstoque):
    listaDicionarioProfissaoRecursos = retornaListaDicionarioProfissaoRecursos(trabalhoEstoque.nivel)
    chaveProfissao = limpaRuidoTexto(trabalhoEstoque.profissao)
    for dicionarioProfissaoRecursos in listaDicionarioProfissaoRecursos:
        if chaveProfissao in dicionarioProfissaoRecursos:
            for x in range(len(dicionarioProfissaoRecursos[chaveProfissao])):
                if textoEhIgual(dicionarioProfissaoRecursos[chaveProfissao][x], trabalhoEstoque.nome):
                    if x == 0 and trabalhoEstoque.nivel == 1:
                        return CHAVE_RCP
                    elif x == 0 and trabalhoEstoque.nivel == 8:
                        return CHAVE_RAP
                    elif x == 1 and trabalhoEstoque.nivel == 1:
                        return CHAVE_RCS
                    elif x == 1 and trabalhoEstoque.nivel == 8:
                        return CHAVE_RAS
                    elif x == 2 and trabalhoEstoque.nivel == 1:
                        return CHAVE_RCT
                    elif x == 2 and trabalhoEstoque.nivel == 8:
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