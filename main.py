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

class Aplicacao:
    def __init__(self) -> None:
        self._imagem = ManipulaImagem()
        self._repositorioTrabalho = RepositorioTrabalho()
        self._dicionarioPersonagemAtributos = {}
        self._repositorioPersonagem = RepositorioPersonagem()
        self._repositorioVendas = None
        self._repositorioProfissao = None
        self._repositorioEstoque = None
        self._repositorioTrabalhoProducao = None
        self._listaPersonagem = self._repositorioPersonagem.pegaTodosPersonagens()
        self._listaPersonagemJaVerificado = []
        self._listaPersonagemAtivo = []
        self._personagemEmUso = None

    def defineListaPersonagemMesmoEmail(self, personagemEmUso):
        listaDicionarioPersonagemMesmoEmail = []
        if variavelExiste(personagemEmUso):
            for personagem in self._listaPersonagem:
                if textoEhIgual(personagem.pegaEmail(), personagemEmUso.pegaEmail()):
                    listaDicionarioPersonagemMesmoEmail.append(personagem)
        return listaDicionarioPersonagemMesmoEmail

    def modificaAtributoUso(self, valor):
        personagemEmUso = None
        if valor:
            personagemEmUso = self._personagemEmUso
        else:
            if not tamanhoIgualZero(self._listaPersonagemJaVerificado):
                personagemEmUso = self._listaPersonagemJaVerificado[-1]
        listaPersonagemMesmoEmail = self.defineListaPersonagemMesmoEmail(personagemEmUso)
        if not tamanhoIgualZero(listaPersonagemMesmoEmail):
            for personagem in self._listaPersonagem:
                for personagemEmUso in listaPersonagemMesmoEmail:
                    if textoEhIgual(personagem.pegaId(), personagemEmUso.pegaId()):
                        if not personagem.pegaUso():
                            self._repositorioPersonagem.alternaUso(personagem)
                            personagem.alternaUso()
                    elif personagem.pegaUso():
                        self._repositorioPersonagem.alternaUso(personagem)
                        personagem.alternaUso()

    def confirmaNomePersonagem(self, personagemReconhecido):
        for personagemAtivo in self._listaPersonagemAtivo:
            if textoEhIgual(personagemReconhecido, personagemAtivo.pegaNome()):
                print(f'Personagem {personagemReconhecido} confirmado!')
                self._personagemEmUso = personagemAtivo
                break
        else:
            print(f'Personagem {personagemReconhecido} não está ativo!')

    def definePersonagemEmUso(self):
        self._personagemEmUso = None
        nomePersonagemReconhecido = self._imagem.retornaTextoNomePersonagemReconhecido(0)
        if variavelExiste(nomePersonagemReconhecido):
            self.confirmaNomePersonagem(nomePersonagemReconhecido)
        elif nomePersonagemReconhecido == 'provisorioatecair':
            print(f'Nome personagem diferente!')
        else:
            print(f'Nome personagem não reconhecido!')

    def defineListaPersonagensAtivos(self):
        print(f'Definindo lista de personagem ativo.')
        self._listaPersonagemAtivo.clear()
        for personagem in self._listaPersonagem:
            if personagem.ehAtivo():
                self._listaPersonagemAtivo.append(personagem)

    def inicializaChavesPersonagem(self):
        self._autoProducaoTrabalho = False
        self._unicaConexao = True
        self._espacoBolsa = True
        self._confirmacao = True
        self._profissaoModificada = False
        self._repositorioVendas = RepositorioVendas(self._personagemEmUso)
        self._repositorioProfissao = RepositorioProfissao(self._personagemEmUso)
        self._repositorioEstoque = RepositorioEstoque(self._personagemEmUso)
        self._repositorioTrabalhoProducao = RepositorioTrabalhoProducao(self._personagemEmUso)
        self._listaTrabalhos = self._repositorioTrabalho.pegaTodosTrabalhos()
        self._listaProfissoes = self._repositorioProfissao.listaProfissoes
        self._listaTrabalhosVendidos = self._repositorioVendas.pegaTodasVendas()
        self._listaTrabalhosEstoque = self._repositorioEstoque.pegaTodosTrabalhosEstoque()
        self._listaTrabalhosProducao = self._repositorioTrabalhoProducao.pegaTodosTrabalhosProducao()

    def retornaCodigoErroReconhecido(self):
        textoErroEncontrado = self._imagem.retornaErroReconhecido()
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

    def verificaLicenca(self, dicionarioTrabalho):
        confirmacao = False
        if variavelExiste(dicionarioTrabalho):
            print(f"Buscando: {dicionarioTrabalho[CHAVE_TIPO_LICENCA]}")
            licencaReconhecida = self._imagem.retornaTextoLicencaReconhecida()
            if variavelExiste(licencaReconhecida) and variavelExiste(dicionarioTrabalho[CHAVE_TIPO_LICENCA]):
                print(f'Licença reconhecida: {licencaReconhecida}.')
                primeiraBusca = True
                listaCiclo = []
                while not texto1PertenceTexto2(licencaReconhecida, dicionarioTrabalho[CHAVE_TIPO_LICENCA]):
                    clickEspecifico(1, "right")
                    listaCiclo.append(licencaReconhecida)
                    licencaReconhecida = self._imagem.retornaTextoLicencaReconhecida()
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
                    # self._repositorioPersonagem.alternaEstado(dicionarioPersonagem[CHAVE_PERSONAGEM_EM_USO])
            else:
                print(f'Erro ao reconhecer licença!')
        return confirmacao, dicionarioTrabalho

    def verificaErro(self):
        sleep(0.5)
        print(f'Verificando erro...')
        CODIGO_ERRO = self.retornaCodigoErroReconhecido()
        if ehErroLicencaNecessaria(CODIGO_ERRO) or ehErroFalhaConexao(CODIGO_ERRO) or ehErroConexaoInterrompida(CODIGO_ERRO) or ehErroServidorEmManutencao(CODIGO_ERRO) or ehErroReinoIndisponivel(CODIGO_ERRO):
            clickEspecifico(2, "enter")
            if ehErroLicencaNecessaria(CODIGO_ERRO):
                self.verificaLicenca(None)
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

    def retornaMenu(self):
        print(f'Reconhecendo menu.')
        textoMenu = self._imagem.retornaTextoMenuReconhecido(26,1,150)
        if variavelExiste(textoMenu):
            if texto1PertenceTexto2('spearonline',textoMenu):
                textoMenu=self._imagem.retornaTextoMenuReconhecido(216,197,270)
                if variavelExiste(textoMenu):
                    if texto1PertenceTexto2('noticias',textoMenu):
                        print(f'Menu notícias...')
                        return MENU_NOTICIAS
                    if texto1PertenceTexto2('personagens',textoMenu):
                        print(f'Menu escolha de personagem...')
                        return MENU_ESCOLHA_PERSONAGEM
                    if texto1PertenceTexto2('artesanato',textoMenu):
                        textoMenu = self._imagem.retornaTextoMenuReconhecido(266, 242, 150)
                        if variavelExiste(textoMenu):
                            if texto1PertenceTexto2('profissoes',textoMenu):
                                textoMenu=self._imagem.retornaTextoMenuReconhecido(191,612,100)
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
                textoMenu = self._imagem.retornaTextoSair()
                if variavelExiste(textoMenu):
                    if textoEhIgual(textoMenu,'sair'):
                        print(f'Menu jogar...')
                        return MENU_JOGAR
                if self._imagem.verificaMenuReferencia():
                    print(f'Menu tela inicial...')
                    return MENU_INICIAL
                textoMenu=self._imagem.retornaTextoMenuReconhecido(291,412,100)
                if variavelExiste(textoMenu):
                    if texto1PertenceTexto2('conquistas',textoMenu):
                        print(f'Menu personagem...')
                        return MENU_PERSONAGEM
                    if texto1PertenceTexto2('interagir',textoMenu):
                        print(f'Menu principal...')
                        return MENU_PRINCIPAL
                textoMenu=self._imagem.retornaTextoMenuReconhecido(191,319,270)
                if variavelExiste(textoMenu):
                    if texto1PertenceTexto2('parâmetros',textoMenu):
                        if texto1PertenceTexto2('requisitos',textoMenu):
                            print(f'Menu atributo do trabalho...')
                            return MENU_TRABALHOS_ATRIBUTOS
                        else:
                            print(f'Menu licenças...')
                            return MENU_LICENSAS
                textoMenu=self._imagem.retornaTextoMenuReconhecido(275,400,150)
                if variavelExiste(textoMenu):
                    if texto1PertenceTexto2('Recompensa',textoMenu):
                        print(f'Menu trabalho específico...')
                        return MENU_TRABALHO_ESPECIFICO
                textoMenu=self._imagem.retornaTextoMenuReconhecido(266,269,150)
                if variavelExiste(textoMenu):
                    if texto1PertenceTexto2('ofertadiaria',textoMenu):
                        print(f'Menu oferta diária...')
                        return MENU_OFERTA_DIARIA
                textoMenu=self._imagem.retornaTextoMenuReconhecido(181,75,150)
                if variavelExiste(textoMenu):
                    if texto1PertenceTexto2('Loja Milagrosa',textoMenu):
                        print(f'Menu loja milagrosa...')
                        return MENU_LOJA_MILAGROSA
                textoMenu=self._imagem.retornaTextoMenuReconhecido(180,40,300)
                if variavelExiste(textoMenu):
                    if texto1PertenceTexto2('recompensasdiarias',textoMenu):
                        print(f'Menu recompensas diárias...')
                        return MENU_RECOMPENSAS_DIARIAS
                textoMenu=self._imagem.retornaTextoMenuReconhecido(310,338,57)
                if variavelExiste(textoMenu):
                    if texto1PertenceTexto2('meu',textoMenu):
                        print(f'Menu meu perfil...')
                        return MENU_MEU_PERFIL           
                textoMenu=self._imagem.retornaTextoMenuReconhecido(169,97,75)
                if variavelExiste(textoMenu):
                    if texto1PertenceTexto2('Bolsa',textoMenu):
                        print(f'Menu bolsa...')
                        return MENU_BOLSA
                clickMouseEsquerdo(1,35,35)
                return MENU_DESCONHECIDO
            clickAtalhoEspecifico('win','left')
            clickAtalhoEspecifico('win','left')
        print(f'Menu não reconhecido...')
        self.verificaErro()
        return MENU_DESCONHECIDO
    
    def retornaValorTrabalhoVendido(self, listaTextoCarta):
        for palavra in listaTextoCarta:
            if textoEhIgual(palavra, 'por') and listaTextoCarta.index(palavra)+1 < len(listaTextoCarta):
                valorProduto = listaTextoCarta[listaTextoCarta.index(palavra)+1].strip()
                if valorProduto.isdigit():
                    return int(valorProduto)
        return 0

    def retornaQuantidadeTrabalhoVendido(self, listaTextoCarta):
        for texto in listaTextoCarta:
            if texto1PertenceTexto2('x', texto):
                valor = texto.replace('x', '').strip()
                if valor.isdigit():
                    print(f'quantidadeProduto:{valor}')
                    return int(valor)
        return 0

    def retornaConteudoCorrespondencia(self):
        textoCarta = self._imagem.retornaTextoCorrespondenciaReconhecido()
        if variavelExiste(textoCarta):
            trabalhoFoiVendido = texto1PertenceTexto2('Item vendido', textoCarta)
            if trabalhoFoiVendido:
                print(f'Produto vendido:')
                listaTextoCarta = ' '.join(textoCarta.split())
                chaveIdTrabalho = self.retornaChaveIdTrabalho(listaTextoCarta)
                return self._repositorioVendas.adicionaNovaVenda(TrabalhoVendido('', listaTextoCarta, str(datetime.date.today()), self._personagemEmUso.pegaId(), self.retornaQuantidadeTrabalhoVendido(listaTextoCarta), chaveIdTrabalho, self.retornaValorTrabalhoVendido(listaTextoCarta)))
            else:
                print(f'Erro...')
        return None

    def retornaChaveIdTrabalho(self, listaTextoCarta):
        for trabalho in self._listaTrabalhos:
            if texto1PertenceTexto2(trabalho.pegaNome(), listaTextoCarta):
                return trabalho.pegaId()
        return ''

    def atualizaQuantidadeTrabalhoEstoque(self, venda):
        for trabalhoEstoque in self._listaTrabalhosEstoque:
            if textoEhIgual(trabalhoEstoque.pegaTrabalhoId(), venda[CHAVE_TRABALHO_ID]):
                novaQuantidade = trabalhoEstoque.pegaQuantidade() - venda[CHAVE_QUANTIDADE_PRODUTO]
                trabalhoEstoque.setQuantidade(novaQuantidade)
                self._repositorioEstoque.modificaTrabalhoEstoque(trabalhoEstoque)
                print(f'Quantidade do trabalho ({trabalhoEstoque.pegaNome()}) atualizada para {novaQuantidade}.')
                return
        print(f'Trabalho ({venda[CHAVE_NOME_PRODUTO]}) não encontrado no estoque.')

    def recuperaCorrespondencia(self, ):
        while self._imagem.existeCorrespondencia():
            clickEspecifico(1, 'enter')
            venda = self.retornaConteudoCorrespondencia()
            if variavelExiste(venda):
                self.atualizaQuantidadeTrabalhoEstoque(venda)
            clickEspecifico(1,'f2')
            continue
        print(f'Caixa de correio vazia!')
        clickMouseEsquerdo(1, 2, 35)

    def reconheceRecuperaTrabalhoConcluido(self):
        erro = self.verificaErro()
        if nenhumErroEncontrado(erro):
            nomeTrabalhoConcluido = self._imagem.retornaNomeTrabalhoFrameProducaoReconhecido()
            clickEspecifico(1, 'down')
            clickEspecifico(1, 'f2')
            print(f'  Trabalho concluido reconhecido: {nomeTrabalhoConcluido}.')
            if variavelExiste(nomeTrabalhoConcluido):
                erro = self.verificaErro()
                if nenhumErroEncontrado(erro):
                    if not self._profissaoModificada:
                        self._profissaoModificada = True
                    clickContinuo(3, 'up')
                    return nomeTrabalhoConcluido
                if ehErroEspacoBolsaInsuficiente(erro):
                    self._espacoBolsa = False
                    clickContinuo(1, 'up')
                    clickEspecifico(1, 'left')
        return None

    def retornaListaPossiveisTrabalhoRecuperado(self, nomeTrabalhoConcluido):
        listaPossiveisDicionariosTrabalhos = []
        if not tamanhoIgualZero(self._listaTrabalhos):
            for trabalho in self._listaTrabalhos:
                if texto1PertenceTexto2(nomeTrabalhoConcluido[1:-1], trabalho.pegaNomeProducao()):
                    listaPossiveisDicionariosTrabalhos.append(trabalho)
        else:
            print(f'Erro ao definir lista de trabalhos.')
        return listaPossiveisDicionariosTrabalhos

    def retornaTrabalhoConcluido(self, nomeTrabalhoConcluido):
        listaPossiveisTrabalhos = self.retornaListaPossiveisTrabalhoRecuperado(nomeTrabalhoConcluido)
        if not tamanhoIgualZero(listaPossiveisTrabalhos):
            listaDicionariosTrabalhosProduzirProduzindo = self._repositorioTrabalhoProducao.retornaListaTrabalhosProducaoParaProduzirProduzindo()
            for possivelTrabalho in listaPossiveisTrabalhos:
                for trabalhoProduzirProduzindo in listaDicionariosTrabalhosProduzirProduzindo:
                    condicoes = trabalhoProduzirProduzindo.ehProduzindo() and textoEhIgual(trabalhoProduzirProduzindo.pegaNome(), possivelTrabalho.pegaNome())
                    if condicoes:
                        trabalhoProduzirProduzindo.setTrabalhoId(possivelTrabalho.pegaId())
                        trabalhoProduzirProduzindo.setNomeProducao(possivelTrabalho.pegaNomeProducao())
                        return trabalhoProduzirProduzindo
            else:
                print(f'Trabalho concluído ({listaPossiveisTrabalhos[0].pegaNome()}) não encontrado na lista produzindo...')
                return self._repositorioTrabalhoProducao.adicionaTrabalhoProducao(TrabalhoProducao('', listaPossiveisTrabalhos[0].pegaId(), listaPossiveisTrabalhos[0].pegaNome(), listaPossiveisTrabalhos[0].pegaNomeProducao(), listaPossiveisTrabalhos[0].pegaExperiencia(), listaPossiveisTrabalhos[0].pegaNivel(), listaPossiveisTrabalhos[0].pegaProfissao(), listaPossiveisTrabalhos[0].pegaRaridade(), listaPossiveisTrabalhos[0].pegaTrabalhoNecessario(), False, CHAVE_LICENCA_INICIANTE, CODIGO_CONCLUIDO))
        return None

    def modificaTrabalhoConcluidoListaProduzirProduzindo(self, trabalhoProducaoConcluido):
        if trabalhoEhProducaoRecursos(trabalhoProducaoConcluido):
            trabalhoProducaoConcluido.setRecorrencia(True)
        if trabalhoProducaoConcluido.pegaRecorrencia():
            print(f'Trabalho recorrente.')
            self._repositorioTrabalhoProducao.removeTrabalhoProducao(trabalhoProducaoConcluido)
            for posicao in range(len(self._listaTrabalhosProducao)):
                if textoEhIgual(self._listaTrabalhosProducao[posicao].pegaId(), trabalhoProducaoConcluido.pegaId()):
                    del self._listaTrabalhosProducao[posicao]
                    break
        else:
            print(f'Trabalho sem recorrencia.')
            self._repositorioTrabalhoProducao.modificaTrabalhoProducao(trabalhoProducaoConcluido)
            print(f'Trabalho ({trabalhoProducaoConcluido.pegaNome()}) modificado para concluído.')
            for dicionarioTrabalho in self._listaTrabalhosProducao:
                if textoEhIgual(dicionarioTrabalho.pegaId(), trabalhoProducaoConcluido.pegaId()):
                    dicionarioTrabalho.setEstado(CODIGO_CONCLUIDO)
                    break
            else:
                self._listaTrabalhosProducao.append(trabalhoProducaoConcluido)
        return trabalhoProducaoConcluido

    def modificaExperienciaProfissao(self, trabalhoProducao):
        for profissao in self._listaProfissoes:
            if textoEhIgual(profissao.pegaNome(), trabalhoProducao.pegaProfissao()):
                experiencia = profissao.pegaExperiencia() + trabalhoProducao.pegaExperiencia()
                if experiencia > 830000:
                    experiencia = 830000
                profissao.setExperiencia(experiencia)
                self._repositorioProfissao.modificaProfissao(profissao)
                print(f'Experiência de {profissao.pegaNome()} atualizada para {experiencia}.')
                break

    def retornaListaDicionarioTrabalhoProduzido(self, trabalhoProducaoConcluido):
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
                    for trabalho in self._listaTrabalhos:
                        condicoes = textoEhIgual(trabalho.pegaProfissao(), trabalhoProducaoConcluido.pegaProfissao()) and trabalho.pegaNivel() == nivelColecao and textoEhIgual(trabalho.pegaRaridade(), CHAVE_RARIDADE_COMUM)
                        if condicoes:
                            trabalhoEstoque = TrabalhoEstoque('', trabalho.pegaNome(),trabalho.pegaProfissao(), trabalho.pegaNivel(), 1, trabalho.pegaRaridade(), trabalho.pegaId())
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

    def modificaQuantidadeTrabalhoEstoque(self, listaTrabalhoEstoqueConcluido, trabalhoEstoque):
        for trabalhoEstoqueConcluido in listaTrabalhoEstoqueConcluido:
            if textoEhIgual(trabalhoEstoqueConcluido.pegaNome(), trabalhoEstoque.pegaNome()):
                novaQuantidade = trabalhoEstoque.pegaQuantidade() + trabalhoEstoqueConcluido.pegaQuantidade()
                trabalhoEstoque.setQuantidade(novaQuantidade)
                print(trabalhoEstoque)
                self._repositorioEstoque.modificaTrabalhoEstoque(trabalhoEstoque)
                for indice in range(len(listaTrabalhoEstoqueConcluido)):
                    if listaTrabalhoEstoqueConcluido[indice].pegaNome() == trabalhoEstoque.pegaNome():
                        del listaTrabalhoEstoqueConcluido[indice]
                        break
                if tamanhoIgualZero(listaTrabalhoEstoqueConcluido):
                    break
        return listaTrabalhoEstoqueConcluido, trabalhoEstoque

    def atualizaEstoquePersonagem(self, trabalhoEstoqueConcluido):
        listaTrabalhoEstoqueConcluido = self.retornaListaDicionarioTrabalhoProduzido(trabalhoEstoqueConcluido)
        if not tamanhoIgualZero(listaTrabalhoEstoqueConcluido):
            if not tamanhoIgualZero(self._listaTrabalhosEstoque):
                for trabalhoEstoque in self._listaTrabalhosEstoque:
                    listaTrabalhoEstoqueConcluido, trabalhoEstoque = self.modificaQuantidadeTrabalhoEstoque(listaTrabalhoEstoqueConcluido, trabalhoEstoque)
                else:
                    if not tamanhoIgualZero(listaTrabalhoEstoqueConcluido):
                        for trabalhoEstoqueConcluido in listaTrabalhoEstoqueConcluido:
                            self._repositorioEstoque.adicionaTrabalhoEstoque(trabalhoEstoqueConcluido)
                            self._listaTrabalhosEstoque.append(trabalhoEstoqueConcluido)
            else:
                for trabalhoEstoqueConcluido in listaTrabalhoEstoqueConcluido:
                    self._repositorioEstoque.adicionaTrabalhoEstoque(trabalhoEstoqueConcluido)
                    self._listaTrabalhosEstoque.append(trabalhoEstoqueConcluido)

    def retornaProfissaoTrabalhoProducaoConcluido(self, trabalhoProducaoConcluido):
        for profissao in self._listaProfissoes:
            if textoEhIgual(profissao.pegaNome(), trabalhoProducaoConcluido.pegaProfissao()):
                return profissao
        return None

    def retornaNivelXpMinimoMaximo(self, profissao):
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

    def verificaProducaoTrabalhoRaro(self, trabalhoProducaoConcluido):
        
        trabalhoProducaoRaro = None
        dicionarioProfissao = self.retornaProfissaoTrabalhoProducaoConcluido(trabalhoProducaoConcluido)
        if variavelExiste(dicionarioProfissao):
            _, _, xpMaximo = self.retornaNivelXpMinimoMaximo(dicionarioProfissao)
            licencaProducaoIdeal = CHAVE_LICENCA_PRINCIPIANTE
            if xpMaximo >= 830000:
                licencaProducaoIdeal = CHAVE_LICENCA_INICIANTE
            if textoEhIgual(trabalhoProducaoConcluido.pegaRaridade(), CHAVE_RARIDADE_MELHORADO):
                print(f'Trabalhos MELHORADO. Profissão {trabalhoProducaoConcluido.pegaProfissao()}. Nível {trabalhoProducaoConcluido.pegaNivel()}.')
                for trabalho in self._listaTrabalhos:
                    condicoes = (textoEhIgual(trabalho.pegaProfissao(), trabalhoProducaoConcluido.pegaProfissao())
                        and textoEhIgual(trabalho.pegaRaridade(), CHAVE_RARIDADE_RARO)
                        and trabalho.pegaNivel() == trabalhoProducaoConcluido.pegaNivel())
                    if condicoes:    
                        if textoEhIgual(trabalho.pegaTrabalhoNecessario(), trabalhoProducaoConcluido.pegaNome()):
                            experiencia = trabalho.pegaExperiencia() * 1.5
                            trabalhoProducaoRaro = TrabalhoProducao('', trabalho.pegaTrabalhoId(), trabalho.pegaNome(), trabalho.pegaNomeProducao(), experiencia, trabalho.pegaNivel(), trabalho.pegaProfissao(), trabalho.pegaRaridade(), trabalho.pegaTrabalhoNecessario(), False, licencaProducaoIdeal, trabalho.pegaEstado())
                            break
        if variavelExiste(trabalhoProducaoRaro):
            trabalhoProducaoRaroComId = self._repositorioTrabalhoProducao.adicionaTrabalhoProducao(trabalhoProducaoRaro)
            self._listaTrabalhosProducao.append(trabalhoProducaoRaroComId)

    def retornaListaPersonagemRecompensaRecebida(self, listaPersonagemPresenteRecuperado):
        if tamanhoIgualZero(listaPersonagemPresenteRecuperado):
            print(f'Limpou a lista...')
            listaPersonagemPresenteRecuperado = []
        nomePersonagemReconhecido = self._imagem.retornaTextoNomePersonagemReconhecido(0)
        if variavelExiste(nomePersonagemReconhecido):
            print(f'{nomePersonagemReconhecido} foi adicionado a lista!')
            listaPersonagemPresenteRecuperado.append(nomePersonagemReconhecido)
        else:
            print(f'Erro ao reconhecer nome...')
        return listaPersonagemPresenteRecuperado

    def recuperaPresente(self):
        evento = 0
        print(f'Buscando recompensa diária...')
        while evento < 2:
            sleep(2)
            referenciaEncontrada = self._imagem.retornaReferencia()
            if variavelExiste(referenciaEncontrada):
                print(f'Referência encontrada!')
                clickMouseEsquerdo(1,referenciaEncontrada[0],referenciaEncontrada[1])
                posicionaMouseEsquerdo(360,600)
                if self.verificaErro() != 0:
                    evento=2
                clickEspecifico(1,'f2')
            print(f'Próxima busca.')
            clickContinuo(8,'up')
            clickEspecifico(1,'left')
            evento += 1
        clickEspecifico(2,'f1')

    def reconheceMenuRecompensa(self, menu):
        print(f'Entrou em recuperaPresente.')
        if menu == MENU_LOJA_MILAGROSA:
            clickEspecifico(1,'down')
            clickEspecifico(1,'enter')
        elif menu == MENU_RECOMPENSAS_DIARIAS:
            self.recuperaPresente()
        else:
            print(f'Recompensa diária já recebida!')

    def deslogaPersonagem(self):
        menu = self.retornaMenu()
        while not ehMenuJogar(menu):
            if ehMenuInicial(menu):
                encerraSecao()
                break
            elif ehMenuJogar(menu):
                break
            else:
                clickMouseEsquerdo(1, 2, 35)
            menu = self.retornaMenu()

    def entraPersonagem(self, listaPersonagemPresenteRecuperado):
        confirmacao = False
        print(f'Buscando próximo personagem...')
        clickEspecifico(1, 'enter')
        sleep(1)
        tentativas = 1
        erro = self.verificaErro()
        while erroEncontrado(erro):
            if erro == CODIGO_CONECTANDO:
                if tentativas > 10:
                    clickEspecifico(2, 'enter')
                    tentativas = 0
                tentativas += 1
            erro = self.verificaErro()
        else:
            clickEspecifico(1, 'f2')
            if len(listaPersonagemPresenteRecuperado) == 1:
                clickContinuo(8, 'left')
            else:
                clickEspecifico(1, 'right')
            nomePersonagem = self._imagem.retornaTextoNomePersonagemReconhecido(1)               
            while True:
                nomePersonagemPresenteado = None
                for nomeLista in listaPersonagemPresenteRecuperado:
                    if nomePersonagem == nomeLista and nomePersonagem != None:
                        nomePersonagemPresenteado = nomeLista
                        break
                if nomePersonagemPresenteado != None:
                    clickEspecifico(1, 'right')
                    nomePersonagem = self._imagem.retornaTextoNomePersonagemReconhecido(1)
                if nomePersonagem == None:
                    print(f'Fim da lista de personagens!')
                    clickEspecifico(1, 'f1')
                    break
                else:
                    clickEspecifico(1, 'f2')
                    sleep(1)
                    tentativas = 1
                    erro = self.verificaErro()
                    while erroEncontrado(erro):
                        if erro == CODIGO_RECEBER_RECOMPENSA:
                            break
                        elif erro == CODIGO_CONECTANDO:
                            if tentativas > 10:
                                clickEspecifico(2, 'enter')
                                tentativas = 0
                            tentativas += 1
                        sleep(1.5)
                        erro = self.verificaErro()
                    confirmacao = True
                    print(f'Login efetuado com sucesso!')
                    break
        return confirmacao

    def recebeTodasRecompensas(self, menu):
        listaPersonagemPresenteRecuperado = self.retornaListaPersonagemRecompensaRecebida(listaPersonagemPresenteRecuperado = [])
        while True:
            self.reconheceMenuRecompensa(menu)
            if self._imagem.retornaExistePixelCorrespondencia():
                vaiParaMenuCorrespondencia()
                self.recuperaCorrespondencia()
            print(f'Lista: {listaPersonagemPresenteRecuperado}.')
            self.deslogaPersonagem()
            if self.entraPersonagem(listaPersonagemPresenteRecuperado):
                listaPersonagemPresenteRecuperado = self.retornaListaPersonagemRecompensaRecebida(listaPersonagemPresenteRecuperado)
            else:
                print(f'Todos os personagens foram verificados!')
                break
            menu = self.retornaMenu()

    def trataMenu(self, menu):
        self._confirmacao = True
        if menu == MENU_DESCONHECIDO:
            pass
        elif menu == MENU_TRABALHOS_ATUAIS:
            estadoTrabalho = self._imagem.retornaEstadoTrabalho()
            if estadoTrabalho == CODIGO_CONCLUIDO:
                nomeTrabalhoConcluido = self.reconheceRecuperaTrabalhoConcluido()
                if variavelExiste(nomeTrabalhoConcluido):
                    trabalhoProducaoConcluido = self.retornaTrabalhoConcluido(nomeTrabalhoConcluido)
                    if variavelExiste(trabalhoProducaoConcluido):
                        trabalhoProducaoConcluido = self.modificaTrabalhoConcluidoListaProduzirProduzindo(trabalhoProducaoConcluido)
                        self.modificaExperienciaProfissao(trabalhoProducaoConcluido)
                        self.atualizaEstoquePersonagem(trabalhoProducaoConcluido)
                        self.verificaProducaoTrabalhoRaro(trabalhoProducaoConcluido)
                    else:
                        print(f'Trabalho produção concluido não reconhecido.')
                else:
                    print(f'Nome trabalho concluído não reconhecido.')
            elif estadoTrabalho == CODIGO_PRODUZINDO:
                if not existeEspacoProducao(self._dicionarioPersonagemAtributos):
                    print(f'Todos os espaços de produção ocupados.')
                    self._confirmacao = False
                else:
                    clickContinuo(3,'up')
                    clickEspecifico(1,'left')
            elif estadoTrabalho == CODIGO_PARA_PRODUZIR:
                clickContinuo(3,'up')
                clickEspecifico(1,'left')
        elif menu == MENU_RECOMPENSAS_DIARIAS or menu == MENU_LOJA_MILAGROSA:
            self.recebeTodasRecompensas(menu)
            for personagem in self._listaPersonagem:
                if not personagem.pegaEstado():
                    personagem.setEstado(True)
                    self._repositorioPersonagem.modificaPersonagem(personagem)
            self._confirmacao = False
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
        elif ehMenuInicial(menu):
            clickEspecifico(1,'f2')
            clickEspecifico(1,'num1')
            clickEspecifico(1,'num7')
        else:
            self._confirmacao = False
        if ehErroOutraConexao(self.verificaErro()):
            self._confirmacao = False
            self._unicaConexao = False

    def vaiParaMenuProduzir(self):
        erro = self.verificaErro()
        if nenhumErroEncontrado(erro):
            menu = self.retornaMenu()
            if ehMenuInicial(menu):
                if self._imagem.retornaExistePixelCorrespondencia():
                    vaiParaMenuCorrespondencia()
                    self.recuperaCorrespondencia()
            while not ehMenuProduzir(menu):
                self.trataMenu(menu)
                if not self._confirmacao:
                    return False
                menu = self.retornaMenu()
            else:
                return True
        elif ehErroOutraConexao(erro):
            self._unicaConexao = False
        return False

    def retornaListaDicionariosTrabalhosRarosVendidos(self, dicionarioUsuario):
        print(f'Definindo lista dicionários produtos raros vendidos...')
        listaDicionariosTrabalhosRarosVendidos = []
        if dicionarioUsuario != None:
            self._personagemEmUso = dicionarioUsuario[CHAVE_PERSONAGEM_EM_USO]
            self._dicionarioPersonagemAtributos[CHAVE_ID_USUARIO] = dicionarioUsuario[CHAVE_ID_USUARIO]
            self._listaProfissoes = self._repositorioProfissao.pegaTodasProfissoes()
            self._listaTrabalhos = self._repositorioTrabalho.pegaTodosTrabalhos()
            self._listaTrabalhosVendidos = self._repositorioVendas.pegaTodasVendas()
            self._listaTrabalhosEstoque = self._repositorioEstoque.pegaTodosTrabalhosEstoque()
            self._listaTrabalhosProducao = self._repositorioTrabalhoProducao.pegaTodosTrabalhosProducao()
        if not tamanhoIgualZero(self._listaTrabalhos):
            for produtoVendido in self._listaTrabalhosVendidos:
                for trabalho in self._listaTrabalhos:
                    condicoes = (
                        textoEhIgual(trabalho[CHAVE_RARIDADE], CHAVE_RARIDADE_RARO)
                        and texto1PertenceTexto2(trabalho[CHAVE_NOME], produtoVendido['nomeProduto'])
                        and textoEhIgual(produtoVendido['nomePersonagem'], self._personagemEmUso[CHAVE_ID])
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

    def verificaProdutosRarosMaisVendidos(self, dicionarioUsuario):
        listaDicionariosProdutosRarosVendidos = self.retornaListaDicionariosTrabalhosRarosVendidos(dicionarioUsuario)
        if not tamanhoIgualZero(listaDicionariosProdutosRarosVendidos):
            # produzProdutoMaisVendido(listaDicionariosProdutosRarosVendidos)
            pass
        else:
            print(f'Lista de trabalhos raros vendidos está vazia!')

    def defineChaveListaDicionariosProfissoesNecessarias(self):
        print(f'Verificando profissões necessárias...')
        self._dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSOES_NECESSARIAS] = []
        for profissao in self._listaProfissoes:
            for trabalhoProducaoDesejado in self._listaTrabalhosProducao:
                chaveProfissaoEhIgualEEstadoEhParaProduzir = textoEhIgual(profissao.pegaNome(), trabalhoProducaoDesejado.pegaProfissao()) and trabalhoProducaoDesejado.ehParaProduzir()
                if chaveProfissaoEhIgualEEstadoEhParaProduzir:
                    self._dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSOES_NECESSARIAS].append(profissao)
                    break
        else:
            self._dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSOES_NECESSARIAS] = sorted(self._dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSOES_NECESSARIAS],key=lambda profissao:profissao.pegaPrioridade(),reverse=True)

    def retornaContadorEspacosProducao(self, contadorEspacosProducao, nivel):
        contadorNivel = 0
        for dicionarioProfissao in self._listaProfissoes:
            if dicionarioProfissao.pegaNivel() >= nivel:
                contadorNivel += 1
        else:
            print(f'Contador de profissões nível {nivel} ou superior: {contadorNivel}.')
            if contadorNivel > 0 and contadorNivel < 3:
                contadorEspacosProducao += 1
            elif contadorNivel >= 3:
                contadorEspacosProducao += 2
        return contadorEspacosProducao

    def retornaQuantidadeEspacosDeProducao(self):
        print(f'Define quantidade de espaços de produção...')
        quantidadeEspacosProducao = 2
        for dicionarioProfissao in self._listaProfissoes:
            nivel, _ , _= self.retornaNivelXpMinimoMaximo(dicionarioProfissao)
            if nivel >= 5:
                quantidadeEspacosProducao += 1
                break
        listaNiveis = [10, 15, 20, 25]
        for nivel in listaNiveis:
            quantidadeEspacosProducao = self.retornaContadorEspacosProducao(quantidadeEspacosProducao, nivel)
        print(f'Espaços de produção disponíveis: {quantidadeEspacosProducao}.')
        return quantidadeEspacosProducao

    def verificaEspacoProducao(self):
        quantidadeEspacoProducao = self.retornaQuantidadeEspacosDeProducao()
        if self._personagemEmUso.pegaEspacoProducao() != quantidadeEspacoProducao:
            self._personagemEmUso.setEspacoProducao(quantidadeEspacoProducao)
            self._repositorioPersonagem.modificaPersonagem(self._personagemEmUso)

    def retornaListaDicionariosTrabalhosProducaoRaridadeEspecifica(self, dicionarioTrabalho, raridade):
        listaTrabalhosProducaoRaridadeEspecifica = []
        listaTrabalhosProducaoParaProduzirProduzindo = self._repositorioTrabalhoProducao.retornaListaTrabalhosProducaoParaProduzirProduzindo()
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

    def retornaNomeTrabalhoPosicaoTrabalhoRaroEspecial(self, dicionarioTrabalho):
        return self._imagem.retornaNomeTrabalhoReconhecido((dicionarioTrabalho[CHAVE_POSICAO] * 72) + 289, 0)

    def retornaFrameTelaTrabalhoEspecifico(self):
        clickEspecifico(1, 'down')
        clickEspecifico(1, 'enter')
        nomeTrabalhoReconhecido = self._imagem.retornaNomeConfirmacaoTrabalhoProducaoReconhecido(0)
        clickEspecifico(1, 'f1')
        clickEspecifico(1, 'up')
        return nomeTrabalhoReconhecido

    def confirmaNomeTrabalhoProducao(self, dicionarioTrabalho, tipoTrabalho):
        print(f'Confirmando nome do trabalho...')
        dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = None
        if tipoTrabalho == 0:
            nomeTrabalhoReconhecido = self.retornaFrameTelaTrabalhoEspecifico()
        else:
            nomeTrabalhoReconhecido = self._imagem.retornaNomeConfirmacaoTrabalhoProducaoReconhecido(tipoTrabalho)
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

    def incrementaChavePosicaoTrabalho(self, dicionarioTrabalho):
        dicionarioTrabalho[CHAVE_POSICAO] += 1
        return dicionarioTrabalho

    def defineDicionarioTrabalhoComumMelhorado(self, dicionarioTrabalho):
        nomeTrabalhoReconhecidoAux = ''
        nomeTrabalhoReconhecido = ''
        print(f'Buscando trabalho {dicionarioTrabalho[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA][0].pegaRaridade()}.')
        contadorParaBaixo = 0
        if not primeiraBusca(dicionarioTrabalho):
            contadorParaBaixo = dicionarioTrabalho[CHAVE_POSICAO]
            clickEspecifico(contadorParaBaixo, 'down')
        while not chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
            erro = self.verificaErro()
            if erroEncontrado(erro):
                dicionarioTrabalho[CHAVE_CONFIRMACAO] = False
                break
            if primeiraBusca(dicionarioTrabalho):
                clicks = 3
                contadorParaBaixo = 3
                clickEspecifico(clicks, 'down')
                yinicialNome = (2 * 70) + 285
                nomeTrabalhoReconhecido = self._imagem.retornaNomeTrabalhoReconhecido(yinicialNome, 1)
            elif contadorParaBaixo == 3:
                yinicialNome = (2 * 70) + 285
                nomeTrabalhoReconhecido = self._imagem.retornaNomeTrabalhoReconhecido(yinicialNome, 1)
            elif contadorParaBaixo == 4:
                yinicialNome = (3 * 70) + 285
                nomeTrabalhoReconhecido = self._imagem.retornaNomeTrabalhoReconhecido(yinicialNome, 1)
            elif contadorParaBaixo > 4:
                nomeTrabalhoReconhecido = self._imagem.retornaNomeTrabalhoReconhecido(530, 1)
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
                        dicionarioTrabalho = self.confirmaNomeTrabalhoProducao(dicionarioTrabalho, tipoTrabalho)
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

    def defineCloneDicionarioTrabalhoDesejado(self, trabalhoProducaoEncontrado):
        return TrabalhoProducao('', trabalhoProducaoEncontrado.pegaTrabalhoId(),trabalhoProducaoEncontrado.pegaNome(), trabalhoProducaoEncontrado.pegaNomeProducao(), trabalhoProducaoEncontrado.pegaExperiencia(), trabalhoProducaoEncontrado.pegaNivel(), trabalhoProducaoEncontrado.pegaProfissao(), trabalhoProducaoEncontrado.pegaRaridade(), trabalhoProducaoEncontrado.pegaTrabalhoNecessario(), trabalhoProducaoEncontrado.pegaRecorrencia(), trabalhoProducaoEncontrado.pegaLinceca(), trabalhoProducaoEncontrado.pegaEstado())

    def clonaTrabalhoProducaoEncontrado(self, dicionarioTrabalho, trabalhoProducaoEncontrado):
        
        print(f'Recorrencia está ligada.')
        cloneTrabalhoProducaoEncontrado = self.defineCloneDicionarioTrabalhoDesejado(trabalhoProducaoEncontrado)
        trabalhoProducaoAdicionado = self._repositorioTrabalhoProducao.adicionaTrabalhoProducao(cloneTrabalhoProducaoEncontrado)
        self._listaTrabalhosProducao.append(trabalhoProducaoAdicionado)
        dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = trabalhoProducaoAdicionado

    def retornaChaveTipoRecurso(self, dicionarioRecurso):
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

    def retornaNomesRecursos(self, chaveProfissao, nivelRecurso):
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

    def retornaTrabalhoRecurso(self, trabalhoProducao):
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
        nomeRecursoPrimario, nomeRecursoSecundario, nomeRecursoTerciario = self.retornaNomesRecursos(chaveProfissao, nivelRecurso)
        return TrabalhoRecurso(trabalhoProducao.pegaProfissao(), trabalhoProducao.pegaNivel(), nomeRecursoTerciario, nomeRecursoSecundario, nomeRecursoPrimario, recursoTerciario)

    def removeTrabalhoEstoque(self, trabalhoProducao):
        if not tamanhoIgualZero(self._listaTrabalhosEstoque):
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
                    nomeRecursoPrimario, nomeRecursoSecundario, nomeRecursoTerciario = self.retornaNomesRecursos(chaveProfissao, 1)
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
                    for trabalhoEstoque in self._listaTrabalhosEstoque:
                        for recursoBuscado in listaNomeRecursoBuscado:
                            if textoEhIgual(trabalhoEstoque.pegaNome(), recursoBuscado[0]):
                                novaQuantidade = trabalhoEstoque.pegaQuantidade() - recursoBuscado[1]
                                if novaQuantidade < 0:
                                    novaQuantidade = 0
                                print(f'Quantidade de {trabalhoEstoque.pegaNome()} atualizada de {trabalhoEstoque.pegaQuantidade()} para {novaQuantidade}.')
                                trabalhoEstoque.setQuantidade(novaQuantidade)
                                self._repositorioEstoque.modificaTrabalhoEstoque(trabalhoEstoque)
                        if textoEhIgual(trabalhoEstoque.pegaNome(), trabalhoProducao.pegaLicenca()):
                            novaQuantidade = trabalhoEstoque.pegaQuantidade() - 1
                            if novaQuantidade < 0:
                                novaQuantidade = 0
                            print(f'Quantidade de {trabalhoEstoque.pegaNome()} atualizada de {trabalhoEstoque.pegaQuantidade()} para {novaQuantidade}.')
                            trabalhoEstoque.setQuantidade(novaQuantidade)
                            self._repositorioEstoque.modificaTrabalhoEstoque(trabalhoEstoque)
                else:
                    trabalhoRecurso = self.retornaTrabalhoRecurso(trabalhoProducao)
                    for trabalhoEstoque in self._listaTrabalhosEstoque:
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
                            self._repositorioEstoque.modificaTrabalhoEstoque(trabalhoEstoque)
            elif trabalhoProducao.ehMelhorado() or trabalhoProducao.ehRaro():
                if not trabalhoEhProducaoRecursos(trabalhoProducao):
                    listaTrabalhosNecessarios = trabalhoProducao.pegaTrabalhoNecessario().split(',')
                    for trabalhoNecessario in listaTrabalhosNecessarios:
                        for trabalhoEstoque in self._listaTrabalhosEstoque:
                            if textoEhIgual(trabalhoNecessario, trabalhoEstoque.pegaNome()):
                                novaQuantidade = trabalhoEstoque.pegaQuantidade() - 1
                                if novaQuantidade < 0:
                                    novaQuantidade = 0
                                print(f'Quantidade de {trabalhoEstoque.pegaNome()} atualizada para {novaQuantidade}.')
                                trabalhoEstoque.setQuantidade(novaQuantidade)
                                self._repositorioEstoque.modificaTrabalhoEstoque(trabalhoEstoque)
                                break
        else:
            print(f'Lista de estoque está vazia!')
            
    def iniciaProcessoDeProducao(self, dicionarioTrabalho):
        
        primeiraBusca = True
        trabalhoProducaoEncontrado = dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO]
        while True:
            menu = self.retornaMenu()
            if menuTrabalhosAtuaisReconhecido(menu):
                if not tamanhoIgualZero(trabalhoProducaoEncontrado):
                    if trabalhoProducaoEncontrado.ehRecorrente():
                        self.clonaTrabalhoProducaoEncontrado(dicionarioTrabalho, trabalhoProducaoEncontrado)
                    else:
                        self._repositorioTrabalhoProducao.modificaTrabalhoProducao(trabalhoProducaoEncontrado)
                    self.removeTrabalhoEstoque(trabalhoProducaoEncontrado)
                    clickContinuo(12,'up')
                    self._confirmacao = True
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
                textoReconhecido = self._imagem.retornaTextoLicencaReconhecida()
                if variavelExiste(textoReconhecido):
                    print(f'Licença reconhecida: {textoReconhecido}.')
                    if not texto1PertenceTexto2('licençasdeproduçao', textoReconhecido):
                        primeiraBusca = True
                        listaCiclo = []
                        while not texto1PertenceTexto2(textoReconhecido, trabalhoProducaoEncontrado.pegaLicenca()):
                            listaCiclo.append(textoReconhecido)
                            clickEspecifico(1, "right")
                            textoReconhecido = self._imagem.retornaTextoLicencaReconhecida()
                            if variavelExiste(textoReconhecido):
                                print(f'Licença reconhecida: {textoReconhecido}.')
                                if textoEhIgual(textoReconhecido, 'nenhumitem'):
                                    if textoEhIgual(trabalhoProducaoEncontrado.pegaLicenca(), CHAVE_LICENCA_INICIANTE):
                                        if not textoEhIgual(listaCiclo[-1], 'nenhumitem'):
                                            print(f'Sem licenças de produção...')
                                            self._personagemEmUso.setEstado(False)
                                            self._repositorioPersonagem.modificaPersonagem(self._personagemEmUso)
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
                                erro = self.verificaErro()
                                if ehErroOutraConexao(erro):
                                    self._unicaConexao = False
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
                        self._personagemEmUso.setEstado(False)
                        self._repositorioPersonagem.modificaPersonagem(self._personagemEmUso)
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
            self._confirmacao = True
            tentativas = 1
            erro = self.verificaErro()
            while erroEncontrado(erro):
                if ehErroRecursosInsuficiente(erro):
                    self._repositorioTrabalhoProducao.removeTrabalhoProducao(trabalhoProducaoEncontrado)
                    posicao = 0
                    for trabalhoProducao in self._listaTrabalhosProducao:
                        if textoEhIgual(trabalhoProducao.pegaId(), trabalhoProducaoEncontrado.pegaId()):
                            del self._listaTrabalhosProducao[posicao]
                            break
                        posicao += 1
                    dicionarioTrabalho[CHAVE_CONFIRMACAO] = False
                elif ehErroEspacoProducaoInsuficiente(erro) or ehErroOutraConexao(erro) or ehErroConectando(erro) or ehErroRestauraConexao(erro):
                    self._confirmacao = False
                    dicionarioTrabalho[CHAVE_CONFIRMACAO] = False
                    if ehErroOutraConexao(erro):
                        self._unicaConexao = False
                    elif ehErroConectando(erro):
                        if tentativas > 10:
                            clickEspecifico(1, 'enter')
                            tentativas = 0
                        tentativas+=1
                erro = self.verificaErro()
            if not self._confirmacao:
                break
            primeiraBusca = False
        return dicionarioTrabalho

    def retornaListaPossiveisTrabalhos(self, nomeTrabalhoConcluido):
        listaPossiveisTrabalhos = []
        for trabalho in self._listaTrabalhos:
            if texto1PertenceTexto2(nomeTrabalhoConcluido[1:-1], trabalho.pegaNomeProducao()):
                trabalhoEncontrado = TrabalhoProducao('', trabalho.pegaId(), trabalho.pegaNome(), trabalho.pegaNomeProducao(), trabalho.pegaExperiencia(), trabalho.pegaNivel(), trabalho.pegaProfissao(), trabalho.pegaRaridade(), trabalho.pegaTrabalhoNecessario(), False, CHAVE_LICENCA_INICIANTE, CODIGO_CONCLUIDO)
                listaPossiveisTrabalhos.append(trabalhoEncontrado)
        return listaPossiveisTrabalhos

    def retornaTrabalhoProducaoConcluido(self, nomeTrabalhoConcluido):
        listaPossiveisTrabalhosProducao = self.retornaListaPossiveisTrabalhos(nomeTrabalhoConcluido)
        if not tamanhoIgualZero(listaPossiveisTrabalhosProducao):
            listaTrabalhosProducaoProduzirProduzindo = self._repositorioTrabalhoProducao.retornaListaTrabalhosProducaoParaProduzirProduzindo()
            for possivelTrabalhoProducao in listaPossiveisTrabalhosProducao:
                for dicionarioTrabalhoProduzirProduzindo in listaTrabalhosProducaoProduzirProduzindo:
                    condicoes = dicionarioTrabalhoProduzirProduzindo.ehProduzindo() and textoEhIgual(dicionarioTrabalhoProduzirProduzindo.pegaNome(), possivelTrabalhoProducao.pegaNome())
                    if condicoes:
                        return dicionarioTrabalhoProduzirProduzindo
            else:
                print(f'Trabalho concluído ({listaPossiveisTrabalhosProducao[0].pegaNome()}) não encontrado na lista produzindo...')
                return listaPossiveisTrabalhosProducao[0]
        return None

    def iniciaBuscaTrabalho(self, dicionarioTrabalho):
        self.defineChaveListaDicionariosProfissoesNecessarias()
        indiceProfissao = 0
        dicionarioTrabalho[CHAVE_POSICAO] = -1
        while indiceProfissao < len(self._dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSOES_NECESSARIAS]):
            if self.vaiParaMenuProduzir():
                profissaoNecessaria = self._dicionarioPersonagemAtributos[CHAVE_LISTA_PROFISSOES_NECESSARIAS][indiceProfissao]
                if not self._confirmacao or not chaveUnicaConexaoEhVerdadeira(self._dicionarioPersonagemAtributos):
                    break
                elif not existeEspacoProducao(self._dicionarioPersonagemAtributos):
                    indiceProfissao += 1
                    continue
                if listaProfissoesFoiModificada(self._dicionarioPersonagemAtributos):
                    self.verificaEspacoProducao()
                entraProfissaoEspecifica(profissaoNecessaria)
                print(f'Verificando profissão: {profissaoNecessaria.pegaNome()}')
                dicionarioTrabalho[CHAVE_PROFISSAO] = profissaoNecessaria.pegaNome()
                dicionarioTrabalho[CHAVE_CONFIRMACAO] = True
                listaDeListasTrabalhosProducao = self.retornaListaDeListasTrabalhosProducao(dicionarioTrabalho)
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
                                nomeTrabalhoReconhecido = self.retornaNomeTrabalhoPosicaoTrabalhoRaroEspecial(dicionarioTrabalho)
                                print(f'Trabalho {trabalhoProducaoPriorizado.pegaRaridade()} reconhecido: {nomeTrabalhoReconhecido}.')
                                if variavelExiste(nomeTrabalhoReconhecido):
                                    if texto1PertenceTexto2(nomeTrabalhoReconhecido, trabalhoProducaoPriorizado.pegaNomeProducao()):
                                        dicionarioTrabalho[CHAVE_CONFIRMACAO] = True
                                        erro = self.verificaErro()
                                        if erroEncontrado(erro):
                                            if ehErroOutraConexao(erro) or ehErroConectando(erro) or ehErroRestauraConexao(erro):
                                                dicionarioTrabalho[CHAVE_CONFIRMACAO] = False
                                                if ehErroOutraConexao(erro):
                                                    dicionarioTrabalho[CHAVE_UNICA_CONEXAO] = False
                                        else:
                                            entraTrabalhoEncontrado(dicionarioTrabalho)
                                        if self._confirmacao:
                                            dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = trabalhoProducaoPriorizado
                                            tipoTrabalho = 0
                                            if trabalhoEhProducaoRecursos(dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO]):
                                                tipoTrabalho = 1
                                            dicionarioTrabalho = self.confirmaNomeTrabalhoProducao(dicionarioTrabalho, tipoTrabalho)
                                            if not chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
                                                clickEspecifico(1,'f1')
                                                clickContinuo(dicionarioTrabalho[CHAVE_POSICAO] + 1, 'up')
                                        else:
                                            break
                                else:
                                    dicionarioTrabalho[CHAVE_POSICAO] = 4
                                dicionarioTrabalho = self.incrementaChavePosicaoTrabalho(dicionarioTrabalho)
                            dicionarioTrabalho[CHAVE_POSICAO] = posicaoAux
                            if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not self._confirmacao:
                                break
                        elif trabalhoProducaoPriorizado.ehMelhorado() or trabalhoProducaoPriorizado.ehComum():
                            dicionarioTrabalho = self.defineDicionarioTrabalhoComumMelhorado(dicionarioTrabalho)
                            self._confirmacao = dicionarioTrabalho[CHAVE_CONFIRMACAO]
                            if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not self._confirmacao:
                                break
                            elif indiceLista + 1 >= len(listaDeListasTrabalhosProducao):
                                vaiParaMenuTrabalhoEmProducao()
                            else:
                                vaiParaOTopoDaListaDeTrabalhosComunsEMelhorados(dicionarioTrabalho)
                        if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not self._confirmacao:
                            break
                    if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not self._confirmacao:
                        break
                    else:
                        indiceLista += 1
                        dicionarioTrabalho[CHAVE_POSICAO] = -1
                if self._confirmacao:
                    if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
                        dicionarioTrabalho = self.iniciaProcessoDeProducao(dicionarioTrabalho)
                    else:
                        saiProfissaoVerificada(dicionarioTrabalho)
                        indiceProfissao += 1
                        dicionarioTrabalho[CHAVE_POSICAO] = -1
                    if chaveUnicaConexaoEhVerdadeira(self._dicionarioPersonagemAtributos):
                        if chaveEspacoBolsaForVerdadeira(self._dicionarioPersonagemAtributos):
                            if self._imagem.retornaEstadoTrabalho() == CODIGO_CONCLUIDO:
                                nomeTrabalhoConcluido = self.reconheceRecuperaTrabalhoConcluido()
                                if variavelExiste(nomeTrabalhoConcluido):
                                    trabalhoProducaoConcluido = self.retornaTrabalhoProducaoConcluido(nomeTrabalhoConcluido)
                                    if variavelExiste(trabalhoProducaoConcluido):
                                        trabalhoProducaoConcluido = self.modificaTrabalhoConcluidoListaProduzirProduzindo(trabalhoProducaoConcluido)
                                        self.modificaExperienciaProfissao(trabalhoProducaoConcluido)
                                        self.atualizaEstoquePersonagem(trabalhoProducaoConcluido)
                                        self.verificaProducaoTrabalhoRaro(trabalhoProducaoConcluido)
                                    else:
                                        print(f'Dicionário trabalho concluido não reconhecido.')
                                else:
                                    print(f'Dicionário trabalho concluido não reconhecido.')
                            elif not existeEspacoProducao(self._dicionarioPersonagemAtributos):
                                break
                        dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = None
                        clickContinuo(3,'up')
                        clickEspecifico(1,'left')
                        sleep(1.5)
            else:
                break
        else:
            if listaProfissoesFoiModificada(self._dicionarioPersonagemAtributos):
                self.verificaEspacoProducao()
            print(f'Fim da lista de profissões...')

    def retornaListaDeListasTrabalhosProducao(self, dicionarioTrabalho):
        listaDeListaTrabalhos = []
        listaTrabalhoProducaoEspecial = self.retornaListaDicionariosTrabalhosProducaoRaridadeEspecifica(dicionarioTrabalho, raridade = CHAVE_RARIDADE_ESPECIAL)
        if not tamanhoIgualZero(listaTrabalhoProducaoEspecial):
            listaTrabalhoProducaoEspecial = sorted(listaTrabalhoProducaoEspecial,key=lambda dicionario:dicionario[CHAVE_NOME])
            listaDeListaTrabalhos.append(listaTrabalhoProducaoEspecial)
        listaTrabalhosProducaoRaros = self.retornaListaDicionariosTrabalhosProducaoRaridadeEspecifica(dicionarioTrabalho, raridade = CHAVE_RARIDADE_RARO)
        if not tamanhoIgualZero(listaTrabalhosProducaoRaros):
            listaTrabalhosProducaoRaros = sorted(listaTrabalhosProducaoRaros,key=lambda trabalhoProducao:trabalhoProducao.pegaNome())
            listaDeListaTrabalhos.append(listaTrabalhosProducaoRaros)
        listaTrabalhosProducaoMelhorados = self.retornaListaDicionariosTrabalhosProducaoRaridadeEspecifica(dicionarioTrabalho, raridade = CHAVE_RARIDADE_MELHORADO)
        if not tamanhoIgualZero(listaTrabalhosProducaoMelhorados):
            listaTrabalhosProducaoMelhorados = sorted(listaTrabalhosProducaoMelhorados,key=lambda trabalhoProducao:trabalhoProducao.pegaNome())
            listaDeListaTrabalhos.append(listaTrabalhosProducaoMelhorados)
        listaTrabalhosProducaoComuns = self.retornaListaDicionariosTrabalhosProducaoRaridadeEspecifica(dicionarioTrabalho, raridade = CHAVE_RARIDADE_COMUM)
        if not tamanhoIgualZero(listaTrabalhosProducaoComuns):
            listaTrabalhosProducaoComuns = sorted(listaTrabalhosProducaoComuns,key=lambda trabalhoProducao:trabalhoProducao.pegaNome())
            listaDeListaTrabalhos.append(listaTrabalhosProducaoComuns)
        return listaDeListaTrabalhos

    def retiraPersonagemListaAtivo(self):
        self.defineListaPersonagensAtivos()
        novaListaPersonagensAtivos = []
        for personagemAtivo in self._listaPersonagemAtivo:
            for personagemRemovido in self._listaPersonagemJaVerificado:
                if textoEhIgual(personagemAtivo.pegaNome(), personagemRemovido.pegaNome()):
                    break
            else:
                novaListaPersonagensAtivos.append(personagemAtivo)
        self._listaPersonagemAtivo = novaListaPersonagensAtivos

    def logaContaPersonagem(self):
        confirmacao=False
        email=self._listaPersonagemAtivo[0].pegaEmail()
        senha=self._listaPersonagemAtivo[0].pegaSenha()
        print(f'Tentando logar conta personagem...')
        preencheCamposLogin(email,senha)
        tentativas=1
        erro=self.verificaErro()
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
            erro=self.verificaErro()
        else:
            print(f'Login efetuado com sucesso!')
            confirmacao=True
        return confirmacao

    def configuraLoginPersonagem(self):
        menu = self.retornaMenu()
        while not ehMenuJogar(menu):
            ehMenuJogar(menu)
            if menu == MENU_NOTICIAS or ehMenuEscolhaPersonagem(menu):
                clickEspecifico(1, 'f1')
            elif menu != MENU_INICIAL:
                clickMouseEsquerdo(1, 2, 35)
            else:
                encerraSecao()
            menu = self.retornaMenu()
        else:
            login = self.logaContaPersonagem()
        return login

    def entraPersonagemAtivo(self):
        contadorPersonagem = 0
        menu = self.retornaMenu()
        if ehMenuJogar(menu):
            print(f'Buscando personagem ativo...')
            clickEspecifico(1, 'enter')
            sleep(1)
            tentativas = 1
            erro = self.verificaErro()
            while erroEncontrado(erro):
                if ehErroConectando(erro):
                    if tentativas > 10:
                        clickEspecifico(2, 'enter')
                        tentativas = 0
                    tentativas += 1
                erro = self.verificaErro()
                continue
            clickEspecifico(1, 'f2')
            clickContinuo(10, 'left')   
            personagemReconhecido = self._imagem.retornaTextoNomePersonagemReconhecido(1)
            while variavelExiste(personagemReconhecido) and contadorPersonagem < 13:
                self.confirmaNomePersonagem(personagemReconhecido)
                if variavelExiste(self._personagemEmUso):
                    self.modificaAtributoUso(True)
                    clickEspecifico(1, 'f2')
                    sleep(1)
                    print(f'Personagem ({self._personagemEmUso.pegaNome()}) encontrado.')
                    tentativas = 1
                    erro = self.verificaErro()
                    while erroEncontrado(erro):
                        if ehErroOutraConexao(erro):
                            self._unicaConexao = False
                            contadorPersonagem = 14
                            break
                        if ehErroConectando(erro):
                            if tentativas > 10:
                                clickEspecifico(2, 'enter')
                                tentativas = 0
                            tentativas += 1
                        erro = self.verificaErro()
                        continue
                    print(f'Login efetuado com sucesso!')
                    return
                clickEspecifico(1, 'right')
                personagemReconhecido = self._imagem.retornaTextoNomePersonagemReconhecido(1)
                contadorPersonagem += 1
            print(f'Personagem não encontrado!')
            if ehMenuEscolhaPersonagem(self.retornaMenu()):
                clickEspecifico(1, 'f1')
                return
        if ehMenuInicial(menu):
            self.deslogaPersonagem()
            return
        clickMouseEsquerdo(1,2,35)

    def iniciaProcessoBusca(self):
        self.defineListaPersonagensAtivos()
        while True:
            listaPersonagensAtivosEstaVazia = tamanhoIgualZero(self._listaPersonagemAtivo)
            if listaPersonagensAtivosEstaVazia:
                self._listaPersonagem = self._repositorioPersonagem.pegaTodosPersonagens()
                self._listaPersonagemJaVerificado.clear()
                self.defineListaPersonagensAtivos()
                continue
            self.definePersonagemEmUso()
            if variavelExiste(self._personagemEmUso):
                self.modificaAtributoUso(True)
                print(f'Personagem ({self._personagemEmUso.pegaNome()}) ESTÁ EM USO.')
                self.inicializaChavesPersonagem()
                print('Inicia busca...')
                if self.vaiParaMenuProduzir():
                    # while defineTrabalhoComumProfissaoPriorizada():
                    #     continue
                    listaTrabalhoProducaoParaProduzirProduzindo = self._repositorioTrabalhoProducao.retornaListaTrabalhosProducaoParaProduzirProduzindo()
                    if not tamanhoIgualZero(listaTrabalhoProducaoParaProduzirProduzindo):
                        dicionarioTrabalho = {
                            CHAVE_LISTA_TRABALHOS_PRODUCAO: listaTrabalhoProducaoParaProduzirProduzindo,
                            CHAVE_TRABALHO_PRODUCAO_ENCONTRADO: None}
                        if self._autoProducaoTrabalho:
                            self.verificaProdutosRarosMaisVendidos(None)
                        self.iniciaBuscaTrabalho(dicionarioTrabalho)
                    else:
                        print(f'Lista de trabalhos desejados vazia.')
                        self._repositorioPersonagem.alternaEstado(self._personagemEmUso)
                if self._unicaConexao:
                    if haMaisQueUmPersonagemAtivo(self._listaPersonagemAtivo):
                        clickMouseEsquerdo(1, 2, 35)
                self._listaPersonagemJaVerificado.append(self._personagemEmUso)
                self.retiraPersonagemListaAtivo()
                continue
            if tamanhoIgualZero(self._listaPersonagemJaVerificado):
                if self.configuraLoginPersonagem():
                    self.entraPersonagemAtivo()
                continue
            if textoEhIgual(self._listaPersonagemJaVerificado[-1].pegaEmail(), self._listaPersonagemAtivo[0].pegaEmail()):
                self.entraPersonagemAtivo()
                continue
            if self.configuraLoginPersonagem():
                self.entraPersonagemAtivo()
        
    def preparaPersonagem(self):
        clickAtalhoEspecifico('alt', 'tab')
        clickAtalhoEspecifico('win', 'left')
        self.iniciaProcessoBusca()

def teste():
    imagem = ManipulaImagem()
    imagem.retornaReferenciaTeste()

if __name__=='__main__':
    # Aplicacao().preparaPersonagem()
    teste()
    # print(self.imagem.reconheceTextoNomePersonagem(self.imagem.abreImagem('tests/imagemTeste/testeMenuTrabalhoProducao.png'), 1))