from teclado import clickAtalhoEspecifico
from constantes import *
from utilitarios import *
from imagem import *
from repositorio import pegaTodosPersonagens

dicionarioPersonagemAtributos = {}


def confirmaNomePersonagem(personagemReconhecido):
    global dicionarioPersonagemAtributos
    dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO] = None
    for dicionarioPersonagemAtivo in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO]:
        if textoEhIgual(personagemReconhecido, dicionarioPersonagemAtivo.pegaNome()):
            print(f'Personagem {personagemReconhecido} confirmado!')
            dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO] = dicionarioPersonagemAtivo
            break

def retornaNomePersonagem(posicao):
    print(f'Verificando nome personagem...')
    posicaoNome = [[2,33,169,27], [190,351,177,30]]
    telaInteira = retornaAtualizacaoTela()
    frameNomePersonagem = telaInteira[posicaoNome[posicao][1]:posicaoNome[posicao][1]+posicaoNome[posicao][3], posicaoNome[posicao][0]:posicaoNome[posicao][0]+posicaoNome[posicao][2]]
    frameNomePersonagemTratado = retornaImagemCinza(frameNomePersonagem)
    frameNomePersonagemTratado = retornaImagemEqualizada(frameNomePersonagemTratado)
    frameNomePersonagemTratado = retornaImagemBinarizadaOtsu(frameNomePersonagemTratado)
    contadorPixelPreto = np.sum(frameNomePersonagemTratado == 0)
    if contadorPixelPreto > 50:
        nomePersonagemReconhecido = reconheceTexto(frameNomePersonagemTratado)
        if variavelExiste(nomePersonagemReconhecido):
            nome = limpaRuidoTexto(nomePersonagemReconhecido)
            print(f'Personagem reconhecido: {nome}.')
            return nome
        elif contadorPixelPreto > 50:
            return 'provisorioatecair'
    return None

def defineChaveDicionarioPersonagemEmUso():
    nomePersonagemReconhecidoTratado = retornaNomePersonagem(0)
    if variavelExiste(nomePersonagemReconhecidoTratado):
        confirmaNomePersonagem(nomePersonagemReconhecidoTratado)
    elif nomePersonagemReconhecidoTratado == 'provisorioatecair':
        print(f'Nome personagem diferente!')

def defineChaveListaDicionarioPersonagemAtivo():
    global dicionarioPersonagemAtributos
    print(f'Definindo lista de personagem ativo.')
    dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO] = []
    for personagem in dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM]:
        chaveEstadoEhAtivo = (personagem.pegaEstado() or personagem.pegaEstado == 1)
        if chaveEstadoEhAtivo:
            dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO].append(personagem)

def iniciaProcessoBusca():
    global dicionarioPersonagemAtributos
    dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM] = pegaTodosPersonagens()
    dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO] = []
    defineChaveListaDicionarioPersonagemAtivo()
    while True:
        if tamanhoIgualZero(dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO]):
            dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM] = pegaTodosPersonagens()
            dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO] = []
            defineChaveListaDicionarioPersonagemAtivo()
        else:
            defineChaveDicionarioPersonagemEmUso()
            if variavelExiste(dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO]):
                modificaAtributoUso(True)
    #             print(f'{D}: Personagem ({dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_NOME]}) ESTÁ EM USO.')
    #             inicializaChavesPersonagem()
    #             print('Inicia busca...')
    #             linhaSeparacao()
    #             if vaiParaMenuProduzir():
    #                 while defineTrabalhoComumProfissaoPriorizada():
    #                     continue
    #                 listaDicionariosTrabalhosParaProduzirProduzindo = retornaListaDicionariosTrabalhosParaProduzirProduzindo()
    #                 if not tamanhoIgualZero(listaDicionariosTrabalhosParaProduzirProduzindo):#verifica se a lista está vazia
    #                     dicionarioTrabalho = {
    #                         CHAVE_LISTA_DESEJO: listaDicionariosTrabalhosParaProduzirProduzindo,
    #                         CHAVE_DICIONARIO_TRABALHO_DESEJADO: None}
    #                     verificaProdutosRarosMaisVendidos(None)
    #                     iniciaBuscaTrabalho(dicionarioTrabalho)
    #                 else:
    #                     print(f'Lista de trabalhos desejados vazia.')
    #                     linhaSeparacao()
    #                     listaPersonagem = [dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO][CHAVE_ID]]
    #                     dicionarioPersonagemAtributos = modificaAtributoPersonagem(dicionarioPersonagemAtributos,listaPersonagem,CHAVE_ESTADO,False)
    #             if dicionarioPersonagemAtributos[CHAVE_UNICA_CONEXAO]:
    #                 if haMaisQueUmPersonagemAtivo():
    #                     clickMouseEsquerdo(1, 2, 35)
    #                 dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO].append(dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO])
    #                 retiraDicionarioPersonagemListaAtivo()
    #             else:
    #                 dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO].append(dicionarioPersonagemAtributos[CHAVE_DICIONARIO_PERSONAGEM_EM_USO])
    #                 retiraDicionarioPersonagemListaAtivo()
    #         else:#se o nome reconhecido não estiver na lista de ativos
    #             if tamanhoIgualZero(dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO]):
    #                 if configuraLoginPersonagem():
    #                     entraPersonagemAtivo()
    #             else:
    #                 if textoEhIgual(dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_RETIRADO][-1][CHAVE_EMAIL],dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIO_PERSONAGEM_ATIVO][0][CHAVE_EMAIL]):
    #                     entraPersonagemAtivo()
    #                 elif configuraLoginPersonagem():
    #                     entraPersonagemAtivo()
    
def preparaPersonagem():
    # clickAtalhoEspecifico('alt', 'tab')
    # clickAtalhoEspecifico('win', 'left')
    iniciaProcessoBusca()

if __name__=='__main__':
    preparaPersonagem()