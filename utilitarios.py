from unidecode import unidecode
from constantes import *
from modelos.trabalho import Trabalho
from modelos.trabalhoEstoque import TrabalhoEstoque
import numpy as np
import os
import re

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

def texto1PertenceTexto2(texto1: str, texto2: str) -> bool:
    '''
        Função para verificar caso texto1 está contido no texto2
        Args:
            texto1 (str): String que contêm o texto a ser verificado
            texto2 (str): String que contêm o texto a ser verificado
        Returns:
            bool: Verdadeiro caso o texto1 está contido no texto2
    '''
    return limpaRuidoTexto(texto= texto1) in limpaRuidoTexto(texto= texto2)

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

def ehErroFalhaAoIniciarConexao(erro: int) -> bool:
    return erro == CODIGO_FALHA_AO_INICIAR_CONEXAO

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