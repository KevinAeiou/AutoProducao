from teclado import *
from constantes import *
from utilitarios import *
from imagem import ManipulaImagem
from time import sleep
import datetime
import re

from repositorio.repositorioPersonagem import *
from repositorio.repositorioEstoque import *
from repositorio.repositorioProfissao import *
from repositorio.repositorioTrabalho import *
from repositorio.repositorioVendas import *
from repositorio.repositorioTrabalhoProducao import *
# from repositorio. import *
from modelos.trabalhoRecurso import TrabalhoRecurso

imagem = ManipulaImagem()
dicionarioPersonagemAtributos = {}
repositorioPersonagem = None
repositorioTrabalho = None
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
    for personagemAtivo in dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM_ATIVO]:
        if textoEhIgual(personagemReconhecido, personagemAtivo.pegaNome()):
            print(f'Personagem {personagemReconhecido} confirmado!')
            dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO] = personagemAtivo
            break
    else:
        print(f'Personagem {personagemReconhecido} não está ativo!')

def defineChaveDicionarioPersonagemEmUso():
    dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO] = None
    nomePersonagemReconhecidoTratado = imagem.retornaTextoNomePersonagemReconhecido(0)
    if variavelExiste(nomePersonagemReconhecidoTratado):
        confirmaNomePersonagem(nomePersonagemReconhecidoTratado)
    elif nomePersonagemReconhecidoTratado == 'provisorioatecair':
        print(f'Nome personagem diferente!')
    else:
        print(f'Nome personagem não reconhecido!')

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
    dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS] = repositorioTrabalho.pegaTodosTrabalhos()
    dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO] = repositorioProfissao.pegaTodasProfissoes()
    dicionarioPersonagemAtributos[CHAVE_LISTA_VENDAS] = repositorioVendas.pegaTodasVendas()
    dicionarioPersonagemAtributos[CHAVE_LISTA_ESTOQUE] = repositorioEstoque.pegaTodosTrabalhosEstoque()
    dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS_PRODUCAO] = repositorioTrabalhoProducao.pegaTodosTrabalhosProducao()

def retornaCodigoErroReconhecido():
    textoErroEncontrado = imagem.retornaErroReconhecido()
    if variavelExiste(textoErroEncontrado):
        textoErroEncontrado = limpaRuidoTexto(textoErroEncontrado)
        textoErroEncontrado = retiraDigitos(textoErroEncontrado)
        tipoErro = ['Você precisa de uma licença defabricação para iniciar este pedido',
            'Falha ao se conectar ao servidor',
            'Você precisa de mais recursos parainiciar este pedido',
            'Selecione um item para iniciar umpedido de artesanato',
            'Conectando',
            'Você precisa de mais experiência de produção para iniciar este pedido',
            'Você recebeu um novo presenteDessgja ir à Loja Milagrosa paraconferir',
            'Todos os espaços de fabricaçãoestão ocupados',
            'Tem certeza de que deseja concluir aprodução',
            'Estamos fazendo de tudo paraconcluíla o mais rápido possível',
            'No momento esta conta está sendousada em outro dispositivo',
            'Gostanadecomprar',
            'Conexão perdida com o servidor',
            'Você precisa de mais',
            'Nome de usuário ou senha inválida',
            'Pedido de produção expirado',
            'reinodejogoselecionado',
            'Versão do jogo desatualizada',
            'restaurandoconexão',
            'paraatarefadeprodução',
            'Bolsa cheia',
            'Desgeja sair do Warspear Online']
        for posicaoTipoErro in range(len(tipoErro)):
            textoErro = limpaRuidoTexto(tipoErro[posicaoTipoErro])
            if textoErro in textoErroEncontrado:
                return posicaoTipoErro+1
    return 0

def verificaLicenca(dicionarioTrabalho):
    confirmacao = False
    if variavelExiste(dicionarioTrabalho):
        print(f"Buscando: {dicionarioTrabalho[CHAVE_TIPO_LICENCA]}")
        licencaReconhecida = imagem.retornaTextoLicencaReconhecida()
        if variavelExiste(licencaReconhecida) and variavelExiste(dicionarioTrabalho[CHAVE_TIPO_LICENCA]):
            print(f'Licença reconhecida: {licencaReconhecida}.')
            primeiraBusca = True
            listaCiclo = []
            while not texto1PertenceTexto2(licencaReconhecida, dicionarioTrabalho[CHAVE_TIPO_LICENCA]):
                clickEspecifico(1, "right")
                listaCiclo.append(licencaReconhecida)
                licencaReconhecida = imagem.retornaTextoLicencaReconhecida()
                if variavelExiste(licencaReconhecida):
                    print(f'Licença reconhecida: {licencaReconhecida}.')
                    if texto1PertenceTexto2('nenhumitem', licencaReconhecida) or len(listaCiclo) > 10:
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
                # print(f'Sem licenças de produção...')
                # clickEspecifico(1, 'f1')
                # repositorioPersonagem.alternaEstado(dicionarioPersonagem[CHAVE_PERSONAGEM_EM_USO])
        else:
            print(f'Erro ao reconhecer licença!')
    return confirmacao, dicionarioTrabalho

def verificaErro():
    sleep(0.5)
    print(f'Verificando erro...')
    CODIGO_ERRO = retornaCodigoErroReconhecido()
    if ehErroLicencaNecessaria(CODIGO_ERRO) or ehErroFalhaConexao(CODIGO_ERRO) or ehErroConexaoInterrompida(CODIGO_ERRO) or ehErroServidorEmManutencao(CODIGO_ERRO) or ehErroReinoIndisponivel(CODIGO_ERRO):
        clickEspecifico(2, "enter")
        if ehErroLicencaNecessaria(CODIGO_ERRO):
            verificaLicenca(None)
        return CODIGO_ERRO
    if ehErroOutraConexao(CODIGO_ERRO) or ehErroRecursosInsuficiente(CODIGO_ERRO) or ehErroTempoDeProducaoExpirada(CODIGO_ERRO) or ehErroExperienciaInsuficiente(CODIGO_ERRO) or ehErroEspacoProducaoInsuficiente(CODIGO_ERRO):
        clickEspecifico(1,'enter')
        if ehErroOutraConexao(CODIGO_ERRO):
            return CODIGO_ERRO
        clickEspecifico(2,'f1')
        clickContinuo(9,'up')
        clickEspecifico(1,'left')
        return CODIGO_ERRO
    if ehErroEscolhaItemNecessaria(CODIGO_ERRO):
        clickEspecifico(1, 'enter')
        clickEspecifico(1, 'f2')
        clickContinuo(9, 'up')
        return CODIGO_ERRO
    if ehErroConectando(CODIGO_ERRO) or ehErroRestauraConexao(CODIGO_ERRO):
        sleep(1)
        return CODIGO_ERRO
    if ehErroReceberRecompensaDiaria(CODIGO_ERRO) or ehErroVersaoJogoDesatualizada(CODIGO_ERRO) or CODIGO_ERRO == CODIGO_ERRO_USA_OBJETO_PARA_PRODUZIR or ehErroSairDoJogo(CODIGO_ERRO):
        clickEspecifico(1,'f2')
        if ehErroVersaoJogoDesatualizada(CODIGO_ERRO):
            clickEspecifico(1,'f1')
            exit()
            return CODIGO_ERRO
        return CODIGO_ERRO
    if ehErroTrabalhoNaoConcluido(CODIGO_ERRO):
        clickEspecifico(1,'f1')
        clickContinuo(8,'up')
        return CODIGO_ERRO
    if ehErroEspacoBolsaInsuficiente(CODIGO_ERRO):
        clickEspecifico(1,'f1')
        clickContinuo(8,'up')
        return CODIGO_ERRO
    if ehErroMoedasMilagrosasInsuficientes(CODIGO_ERRO):
        clickEspecifico(1,'f1')
        return CODIGO_ERRO
    if ehErroUsuarioOuSenhaInvalida(CODIGO_ERRO):
        clickEspecifico(1,'enter')
        clickEspecifico(1,'f1')
        return CODIGO_ERRO
    else:
        print(f'Nem um erro encontrado!')
    return CODIGO_ERRO

def retornaMenu():
    print(f'Reconhecendo menu.')
    textoMenu = imagem.retornaTextoMenuReconhecido(26,1,150)
    if variavelExiste(textoMenu):
        if texto1PertenceTexto2('spearonline',textoMenu):
            textoMenu=imagem.retornaTextoMenuReconhecido(216,197,270)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('noticias',textoMenu):
                    print(f'Menu notícias...')
                    return MENU_NOTICIAS
                if texto1PertenceTexto2('personagens',textoMenu):
                    print(f'Menu escolha de personagem...')
                    return MENU_ESCOLHA_PERSONAGEM
                if texto1PertenceTexto2('artesanato',textoMenu):
                    textoMenu = imagem.retornaTextoMenuReconhecido(266, 242, 150)
                    if variavelExiste(textoMenu):
                        if texto1PertenceTexto2('profissoes',textoMenu):
                            textoMenu=imagem.retornaTextoMenuReconhecido(191,612,100)
                            if variavelExiste(textoMenu):
                                if texto1PertenceTexto2('fechar',textoMenu):
                                    print(f'Menu produzir...')
                                    return MENU_PROFISSOES
                                if texto1PertenceTexto2('voltar',textoMenu):
                                    print(f'Menu trabalhos diponíveis...')
                                    return MENU_TRABALHOS_DISPONIVEIS
                        if texto1PertenceTexto2('pedidosativos',textoMenu):
                            print(f'Menu trabalhos atuais...')
                            return MENU_TRABALHOS_ATUAIS
            textoMenu = imagem.retornaTextoSair()
            if variavelExiste(textoMenu):
                if textoEhIgual(textoMenu,'sair'):
                    print(f'Menu jogar...')
                    return MENU_JOGAR
            if imagem.verificaMenuReferencia():
                print(f'Menu tela inicial...')
                return MENU_INICIAL
            textoMenu=imagem.retornaTextoMenuReconhecido(291,412,100)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('conquistas',textoMenu):
                    print(f'Menu personagem...')
                    return MENU_PERSONAGEM
                if texto1PertenceTexto2('interagir',textoMenu):
                    print(f'Menu principal...')
                    return MENU_PRINCIPAL
            textoMenu=imagem.retornaTextoMenuReconhecido(191,319,270)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('parâmetros',textoMenu):
                    if texto1PertenceTexto2('requisitos',textoMenu):
                        print(f'Menu atributo do trabalho...')
                        return MENU_TRABALHOS_ATRIBUTOS
                    else:
                        print(f'Menu licenças...')
                        return MENU_LICENSAS
            textoMenu=imagem.retornaTextoMenuReconhecido(275,400,150)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('Recompensa',textoMenu):
                    print(f'Menu trabalho específico...')
                    return MENU_TRABALHO_ESPECIFICO
            textoMenu=imagem.retornaTextoMenuReconhecido(266,269,150)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('ofertadiaria',textoMenu):
                    print(f'Menu oferta diária...')
                    return MENU_OFERTA_DIARIA
            textoMenu=imagem.retornaTextoMenuReconhecido(181,75,150)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('Loja Milagrosa',textoMenu):
                    print(f'Menu loja milagrosa...')
                    return MENU_LOJA_MILAGROSA
            textoMenu=imagem.retornaTextoMenuReconhecido(180,40,300)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('recompensasdiarias',textoMenu):
                    print(f'Menu recompensas diárias...')
                    return MENU_RECOMPENSAS_DIARIAS
            textoMenu=imagem.retornaTextoMenuReconhecido(310,338,57)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('meu',textoMenu):
                    print(f'Menu meu perfil...')
                    return MENU_MEU_PERFIL           
            textoMenu=imagem.retornaTextoMenuReconhecido(169,97,75)
            if variavelExiste(textoMenu):
                if texto1PertenceTexto2('Bolsa',textoMenu):
                    print(f'Menu bolsa...')
                    return MENU_BOLSA
            clickMouseEsquerdo(1,35,35)
            return MENU_DESCONHECIDO
        clickAtalhoEspecifico('win','left')
        clickAtalhoEspecifico('win','left')
    print(f'Menu não reconhecido...')
    verificaErro()
    return MENU_DESCONHECIDO

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
    telaInteira = imagem.retornaAtualizacaoTela()
    textoCarta = imagem.retornaTextoCorrespondenciaReconhecido(telaInteira)
    novaVenda = None
    if variavelExiste(textoCarta):
        produto = verificaVendaProduto(textoCarta)
        if variavelExiste(produto):
            if produto:
                print(f'Produto vendido:')
                listaTextoCarta = textoCarta.split()
                quantidadeProduto = retornaQuantidadeProdutoVendido(listaTextoCarta)
                ouro = imagem.retornaValorDoTrabalhoVendido(telaInteira)
                dataAtual = str(datetime.date.today())
                listaTextoCarta = ' '.join(listaTextoCarta)
                chaveIdTrabalho = ''
                for dicionarioTrabalho in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS]:
                    if texto1PertenceTexto2(dicionarioTrabalho[CHAVE_NOME], listaTextoCarta):
                        chaveIdTrabalho = dicionarioTrabalho[CHAVE_ID]
                        break
                novaVenda = TrabalhoVendido('', listaTextoCarta, dataAtual, dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO][CHAVE_ID], quantidadeProduto, chaveIdTrabalho, ouro)
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
            print(f'Quantidade do trabalho ({trabalhoEstoque.pegaNome()}) atualizada para {novaQuantidade}.')
            break
    else:
        nomeProduto = venda["nomeProduto"]
        print(f'Trabalho ({nomeProduto}) não encontrado no estoque.')

def recuperaCorrespondencia():
    verificaTrabalhoRaroVendido = False
    while imagem.existeCorrespondencia():
        clickEspecifico(1, 'enter')
        venda = retornaConteudoCorrespondencia()
        if variavelExiste(venda):
            verificaTrabalhoRaroVendido = True
            atualizaQuantidadeTrabalhoEstoque(venda)
        clickEspecifico(1,'f2')
    else:
        print(f'Caixa de correio vazia!')
        clickMouseEsquerdo(1, 2, 35)
    return verificaTrabalhoRaroVendido

def reconheceRecuperaTrabalhoConcluido():
    global dicionarioPersonagemAtributos
    erro = verificaErro()
    if not erroEncontrado(erro):
        nomeTrabalhoConcluido = imagem.retornaNomeTrabalhoFrameProducaoReconhecido()
        clickEspecifico(1, 'down')
        clickEspecifico(1, 'f2')
        print(f'  Trabalho concluido reconhecido: {nomeTrabalhoConcluido}.')
        if variavelExiste(nomeTrabalhoConcluido):
            erro = verificaErro()
            if not erroEncontrado(erro):
                if not dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_MODIFICADA]:
                    dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO_MODIFICADA] = True
                clickContinuo(3, 'up')
                return nomeTrabalhoConcluido
            if ehErroEspacoBolsaInsuficiente(erro):
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

def retornaTrabalhoConcluido(nomeTrabalhoConcluido):
    listaPossiveisTrabalhos = retornaListaPossiveisTrabalhoRecuperado(nomeTrabalhoConcluido)
    if not tamanhoIgualZero(listaPossiveisTrabalhos):
        listaDicionariosTrabalhosProduzirProduzindo = repositorioTrabalhoProducao.retornaListaTrabalhosProducaoParaProduzirProduzindo()
        for possivelTrabalho in listaPossiveisTrabalhos:
            for trabalhoProduzirProduzindo in listaDicionariosTrabalhosProduzirProduzindo:
                condicoes = trabalhoProduzirProduzindo.ehProduzindo() and textoEhIgual(trabalhoProduzirProduzindo.pegaNome(), possivelTrabalho.pegaNome())
                if condicoes:
                    trabalhoProduzirProduzindo.setTrabalhoId(possivelTrabalho.pegaId())
                    trabalhoProduzirProduzindo.setNomeProducao(possivelTrabalho.pegaNomeProducao())
                    return trabalhoProduzirProduzindo
        else:
            print(f'Trabalho concluído ({listaPossiveisTrabalhos[0].pegaNome()}) não encontrado na lista produzindo...')
            return TrabalhoProducao('', listaPossiveisTrabalhos[0].pegaId(), listaPossiveisTrabalhos[0].pegaNome(), listaPossiveisTrabalhos[0].pegaNomeProducao(), listaPossiveisTrabalhos[0].pegaExperiencia(), listaPossiveisTrabalhos[0].pegaNivel(), listaPossiveisTrabalhos[0].pegaProfissao(), listaPossiveisTrabalhos[0].pegaRaridade(), listaPossiveisTrabalhos[0].pegaTrabalhoNecessario(), False, CHAVE_LICENCA_INICIANTE, CODIGO_CONCLUIDO)
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
                        trabalhoProducaoRaro = TrabalhoProducao('', trabalho.pegaTrabalhoId(), trabalho.pegaNome(), trabalho.pegaNomeProducao(), experiencia, trabalho.pegaNivel(), trabalho.pegaProfissao(), trabalho.pegaRaridade(), trabalho.pegaTrabalhoNecessario(), False, licencaProducaoIdeal, trabalho.pegaEstado())
                        break
    if variavelExiste(trabalhoProducaoRaro):
        trabalhoProducaoRaroComId = repositorioTrabalhoProducao.adicionaTrabalhoProducao(trabalhoProducaoRaro)
        dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS_PRODUCAO].append(trabalhoProducaoRaroComId)

def retornaListaPersonagemRecompensaRecebida(listaPersonagemPresenteRecuperado):
    if tamanhoIgualZero(listaPersonagemPresenteRecuperado):
        print(f'Limpou a lista...')
        listaPersonagemPresenteRecuperado = []
    nomePersonagemReconhecido = imagem.retornaTextoNomePersonagemReconhecido(0)
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
        referenciaEncontrada = imagem.retornaReferencia()
        if variavelExiste(referenciaEncontrada):
            print(f'Referência encontrada!')
            clickMouseEsquerdo(1,referenciaEncontrada[0],referenciaEncontrada[1])
            posicionaMouseEsquerdo(360,600)
            if verificaErro() != 0:
                evento=2
            clickEspecifico(1,'f2')
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
    erro = verificaErro()
    while erroEncontrado(erro):
        if erro == CODIGO_CONECTANDO:
            if tentativas > 10:
                clickEspecifico(2, 'enter')
                tentativas = 0
            tentativas += 1
        erro = verificaErro()
    else:
        clickEspecifico(1, 'f2')
        if len(listaPersonagemPresenteRecuperado) == 1:
            clickContinuo(8, 'left')
        else:
            clickEspecifico(1, 'right')
        nomePersonagem = imagem.retornaTextoNomePersonagemReconhecido(1)               
        while True:
            nomePersonagemPresenteado = None
            for nomeLista in listaPersonagemPresenteRecuperado:
                if nomePersonagem == nomeLista and nomePersonagem != None:
                    nomePersonagemPresenteado = nomeLista
                    break
            if nomePersonagemPresenteado != None:
                clickEspecifico(1, 'right')
                nomePersonagem = imagem.retornaTextoNomePersonagemReconhecido(1)
            if nomePersonagem == None:
                print(f'Fim da lista de personagens!')
                clickEspecifico(1, 'f1')
                break
            else:
                clickEspecifico(1, 'f2')
                sleep(1)
                tentativas = 1
                erro = verificaErro()
                while erroEncontrado(erro):
                    if erro == CODIGO_RECEBER_RECOMPENSA:
                        break
                    elif erro == CODIGO_CONECTANDO:
                        if tentativas > 10:
                            clickEspecifico(2, 'enter')
                            tentativas = 0
                        tentativas += 1
                    sleep(1.5)
                    erro = verificaErro()
                confirmacao = True
                print(f'Login efetuado com sucesso!')
                break
    return confirmacao

def recebeTodasRecompensas(menu):
    listaPersonagemPresenteRecuperado = retornaListaPersonagemRecompensaRecebida(listaPersonagemPresenteRecuperado = [])
    while True:
        reconheceMenuRecompensa(menu)
        if imagem.existePixelCorrespondencia():
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
        estadoTrabalho = imagem.retornaEstadoTrabalho()
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
                    print(f'Trabalho produção concluido não reconhecido.')
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
    erro = verificaErro()
    if erro == CODIGO_ERRO_OUTRA_CONEXAO:
        dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO] = False
        dicionarioPersonagemAtributos[CHAVE_UNICA_CONEXAO] = False

def vaiParaMenuProduzir():
    global dicionarioPersonagemAtributos
    erro = verificaErro()
    if not erroEncontrado(erro):
        menu = retornaMenu()
        if ehMenuInicial(menu):
            if imagem.existePixelCorrespondencia():
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
        dicionarioPersonagemAtributos[CHAVE_LISTA_VENDAS] = repositorioVendas.pegaTodasVendas()
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

def defineChaveListaDicionariosProfissoesNecessarias():
    global dicionarioPersonagemAtributos
    print(f'Verificando profissões necessárias...')
    dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIOS_PROFISSOES_NECESSARIAS] = []
    posicao = 1
    for profissao in dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO]:
        for trabalhoProducaoDesejado in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS_PRODUCAO]:
            chaveProfissaoEhIgualEEstadoEhParaProduzir = textoEhIgual(profissao.pegaNome(), trabalhoProducaoDesejado.pegaProfissao()) and trabalhoProducaoDesejado.ehParaProduzir()
            if chaveProfissaoEhIgualEEstadoEhParaProduzir:
                dicionarioProfissao = {
                    CHAVE_ID:profissao.pegaId(),
                    CHAVE_NOME:profissao.pegaNome(),
                    CHAVE_PRIORIDADE:profissao.pegaPrioridade(),
                    CHAVE_POSICAO:posicao}
                dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIOS_PROFISSOES_NECESSARIAS].append(dicionarioProfissao)
                break
        posicao+=1
    else:
        dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIOS_PROFISSOES_NECESSARIAS] = sorted(dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIOS_PROFISSOES_NECESSARIAS],key=lambda dicionario:dicionario[CHAVE_PRIORIDADE],reverse=True)

def retornaContadorEspacosProducao(contadorEspacosProducao, nivel):
    contadorNivel = 0
    for dicionarioProfissao in dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO]:
        if dicionarioProfissao.pegaNivel() >= nivel:
            contadorNivel += 1
    else:
        print(f'Contador de profissões nível {nivel} ou superior: {contadorNivel}.')
        if contadorNivel > 0 and contadorNivel < 3:
            contadorEspacosProducao += 1
        elif contadorNivel >= 3:
            contadorEspacosProducao += 2
    return contadorEspacosProducao

def retornaQuantidadeEspacosDeProducao():
    print(f'Define quantidade de espaços de produção...')
    quantidadeEspacosProducao = 2
    for dicionarioProfissao in dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSAO]:
        nivel, _ , _= retornaNivelXpMinimoMaximo(dicionarioProfissao)
        if nivel >= 5:
            quantidadeEspacosProducao += 1
            break
    listaNiveis = [10, 15, 20, 25]
    for nivel in listaNiveis:
        quantidadeEspacosProducao = retornaContadorEspacosProducao(quantidadeEspacosProducao, nivel)
    print(f'Espaços de produção disponíveis: {quantidadeEspacosProducao}.')
    return quantidadeEspacosProducao

def verificaEspacoProducao():
    global dicionarioPersonagemAtributos
    quantidadeEspacoProducao = retornaQuantidadeEspacosDeProducao()
    if dicionarioPersonagemAtributos[CHAVE_ESPACO_PRODUCAO] != quantidadeEspacoProducao:
        dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO].setEspacoProducao(quantidadeEspacoProducao)
        repositorioPersonagem.modificaPersonagem(dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO])

def retornaListaDicionariosTrabalhosProducaoRaridadeEspecifica(dicionarioTrabalho, raridade):
    listaTrabalhosProducaoRaridadeEspecifica = []
    listaTrabalhosProducaoParaProduzirProduzindo = repositorioTrabalhoProducao.retornaListaTrabalhosProducaoParaProduzirProduzindo()
    print(f'Buscando trabalho {raridade} na lista...')
    for trabalhoProducao in listaTrabalhosProducaoParaProduzirProduzindo:
        raridadeEhIgualProfissaoEhIgualEstadoEhParaProduzir = textoEhIgual(trabalhoProducao.pegaRaridade(), raridade) and textoEhIgual(trabalhoProducao.pegaProfissao(), dicionarioTrabalho[CHAVE_PROFISSAO]) and trabalhoProducao.ehParaProduzir()
        if raridadeEhIgualProfissaoEhIgualEstadoEhParaProduzir:
            for trabalhoProducaoRaridadeEspecifica in listaTrabalhosProducaoRaridadeEspecifica:
                if textoEhIgual(trabalhoProducaoRaridadeEspecifica.pegaNome(), trabalhoProducao.pegaNome()):
                    break
            else:
                print(f'Trabalho {raridade} encontado: {trabalhoProducao.pegaNome()}')
                listaTrabalhosProducaoRaridadeEspecifica.append(trabalhoProducao)
    if tamanhoIgualZero(listaTrabalhosProducaoRaridadeEspecifica):
        print(f'Nem um trabaho {raridade} na lista!')
    return listaTrabalhosProducaoRaridadeEspecifica

def retornaNomeTrabalhoPosicaoTrabalhoRaroEspecial(dicionarioTrabalho):
    return imagem.retornaNomeTrabalhoReconhecido((dicionarioTrabalho[CHAVE_POSICAO] * 72) + 289, 0)

def retornaFrameTelaTrabalhoEspecifico():
    clickEspecifico(1, 'down')
    clickEspecifico(1, 'enter')
    nomeTrabalhoReconhecido = imagem.retornaNomeConfirmacaoTrabalhoProducaoReconhecido(0)
    clickEspecifico(1, 'f1')
    clickEspecifico(1, 'up')
    return nomeTrabalhoReconhecido

def confirmaNomeTrabalhoProducao(dicionarioTrabalho, tipoTrabalho):
    print(f'Confirmando nome do trabalho...')
    dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = None
    if tipoTrabalho == 0:
        nomeTrabalhoReconhecido = retornaFrameTelaTrabalhoEspecifico()
    else:
        nomeTrabalhoReconhecido = imagem.retornaNomeConfirmacaoTrabalhoProducaoReconhecido(tipoTrabalho)
    if variavelExiste(nomeTrabalhoReconhecido) and CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA in dicionarioTrabalho:
        if len(nomeTrabalhoReconhecido) >= 30:
            nomeTrabalhoReconhecido = nomeTrabalhoReconhecido[:29]
        for trabalhoProducaoPriorizada in dicionarioTrabalho[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA]:
            if trabalhoProducaoPriorizada.pegaNomeProducao():
                nomeTrabalhoProducaoDesejado = trabalhoProducaoPriorizada.pegaNome().replace('-','')
                nomeProducaoTrabalhoProducaoDesejado = trabalhoProducaoPriorizada.pegaNomeProducao().replace('-','')
                if len(trabalhoProducaoPriorizada.pegaNome()) >= 30:
                    nomeTrabalhoProducaoDesejado = nomeTrabalhoProducaoDesejado[:29]
                if len(trabalhoProducaoPriorizada.pegaNomeProducao()) >= 30:
                    nomeProducaoTrabalhoProducaoDesejado = nomeProducaoTrabalhoProducaoDesejado[:29]
                if trabalhoEhProducaoRecursos(trabalhoProducaoPriorizada):
                    if texto1PertenceTexto2(nomeTrabalhoReconhecido, nomeProducaoTrabalhoProducaoDesejado):
                        dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = trabalhoProducaoPriorizada
                        print(f'Trabalho confirmado: {nomeTrabalhoReconhecido}')
                        return dicionarioTrabalho
                else:
                    if textoEhIgual(nomeTrabalhoReconhecido, nomeTrabalhoProducaoDesejado) or textoEhIgual(nomeTrabalhoReconhecido, nomeProducaoTrabalhoProducaoDesejado):
                        dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = trabalhoProducaoPriorizada
                        print(f'Trabalho confirmado: {nomeTrabalhoReconhecido}')
                        return dicionarioTrabalho
        else:
            print(f'Trabalho negado: {nomeTrabalhoReconhecido}')
    return dicionarioTrabalho

def incrementaChavePosicaoTrabalho(dicionarioTrabalho):
    dicionarioTrabalho[CHAVE_POSICAO] += 1
    return dicionarioTrabalho

def defineDicionarioTrabalhoComumMelhorado(dicionarioTrabalho):
    nomeTrabalhoReconhecidoAux = ''
    nomeTrabalhoReconhecido = ''
    print(f'Buscando trabalho {dicionarioTrabalho[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA][0].pegaRaridade()}.')
    contadorParaBaixo = 0
    if not primeiraBusca(dicionarioTrabalho):
        contadorParaBaixo = dicionarioTrabalho[CHAVE_POSICAO]
        clickEspecifico(contadorParaBaixo, 'down')
    while not chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
        erro = verificaErro(dicionarioTrabalho)
        if erroEncontrado(erro):
            dicionarioTrabalho[CHAVE_CONFIRMACAO] = False
            break
        if primeiraBusca(dicionarioTrabalho):
            clicks = 3
            contadorParaBaixo = 3
            clickEspecifico(clicks, 'down')
            yinicialNome = (2 * 70) + 285
            nomeTrabalhoReconhecido = imagem.retornaNomeTrabalhoReconhecido(yinicialNome, 1)
        elif contadorParaBaixo == 3:
            yinicialNome = (2 * 70) + 285
            nomeTrabalhoReconhecido = imagem.retornaNomeTrabalhoReconhecido(yinicialNome, 1)
        elif contadorParaBaixo == 4:
            yinicialNome = (3 * 70) + 285
            nomeTrabalhoReconhecido = imagem.retornaNomeTrabalhoReconhecido(yinicialNome, 1)
        elif contadorParaBaixo > 4:
            nomeTrabalhoReconhecido = imagem.retornaNomeTrabalhoReconhecido(530, 1)
        nomeReconhecidoNaoEstaVazioEnomeReconhecidoNaoEhIgualAoAnterior = (
            variavelExiste(nomeTrabalhoReconhecido) and not textoEhIgual(nomeTrabalhoReconhecido, nomeTrabalhoReconhecidoAux))
        if nomeReconhecidoNaoEstaVazioEnomeReconhecidoNaoEhIgualAoAnterior:
            nomeTrabalhoReconhecidoAux = nomeTrabalhoReconhecido
            print(f'Trabalho reconhecido: {nomeTrabalhoReconhecido}')
            for trabalhoProducao in dicionarioTrabalho[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA]:
                print(f'Trabalho na lista: {trabalhoProducao.pegaNome()}')
                if texto1PertenceTexto2(nomeTrabalhoReconhecido, trabalhoProducao.pegaNomeProducao()):
                    clickEspecifico(1, 'enter')
                    dicionarioTrabalho[CHAVE_POSICAO] = contadorParaBaixo
                    dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = trabalhoProducao
                    contadorParaBaixo += 1
                    tipoTrabalho = 0
                    if trabalhoEhProducaoRecursos(dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO]):
                        tipoTrabalho = 1
                    dicionarioTrabalho = confirmaNomeTrabalhoProducao(dicionarioTrabalho, tipoTrabalho)
                    if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
                        break
                    else:
                        clickEspecifico(1, 'f1')
            else:
                clickEspecifico(1, 'down')
                dicionarioTrabalho[CHAVE_POSICAO] = contadorParaBaixo
                contadorParaBaixo += 1
        else:
            if not primeiraBusca(dicionarioTrabalho) and dicionarioTrabalho[CHAVE_POSICAO] > 5:
                print(f'Trabalho {dicionarioTrabalho[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA][0].pegaRaridade()} não reconhecido!')
                break
            else:
                clickEspecifico(1, 'down')
                dicionarioTrabalho[CHAVE_POSICAO] = contadorParaBaixo
                contadorParaBaixo += 1
    return dicionarioTrabalho

def defineCloneDicionarioTrabalhoDesejado(trabalhoProducaoEncontrado):
    return TrabalhoProducao('', trabalhoProducaoEncontrado.pegaTrabalhoId(),trabalhoProducaoEncontrado.pegaNome(), trabalhoProducaoEncontrado.pegaNomeProducao(), trabalhoProducaoEncontrado.pegaExperiencia(), trabalhoProducaoEncontrado.pegaNivel(), trabalhoProducaoEncontrado.pegaProfissao(), trabalhoProducaoEncontrado.pegaRaridade(), trabalhoProducaoEncontrado.pegaTrabalhoNecessario(), trabalhoProducaoEncontrado.pegaRecorrencia(), trabalhoProducaoEncontrado.pegaLinceca(), trabalhoProducaoEncontrado.pegaEstado())

def clonaTrabalhoProducaoEncontrado(dicionarioTrabalho, trabalhoProducaoEncontrado):
    global dicionarioPersonagemAtributos
    print(f'Recorrencia está ligada.')
    cloneTrabalhoProducaoEncontrado = defineCloneDicionarioTrabalhoDesejado(trabalhoProducaoEncontrado)
    trabalhoProducaoAdicionado = repositorioTrabalhoProducao.adicionaTrabalhoProducao(cloneTrabalhoProducaoEncontrado)
    dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS_PRODUCAO].append(trabalhoProducaoAdicionado)
    dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = trabalhoProducaoAdicionado

def retornaChaveTipoRecurso(dicionarioRecurso):
    listaDicionarioProfissaoRecursos = retornaListaDicionarioProfissaoRecursos(dicionarioRecurso[CHAVE_NIVEL])
    chaveProfissao = limpaRuidoTexto(dicionarioRecurso[CHAVE_PROFISSAO])
    for dicionarioProfissaoRecursos in listaDicionarioProfissaoRecursos:
        if chaveProfissao in dicionarioProfissaoRecursos:
            for x in range(len(dicionarioProfissaoRecursos[chaveProfissao])):
                if textoEhIgual(dicionarioProfissaoRecursos[chaveProfissao][x],dicionarioRecurso[CHAVE_NOME]):
                    if x == 0 and dicionarioRecurso[CHAVE_NIVEL] == 1:
                        return CHAVE_RCP
                    elif x == 0 and dicionarioRecurso[CHAVE_NIVEL] == 8:
                        return CHAVE_RAP
                    elif x == 1 and dicionarioRecurso[CHAVE_NIVEL] == 1:
                        return CHAVE_RCS
                    elif x == 1 and dicionarioRecurso[CHAVE_NIVEL] == 8:
                        return CHAVE_RAS
                    elif x == 2 and dicionarioRecurso[CHAVE_NIVEL] == 1:
                        return CHAVE_RCT
                    elif x == 2 and dicionarioRecurso[CHAVE_NIVEL] == 8:
                        return CHAVE_RAT
                    break
    return None

def retornaNomesRecursos(chaveProfissao, nivelRecurso):
    nomeRecursoPrimario = None
    nomeRecursoSecundario = None
    nomeRecursoTerciario = None
    listaDicionarioProfissao = retornaListaDicionarioProfissaoRecursos(nivelRecurso)
    if not tamanhoIgualZero(listaDicionarioProfissao):
        for dicionarioProfissao in listaDicionarioProfissao:
            if chaveProfissao in dicionarioProfissao:
                nomeRecursoPrimario = dicionarioProfissao[chaveProfissao][0]
                nomeRecursoSecundario = dicionarioProfissao[chaveProfissao][1]
                nomeRecursoTerciario = dicionarioProfissao[chaveProfissao][2]
                break
    return nomeRecursoPrimario, nomeRecursoSecundario, nomeRecursoTerciario

def retornaTrabalhoRecurso(trabalhoProducao):
    print(f'Define quantidade de recursos.')
    nivelTrabalhoProducao = trabalhoProducao.pegaNivel()
    nivelRecurso = 1
    recursoTerciario = 0
    if textoEhIgual(trabalhoProducao.pegaProfissao(), CHAVE_PROFISSAO_ARMA_DE_LONGO_ALCANCE):
        recursoTerciario = 1
    if nivelTrabalhoProducao <= 14:
        if nivelTrabalhoProducao == 10:
            recursoTerciario += 2
        elif nivelTrabalhoProducao == 12:
            recursoTerciario += 4
        elif nivelTrabalhoProducao == 14:
            recursoTerciario += 6
    else:
        nivelRecurso = 8
        if nivelTrabalhoProducao == 16:
            recursoTerciario += 2
        elif nivelTrabalhoProducao == 18:
            recursoTerciario += 4
        elif nivelTrabalhoProducao == 20:
            recursoTerciario += 6
        elif nivelTrabalhoProducao == 22:
            recursoTerciario += 8
        elif nivelTrabalhoProducao == 24:
            recursoTerciario += 10
        elif nivelTrabalhoProducao == 26:
            recursoTerciario += 12
        elif nivelTrabalhoProducao == 28:
            recursoTerciario += 14
        elif nivelTrabalhoProducao == 30:
            recursoTerciario += 16
        elif nivelTrabalhoProducao == 32:
            recursoTerciario += 18
    chaveProfissao = limpaRuidoTexto(trabalhoProducao.pegaProfissao())
    nomeRecursoPrimario, nomeRecursoSecundario, nomeRecursoTerciario = retornaNomesRecursos(chaveProfissao, nivelRecurso)
    return TrabalhoRecurso(trabalhoProducao.pegaProfissao(), trabalhoProducao.pegaNivel(), nomeRecursoTerciario, nomeRecursoSecundario, nomeRecursoPrimario, recursoTerciario)

def removeTrabalhoEstoque(trabalhoProducao):
    if not tamanhoIgualZero(dicionarioPersonagemAtributos[CHAVE_LISTA_ESTOQUE]):
        if trabalhoProducao.ehComum():
            if trabalhoEhProducaoRecursos(trabalhoProducao):
                print(f'Trabalho é recurso de produção!')
                print(f'Nome recurso produzido: {trabalhoProducao.pegaNome()}')
                dicionarioRecurso = {
                    CHAVE_NOME:trabalhoProducao.pegaNome(),
                    CHAVE_PROFISSAO:trabalhoProducao.pegaProfissao(),
                    CHAVE_NIVEL:trabalhoProducao.pegaNivel()}
                dicionarioRecurso[CHAVE_TIPO] = retornaChaveTipoRecurso(dicionarioRecurso)
                print(f'Dicionário recurso reconhecido:')
                for atributo in dicionarioRecurso:
                    print(f'{atributo} - {dicionarioRecurso[atributo]}')
                chaveProfissao = limpaRuidoTexto(dicionarioRecurso[CHAVE_PROFISSAO])
                nomeRecursoPrimario, nomeRecursoSecundario, nomeRecursoTerciario = retornaNomesRecursos(chaveProfissao, 1)
                listaNomeRecursoBuscado = []
                if dicionarioRecurso[CHAVE_TIPO] == CHAVE_RCS:
                    listaNomeRecursoBuscado.append([nomeRecursoPrimario, 2])
                elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RCT:
                    listaNomeRecursoBuscado.append([nomeRecursoPrimario, 3])
                elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAP:
                    listaNomeRecursoBuscado.append([nomeRecursoPrimario, 6])
                elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAS:
                    listaNomeRecursoBuscado.append([nomeRecursoPrimario, 7])
                    listaNomeRecursoBuscado.append([nomeRecursoSecundario, 2])
                elif dicionarioRecurso[CHAVE_TIPO] == CHAVE_RAT:
                    listaNomeRecursoBuscado.append([nomeRecursoPrimario, 8])
                    listaNomeRecursoBuscado.append([nomeRecursoTerciario, 2])
                for trabalhoEstoque in dicionarioPersonagemAtributos[CHAVE_LISTA_ESTOQUE]:
                    for recursoBuscado in listaNomeRecursoBuscado:
                        if textoEhIgual(trabalhoEstoque.pegaNome(), recursoBuscado[0]):
                            novaQuantidade = trabalhoEstoque.pegaQuantidade() - recursoBuscado[1]
                            if novaQuantidade < 0:
                                novaQuantidade = 0
                            print(f'Quantidade de {trabalhoEstoque.pegaNome()} atualizada de {trabalhoEstoque.pegaQuantidade()} para {novaQuantidade}.')
                            trabalhoEstoque.setQuantidade(novaQuantidade)
                            repositorioEstoque.modificaTrabalhoEstoque(trabalhoEstoque)
                    if textoEhIgual(trabalhoEstoque.pegaNome(), trabalhoProducao.pegaLicenca()):
                        novaQuantidade = trabalhoEstoque.pegaQuantidade() - 1
                        if novaQuantidade < 0:
                            novaQuantidade = 0
                        print(f'Quantidade de {trabalhoEstoque.pegaNome()} atualizada de {trabalhoEstoque.pegaQuantidade()} para {novaQuantidade}.')
                        trabalhoEstoque.setQuantidade(novaQuantidade)
                        repositorioEstoque.modificaTrabalhoEstoque(trabalhoEstoque)
            else:
                trabalhoRecurso = retornaTrabalhoRecurso(trabalhoProducao)
                for trabalhoEstoque in dicionarioPersonagemAtributos[CHAVE_LISTA_ESTOQUE]:
                    novaQuantidade = None
                    if textoEhIgual(trabalhoEstoque.pegaNome(), trabalhoRecurso.pegaPrimario()):
                        novaQuantidade = trabalhoEstoque.pegaQuantidade() - trabalhoRecurso.pegaQuantidadePrimario()
                        if novaQuantidade < 0:
                            novaQuantidade = 0
                    elif textoEhIgual(trabalhoEstoque.pegaNome(), trabalhoRecurso.pegaSecundario()):
                        novaQuantidade = trabalhoEstoque.pegaQuantidade() - trabalhoRecurso.pegaQuantidadeSecundario()
                        if novaQuantidade < 0:
                            novaQuantidade = 0
                    elif textoEhIgual(trabalhoEstoque.pegaNome(), trabalhoRecurso.pegaTerciario()):
                        novaQuantidade = trabalhoEstoque.pegaQuantidade() - trabalhoRecurso.pegaQuantidadeTerciario()
                        if novaQuantidade < 0:
                            novaQuantidade = 0
                    elif textoEhIgual(trabalhoEstoque.pegaNome(), trabalhoRecurso.pegaLicenca()):
                        novaQuantidade = trabalhoEstoque.pegaQuantidade() - 1
                        if novaQuantidade < 0:
                            novaQuantidade = 0
                    if variavelExiste(novaQuantidade):
                        print(f'Quantidade de {trabalhoEstoque.pegaNome()} atualizada para {novaQuantidade}.')
                        trabalhoEstoque.setQuantidade(novaQuantidade)
                        repositorioEstoque.modificaTrabalhoEstoque(trabalhoEstoque)
        elif trabalhoProducao.ehMelhorado() or trabalhoProducao.ehRaro():
            if not trabalhoEhProducaoRecursos(trabalhoProducao):
                listaTrabalhosNecessarios = trabalhoProducao.pegaTrabalhoNecessario().split(',')
                for trabalhoNecessario in listaTrabalhosNecessarios:
                    for trabalhoEstoque in dicionarioPersonagemAtributos[CHAVE_LISTA_ESTOQUE]:
                        if textoEhIgual(trabalhoNecessario, trabalhoEstoque.pegaNome()):
                            novaQuantidade = trabalhoEstoque.pegaQuantidade() - 1
                            if novaQuantidade < 0:
                                novaQuantidade = 0
                            print(f'Quantidade de {trabalhoEstoque.pegaNome()} atualizada para {novaQuantidade}.')
                            trabalhoEstoque.setQuantidade(novaQuantidade)
                            repositorioEstoque.modificaTrabalhoEstoque(trabalhoEstoque)
                            break
    else:
        print(f'Lista de estoque está vazia!')
        
def iniciaProcessoDeProducao(dicionarioTrabalho):
    global dicionarioPersonagemAtributos
    primeiraBusca = True
    trabalhoProducaoEncontrado = dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO]
    while True:
        menu = retornaMenu()
        if menuTrabalhosAtuaisReconhecido(menu):
            if not tamanhoIgualZero(trabalhoProducaoEncontrado):
                if trabalhoProducaoEncontrado.ehRecorrente():
                    clonaTrabalhoProducaoEncontrado(dicionarioTrabalho, trabalhoProducaoEncontrado)
                else:
                    repositorioTrabalhoProducao.modificaTrabalhoProducao(trabalhoProducaoEncontrado)
                removeTrabalhoEstoque(trabalhoProducaoEncontrado)
                clickContinuo(12,'up')
                dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO] = True
                break
            else:
                print(f'Dicionário trabalho desejado está vazio!')
                break
        elif menuTrabalhoEspecificoReconhecido(menu):
            if primeiraBusca:
                print(f'Entra menu licença.')
                clickEspecifico(1, 'up')
                clickEspecifico(1, 'enter')
            else:
                print(f'Clica f2.')
                clickEspecifico(1, 'f2')
        elif menuLicencasReconhecido(menu):
            print(f"Buscando: {trabalhoProducaoEncontrado.pegaLicenca()}")
            textoReconhecido = imagem.retornaTextoLicencaReconhecida()
            if variavelExiste(textoReconhecido):
                print(f'Licença reconhecida: {textoReconhecido}.')
                if not texto1PertenceTexto2('licençasdeproduçao', textoReconhecido):
                    primeiraBusca = True
                    listaCiclo = []
                    while not texto1PertenceTexto2(textoReconhecido, trabalhoProducaoEncontrado.pegaLicenca()):
                        listaCiclo.append(textoReconhecido)
                        clickEspecifico(1, "right")
                        textoReconhecido = imagem.retornaTextoLicencaReconhecida()
                        if variavelExiste(textoReconhecido):
                            print(f'Licença reconhecida: {textoReconhecido}.')
                            if textoEhIgual(textoReconhecido, 'nenhumitem'):
                                if textoEhIgual(trabalhoProducaoEncontrado.pegaLicenca(), CHAVE_LICENCA_INICIANTE):
                                    if not textoEhIgual(listaCiclo[-1], 'nenhumitem'):
                                        print(f'Sem licenças de produção...')
                                        dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO].setEstado(False)
                                        repositorioPersonagem.modificaPersonagem(dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO])
                                        clickEspecifico(3, 'f1')
                                        clickContinuo(10, 'up')
                                        clickEspecifico(1, 'left')
                                        break
                                else:
                                    print(f'{trabalhoProducaoEncontrado.pegaLicenca()} não encontrado!')
                                    print(f'Licença buscada agora é Licença de produção do iniciante!')
                                    trabalhoProducaoEncontrado.setLicenca(CHAVE_LICENCA_INICIANTE)
                                    dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = trabalhoProducaoEncontrado
                            else:
                                if len(listaCiclo) > 10:
                                    print(f'{trabalhoProducaoEncontrado.pegaLicenca()} não encontrado!')
                                    print(f'Licença buscada agora é Licença de produção do iniciante!')
                                    trabalhoProducaoEncontrado.setLicenca(CHAVE_LICENCA_INICIANTE)
                                    dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = trabalhoProducaoEncontrado          
                        else:
                            erro = verificaErro()
                            if ehErroOutraConexao(erro):
                                dicionarioPersonagemAtributos[CHAVE_UNICA_CONEXAO] = False
                            print(f'Erro ao reconhecer licença!')
                            break
                        primeiraBusca = False
                    else:
                        if primeiraBusca:
                            clickEspecifico(1, "f1")
                        else:
                            clickEspecifico(1, "f2")
                else:
                    print(f'Sem licenças de produção...')
                    dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO].setEstado(False)
                    repositorioPersonagem.modificaPersonagem(dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO])
                    clickEspecifico(3, 'f1')
                    clickContinuo(10, 'up')
                    clickEspecifico(1, 'left')
                    break
            else:
                print(f'Erro ao reconhecer licença!')
                
                break
        elif menuEscolhaEquipamentoReconhecido(menu) or menuAtributosEquipamentoReconhecido(menu):
            print(f'Clica f2.')
            clickEspecifico(1, 'f2')
        else:
            break
        print(f'Tratando possíveis erros...')
        dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO] = True
        tentativas = 1
        erro = verificaErro(trabalhoProducaoEncontrado)
        while erroEncontrado(erro):
            if ehErroRecursosInsuficiente(erro):
                repositorioTrabalhoProducao.removeTrabalhoProducao(trabalhoProducaoEncontrado)
                posicao = 0
                for trabalhoProducao in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS_PRODUCAO]:
                    if textoEhIgual(trabalhoProducao.pegaId(), trabalhoProducaoEncontrado.pegaId()):
                        del dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS_PRODUCAO][posicao]
                        break
                    posicao += 1
                dicionarioTrabalho[CHAVE_CONFIRMACAO] = False
            elif ehErroEspacoProducaoInsuficiente(erro) or ehErroOutraConexao(erro) or ehErroConectando(erro) or ehErroRestauraConexao(erro):
                dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO] = False
                dicionarioTrabalho[CHAVE_CONFIRMACAO] = False
                if ehErroOutraConexao(erro):
                    dicionarioPersonagemAtributos[CHAVE_UNICA_CONEXAO] = False
                elif ehErroConectando(erro):
                    if tentativas > 10:
                        clickEspecifico(1, 'enter')
                        tentativas = 0
                    tentativas+=1
            erro = verificaErro(trabalhoProducaoEncontrado)
        if not chaveConfirmacaoEhVerdadeira(dicionarioTrabalho):
            break
        primeiraBusca = False
    return dicionarioTrabalho

def retornaListaPossiveisTrabalhos(nomeTrabalhoConcluido):
    listaPossiveisTrabalhos = []
    for trabalho in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS]:
        if texto1PertenceTexto2(nomeTrabalhoConcluido[1:-1], trabalho.pegaNomeProducao()):
            trabalhoEncontrado = TrabalhoProducao('', trabalho.pegaId(), trabalho.pegaNome(), trabalho.pegaNomeProducao(), trabalho.pegaExperiencia(), trabalho.pegaNivel(), trabalho.pegaProfissao(), trabalho.pegaRaridade(), trabalho.pegaTrabalhoNecessario(), False, CHAVE_LICENCA_INICIANTE, CODIGO_CONCLUIDO)
            listaPossiveisTrabalhos.append(trabalhoEncontrado)
    return listaPossiveisTrabalhos

def retornaTrabalhoProducaoConcluido(nomeTrabalhoConcluido):
    listaPossiveisTrabalhosProducao = retornaListaPossiveisTrabalhos(nomeTrabalhoConcluido)
    if not tamanhoIgualZero(listaPossiveisTrabalhosProducao):
        listaTrabalhosProducaoProduzirProduzindo = repositorioTrabalhoProducao.retornaListaTrabalhosProducaoParaProduzirProduzindo()
        for possivelTrabalhoProducao in listaPossiveisTrabalhosProducao:
            for dicionarioTrabalhoProduzirProduzindo in listaTrabalhosProducaoProduzirProduzindo:
                condicoes = dicionarioTrabalhoProduzirProduzindo.ehProduzindo() and textoEhIgual(dicionarioTrabalhoProduzirProduzindo.pegaNome(), possivelTrabalhoProducao.pegaNome())
                if condicoes:
                    return dicionarioTrabalhoProduzirProduzindo
        else:
            print(f'Trabalho concluído ({listaPossiveisTrabalhosProducao[0].pegaNome()}) não encontrado na lista produzindo...')
            return listaPossiveisTrabalhosProducao[0]
    return None

def iniciaBuscaTrabalho(dicionarioTrabalho):
    global dicionarioPersonagemAtributos
    defineChaveListaDicionariosProfissoesNecessarias()
    indiceProfissao = 0
    dicionarioTrabalho[CHAVE_POSICAO] = -1
    while indiceProfissao < len(dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIOS_PROFISSOES_NECESSARIAS]):
        if vaiParaMenuProduzir():
            dicionarioProfissaoNecessaria = dicionarioPersonagemAtributos[CHAVE_LISTA_DICIONARIOS_PROFISSOES_NECESSARIAS][indiceProfissao]
            if not chaveConfirmacaoEhVerdadeira(dicionarioPersonagemAtributos) or not chaveUnicaConexaoEhVerdadeira(dicionarioPersonagemAtributos):
                break
            elif not existeEspacoProducao(dicionarioPersonagemAtributos):
                indiceProfissao += 1
                continue
            if listaProfissoesFoiModificada(dicionarioPersonagemAtributos):
                verificaEspacoProducao()
            entraProfissaoEspecifica(dicionarioProfissaoNecessaria)
            print(f'Verificando profissão: {dicionarioProfissaoNecessaria[CHAVE_NOME]}')
            dicionarioTrabalho[CHAVE_PROFISSAO] = dicionarioProfissaoNecessaria[CHAVE_NOME]
            dicionarioTrabalho[CHAVE_CONFIRMACAO] = True
            listaDeListasTrabalhosProducao = retornaListaDeListasTrabalhosProducao(dicionarioTrabalho)
            indiceLista = 0
            for listaTrabalhosProducao in listaDeListasTrabalhosProducao:
                dicionarioTrabalho[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA] = listaTrabalhosProducao
                for trabalhoProducaoPriorizado in dicionarioTrabalho[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA]:
                    if trabalhoProducaoPriorizado.ehEspecial() or trabalhoProducaoPriorizado.ehRaro():
                        print(f'Trabalho desejado: {trabalhoProducaoPriorizado.pegaNome()}.')
                        posicaoAux = -1
                        if dicionarioTrabalho[CHAVE_POSICAO] != -1:
                            posicaoAux = dicionarioTrabalho[CHAVE_POSICAO]
                        dicionarioTrabalho[CHAVE_POSICAO] = 0
                        while naoFizerQuatroVerificacoes(dicionarioTrabalho) and not chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
                            nomeTrabalhoReconhecido = retornaNomeTrabalhoPosicaoTrabalhoRaroEspecial(dicionarioTrabalho)
                            print(f'Trabalho {trabalhoProducaoPriorizado.pegaRaridade()} reconhecido: {nomeTrabalhoReconhecido}.')
                            if variavelExiste(nomeTrabalhoReconhecido):
                                if texto1PertenceTexto2(nomeTrabalhoReconhecido, trabalhoProducaoPriorizado.pegaNomeProducao()):
                                    dicionarioTrabalho[CHAVE_CONFIRMACAO] = True
                                    erro = verificaErro()
                                    if erroEncontrado(erro):
                                        if ehErroOutraConexao(erro) or ehErroConectando(erro) or ehErroRestauraConexao(erro):
                                            dicionarioTrabalho[CHAVE_CONFIRMACAO] = False
                                            if ehErroOutraConexao(erro):
                                                dicionarioTrabalho[CHAVE_UNICA_CONEXAO] = False
                                    else:
                                        entraTrabalhoEncontrado(dicionarioTrabalho)
                                    if chaveConfirmacaoEhVerdadeira(dicionarioTrabalho):
                                        dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = trabalhoProducaoPriorizado
                                        tipoTrabalho = 0
                                        if trabalhoEhProducaoRecursos(dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO]):
                                            tipoTrabalho = 1
                                        dicionarioTrabalho = confirmaNomeTrabalhoProducao(dicionarioTrabalho, tipoTrabalho)
                                        if not chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
                                            clickEspecifico(1,'f1')
                                            clickContinuo(dicionarioTrabalho[CHAVE_POSICAO] + 1, 'up')
                                    else:
                                        break
                            else:
                                dicionarioTrabalho[CHAVE_POSICAO] = 4
                            dicionarioTrabalho = incrementaChavePosicaoTrabalho(dicionarioTrabalho)
                        dicionarioTrabalho[CHAVE_POSICAO] = posicaoAux
                        if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not chaveConfirmacaoEhVerdadeira(dicionarioTrabalho):
                            break
                    elif trabalhoProducaoPriorizado.ehMelhorado() or trabalhoProducaoPriorizado.ehComum():
                        dicionarioTrabalho = defineDicionarioTrabalhoComumMelhorado(dicionarioTrabalho)
                        dicionarioPersonagemAtributos[CHAVE_CONFIRMACAO] = dicionarioTrabalho[CHAVE_CONFIRMACAO]
                        if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not chaveConfirmacaoEhVerdadeira(dicionarioTrabalho):
                            break
                        elif indiceLista + 1 >= len(listaDeListasTrabalhosProducao):
                            vaiParaMenuTrabalhoEmProducao()
                        else:
                            vaiParaOTopoDaListaDeTrabalhosComunsEMelhorados(dicionarioTrabalho)
                    if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not chaveConfirmacaoEhVerdadeira(dicionarioTrabalho):
                        break
                if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not chaveConfirmacaoEhVerdadeira(dicionarioTrabalho):
                    break
                else:
                    indiceLista += 1
                    dicionarioTrabalho[CHAVE_POSICAO] = -1
            if chaveConfirmacaoEhVerdadeira(dicionarioPersonagemAtributos):
                if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
                    dicionarioTrabalho = iniciaProcessoDeProducao(dicionarioTrabalho)
                else:
                    saiProfissaoVerificada(dicionarioTrabalho)
                    indiceProfissao += 1
                    dicionarioTrabalho[CHAVE_POSICAO] = -1
                if chaveUnicaConexaoEhVerdadeira(dicionarioPersonagemAtributos):
                    if chaveEspacoBolsaForVerdadeira(dicionarioPersonagemAtributos):
                        if imagem.retornaEstadoTrabalho() == CODIGO_CONCLUIDO:
                            nomeTrabalhoConcluido = reconheceRecuperaTrabalhoConcluido()
                            if variavelExiste(nomeTrabalhoConcluido):
                                trabalhoProducaoConcluido = retornaTrabalhoProducaoConcluido(nomeTrabalhoConcluido)
                                if variavelExiste(trabalhoProducaoConcluido):
                                    trabalhoProducaoConcluido = modificaTrabalhoConcluidoListaProduzirProduzindo(trabalhoProducaoConcluido)
                                    modificaExperienciaProfissao(trabalhoProducaoConcluido)
                                    atualizaEstoquePersonagem(trabalhoProducaoConcluido)
                                    verificaProducaoTrabalhoRaro(trabalhoProducaoConcluido)
                                else:
                                    print(f'Dicionário trabalho concluido não reconhecido.')
                            else:
                                print(f'Dicionário trabalho concluido não reconhecido.')
                        elif not existeEspacoProducao(dicionarioPersonagemAtributos):
                            break
                    dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = None
                    clickContinuo(3,'up')
                    clickEspecifico(1,'left')
                    sleep(1.5)
        else:
            break
    else:
        if listaProfissoesFoiModificada(dicionarioPersonagemAtributos):
            verificaEspacoProducao()
        print(f'Fim da lista de profissões...')

def retornaListaDeListasTrabalhosProducao(dicionarioTrabalho):
    listaDeListaTrabalhos = []
    listaTrabalhoProducaoEspecial = retornaListaDicionariosTrabalhosProducaoRaridadeEspecifica(dicionarioTrabalho, raridade = CHAVE_RARIDADE_ESPECIAL)
    if not tamanhoIgualZero(listaTrabalhoProducaoEspecial):
        listaTrabalhoProducaoEspecial = sorted(listaTrabalhoProducaoEspecial,key=lambda dicionario:dicionario[CHAVE_NOME])
        listaDeListaTrabalhos.append(listaTrabalhoProducaoEspecial)
    listaTrabalhosProducaoRaros = retornaListaDicionariosTrabalhosProducaoRaridadeEspecifica(dicionarioTrabalho, raridade = CHAVE_RARIDADE_RARO)
    if not tamanhoIgualZero(listaTrabalhosProducaoRaros):
        listaTrabalhosProducaoRaros = sorted(listaTrabalhosProducaoRaros,key=lambda trabalhoProducao:trabalhoProducao.pegaNome())
        listaDeListaTrabalhos.append(listaTrabalhosProducaoRaros)
    listaTrabalhosProducaoMelhorados = retornaListaDicionariosTrabalhosProducaoRaridadeEspecifica(dicionarioTrabalho, raridade = CHAVE_RARIDADE_MELHORADO)
    if not tamanhoIgualZero(listaTrabalhosProducaoMelhorados):
        listaTrabalhosProducaoMelhorados = sorted(listaTrabalhosProducaoMelhorados,key=lambda trabalhoProducao:trabalhoProducao.pegaNome())
        listaDeListaTrabalhos.append(listaTrabalhosProducaoMelhorados)
    listaTrabalhosProducaoComuns = retornaListaDicionariosTrabalhosProducaoRaridadeEspecifica(dicionarioTrabalho, raridade = CHAVE_RARIDADE_COMUM)
    if not tamanhoIgualZero(listaTrabalhosProducaoComuns):
        listaTrabalhosProducaoComuns = sorted(listaTrabalhosProducaoComuns,key=lambda trabalhoProducao:trabalhoProducao.pegaNome())
        listaDeListaTrabalhos.append(listaTrabalhosProducaoComuns)
    return listaDeListaTrabalhos

def retiraDicionarioPersonagemListaAtivo():
    defineChaveListaPersonagensAtivos()
    novaListaPersonagensAtivos = []
    for personagemAtivo in dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM_ATIVO]:
        for personagemRemovido in dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM_RETIRADO]:
            if textoEhIgual(personagemAtivo.pegaNome(),personagemRemovido.pegaNome()):
                break
        else:
            novaListaPersonagensAtivos.append(personagemAtivo)
    dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM_ATIVO] = novaListaPersonagensAtivos

def logaContaPersonagem():
    confirmacao=False
    email=dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM_ATIVO][0].pegaEmail()
    senha=dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM_ATIVO][0].pegaSenha()
    print(f'Tentando logar conta personagem...')
    preencheCamposLogin(email,senha)
    tentativas=1
    erro=verificaErro()
    while erroEncontrado(erro):
        if erro==CODIGO_CONECTANDO or erro==CODIGO_RESTAURA_CONEXAO:
            if tentativas>10:
                clickEspecifico(1,'enter')
                tentativas = 0
            tentativas+=1
        elif erro==CODIGO_ERRO_USUARIO_SENHA_INVALIDA:
            break
        else:
            print('Erro ao tentar logar...')
        erro=verificaErro()
    else:
        print(f'Login efetuado com sucesso!')
        confirmacao=True
    return confirmacao

def configuraLoginPersonagem():
    menu = retornaMenu()
    while menu != MENU_JOGAR:
        if menu == MENU_NOTICIAS or menu == MENU_ESCOLHA_PERSONAGEM:
            clickEspecifico(1, 'f1')
        elif menu != MENU_INICIAL:
            clickMouseEsquerdo(1, 2, 35)
        else:
            encerraSecao()
        menu = retornaMenu()
    else:
        login = logaContaPersonagem()
    return login

def entraPersonagemAtivo():
    global dicionarioPersonagemAtributos
    contadorPersonagem = 0
    menu = retornaMenu()
    if menu == MENU_JOGAR:
        print(f'Buscando personagem ativo...')
        clickEspecifico(1, 'enter')
        sleep(1)
        tentativas = 1
        erro = verificaErro()
        while erroEncontrado(erro):
            if erro == CODIGO_CONECTANDO:
                if tentativas > 10:
                    clickEspecifico(2, 'enter')
                    tentativas = 0
                tentativas += 1
            erro = verificaErro()
        else:
            clickEspecifico(1, 'f2')
            clickContinuo(10, 'left')   
            personagemReconhecido = imagem.retornaTextoNomePersonagemReconhecido(1)
            while variavelExiste(personagemReconhecido) and contadorPersonagem < 13:
                confirmaNomePersonagem(personagemReconhecido)
                if variavelExiste(dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO]):
                    modificaAtributoUso(True)
                    clickEspecifico(1, 'f2')
                    sleep(1)
                    print(f'Personagem ({dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO].pegaNome()}) encontrado.')
                    tentativas = 1
                    erro = verificaErro()
                    while erroEncontrado(erro):
                        if ehErroOutraConexao(erro):
                            dicionarioPersonagemAtributos[CHAVE_UNICA_CONEXAO] = False
                            contadorPersonagem = 14
                            break
                        elif ehErroConectando(erro):
                            if tentativas > 10:
                                clickEspecifico(2, 'enter')
                                tentativas = 0
                            tentativas += 1
                        erro = verificaErro()
                    else:
                        print(f'Login efetuado com sucesso!')
                        break
                else:
                    clickEspecifico(1, 'right')
                    personagemReconhecido = imagem.retornaTextoNomePersonagemReconhecido(1)
                contadorPersonagem += 1
            else:
                print(f'Personagem não encontrado!')
                if retornaMenu() == MENU_ESCOLHA_PERSONAGEM:
                    clickEspecifico(1, 'f1')
    elif menu == MENU_INICIAL:
        deslogaPersonagem(dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM_RETIRADO][-1].pegaEmail())
    else:
        clickMouseEsquerdo(1,2,35)

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
                print(f'Personagem ({dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO].pegaNome()}) ESTÁ EM USO.')
                inicializaChavesPersonagem()
                print('Inicia busca...')
                if vaiParaMenuProduzir():
                    # while defineTrabalhoComumProfissaoPriorizada():
                    #     continue
                    listaDicionariosTrabalhosParaProduzirProduzindo = repositorioTrabalhoProducao.retornaListaTrabalhosProducaoParaProduzirProduzindo()
                    if not tamanhoIgualZero(listaDicionariosTrabalhosParaProduzirProduzindo):
                        dicionarioTrabalho = {
                            CHAVE_LISTA_TRABALHOS_PRODUCAO: listaDicionariosTrabalhosParaProduzirProduzindo,
                            CHAVE_TRABALHO_PRODUCAO_ENCONTRADO: None}
                        # if dicionarioPersonagemAtributos[CHAVE_VERIFICA_TRABALHO]:
                        #     verificaProdutosRarosMaisVendidos(None)
                        iniciaBuscaTrabalho(dicionarioTrabalho)
                    else:
                        print(f'Lista de trabalhos desejados vazia.')
                        repositorioPersonagem.alternaEstado(dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO])
                if dicionarioPersonagemAtributos[CHAVE_UNICA_CONEXAO]:
                    if haMaisQueUmPersonagemAtivo(dicionarioPersonagemAtributos):
                        clickMouseEsquerdo(1, 2, 35)
                    dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM_RETIRADO].append(dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO])
                    retiraDicionarioPersonagemListaAtivo()
                else:
                    dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM_RETIRADO].append(dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO])
                    retiraDicionarioPersonagemListaAtivo()
            else:#se o nome reconhecido não estiver na lista de ativos
                if tamanhoIgualZero(dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM_RETIRADO]):
                    if configuraLoginPersonagem():
                        entraPersonagemAtivo()
                else:
                    if textoEhIgual(dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM_RETIRADO][-1].pegaEmail(),dicionarioPersonagemAtributos[CHAVE_LISTA_PERSONAGEM_ATIVO][0].pegaEmail()):
                        entraPersonagemAtivo()
                    elif configuraLoginPersonagem():
                        entraPersonagemAtivo()
    
def preparaPersonagem():
    global repositorioPersonagem, repositorioTrabalho
    repositorioPersonagem = RepositorioPersonagem()
    repositorioTrabalho = RepositorioTrabalho()
    clickAtalhoEspecifico('alt', 'tab')
    clickAtalhoEspecifico('win', 'left')
    iniciaProcessoBusca()

def teste():
    global dicionarioPersonagemAtributos, repositorioTrabalho, repositorioTrabalhoProducao, repositorioPersonagem
    repositorioPersonagem = RepositorioPersonagem()
    listaPersonagem = repositorioPersonagem.pegaTodosPersonagens()
    repositorioTrabalhoProducao = RepositorioTrabalhoProducao(listaPersonagem[5])
    repositorioTrabalho = RepositorioTrabalho()
    dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS] = repositorioTrabalho.pegaTodosTrabalhos()
    retornaTrabalhoConcluido('Bracelete Transcendental')

if __name__=='__main__':
    # teste()
    preparaPersonagem()
    # imagem.salvaNovaTela('testeErroSelecionarItemNecessario.png')
    # print(imagem.reconheceTextoNomePersonagem(imagem.abreImagem('tests/imagemTeste/testeMenuTrabalhoProducao.png'), 1))