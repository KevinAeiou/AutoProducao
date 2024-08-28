from teclado import *
from constantes import *
from utilitarios import *
from imagem import *
from time import sleep
import re
import datetime
import uuid

from repositorio.repositorioPersonagem import *
from repositorio.repositorioEstoque import *
from repositorio.repositorioProfissao import *
from repositorio.repositorioTrabalho import *
from repositorio.repositorioVendas import *
from repositorio.repositorioTrabalhoProducao import *
# from repositorio. import *
from tests.testRepositorioEstoque import *
from tests.testRepositorioPersonagem import *
from tests.testRepositorioProfissao import *
from tests.testRepositorioTrabalho import *
from tests.testRepositorioTrabalhoProducao import *
from tests.testRepositorioVendas import *
# from tests. import *

dicionarioPersonagemAtributos = {}
repositorioPersonagem = RepositorioPersonagem()
repositorioTrabalho = RepositorioTrabalho()
repositorioVendas = None
repositorioProfissao = None
repositorioEstoque = None
repositorioTrabalhoProducao = None

def defineListaDicionarioPersonagemMesmoEmail(personagemEmUso):
    listaDicionarioPersonagemMesmoEmail = []
    if variavelExiste(personagemEmUso):
        for personagem in dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM]:
            if textoEhIgual(personagem.pegaEmail(), personagemEmUso.pegaEmail()):
                listaDicionarioPersonagemMesmoEmail.append(personagem)
    return listaDicionarioPersonagemMesmoEmail

def modificaAtributoUso(valor):
    personagemEmUso = None
    if valor:
        personagemEmUso = dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO]
    else:
        if not tamanhoIgualZero(dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM_RETIRADO]):
            personagemEmUso = dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM_RETIRADO][-1]
    listaPersonagemMesmoEmail = defineListaDicionarioPersonagemMesmoEmail(personagemEmUso)
    if not tamanhoIgualZero(listaPersonagemMesmoEmail):
        for personagem in dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM]:
            for personagemEmUso in listaPersonagemMesmoEmail:
                if textoEhIgual(personagem.pegaId(), personagemEmUso.pegaId()):
                    if not personagem.pegaUso():
                        repositorioPersonagem.alternaUso(personagem)
                        personagem.alternaUso()
                elif personagem.pegaUso():
                    repositorioPersonagem.alternaUso(personagem)
                    personagem.alternaUso()

def confirmaNomePersonagem(personagemReconhecido):
    global dicionarioPersonagemAtributos
    dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO] = None
    for personagemAtivo in dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM_ATIVO]:
        if textoEhIgual(personagemReconhecido, personagemAtivo.pegaNome()):
            print(f'Personagem {personagemReconhecido} confirmado!')
            dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO] = personagemAtivo
            break
    else:
        print(f'Personagem {personagemReconhecido} não está ativo!')
    

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

def defineChaveListaPersonagensAtivos():
    global dicionarioPersonagemAtributos
    print(f'Definindo lista de personagem ativo.')
    dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM_ATIVO] = []
    for personagem in dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM]:
        if personagem.ehAtivo():
            dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM_ATIVO].append(personagem)

def inicializaChavesPersonagem():
    global dicionarioPersonagemAtributos, repositorioVendas, repositorioProfissao, repositorioEstoque, repositorioTrabalhoProducao
    dicionarioPersonagemAtributos[CHAVE_VERIFICA_TRABALHO] = False
    dicionarioPersonagemAtributos[CHAVE_UNICA_CONEXAO] = True
    dicionarioPersonagemAtributos[CHAVE_ESPACO_BOLSA] = True
    dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO] = True
    dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_MODIFICADA] = False
    repositorioVendas = RepositorioVendas(dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO])
    repositorioProfissao = RepositorioProfissao(dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO])
    repositorioEstoque = RepositorioEstoque(dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO])
    repositorioTrabalhoProducao = RepositorioTrabalhoProducao(dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO])
    dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO] = repositorioProfissao.pegaTodasProfissoes()
    dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS] = repositorioTrabalho.pegaTodosTrabalhos()
    dicionarioPersonagemAtributos[CHAVE_LISTA_VENDAS] = repositorioVendas.pegaTodasVendas()
    dicionarioPersonagemAtributos[CHAVE_LISTA_ESTOQUE] = repositorioEstoque.pegaTodosTrabalhosEstoque()
    dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS_PRODUCAO] = repositorioTrabalhoProducao.pegaTodosTrabalhosProducao()

def retornaTipoErro():
    erro = 0
    telaInteira = retornaAtualizacaoTela()
    frameErro = telaInteira[335:335+100,150:526]
    textoErroEncontrado = reconheceTexto(frameErro)
    print(f'{textoErroEncontrado}')
    if variavelExiste(textoErroEncontrado):
        textoErroEncontrado = limpaRuidoTexto(textoErroEncontrado)
        textoErroEncontrado = retiraDigitos(textoErroEncontrado)
        tipoErro = ['Você precisa de uma licença defabricação para iniciar este pedido',
            'Falha ao se conectar ao servidor',
            'Você precisa de mais recursos parainiciar este pedido',
            'Selecione um item para produzir',
            'Conectando',
            'Você precisa de mais experiência de produção para iniciar este pedido',
            'Você recebeu um novo presenteDessgja ir à Loja Milagrosa paraconferir',
            'Todos os espaços de fabricaçãoestão ocupados',
            'agorapormoedas',
            'Estamos fazendo de tudo paraconcluíla o mais rápido possível',
            'No momento esta conta está sendousada em outro dispositivo',
            'Gostanadecomprar',
            'Conexão perdida com o servidor',
            'Vocêprecisademaismoedas',
            'Nome de usuário ou senha inválida',
            'Pedido de produção expirado',
            'reinodejogoselecionado',
            'jogoestadesatualizada',
            'restaurandoconexão',
            'paraatarefadeprodução',
            'Bolsa chela Deseja liberar',
            'Desgeja sair do Warspear Online']
        for posicaoTipoErro in range(len(tipoErro)):
            textoErro = limpaRuidoTexto(tipoErro[posicaoTipoErro])
            if textoErro in textoErroEncontrado:
                print(f'"{textoErro}" encontrado em "{textoErroEncontrado}".')
                erro = posicaoTipoErro+1
    return erro

def retornaLicencaReconhecida():
    licencaRetornada = None
    listaLicencas = ['iniciante','principiante','aprendiz','mestre','nenhumitem','licençasdeproduçao']
    telaInteira = retornaAtualizacaoTela()
    frameTela = telaInteira[275:317,169:512]
    frameTelaCinza = retornaImagemCinza(frameTela)
    frameTelaEqualizado = retornaImagemEqualizada(frameTelaCinza)
    textoReconhecido = reconheceTexto(frameTelaEqualizado)
    if variavelExiste(textoReconhecido):
        for licenca in listaLicencas:
            if texto1PertenceTexto2(licenca, textoReconhecido):
                return textoReconhecido
    return licencaRetornada

def verificaLicenca(dicionarioTrabalho, dicionarioPersonagem):
    confirmacao = False
    if variavelExiste(dicionarioTrabalho):
        print(f"Buscando: {dicionarioTrabalho[CHAVE_TIPO_LICENCA]}")
        textoReconhecido = retornaLicencaReconhecida()
        if variavelExiste(textoReconhecido) and variavelExiste(dicionarioTrabalho[CHAVE_TIPO_LICENCA]):
            print(f'Licença reconhecida: {textoReconhecido}.')
            if not texto1PertenceTexto2('licençasdeproduçao', textoReconhecido):
                primeiraBusca = True
                listaCiclo = []
                while not texto1PertenceTexto2(textoReconhecido, dicionarioTrabalho[CHAVE_TIPO_LICENCA]):
                    clickEspecifico(1, "right")
                    listaCiclo.append(textoReconhecido)
                    textoReconhecido = retornaLicencaReconhecida()
                    if variavelExiste(textoReconhecido):
                        print(f'Licença reconhecida: {textoReconhecido}.')
                        if texto1PertenceTexto2('nenhumitem', textoReconhecido) or len(listaCiclo) > 10:
                            if textoEhIgual(dicionarioTrabalho[CHAVE_TIPO_LICENCA], 'Licença de produção do iniciante')and primeiraBusca:
                                break
                            dicionarioTrabalho[CHAVE_TIPO_LICENCA] = 'Licença de produção do iniciante'
                            print(f'Licença para trabalho agora é: {dicionarioTrabalho[CHAVE_TIPO_LICENCA]}.')
                            listaCiclo = []
                    else:
                        print(f'Erro ao reconhecer licença!')
                        break
                    primeiraBusca = False
                else:
                    if primeiraBusca:
                        clickEspecifico(1, "f1")
                    else:
                        clickEspecifico(1, "f2")
                    confirmacao = True
            else:
                print(f'Sem licenças de produção...')
                clickEspecifico(1, 'f1')
                repositorioPersonagem.alternaEstado(dicionarioPersonagem[CHAVE_PERSONAGEM_EM_USO])
        else:
            print(f'Erro ao reconhecer licença!')
    return confirmacao, dicionarioTrabalho

def verificaErro():
    sleep(0.5)
    print(f'Verificando erro...')
    CODIGO_ERRO = retornaTipoErro()
    if CODIGO_ERRO == CODIGO_ERRO_PRECISA_LICENCA or CODIGO_ERRO == CODIGO_ERRO_FALHA_CONECTAR or CODIGO_ERRO == CODIGO_ERRO_CONEXAO_INTERROMPIDA or CODIGO_ERRO == CODIGO_ERRO_MANUTENCAO_SERVIDOR or CODIGO_ERRO == CODIGO_ERRO_REINO_INDISPONIVEL:
        clickEspecifico(2, "enter")
        if CODIGO_ERRO == CODIGO_ERRO_PRECISA_LICENCA:
            verificaLicenca(None, None)
        elif CODIGO_ERRO == CODIGO_ERRO_FALHA_CONECTAR:
            print(f'Erro na conexão...')
        elif CODIGO_ERRO == CODIGO_ERRO_CONEXAO_INTERROMPIDA:
            print(f'Erro ao conectar...')
        elif CODIGO_ERRO == CODIGO_ERRO_MANUTENCAO_SERVIDOR:
            print(f'Servidor em manutenção!')
        elif CODIGO_ERRO == CODIGO_ERRO_REINO_INDISPONIVEL:
            print(f'Reino de jogo indisponível!')
    elif CODIGO_ERRO == CODIGO_ERRO_OUTRA_CONEXAO:
        clickEspecifico(1,'enter')
        print(f'Voltando para a tela inicial.')
    elif CODIGO_ERRO == CODIGO_ERRO_RECURSOS_INSUFICIENTES or CODIGO_ERRO == CODIGO_ERRO_TEMPO_PRODUCAO_EXPIRADA or CODIGO_ERRO == CODIGO_ERRO_EXPERIENCIA_INSUFICIENTE or CODIGO_ERRO == CODIGO_ERRO_ESPACO_PRODUCAO_INSUFICIENTE:
        clickEspecifico(1,'enter')
        clickEspecifico(2,'f1')
        clickContinuo(9,'up')
        clickEspecifico(1,'left')
        if CODIGO_ERRO == CODIGO_ERRO_RECURSOS_INSUFICIENTES:
            print(f'Retirrando trabalho da lista.')
        elif CODIGO_ERRO == CODIGO_ERRO_EXPERIENCIA_INSUFICIENTE:
            print(f'Voltando para o menu profissões.')
        elif CODIGO_ERRO == CODIGO_ERRO_ESPACO_PRODUCAO_INSUFICIENTE:
            print(f'Sem espaços livres para produção....')
        elif CODIGO_ERRO == CODIGO_ERRO_TEMPO_PRODUCAO_EXPIRADA:
            print(f'O trabalho não está disponível.')
    elif CODIGO_ERRO == CODIGO_ERRO_ESCOLHA_ITEM_NECESSARIA:
        print(f'Escolhendo item')
        clickEspecifico(1, 'enter')
        clickEspecifico(1, 'f2')
        clickContinuo(9, 'up')
    elif CODIGO_ERRO == CODIGO_CONECTANDO or CODIGO_ERRO == CODIGO_RESTAURA_CONEXAO:
        if CODIGO_ERRO == CODIGO_CONECTANDO:
            print(f'Conectando...')
        elif CODIGO_ERRO == CODIGO_RESTAURA_CONEXAO:
            print(f'Restaurando conexão...')
        sleep(1)
    elif CODIGO_ERRO == CODIGO_RECEBER_RECOMPENSA or CODIGO_ERRO == CODIGO_ERRO_ATUALIZACAO_JOGO or CODIGO_ERRO == CODIGO_ERRO_USA_OBJETO_PARA_PRODUZIR or CODIGO_ERRO == CODIGO_SAIR_JOGO:
        clickEspecifico(1,'f2')
        if CODIGO_ERRO == CODIGO_RECEBER_RECOMPENSA:
            print(f'Recuperar presente.')
        elif CODIGO_ERRO == CODIGO_ERRO_USA_OBJETO_PARA_PRODUZIR:
            print(f'Usa objeto para produzir outro.')
        elif CODIGO_ERRO == CODIGO_SAIR_JOGO:
            print(f'Sair do jogo.')
        elif CODIGO_ERRO == CODIGO_ERRO_ATUALIZACAO_JOGO:
            print(f'Atualizando jogo...')
            clickEspecifico(1,'f1')
            exit()
    elif CODIGO_ERRO == CODIGO_ERRO_CONCLUIR_TRABALHO:
        print(f'Trabalho não está concluido!')
        clickEspecifico(1,'f1')
        clickContinuo(8,'up')
    elif CODIGO_ERRO == CODIGO_ERRO_ESPACO_BOLSA_INSUFICIENTE:
        clickEspecifico(1,'f1')
        clickContinuo(8,'up')
        print(f'Ignorando trabalho concluído!')
    elif CODIGO_ERRO == CODIGO_ERRO_MOEDAS_INSUFICIENTES:
        clickEspecifico(1,'f1')
    elif CODIGO_ERRO == CODIGO_ERRO_EMAIL_SENHA_INCORRETA:
        clickEspecifico(1,'enter')
        clickEspecifico(1,'f1')
        print(f'Login ou senha incorreta...')
    else:
        print(f'Nem um erro encontrado!')
    return CODIGO_ERRO
                    
def retornaTextoMenuReconhecido(x, y, largura):
    telaInteira = retornaAtualizacaoTela()
    alturaFrame = 30
    texto = None
    frameTela = telaInteira[y:y+alturaFrame,x:x+largura]
    if y > 30:
        frameTela = retornaImagemCinza(frameTela)
        frameTela = retornaImagemEqualizada(frameTela)
        frameTela = retornaImagemBinarizada(frameTela)
    contadorPixelPreto = np.sum(frameTela==0)
    if existePixelPretoSuficiente(contadorPixelPreto):
        texto = reconheceTexto(frameTela)
        if variavelExiste(texto):
            texto = limpaRuidoTexto(texto)
    return texto

def retornaTextoSair():
    texto = None
    telaInteira = retornaAtualizacaoTela()
    frameTela = telaInteira[telaInteira.shape[0]-50:telaInteira.shape[0]-15,50:50+60]
    frameTelaTratado = retornaImagemCinza(frameTela)
    frameTelaTratado = retornaImagemBinarizada(frameTelaTratado)
    contadorPixelPreto = np.sum(frameTelaTratado==0)
    if contadorPixelPreto > 100 and contadorPixelPreto < 400:
        texto = reconheceTexto(frameTelaTratado)
        if variavelExiste(texto):
            texto = limpaRuidoTexto(texto)
    return texto

def verificaMenuReferencia():
    confirmacao = False
    posicaoMenu = [[703,627],[712,1312]]
    telaInteira = retornaAtualizacaoTela()
    for posicao in posicaoMenu:
        frameTela = telaInteira[posicao[0]:posicao[0] + 53, posicao[1]:posicao[1] + 53]
        contadorPixelPreto = np.sum(frameTela == (85,204,255))
        if contadorPixelPreto == 1720:
            confirmacao = True
            break
    return confirmacao

def retornaMenu():
    print(f'Reconhecendo menu.')
    textoMenu = retornaTextoMenuReconhecido(26,1,150)
    if variavelExiste(textoMenu):
        if texto1PertenceTexto2('spearonline',textoMenu):
            textoMenu=retornaTextoMenuReconhecido(216,197,270)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('Notícias',textoMenu):
                    print(f'Menu notícias...')
                    return MENU_NOTICIAS
                elif texto1PertenceTexto2('Personagens',textoMenu):
                    print(f'Menu escolha de personagem...')
                    return MENU_ESCOLHA_PERSONAGEM
                elif texto1PertenceTexto2('Produção',textoMenu):
                    textoMenu=retornaTextoMenuReconhecido(266,242,150)
                    if variavelExiste(textoMenu):
                        if texto1PertenceTexto2('Artesanatos',textoMenu):
                            textoMenu=retornaTextoMenuReconhecido(191,612,100)
                            if variavelExiste(textoMenu):
                                if texto1PertenceTexto2('fechar',textoMenu):
                                    print(f'Menu produzir...')
                                    return MENU_PRODUZIR
                                elif texto1PertenceTexto2('voltar',textoMenu):
                                    print(f'Menu trabalhos diponíveis...')
                                    return MENU_TRABALHOS_DISPONIVEIS
                        elif texto1PertenceTexto2('Pedidos ativos',textoMenu):
                            print(f'Menu trabalhos atuais...')
                            return MENU_TRABALHOS_ATUAIS
            textoMenu = retornaTextoSair()
            if variavelExiste(textoMenu):
                if textoEhIgual(textoMenu,'sair'):
                    print(f'Menu jogar...')
                    return MENU_JOGAR
            if verificaMenuReferencia():
                print(f'Menu tela inicial...')
                return MENU_INICIAL
            textoMenu=retornaTextoMenuReconhecido(291,412,100)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('conquistas',textoMenu):
                    print(f'Menu personagem...')
                    return MENU_PERSONAGEM
                elif texto1PertenceTexto2('interagir',textoMenu):
                    print(f'Menu principal...')
                    return MENU_PRINCIPAL
            textoMenu=retornaTextoMenuReconhecido(191,319,270)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('parâmetros',textoMenu):
                    if texto1PertenceTexto2('requisitos',textoMenu):
                        print(f'Menu atributo do trabalho...')
                        return MENU_TRABALHOS_ATRIBUTOS
                    else:
                        print(f'Menu licenças...')
                        return MENU_LICENSAS
            textoMenu=retornaTextoMenuReconhecido(275,400,150)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('Recompensa',textoMenu):
                    print(f'Menu trabalho específico...')
                    return MENU_TRABALHO_ESPECIFICO
            textoMenu=retornaTextoMenuReconhecido(266,269,150)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('ofertadiária',textoMenu):
                    print(f'Menu oferta diária...')
                    return MENU_OFERTA_DIARIA
            textoMenu=retornaTextoMenuReconhecido(181,71,150)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('Loja Milagrosa',textoMenu):
                    print(f'Menu loja milagrosa...')
                    return MENU_LOJA_MILAGROSA
            textoMenu=retornaTextoMenuReconhecido(180,40,300)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('Recompensas diárias',textoMenu):
                    print(f'Menu recompensas diárias...')
                    return MENU_RECOMPENSAS_DIARIAS
            textoMenu=retornaTextoMenuReconhecido(180,60,300)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('Recompensas diárias',textoMenu):
                    print(f'Menu recompensas diárias...')
                    return MENU_RECOMPENSAS_DIARIAS
            textoMenu=retornaTextoMenuReconhecido(310,338,57)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('meu',textoMenu):
                    print(f'Menu meu perfil...')
                    return MENU_MEU_PERFIL           
            textoMenu=retornaTextoMenuReconhecido(169,97,75)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('Bolsa',textoMenu):
                    print(f'Menu bolsa...')
                    return MENU_BOLSA
            clickMouseEsquerdo(1,35,35)
        else:
            clickAtalhoEspecifico('win','left')
            clickAtalhoEspecifico('win','left')
    else:
        print(f'Menu não reconhecido...')
    verificaErro(None)
    return MENU_DESCONHECIDO

def existePixelCorrespondencia():
    confirmacao = False
    tela = retornaAtualizacaoTela()
    frameTela = tela[665:690, 644:675]
    contadorPixelCorrespondencia = np.sum(frameTela==(173,239,247))
    if contadorPixelCorrespondencia > 50:
        print(f'Há correspondencia!')
        confirmacao = True
    else:
        print(f'Não há correspondencia!')
    return confirmacao

def verificaCaixaCorreio():
    print(f'Verificando se possui correspondencia...')
    return np.sum(retornaAtualizacaoTela()[233:233+30, 235:235+200] == 255) > 0

def verificaVendaProduto(texto):
    return texto1PertenceTexto2('Lote vendido', texto)

def retornaQuantidadeProdutoVendido(listaTextoCarta):
    x = 0
    quantidadeProduto = 0
    for texto in listaTextoCarta:
        if texto1PertenceTexto2('x', texto):
            quantidadeProduto = re.sub('[^0-9]', '', listaTextoCarta[x])
            if not quantidadeProduto.isdigit():
                quantidadeProduto = re.sub('[^0-9]', '', listaTextoCarta[x-1])
                if not quantidadeProduto.isdigit():
                    print(f'Não foi possível reconhecer a quantidade do produto.')
            print(f'quantidadeProduto:{quantidadeProduto}')
        x += 1
    return int(quantidadeProduto)

def retornaConteudoCorrespondencia():
    telaInteira = retornaAtualizacaoTela()
    frameTela = telaInteira[231:231+50, 168:168+343]
    textoCarta = reconheceTexto(frameTela)
    novaVenda = None
    if variavelExiste(textoCarta):
        produto = verificaVendaProduto(textoCarta)
        if variavelExiste(produto):
            if produto:
                print(f'Produto vendido:')
                listaTextoCarta = textoCarta.split()
                quantidadeProduto = retornaQuantidadeProdutoVendido(listaTextoCarta)
                frameTela = telaInteira[490:490+30,410:410+100]
                frameTelaTratado = retornaImagemCinza(frameTela)
                frameTelaTratado = retornaImagemBinarizada(frameTelaTratado)
                ouro = reconheceDigito(frameTelaTratado)
                ouro = re.sub('[^0-9]','',ouro)
                if ouro.isdigit():
                    ouro = int(ouro)
                else:
                    ouro = 0
                dataAtual = str(datetime.date.today())
                listaTextoCarta = ' '.join(listaTextoCarta)
                chaveIdTrabalho = ''
                for dicionarioTrabalho in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS]:
                    if texto1PertenceTexto2(dicionarioTrabalho[CHAVE_NOME], listaTextoCarta):
                        chaveIdTrabalho = dicionarioTrabalho[CHAVE_ID]
                        break
                id = uuid.uuid4()
                novaVenda = TrabalhoVendido(
                    id,
                    listaTextoCarta,
                    dataAtual,
                    dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO][CHAVE_ID],
                    quantidadeProduto,
                    chaveIdTrabalho,
                    int(ouro))
                repositorioVendas.adicionaNovaVenda(novaVenda)
        else:
            print(f'Erro...')
    return novaVenda

def atualizaQuantidadeTrabalhoEstoque(venda):
    for trabalhoEstoque in dicionarioPersonagemAtributos[CHAVE_LISTA_ESTOQUE]:
        if textoEhIgual(trabalhoEstoque.pegaTrabalhoId(), venda.pegaTrabalhoId()):
            quantidadeVendida = venda.pegaQuantidade()
            if quantidadeVendida == 0:
                quantidadeVendida = 1
            novaQuantidade = trabalhoEstoque.pegaQuantidade() - quantidadeVendida
            if novaQuantidade < 0:
                novaQuantidade = 0
            trabalhoEstoque.setQuantidade(novaQuantidade)
            repositorioEstoque.modificaTrabalhoEstoque(trabalhoEstoque)
            print(f'Quantidade do trabalho ({trabalhoEstoque[CHAVE_NOME]}) atualizada para {novaQuantidade}.')
            break
    else:
        nomeProduto = venda["nomeProduto"]
        print(f'Trabalho ({nomeProduto}) não encontrado no estoque.')

def recuperaCorrespondencia():
    verificaTrabalhoRaroVendido = False
    while verificaCaixaCorreio():
        clickEspecifico(1, 'enter')
        venda = retornaConteudoCorrespondencia()
        if not tamanhoIgualZero(venda):
            verificaTrabalhoRaroVendido = True
            atualizaQuantidadeTrabalhoEstoque(venda)
        clickEspecifico(1,'f2')
    else:
        print(f'Caixa de correio vazia!')
        clickMouseEsquerdo(1, 2, 35)
    return verificaTrabalhoRaroVendido

def retornaEstadoTrabalho():
    estadoTrabalho = CODIGO_PARA_PRODUZIR
    telaInteira = retornaAtualizacaoTela()
    frameTelaInteira = telaInteira[311:311+43, 233:486]
    texto = reconheceTexto(frameTelaInteira)
    if variavelExiste(texto):
        if textoEhIgual("pedidoconcluído", texto):
            print(f'Pedido concluído!')
            estadoTrabalho = CODIGO_CONCLUIDO
        elif texto1PertenceTexto2('adicionarnovo', texto):
            print(f'Nem um trabalho!')
            estadoTrabalho = CODIGO_PARA_PRODUZIR
        else:
            print(f'Em produção...')
            estadoTrabalho = CODIGO_PRODUZINDO
    else:
        print(f'Ocorreu algum erro ao verificar o espaço de produção!')
    return estadoTrabalho

def reconheceRecuperaTrabalhoConcluido():
    global dicionarioPersonagemAtributos
    telaInteira = retornaAtualizacaoTela()
    frameNomeTrabalho = telaInteira[285:285+37, 233:486]
    frameNomeTrabalhoBinarizado = retornaImagemBinarizada(frameNomeTrabalho)
    erro = verificaErro(None)
    if not erroEncontrado(erro):
        nomeTrabalhoConcluido = reconheceTexto(frameNomeTrabalhoBinarizado)
        clickEspecifico(1, 'down')
        clickEspecifico(1, 'f2')
        print(f'  Trabalho concluido reconhecido: {nomeTrabalhoConcluido}.')
        if variavelExiste(nomeTrabalhoConcluido):
            erro = verificaErro(None)
            if not erroEncontrado(erro):
                if not dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_MODIFICADA]:
                    dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_MODIFICADA] = True
                clickContinuo(3, 'up')
                return nomeTrabalhoConcluido
            else:
                dicionarioPersonagemAtributos[CHAVE_ESPACO_BOLSA] = False
                clickContinuo(1, 'up')
                clickEspecifico(1, 'left')
    return None

def retornaListaPossiveisTrabalhoRecuperado(nomeTrabalhoConcluido):
    listaPossiveisDicionariosTrabalhos = []
    if not tamanhoIgualZero(dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS]):
        for trabalho in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS]:
            if texto1PertenceTexto2(nomeTrabalhoConcluido[1:-1], trabalho.pegaNomeProducao()):
                listaPossiveisDicionariosTrabalhos.append(trabalho)
    else:
        print(f'Erro ao definir lista de trabalhos.')
    return listaPossiveisDicionariosTrabalhos

def retornaListaTrabalhosParaProduzirProduzindo():
    listaTrabalhosParaProduzirProduzindo = []
    for trabalhoDesejado in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS_PRODUCAO]:
        if trabalhoEhParaProduzir(trabalhoDesejado) or trabalhoEhProduzindo(trabalhoDesejado):
            listaTrabalhosParaProduzirProduzindo.append(trabalhoDesejado)
    return listaTrabalhosParaProduzirProduzindo

def retornaTrabalhoConcluido(nomeTrabalhoConcluido):
    listaPossiveisTrabalhos = retornaListaPossiveisTrabalhoRecuperado(nomeTrabalhoConcluido)
    if not tamanhoIgualZero(listaPossiveisTrabalhos):
        listaDicionariosTrabalhosProduzirProduzindo = retornaListaTrabalhosParaProduzirProduzindo()
        for possivelTrabalho in listaPossiveisTrabalhos:
            for trabalhoProduzirProduzindo in listaDicionariosTrabalhosProduzirProduzindo:
                condicoes = (trabalhoEhProduzindo(trabalhoProduzirProduzindo) and textoEhIgual(trabalhoProduzirProduzindo.pegaNome(), possivelTrabalho.pegaNome()))
                if condicoes:
                    trabalhoProduzirProduzindo.setTrabalhoId(possivelTrabalho.pegaId())
                    trabalhoProduzirProduzindo.setNomeProducao(possivelTrabalho.pegaNomeProducao())
                    return trabalhoProduzirProduzindo
        else:
            print(f'Trabalho concluído ({listaPossiveisTrabalhos[0].pegaNome()}) não encontrado na lista produzindo...')
            return TrabalhoProducao('', listaPossiveisTrabalhos[0].pegaNome(), listaPossiveisTrabalhos[0].pegaNomeProducao(), CODIGO_CONCLUIDO, listaPossiveisTrabalhos[0].pegaExperiencia(), listaPossiveisTrabalhos[0].pegaNivel(), listaPossiveisTrabalhos[0].pegaProfissao(), listaPossiveisTrabalhos[0].pegaRaridade(), False, CHAVE_LICENCA_INICIANTE, listaPossiveisTrabalhos[0].pegaId())
    return None

def modificaTrabalhoConcluidoListaProduzirProduzindo(trabalhoProducaoConcluido):
    global dicionarioPersonagemAtributos
    if trabalhoEhProducaoRecursos(trabalhoProducaoConcluido):
        trabalhoProducaoConcluido.setRecorrencia(True)
    if trabalhoProducaoConcluido.pegaRecorrencia():
        print(f'Trabalho recorrente.')
        repositorioTrabalhoProducao.removeTrabalhoProducao(trabalhoProducaoConcluido)
        for posicao in range(len(dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS_PRODUCAO])):
            if textoEhIgual(dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS_PRODUCAO][posicao].pegaId(), trabalhoProducaoConcluido.pegaId()):
                del dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS_PRODUCAO][posicao]
                break
    else:
        print(f'Trabalho sem recorrencia.')
        repositorioTrabalhoProducao.modificaTrabalhoProducao(trabalhoProducaoConcluido)
        print(f'Trabalho ({trabalhoProducaoConcluido.pegaNome()}) modificado para concluído.')
        for dicionarioTrabalho in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS_PRODUCAO]:
            if textoEhIgual(dicionarioTrabalho.pegaId(), trabalhoProducaoConcluido.pegaId()):
                dicionarioTrabalho.setEstado(CODIGO_CONCLUIDO)
                break
        else:
            dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS_PRODUCAO].append(trabalhoProducaoConcluido)
    return trabalhoProducaoConcluido

def modificaExperienciaProfissao(trabalhoProducao):
    for profissao in dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO]:
        if textoEhIgual(profissao.pegaNome(), trabalhoProducao.pegaProfissao()):
            experiencia = profissao.pegaExperiencia() + trabalhoProducao.pegaExperiencia()
            if experiencia > 830000:
                experiencia = 830000
            profissao.setExperiencia(experiencia)
            repositorioProfissao.modificaProfissao(profissao)
            print(f'Experiência de {profissao.pegaNome()} atualizada para {experiencia}.')
            break

def retornaListaDicionarioTrabalhoProduzido(trabalhoProducaoConcluido):
    '''
    Função que recebe um objeto TrabalhoProducao
    '''
    listaTrabalhoEstoqueConcluido = []
    trabalhoEstoque = None
    if trabalhoEhProducaoRecursos(trabalhoProducaoConcluido):
        if trabalhoEhProducaoLicenca(trabalhoProducaoConcluido):
            trabalhoEstoque = TrabalhoEstoque('', CHAVE_LICENCA_APRENDIZ, '', 0, 2, 'Recurso', trabalhoProducaoConcluido.pegaTrabalhoId())
        else:
            if trabalhoEhMelhoriaEssenciaComum(trabalhoProducaoConcluido):
                trabalhoEstoque = TrabalhoEstoque('', 'Essência composta', '', 0, 5, 'Recurso', trabalhoProducaoConcluido.pegaTrabalhoId())
            elif trabalhoEhMelhoriaEssenciaComposta(trabalhoProducaoConcluido):
                trabalhoEstoque = TrabalhoEstoque('', 'Essência de energia', '', 0, 1, 'Recurso', trabalhoProducaoConcluido.pegaTrabalhoId())
            elif trabalhoEhMelhoriaSubstanciaComum(trabalhoProducaoConcluido):
                trabalhoEstoque = TrabalhoEstoque('', 'Substância composta', '', 0, 5, 'Recurso', trabalhoProducaoConcluido.pegaTrabalhoId())
            elif trabalhoEhMelhoriaSubstanciaComposta(trabalhoProducaoConcluido):
                trabalhoEstoque = TrabalhoEstoque('', 'Substância energética', '', 0, 1, 'Recurso', trabalhoProducaoConcluido.pegaTrabalhoId())
            elif trabalhoEhMelhoriaCatalisadorComum(trabalhoProducaoConcluido):
                trabalhoEstoque = TrabalhoEstoque('', 'Catalisador amplificado', '', 0, 5, 'Recurso', trabalhoProducaoConcluido.pegaTrabalhoId())
            elif trabalhoEhMelhoriaCatalisadorComposto(trabalhoProducaoConcluido):
                trabalhoEstoque = TrabalhoEstoque('', 'Catalisador de energia', '', 0, 1, 'Recurso', trabalhoProducaoConcluido.pegaTrabalhoId())
            if variavelExiste(trabalhoEstoque):
                if textoEhIgual(trabalhoProducaoConcluido.pegaLicenca(), CHAVE_LICENCA_APRENDIZ):
                    trabalhoEstoque.setQuantidade(trabalhoEstoque.pegaQuantidade() * 2)
        if variavelExiste(trabalhoEstoque):
            listaTrabalhoEstoqueConcluido.append(trabalhoEstoque)
        if trabalhoEhColecaoRecursosComuns(trabalhoProducaoConcluido) or trabalhoEhColecaoRecursosAvancados(trabalhoProducaoConcluido):
                nivelColecao = 1
                if trabalhoEhColecaoRecursosAvancados(trabalhoProducaoConcluido):
                    nivelColecao = 8
                for trabalho in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS]:
                    condicoes = textoEhIgual(trabalho.pegaProfissao(), trabalhoProducaoConcluido.pegaProfissao()) and trabalho.pegaNivel() == nivelColecao and textoEhIgual(trabalho.pegaRaridade(), CHAVE_RARIDADE_COMUM)
                    if condicoes:
                        trabalhoEstoque = TrabalhoEstoque('', trabalho.pegaNome(),trabalho.pegaProfissao(), trabalho.pegaNivel(), trabalho.pegaQuantidade(), trabalho.pegaRaridade(), trabalho.pegaTrabalhoId())
                        listaTrabalhoEstoqueConcluido.append(trabalhoEstoque)
                for trabalhoEstoque in listaTrabalhoEstoqueConcluido:
                    tipoRecurso = retornaChaveTipoRecurso(trabalhoEstoque)
                    if variavelExiste(tipoRecurso):
                        if tipoRecurso == CHAVE_RCT:
                            trabalhoEstoque.setQuantidade(2)
                        if tipoRecurso == CHAVE_RAT or tipoRecurso == CHAVE_RCS:
                            trabalhoEstoque.setQuantidade(3)
                        elif tipoRecurso == CHAVE_RAS or tipoRecurso == CHAVE_RCP:
                            trabalhoEstoque.setQuantidade(4)
                        elif tipoRecurso == CHAVE_RAP:
                            trabalhoEstoque.setQuantidade(5)
                        if textoEhIgual(trabalhoProducaoConcluido.pegaLicenca(), CHAVE_LICENCA_APRENDIZ):
                            trabalhoEstoque.setQuantidade(trabalhoEstoque.pegaQuantidade() * 2)
                    else:
                        print(f'Tipo de recurso não encontrado!')
        if tamanhoIgualZero(listaTrabalhoEstoqueConcluido):
                trabalhoEstoque = TrabalhoEstoque('', trabalhoProducaoConcluido.pegaNome(), trabalhoProducaoConcluido.pegaProfissao(), trabalhoProducaoConcluido.pegaNivel(), 0, trabalhoProducaoConcluido.pegaRaridade(), trabalhoProducaoConcluido.pegaTrabalhoId())
                tipoRecurso = retornaChaveTipoRecurso(trabalhoEstoque)
                if variavelExiste(tipoRecurso):
                    if tipoRecurso == CHAVE_RCS or tipoRecurso == CHAVE_RCT:
                        trabalhoEstoque.setQuantidade(1)
                    elif tipoRecurso == CHAVE_RCP or tipoRecurso == CHAVE_RAP or tipoRecurso == CHAVE_RAS or tipoRecurso == CHAVE_RAT:
                        trabalhoEstoque.setQuantidade(2)
                    if textoEhIgual(trabalhoProducaoConcluido[CHAVE_TIPO_LICENCA], CHAVE_LICENCA_APRENDIZ):
                        trabalhoEstoque.setQuantidade(trabalhoEstoque.pegaQuantidade() * 2)
                    listaTrabalhoEstoqueConcluido.append(trabalhoEstoque)
                else:
                    print(f'Tipo de recurso não encontrado!')
    else:
        trabalhoEstoque = TrabalhoEstoque('', trabalhoProducaoConcluido.pegaNome(), trabalhoProducaoConcluido.pegaProfissao(), trabalhoProducaoConcluido.pegaNivel(), 1, trabalhoProducaoConcluido.pegaRaridade(), trabalhoProducaoConcluido.pegaTrabalhoId())
        listaTrabalhoEstoqueConcluido.append(trabalhoEstoque)
    print(f'Lista de dicionários trabalhos concluídos:')
    for trabalhoEstoqueConcluido in listaTrabalhoEstoqueConcluido:
            print(trabalhoEstoqueConcluido)
    return listaTrabalhoEstoqueConcluido

def modificaQuantidadeTrabalhoEstoque(listaTrabalhoEstoqueConcluido, trabalhoEstoque):
    for trabalhoEstoqueConcluido in listaTrabalhoEstoqueConcluido:
        if textoEhIgual(trabalhoEstoqueConcluido.pegaNome(), trabalhoEstoque.pegaNome()):
            novaQuantidade = trabalhoEstoque.pegaQuantidade() + trabalhoEstoqueConcluido.pegaQuantidade()
            trabalhoEstoque.setQuantidade(novaQuantidade)
            print(trabalhoEstoque)
            repositorioEstoque.modificaTrabalhoEstoque(trabalhoEstoque)
            for indice in range(len(listaTrabalhoEstoqueConcluido)):
                if listaTrabalhoEstoqueConcluido[indice].pegaNome() == trabalhoEstoque.pegaNome():
                    del listaTrabalhoEstoqueConcluido[indice]
                    break
            if tamanhoIgualZero(listaTrabalhoEstoqueConcluido):
                break
    return listaTrabalhoEstoqueConcluido, trabalhoEstoque

def atualizaEstoquePersonagem(trabalhoEstoqueConcluido):
    global dicionarioPersonagemAtributos
    listaTrabalhoEstoqueConcluido = retornaListaDicionarioTrabalhoProduzido(trabalhoEstoqueConcluido)
    if not tamanhoIgualZero(listaTrabalhoEstoqueConcluido):
        if not tamanhoIgualZero(dicionarioPersonagemAtributos[CHAVE_LISTA_ESTOQUE]):
            for trabalhoEstoque in dicionarioPersonagemAtributos[CHAVE_LISTA_ESTOQUE]:
                listaTrabalhoEstoqueConcluido, trabalhoEstoque = modificaQuantidadeTrabalhoEstoque(listaTrabalhoEstoqueConcluido, trabalhoEstoque)
            else:
                if not tamanhoIgualZero(listaTrabalhoEstoqueConcluido):
                    for trabalhoEstoqueConcluido in listaTrabalhoEstoqueConcluido:
                        repositorioEstoque.adicionaTrabalhoEstoque(trabalhoEstoqueConcluido)
                        dicionarioPersonagemAtributos[CHAVE_LISTA_ESTOQUE].append(trabalhoEstoqueConcluido)
        else:
            for trabalhoEstoqueConcluido in listaTrabalhoEstoqueConcluido:
                repositorioEstoque.adicionaTrabalhoEstoque(trabalhoEstoqueConcluido)
                dicionarioPersonagemAtributos[CHAVE_LISTA_ESTOQUE].append(trabalhoEstoqueConcluido)

def retornaProfissaoTrabalhoProducaoConcluido(trabalhoProducaoConcluido):
    for profissao in dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO]:
        if textoEhIgual(profissao.pegaNome(), trabalhoProducaoConcluido.pegaProfissao()):
            return profissao
    return None

def retornaNivelXpMinimoMaximo(profissao):
    listaXPMaximo = [
        20, 200, 540, 1250, 2550, 4700, 7990, 12770
        ,19440, 28440, 40270, 55450, 74570, 98250, 127180, 156110
        ,185040, 215000, 245000, 300000, 375000, 470000, 585000, 706825
        ,830000, 830000]
    xpAtual = profissao.pegaExperiencia()
    nivelProfissao = 1
    xpMinimo = 0
    xpMaximo = 0
    for posicao in range(0,len(listaXPMaximo)):
        if listaXPMaximo[posicao] == 20:
            if xpAtual < listaXPMaximo[posicao]:
                xpMinimo = 0
                xpMaximo = listaXPMaximo[posicao]
                break
        else:
            if xpAtual < listaXPMaximo[posicao] and xpAtual >= listaXPMaximo[posicao-1]:
                nivelProfissao = posicao + 1
                xpMinimo = listaXPMaximo[posicao-1]
                xpMaximo = listaXPMaximo[posicao]
                break
    return nivelProfissao, xpMinimo, xpMaximo

def verificaProducaoTrabalhoRaro(trabalhoProducaoConcluido):
    global dicionarioPersonagemAtributos
    trabalhoProducaoRaro = None
    dicionarioProfissao = retornaProfissaoTrabalhoProducaoConcluido(trabalhoProducaoConcluido)
    if variavelExiste(dicionarioProfissao):
        _, _, xpMaximo = retornaNivelXpMinimoMaximo(dicionarioProfissao)
        licencaProducaoIdeal = CHAVE_LICENCA_PRINCIPIANTE
        if xpMaximo >= 830000:
            licencaProducaoIdeal = CHAVE_LICENCA_INICIANTE
        if textoEhIgual(trabalhoProducaoConcluido.pegaRaridade(), CHAVE_RARIDADE_MELHORADO):
            print(f'Trabalhos MELHORADO. Profissão {trabalhoProducaoConcluido.pegaProfissao()}. Nível {trabalhoProducaoConcluido.pegaNivel()}.')
            for trabalho in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS]:
                condicoes = (textoEhIgual(trabalho.pegaProfissao(), trabalhoProducaoConcluido.pegaProfissao())
                    and textoEhIgual(trabalho.pegaRaridade(), CHAVE_RARIDADE_RARO)
                    and trabalho.pegaNivel() == trabalhoProducaoConcluido.pegaNivel())
                if condicoes:    
                    if textoEhIgual(trabalho.pegaTrabalhoNecessario(), trabalhoProducaoConcluido.pegaNome()):
                        experiencia = trabalho.pegaExperiencia() * 1.5
                        trabalhoProducaoRaro = TrabalhoProducao('', trabalho.pegaNome(), trabalho.pegaNomeProducao(), trabalho.pegaEstado(), experiencia, trabalho.pegaNivel(), trabalho.pegaProfissao(), trabalho.pegaRaridade(), False, licencaProducaoIdeal, trabalho.pegaTrabalhoId())
                        break
    if variavelExiste(trabalhoProducaoRaro):
        trabalhoProducaoRaroComId = repositorioTrabalhoProducao.adicionaTrabalhoProducao(trabalhoProducaoRaro)
        dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS_PRODUCAO].append(trabalhoProducaoRaroComId)

def retornaListaPersonagemRecompensaRecebida(listaPersonagemPresenteRecuperado):
    if tamanhoIgualZero(listaPersonagemPresenteRecuperado):
        print(f'Limpou a lista...')
        listaPersonagemPresenteRecuperado = []
    nomePersonagemReconhecido = retornaNomePersonagem(0)
    if variavelExiste(nomePersonagemReconhecido):
        print(f'{nomePersonagemReconhecido} foi adicionado a lista!')
        listaPersonagemPresenteRecuperado.append(nomePersonagemReconhecido)
    else:
        print(f'Erro ao reconhecer nome...')
    return listaPersonagemPresenteRecuperado

def recuperaPresente():
    evento = 0
    print(f'Buscando recompensa diária...')
    while evento < 2:
        sleep(2)
        print(f'Buscando referência "PEGAR"...')
        telaInteira = retornaAtualizacaoTela()
        frameTela = telaInteira[0:telaInteira.shape[0],330:488]
        imagem = retornaImagemCinza(frameTela)
        imagem = cv2.GaussianBlur(imagem,(1,1),0)
        imagem = cv2.Canny(imagem,150,180)
        kernel = np.ones((2,2),np.uint8)
        imagem = retornaImagemDitalata(imagem,kernel,1)
        imagem = retornaImagemErodida(imagem,kernel,1)
        contornos,h1 = cv2.findContours(imagem,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for cnt in contornos:
            area = cv2.contourArea(cnt)
            if area > 4500 and area < 5700:
                x, y, l, a = cv2.boundingRect(cnt)
                print(f'Area:{area}, x:{x}, y:{y}.')
                cv2.rectangle(frameTela,(x,y),(x+l,y+a),(0,255,0),2)
                frameTratado = frameTela[y:y+a,x:x+l]
                centroX = 330+x+(l/2)
                centroY = y+(a/2)
                print(f'Referência encontrada!')
                clickMouseEsquerdo(1,centroX,centroY)
                posicionaMouseEsquerdo(telaInteira.shape[1]//2,telaInteira.shape[0]//2)
                if verificaErro(None) != 0:
                    evento=2
                    break
                clickEspecifico(1,'f2')
                break
        print(f'Próxima busca.')
        clickContinuo(8,'up')
        clickEspecifico(1,'left')
        evento += 1
    clickEspecifico(2,'f1')

def reconheceMenuRecompensa(menu):
    print(f'Entrou em recuperaPresente.')
    if menu == MENU_LOJA_MILAGROSA:
        clickEspecifico(1,'down')
        clickEspecifico(1,'enter')
    elif menu == MENU_RECOMPENSAS_DIARIAS:
        recuperaPresente()
    else:
        print(f'Recompensa diária já recebida!')

def deslogaPersonagem(personagemEmail):
    menu = retornaMenu()
    while menu != MENU_JOGAR:
        if menu == MENU_INICIAL:
            encerraSecao()
            break
        elif menu == MENU_JOGAR:
            break
        else:
            clickMouseEsquerdo(1, 2, 35)
        menu = retornaMenu()
    if personagemEmail != None and dicionarioPersonagemAtributos != None:
        modificaAtributoUso(False)

def entraPersonagem(listaPersonagemPresenteRecuperado):
    confirmacao = False
    print(f'Buscando próximo personagem...')
    clickEspecifico(1, 'enter')
    sleep(1)
    tentativas = 1
    erro = verificaErro(None)
    while erroEncontrado(erro):
        if erro == CODIGO_CONECTANDO:
            if tentativas > 10:
                clickEspecifico(2, 'enter')
                tentativas = 0
            tentativas += 1
        erro = verificaErro(None)
    else:
        clickEspecifico(1, 'f2')
        if len(listaPersonagemPresenteRecuperado) == 1:
            clickContinuo(8, 'left')
        else:
            clickEspecifico(1, 'right')
        nomePersonagem = retornaNomePersonagem(1)               
        while True:
            nomePersonagemPresenteado = None
            for nomeLista in listaPersonagemPresenteRecuperado:
                if nomePersonagem == nomeLista and nomePersonagem != None:
                    nomePersonagemPresenteado = nomeLista
                    break
            if nomePersonagemPresenteado != None:
                clickEspecifico(1, 'right')
                nomePersonagem = retornaNomePersonagem(1)
            if nomePersonagem == None:
                print(f'Fim da lista de personagens!')
                clickEspecifico(1, 'f1')
                break
            else:
                clickEspecifico(1, 'f2')
                sleep(1)
                tentativas = 1
                erro = verificaErro(None)
                while erroEncontrado(erro):
                    if erro == CODIGO_RECEBER_RECOMPENSA:
                        break
                    elif erro == CODIGO_CONECTANDO:
                        if tentativas > 10:
                            clickEspecifico(2, 'enter')
                            tentativas = 0
                        tentativas += 1
                    sleep(1.5)
                    erro = verificaErro(None)
                confirmacao = True
                print(f'Login efetuado com sucesso!')
                break
    return confirmacao

def recebeTodasRecompensas(menu):
    listaPersonagemPresenteRecuperado = retornaListaPersonagemRecompensaRecebida(listaPersonagemPresenteRecuperado = [])
    while True:
        reconheceMenuRecompensa(menu)
        if existePixelCorrespondencia():
            vaiParaMenuCorrespondencia()
            recuperaCorrespondencia()
        print(f'Lista: {listaPersonagemPresenteRecuperado}.')
        deslogaPersonagem(None)
        if entraPersonagem(listaPersonagemPresenteRecuperado):
            listaPersonagemPresenteRecuperado = retornaListaPersonagemRecompensaRecebida(listaPersonagemPresenteRecuperado)
        else:
            print(f'Todos os personagens foram verificados!')
            break
        menu = retornaMenu()

def trataMenu(menu):
    global dicionarioPersonagemAtributos
    dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO] = True
    if menu == MENU_DESCONHECIDO:
        pass
    elif menu == MENU_TRABALHOS_ATUAIS:
        estadoTrabalho = retornaEstadoTrabalho()
        if estadoTrabalho == CODIGO_CONCLUIDO:
            nomeTrabalhoConcluido = reconheceRecuperaTrabalhoConcluido()
            if variavelExiste(nomeTrabalhoConcluido):
                trabalhoProducaoConcluido = retornaTrabalhoConcluido(nomeTrabalhoConcluido)
                if not variavelExiste(trabalhoProducaoConcluido):
                    trabalhoProducaoConcluido = modificaTrabalhoConcluidoListaProduzirProduzindo(trabalhoProducaoConcluido)
                    modificaExperienciaProfissao(trabalhoProducaoConcluido)
                    atualizaEstoquePersonagem(trabalhoProducaoConcluido)
                    verificaProducaoTrabalhoRaro(trabalhoProducaoConcluido)
                else:
                    print(f'Dicionário trabalho concluido não reconhecido.')
            else:
                print(f'Nome trabalho concluído não reconhecido.')
        elif estadoTrabalho == CODIGO_PRODUZINDO:
            if not existeEspacoProducao(dicionarioPersonagemAtributos):
                print(f'Todos os espaços de produção ocupados.')
                dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO] = False
            else:
                clickContinuo(3,'up')
                clickEspecifico(1,'left')
        elif estadoTrabalho == CODIGO_PARA_PRODUZIR:
            clickContinuo(3,'up')
            clickEspecifico(1,'left')
    elif menu == MENU_RECOMPENSAS_DIARIAS or menu == MENU_LOJA_MILAGROSA:
        recebeTodasRecompensas(menu)
        for personagem in dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM]:
            if not personagem.pegaEstado():
                personagem.setEstado(True)
                repositorioPersonagem.modificaPersonagem(personagem)
        dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO] = False
    elif menu == MENU_PRINCIPAL:
        clickEspecifico(1,'num1')
        clickEspecifico(1,'num7')
    elif menu == MENU_PERSONAGEM:
        clickEspecifico(1,'num7')
    elif menu == MENU_TRABALHOS_DISPONIVEIS:
        clickEspecifico(1,'up')
        clickEspecifico(2,'left')
    elif menu == MENU_TRABALHO_ESPECIFICO:
        clickEspecifico(1,'f1')
        clickContinuo(3,'up')
        clickEspecifico(2,'left')
    elif menu == MENU_OFERTA_DIARIA:
        clickEspecifico(1,'f1')
    elif menu == MENU_INICIAL:
        clickEspecifico(1,'f2')
        clickEspecifico(1,'num1')
        clickEspecifico(1,'num7')
    else:
        dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO] = False
    erro = verificaErro(None)
    if erro == CODIGO_ERRO_OUTRA_CONEXAO:
        dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO] = False
        dicionarioPersonagemAtributos[CHAVE_UNICA_CONEXAO] = False

def vaiParaMenuProduzir():
    global dicionarioPersonagemAtributos
    erro = verificaErro()
    if not erroEncontrado(erro):
        menu = retornaMenu()
        if ehMenuInicial(menu):
            if existePixelCorrespondencia():
                vaiParaMenuCorrespondencia()
                recuperaCorrespondencia()
        while not ehMenuProduzir(menu):
            trataMenu(menu)
            if not chaveConfirmacaoEhVerdadeira(dicionarioPersonagemAtributos):
                break
            menu = retornaMenu()
        else:
            return True
    elif ehErroOutraConexao(erro):
        dicionarioPersonagemAtributos[CHAVE_UNICA_CONEXAO] = False
    return False

def retornaListaDicionariosTrabalhosRarosVendidos(dicionarioUsuario):
    print(f'Definindo lista dicionários produtos raros vendidos...')
    global dicionarioPersonagemAtributos
    listaDicionariosTrabalhosRarosVendidos = []
    if dicionarioUsuario != None:
        dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO] = dicionarioUsuario[CHAVE_PERSONAGEM_EM_USO]
        dicionarioPersonagemAtributos[CHAVE_ID_USUARIO] = dicionarioUsuario[CHAVE_ID_USUARIO]
        dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO] = repositorioProfissao.pegaTodasProfissoes()
        dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS] = repositorioTrabalho.pegaTodosTrabalhos()
        dicionarioPersonagemAtributos[CHAVE_LISTA_VENDAS] = repositorioVendas.pegaTodosTrabalhoVendidos()
        dicionarioPersonagemAtributos[CHAVE_LISTA_ESTOQUE] = repositorioEstoque.pegaTodosTrabalhosEstoque()
        dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS_PRODUCAO] = repositorioTrabalhoProducao.pegaTodosTrabalhosProducao()
    if not tamanhoIgualZero(dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS]):
        for produtoVendido in dicionarioPersonagemAtributos[CHAVE_LISTA_VENDAS]:
            for trabalho in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS]:
                condicoes = (
                    textoEhIgual(trabalho[CHAVE_RARIDADE], CHAVE_RARIDADE_RARO)
                    and texto1PertenceTexto2(trabalho[CHAVE_NOME], produtoVendido['nomeProduto'])
                    and textoEhIgual(produtoVendido['nomePersonagem'], dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO][CHAVE_ID])
                    and not trabalhoEhProducaoRecursos(trabalho))
                if condicoes:
                    # dicionarioTrabalhoRaroVendido = {
                    #     CHAVE_ID:trabalho[CHAVE_ID],
                    #     CHAVE_NOME:trabalho[CHAVE_NOME],
                    #     CHAVE_NOME_PRODUCAO:trabalho[CHAVE_NOME_PRODUCAO],
                    #     CHAVE_NIVEL:trabalho[CHAVE_NIVEL],
                    #     CHAVE_RARIDADE:trabalho[CHAVE_RARIDADE],
                    #     CHAVE_PROFISSAO:trabalho[CHAVE_PROFISSAO],
                    #     CHAVE_QUANTIDADE:produtoVendido['quantidadeProduto'],
                    #     CHAVE_EXPERIENCIA:trabalho[CHAVE_EXPERIENCIA]}
                    # if CHAVE_TRABALHO_NECESSARIO in trabalho:
                    #     dicionarioTrabalhoRaroVendido[CHAVE_TRABALHO_NECESSARIO] = trabalho[CHAVE_TRABALHO_NECESSARIO]
                    # listaDicionariosTrabalhosRarosVendidos.append(dicionarioTrabalhoRaroVendido)
                    break
    listaDicionariosTrabalhosRarosVendidosOrdenados = sorted(listaDicionariosTrabalhosRarosVendidos, key = lambda dicionario: (dicionario[CHAVE_PROFISSAO], dicionario[CHAVE_NIVEL], dicionario[CHAVE_NOME]))
    return listaDicionariosTrabalhosRarosVendidosOrdenados

def verificaProdutosRarosMaisVendidos(dicionarioUsuario):
    listaDicionariosProdutosRarosVendidos = retornaListaDicionariosTrabalhosRarosVendidos(dicionarioUsuario)
    if not tamanhoIgualZero(listaDicionariosProdutosRarosVendidos):
        # produzProdutoMaisVendido(listaDicionariosProdutosRarosVendidos)
        pass
    else:
        print(f'Lista de trabalhos raros vendidos está vazia!')

def defineChaveListaProfissoesNecessarias():
    global dicionarioPersonagemAtributos
    print(f'Verificando profissões necessárias...')
    dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_VERIFICADA] = []
    posicao = 1
    for profissao in dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO]:
        for trabalhoProducaoDesejado in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS_PRODUCAO]:
            chaveProfissaoEhIgualEEstadoEhParaProduzir = textoEhIgual(profissao.pegaNome(), trabalhoProducaoDesejado.pegaProfissao()) and trabalhoProducaoDesejado.ehParaProduzir()
            if chaveProfissaoEhIgualEEstadoEhParaProduzir:
                dicionarioProfissao = {
                    CHAVE_ID:profissao.pegaId(),
                    CHAVE_NOME:profissao.pegaNome(),
                    CHAVE_PRIORIDADE:profissao.pegaPrionaridade(),
                    CHAVE_POSICAO:posicao}
                dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_VERIFICADA].append(dicionarioProfissao)
                break
        posicao+=1
    else:
        dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_VERIFICADA] = sorted(dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_VERIFICADA],key=lambda dicionario:dicionario[CHAVE_PRIORIDADE],reverse=True)

def iniciaBuscaTrabalho(dicionarioTrabalho):
    global dicionarioPersonagemAtributos
    defineChaveListaProfissoesNecessarias()
    indiceProfissao = 0
    dicionarioTrabalho[CHAVE_POSICAO] = -1
    while indiceProfissao < len(dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_VERIFICADA]):#percorre lista de profissao
        if vaiParaMenuProduzir():
            dicionarioProfissaoVerificada = dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_VERIFICADA][indiceProfissao]
            if not chaveConfirmacaoForVerdadeira(dicionarioPersonagemAtributos) or not chaveUnicaConexaoForVerdadeira(dicionarioPersonagemAtributos):
                break
            elif not existeEspacoProducao():
                indiceProfissao += 1
                continue
            if listaProfissoesFoiModificada():
                atualizaListaProfissao()
                verificaEspacoProducao()
            entraProfissaoEspecifica(dicionarioProfissaoVerificada)
            print(f'Verificando profissão: {dicionarioProfissaoVerificada[CHAVE_NOME]}')
            
            listaDeListaTrabalhos = []
            dicionarioTrabalho[CHAVE_PROFISSAO] = dicionarioProfissaoVerificada[CHAVE_NOME]
            dicionarioTrabalho[CHAVE_CONFIRMACAO] = True
            listaDicionariosTrabalhosEspeciais = retornaListaDicionariosTrabalhosRaridadeEspecifica(dicionarioTrabalho, raridade = CHAVE_RARIDADE_ESPECIAL)
            if not tamanhoIgualZero(listaDicionariosTrabalhosEspeciais):
                listaDicionariosTrabalhosEspeciais = sorted(listaDicionariosTrabalhosEspeciais,key=lambda dicionario:dicionario[CHAVE_NOME])
                listaDeListaTrabalhos.append(listaDicionariosTrabalhosEspeciais)
            listaDicionariosTrabalhosRaros = retornaListaDicionariosTrabalhosRaridadeEspecifica(dicionarioTrabalho, raridade = CHAVE_RARIDADE_RARO)
            if not tamanhoIgualZero(listaDicionariosTrabalhosRaros):
                listaDicionariosTrabalhosRaros = sorted(listaDicionariosTrabalhosRaros,key=lambda dicionario:(dicionario[CHAVE_PRIORIDADE], dicionario[CHAVE_NOME]))
                listaDeListaTrabalhos.append(listaDicionariosTrabalhosRaros)
            listaDicionariosTrabalhosMelhorados = retornaListaDicionariosTrabalhosRaridadeEspecifica(dicionarioTrabalho, raridade = CHAVE_RARIDADE_MELHORADO)
            if not tamanhoIgualZero(listaDicionariosTrabalhosMelhorados):
                listaDicionariosTrabalhosMelhorados = sorted(listaDicionariosTrabalhosMelhorados,key=lambda dicionario:dicionario[CHAVE_NOME])
                listaDeListaTrabalhos.append(listaDicionariosTrabalhosMelhorados)
            listaDicionariosTrabalhosComuns = retornaListaDicionariosTrabalhosRaridadeEspecifica(dicionarioTrabalho, raridade = CHAVE_RARIDADE_COMUM)
            if not tamanhoIgualZero(listaDicionariosTrabalhosComuns):
                listaDicionariosTrabalhosComuns = sorted(listaDicionariosTrabalhosComuns,key=lambda dicionario:(dicionario[CHAVE_PRIORIDADE], dicionario[CHAVE_NOME]))
                listaDeListaTrabalhos.append(listaDicionariosTrabalhosComuns)
            indiceLista = 0
            while indiceLista < len(listaDeListaTrabalhos):
                listaVerificada = listaDeListaTrabalhos[indiceLista]
                dicionarioTrabalho[CHAVE_LISTA_DESEJO_PRIORIZADA] = listaVerificada
                for dicionarioTrabalhoVerificado in listaVerificada:
                    if raridadeTrabalhoEhEspecial(dicionarioTrabalhoVerificado)or raridadeTrabalhoEhRaro(dicionarioTrabalhoVerificado):
                        print(f'Trabalho desejado: {dicionarioTrabalhoVerificado[CHAVE_NOME]}.')
                        posicaoAux = -1
                        if dicionarioTrabalho[CHAVE_POSICAO] != -1:
                            posicaoAux = dicionarioTrabalho[CHAVE_POSICAO]
                        dicionarioTrabalho[CHAVE_POSICAO] = 0
                        while naoFizerQuatroVerificacoes(dicionarioTrabalho)and not chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
                            nomeTrabalhoReconhecido = retornaNomeTrabalhoPosicaoTrabalhoRaroEspecial(dicionarioTrabalho)
                            print(f'Trabalho {dicionarioTrabalhoVerificado[CHAVE_RARIDADE]} reconhecido: {nomeTrabalhoReconhecido}.')
                            if variavelExiste(nomeTrabalhoReconhecido):
                                if texto1PertenceTexto2(nomeTrabalhoReconhecido, dicionarioTrabalhoVerificado[CHAVE_NOME_PRODUCAO]):
                                    dicionarioTrabalho = entraTrabalhoEncontrado(dicionarioTrabalho, dicionarioTrabalhoVerificado)
                                    if chaveConfirmacaoForVerdadeira(dicionarioTrabalho):
                                        dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO] = dicionarioTrabalhoVerificado
                                        tipoTrabalho = 0
                                        if trabalhoEhProducaoRecursos(dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO]):
                                            tipoTrabalho = 1
                                        dicionarioTrabalho = confirmaNomeTrabalho(dicionarioTrabalho, tipoTrabalho)
                                        if not chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
                                            clickEspecifico(1,'f1')
                                            clickContinuo(dicionarioTrabalho[CHAVE_POSICAO]+1,'up')
                                    else:
                                        break
                            else:
                                dicionarioTrabalho[CHAVE_POSICAO] = 4
                            dicionarioTrabalho = incrementaChavePosicaoTrabalho(dicionarioTrabalho)
                        dicionarioTrabalho[CHAVE_POSICAO] = posicaoAux
                        
                        if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not chaveConfirmacaoForVerdadeira(dicionarioTrabalho):
                            break
                    elif raridadeTrabalhoEhMelhorado(dicionarioTrabalhoVerificado)or raridadeTrabalhoEhComum(dicionarioTrabalhoVerificado):
                        dicionarioTrabalho = defineDicionarioTrabalhoComumMelhorado(dicionarioTrabalho)
                        dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO] = dicionarioTrabalho[CHAVE_CONFIRMACAO]
                        if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not chaveConfirmacaoForVerdadeira(dicionarioTrabalho):
                            break
                        elif indiceLista + 1 >= len(listaDeListaTrabalhos):
                            vaiParaMenuTrabalhoEmProducao()
                        else:
                            vaiParaOTopoDaListaDeTrabalhosComunsEMelhorados(dicionarioTrabalho)
                    if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not chaveConfirmacaoForVerdadeira(dicionarioTrabalho):
                        break
                if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not chaveConfirmacaoForVerdadeira(dicionarioTrabalho):
                    break
                else:
                    indiceLista += 1
                    dicionarioTrabalho[CHAVE_POSICAO] = -1
            if chaveConfirmacaoForVerdadeira(dicionarioPersonagemAtributos):# CHAVE que indica que nem um erro foi detectado
                if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):# Começa processo de produção do trabalho
                    dicionarioTrabalho = iniciaProcessoDeProducao(dicionarioTrabalho)
                    
                else:
                    saiProfissaoVerificada(dicionarioTrabalho)
                    indiceProfissao += 1
                    dicionarioTrabalho[CHAVE_POSICAO] = -1
                if chaveUnicaConexaoForVerdadeira(dicionarioPersonagemAtributos):
                    if chaveEspacoBolsaForVerdadeira(dicionarioPersonagemAtributos):
                        if retornaEstadoTrabalho() == CODIGO_CONCLUIDO:
                            nomeTrabalhoConcluido = reconheceRecuperaTrabalhoConcluido()
                            if variavelExiste(nomeTrabalhoConcluido):
                                dicionarioTrabalhoConcluido = retornaDicionarioTrabalhoConcluido(nomeTrabalhoConcluido)
                                if not tamanhoIgualZero(dicionarioTrabalhoConcluido):
                                    dicionarioTrabalhoConcluido = modificaTrabalhoConcluidoListaProduzirProduzindo(dicionarioTrabalhoConcluido)
                                    modificaExperienciaProfissao(dicionarioTrabalhoConcluido)
                                    atualizaEstoquePersonagem(dicionarioTrabalhoConcluido)
                                    verificaProducaoTrabalhoRaro(dicionarioTrabalhoConcluido)
                                else:
                                    print(f'{D}: Dicionário trabalho concluido não reconhecido.')
                                    
                            else:
                                print(f'{D}: Dicionário trabalho concluido não reconhecido.')
                                
                        elif not existeEspacoProducao():
                            break
                    dicionarioTrabalho[CHAVE_DICIONARIO_TRABALHO_DESEJADO] = None
                    clickContinuo(3,'up')
                    clickEspecifico(1,'left')
                    
                    sleep(1.5)
        else:
            break
    else:
        if listaProfissoesFoiModificada():
            atualizaListaProfissao()
            verificaEspacoProducao()
        print(f'Fim da lista de profissões...')
        
def iniciaProcessoBusca():
    global dicionarioPersonagemAtributos
    dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM] = repositorioPersonagem.pegaTodosPersonagens()
    dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM_RETIRADO] = []
    defineChaveListaPersonagensAtivos()
    while True:
        if tamanhoIgualZero(dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM_ATIVO]):
            dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM] = repositorioPersonagem.pegaTodosPersonagens()
            dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM_RETIRADO] = []
            defineChaveListaPersonagensAtivos()
        else:
            defineChaveDicionarioPersonagemEmUso()
            if variavelExiste(dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO]):
                modificaAtributoUso(True)
                print(f'Personagem ({dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO][CHAVE_NOME]}) ESTÁ EM USO.')
                inicializaChavesPersonagem()
                print('Inicia busca...')
                if vaiParaMenuProduzir():
                    # while defineTrabalhoComumProfissaoPriorizada():
                    #     continue
                    listaDicionariosTrabalhosParaProduzirProduzindo = retornaListaTrabalhosParaProduzirProduzindo()
                    if not tamanhoIgualZero(listaDicionariosTrabalhosParaProduzirProduzindo):
                        dicionarioTrabalho = {
                            CHAVE_LISTA_TRABALHOS_PRODUCAO: listaDicionariosTrabalhosParaProduzirProduzindo,
                            CHAVE_DICIONARIO_TRABALHO_DESEJADO: None}
                        # if dicionarioPersonagemAtributos[CHAVE_VERIFICA_TRABALHO]:
                        #     verificaProdutosRarosMaisVendidos(None)
                        iniciaBuscaTrabalho(dicionarioTrabalho)
    #                 else:
    #                     print(f'Lista de trabalhos desejados vazia.')
    #                      
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
                    pass
    
def preparaPersonagem():
    clickAtalhoEspecifico('alt', 'tab')
    # clickAtalhoEspecifico('win', 'left')
    iniciaProcessoBusca()

def testes():
    # testRepositorioPersonagem = TestRepositorioPersonagem()
    testRepositorioProfissao = TestRepositorioProfisssao()
    # testRepositorioTrabalho = TestRepositorioTrabalho()
    # testRepositorioVendas = TestRespositorioVendas()
    # testRepositorioEstoque = TestRepositorioEstoque()
    testRepositorioTrabalhoProducao = TestRepositorioTrabalhoProducao()

    # testRepositorioPersonagem.testDeveRetornarListaComOitoPersonagens()
    # testRepositorioPersonagem.testDeveAlternarChaveUso()
    # testRepositorioPersonagem.testDeveAlternarChaveEstado()
    # testRepositorioProfissao.testDeveRetornarListaComNoveProfissoes()
    # testRepositorioProfissao.testDeveModificarPrimeiraProfissao()
    testRepositorioProfissao.testDeveMostrarListadeProfissoesOrdenadaPorExperiencia()
    # testRepositorioTrabalho.testDeveRetornarListaComMaisDeZeroItens()
    # testRepositorioVendas.testDeveLimparListaVenda()
    # testRepositorioVendas.testDeveAdicionarNovaVendaALista()
    # testRepositorioVendas.testDeveRemoverPrimeiraVendaDaLista()
    # testRepositorioVendas.testDeveRetornarListaComMaisDeZeroItens()
    # testRepositorioEstoque.testDeveRetornaListaComMaisDeZeroItens()
    # testRepositorioEstoque.testDeveAdicionarItemAoEstoque()
    # testRepositorioEstoque.testDeveModificarQuantidadeDoPrimeiroItemDoEstoque()
    # testRepositorioTrabalhoProducao.testDeveRetornarZeroItensQuandoLimparListaProducao()
    # testRepositorioTrabalhoProducao.testDeveAdicionarItemNaLista()
    # testRepositorioTrabalhoProducao.testDeveRetornarListaComMaisDeZeroItens()
    # testRepositorioTrabalhoProducao.testDeveRemoverPrimeiroItemDaLista()
    # testRepositorioTrabalhoProducao.testDeveModificarPrimeiroItemDaLista()

if __name__=='__main__':
    # preparaPersonagem()
    testes()