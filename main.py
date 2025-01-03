from teclado import *
from constantes import *
from utilitarios import *
from imagem import ManipulaImagem
from time import sleep
import datetime
import uuid
import logging
import re

from modelos.trabalhoRecurso import TrabalhoRecurso
from modelos.trabalho import Trabalho
from modelos.trabalhoVendido import TrabalhoVendido
from modelos.trabalhoProducao import TrabalhoProducao
from modelos.trabalhoEstoque import TrabalhoEstoque
from modelos.personagem import Personagem
from modelos.profissao import Profissao

from dao.personagemDaoSqlite import PersonagemDaoSqlite
from dao.trabalhoDaoSqlite import TrabalhoDaoSqlite
from dao.profissaoDaoSqlite import ProfissaoDaoSqlite
from dao.vendaDaoSqlite import VendaDaoSqlite
from dao.estoqueDaoSqlite import EstoqueDaoSqlite
from dao.trabalhoProducaoDaoSqlite import TrabalhoProducaoDaoSqlite

from repositorio.repositorioPersonagem import RepositorioPersonagem
from repositorio.repositorioTrabalho import RepositorioTrabalho
from repositorio.repositorioProfissao import RepositorioProfissao
from repositorio.repositorioTrabalhoProducao import RepositorioTrabalhoProducao
from repositorio.repositorioVendas import RepositorioVendas

class Aplicacao:
    def __init__(self) -> None:
        logging.basicConfig(level = logging.INFO, filename = 'logs/aplicacao.log', encoding='utf-8', format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt = '%d/%m/%Y %I:%M:%S %p')
        self.__loggerRepositorioTrabalho = logging.getLogger('repositorioTrabalho')
        self.__loggerRepositorioPersonagem = logging.getLogger('repositorioPersonagem')
        self.__loggerRepositorioProfissao = logging.getLogger('repositorioProfissao')
        self.__loggerPersonagemDao = logging.getLogger('personagemDao')
        self.__loggerTrabalhoProducaoDao = logging.getLogger('trabalhoProducaoDao')
        self.__loggerTrabalhoDao = logging.getLogger('trabalhoDao')
        self.__loggerVendaDao = logging.getLogger('vendaDao')
        self.__loggerProfissaoDao = logging.getLogger('profissaoDao')
        self.__loggerEstoqueDao = logging.getLogger('estoqueDao')
        self._imagem = ManipulaImagem()
        self.__listaPersonagemJaVerificado = []
        self.__listaPersonagemAtivo = []
        self.__listaProfissoesNecessarias = []
        self.__personagemEmUso = None
        self.__repositorioTrabalho = RepositorioTrabalho()
        self.__repositorioPersonagem = RepositorioPersonagem()

    def personagemEmUso(self, personagem):
        self.__personagemEmUso = personagem

    def defineListaPersonagemMesmoEmail(self):
        listaDicionarioPersonagemMesmoEmail = []
        if variavelExiste(self.__personagemEmUso):
            personagens = self.pegaPersonagens()
            for personagem in personagens:
                if textoEhIgual(personagem.email, self.__personagemEmUso.email):
                    listaDicionarioPersonagemMesmoEmail.append(personagem)
        return listaDicionarioPersonagemMesmoEmail

    def modificaAtributoUso(self): 
        listaPersonagemMesmoEmail = self.defineListaPersonagemMesmoEmail()
        personagens = self.pegaPersonagens()
        for personagem in personagens:
            for personagemMesmoEmail in listaPersonagemMesmoEmail:
                if textoEhIgual(personagem.id, personagemMesmoEmail.id) and not personagem.uso:
                    personagem.alternaUso()
                    self.modificaPersonagem(personagem)
                    break
            else:
                if personagem.uso:
                    personagem.alternaUso()
                    self.modificaPersonagem(personagem)

    def confirmaNomePersonagem(self, personagemReconhecido):
        '''
        Esta função é responsável por confirmar se o nome do personagem reconhecido está na lista de personagens ativos atual
        Argumentos:
            personagemReconhecido {string} -- Valor reconhecido via processamento de imagem
        '''
        for personagemAtivo in self.__listaPersonagemAtivo:
            if textoEhIgual(personagemReconhecido, personagemAtivo.nome):
                print(f'Personagem {personagemReconhecido} confirmado!')
                self.personagemEmUso(personagemAtivo)
                return
        print(f'Personagem {personagemReconhecido} não encontrado na lista de personagens ativos atual!')

    def definePersonagemEmUso(self):
        '''
        Esta função é responsável por atribuir ao atributo __personagemEmUso o objeto da classe Personagem que foi reconhecida 
        '''
        self.__personagemEmUso = None
        nomePersonagemReconhecido = self._imagem.retornaTextoNomePersonagemReconhecido(0)
        if variavelExiste(nomePersonagemReconhecido):
            self.confirmaNomePersonagem(nomePersonagemReconhecido)
            return
        if nomePersonagemReconhecido == 'provisorioatecair':
            print(f'Nome personagem diferente!')
            return
        print(f'Nome personagem não reconhecido!')

    def defineListaPersonagensAtivos(self):
        '''
        Esta função é responsável por preencher a lista de personagens ativos, recuperando os dados do banco
        '''
        print(f'Definindo lista de personagem ativo')
        personagens = self.pegaPersonagens()
        self.__listaPersonagemAtivo.clear()
        for personagem in personagens:
            if personagem.ehAtivo():
                self.__listaPersonagemAtivo.append(personagem)

    def inicializaChavesPersonagem(self):
        self._autoProducaoTrabalho = self.__personagemEmUso.autoProducao
        self._unicaConexao = True
        self._espacoBolsa = True
        self.__confirmacao = True
        self._profissaoModificada = False

    def retornaCodigoErroReconhecido(self):
        textoErroEncontrado = self._imagem.retornaErroReconhecido()
        if variavelExiste(textoErroEncontrado):
            textoErroEncontrado = limpaRuidoTexto(textoErroEncontrado)
            textoErroEncontrado = retiraDigitos(textoErroEncontrado)
            tipoErro = ['Você precisa de uma licença de artesanato para iniciar este pedido',
                'Falha ao se conectar ao servidor',
                'Você precisa de mais recursos parainiciar este pedido',
                'Selecione um item para iniciar umpedido de artesanato',
                'Conectando',
                'Você precisa de mais experiência de produção para iniciar este pedido',
                'Você recebeu um novo presenteDessgja ir à Loja Milagrosa paraconferir',
                'Todos os espaços de artesanato estão ocupados',
                'Tem certeza de que deseja concluir aprodução',
                'Estamos fazendo de tudo paraconcluíla o mais rápido possível',
                'No momento esta conta está sendousada em outro dispositivo',
                'Gostanadecomprar',
                'Conexão perdida com o servidor',
                'Você precisa de mais',
                'Nome de usuário ou senha inválida',
                'Pedido de artesanato expirado',
                'O reino selecionado está indisponível',
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
        if variavelExiste(textoMenu) and texto1PertenceTexto2('spearonline',textoMenu):
            posicao = self._imagem.retornaPosicaoFrameMenuReconhecido()
            if variavelExiste(posicao):
                textoMenu = self._imagem.retornaTextoMenuReconhecido(posicao[0], posicao[1], posicao[2], posicao[3])
                if variavelExiste(textoMenu):
                    if texto1PertenceTexto2('recompensasdiarias',textoMenu):
                        print(f'Menu recompensas diárias...')
                        return MENU_RECOMPENSAS_DIARIAS
                    if texto1PertenceTexto2('selecioneopersonagem',textoMenu):
                        print(f'Menu escolha de personagem...')
                        return MENU_ESCOLHA_PERSONAGEM
                    if texto1PertenceTexto2('artesanato',textoMenu):
                        if texto1PertenceTexto2('pedidosativos',textoMenu):
                            print(f'Menu trabalhos atuais...')
                            return MENU_TRABALHOS_ATUAIS
                        if texto1PertenceTexto2('profissoes',textoMenu):
                            textoMenu=self._imagem.retornaTextoMenuReconhecido(191,612,100)
                            if variavelExiste(textoMenu):
                                if texto1PertenceTexto2('fechar',textoMenu):
                                    print(f'Menu produzir...')
                                    return MENU_PROFISSOES
                                if texto1PertenceTexto2('voltar',textoMenu):
                                    print(f'Menu trabalhos diponíveis...')
                                    return MENU_TRABALHOS_DISPONIVEIS
            textoMenu=self._imagem.retornaTextoMenuReconhecido(216,197,270)
            if variavelExiste(textoMenu) and texto1PertenceTexto2('noticias',textoMenu):
                print(f'Menu notícias...')
                return MENU_NOTICIAS
            textoMenu = self._imagem.retornaTextoSair()
            if variavelExiste(textoMenu) and textoEhIgual(textoMenu,'sair'):
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
            if variavelExiste(textoMenu) and texto1PertenceTexto2('parâmetros',textoMenu):
                if texto1PertenceTexto2('requisitos',textoMenu):
                    print(f'Menu atributo do trabalho...')
                    return MENU_TRABALHOS_ATRIBUTOS
                else:
                    print(f'Menu licenças...')
                    return MENU_LICENSAS
            textoMenu=self._imagem.retornaTextoMenuReconhecido(275,400,150)
            if variavelExiste(textoMenu) and texto1PertenceTexto2('Recompensa',textoMenu):
                print(f'Menu trabalho específico...')
                return MENU_TRABALHO_ESPECIFICO
            textoMenu=self._imagem.retornaTextoMenuReconhecido(266,269,150)
            if variavelExiste(textoMenu) and texto1PertenceTexto2('ofertadiaria',textoMenu):
                print(f'Menu oferta diária...')
                return MENU_OFERTA_DIARIA
            textoMenu=self._imagem.retornaTextoMenuReconhecido(181,75,150)
            if variavelExiste(textoMenu) and texto1PertenceTexto2('Loja Milagrosa',textoMenu):
                print(f'Menu loja milagrosa...')
                return MENU_LOJA_MILAGROSA
            # textoMenu=self._imagem.retornaTextoMenuReconhecido(180,40,300)
            textoMenu=self._imagem.retornaTextoMenuReconhecido(180,60,300)
            if variavelExiste(textoMenu) and texto1PertenceTexto2('recompensasdiarias',textoMenu):
                print(f'Menu recompensas diárias...')
                return MENU_RECOMPENSAS_DIARIAS
            textoMenu=self._imagem.retornaTextoMenuReconhecido(310,338,57)
            if variavelExiste(textoMenu) and texto1PertenceTexto2('meu',textoMenu):
                print(f'Menu meu perfil...')
                return MENU_MEU_PERFIL           
            textoMenu=self._imagem.retornaTextoMenuReconhecido(169,97,75)
            if variavelExiste(textoMenu) and texto1PertenceTexto2('Bolsa',textoMenu):
                print(f'Menu bolsa...')
                return MENU_BOLSA
            clickMouseEsquerdo(1,35,35)
        print(f'Menu não reconhecido...')
        self.verificaErro()
        return MENU_DESCONHECIDO
    
    def retornaValorTrabalhoVendido(self, textoCarta):
        listaTextoCarta = textoCarta.split()
        for palavra in listaTextoCarta:
            if textoEhIgual(palavra, 'por') and listaTextoCarta.index(palavra)+1 < len(listaTextoCarta):
                valorProduto = listaTextoCarta[listaTextoCarta.index(palavra)+1].strip()
                if valorProduto.isdigit():
                    return int(valorProduto)
        return 0

    def retornaQuantidadeTrabalhoVendido(self, textoCarta):
        listaTextoCarta = textoCarta.split()
        for texto in listaTextoCarta:
            if texto1PertenceTexto2('x', texto):
                valor = texto.replace('x', '').strip()
                if valor.isdigit():
                    print(f'quantidadeProduto:{valor}')
                    return int(valor)
        return 1

    def retornaConteudoCorrespondencia(self):
        textoCarta = self._imagem.retornaTextoCorrespondenciaReconhecido()
        if variavelExiste(textoCarta):
            trabalhoFoiVendido = texto1PertenceTexto2('Item vendido', textoCarta)
            if trabalhoFoiVendido:
                print(f'Produto vendido')
                textoCarta = re.sub("Item vendido", "", textoCarta).strip()
                trabalhoVendido = TrabalhoVendido()
                trabalhoVendido.nomeProduto = textoCarta
                trabalhoVendido.dataVenda = str(datetime.date.today())
                trabalhoVendido.nomePersonagem = self.__personagemEmUso.id
                trabalhoVendido.setQuantidade(self.retornaQuantidadeTrabalhoVendido(textoCarta))
                trabalhoVendido.trabalhoId = self.retornaChaveIdTrabalho(textoCarta)
                trabalhoVendido.setValor(self.retornaValorTrabalhoVendido(textoCarta))
                vendaDAO = VendaDaoSqlite(self.__personagemEmUso)
                if vendaDAO.insereTrabalhoVendido(trabalhoVendido):
                    self.__loggerVendaDao.info(f'({trabalhoVendido}) inserido com sucesso!')
                    return trabalhoVendido
                self.__loggerVendaDao.error(f'Erro ao inserir ({trabalhoVendido}): {vendaDAO.pegaErro()}')
        return None

    def retornaChaveIdTrabalho(self, textoCarta):
        trabalhos = self.pegaTrabalhosBanco()
        for trabalho in trabalhos:
            if texto1PertenceTexto2(trabalho.nome, textoCarta):
                return trabalho.id
        return ''

    def atualizaQuantidadeTrabalhoEstoque(self, venda):
        logger = logging.getLogger('estoqueDao')
        estoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
        estoque = estoqueDao.pegaEstoque()
        if variavelExiste(estoque):
            for trabalhoEstoque in estoque:
                if textoEhIgual(trabalhoEstoque.trabalhoId, venda.trabalhoId):
                    novaQuantidade = trabalhoEstoque.quantidade - venda.quantidadeProduto
                    trabalhoEstoque.quantidade = novaQuantidade
                    estoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
                    if estoqueDao.modificaTrabalhoEstoque(trabalhoEstoque):
                        logger.info(f'Quantidade de ({trabalhoEstoque}) atualizada para {novaQuantidade}.')
                        return
                    logger.error(f'Erro ao modificar ({trabalhoEstoque}) no estoque: {estoqueDao.pegaErro()}')
                    return
            logger.warning(f'Trabalho ({venda}) não encontrado no estoque.')
            return
        logger.error(f'Erro ao pegar trabalhos no estoque: {estoqueDao.pegaErro()}')

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
            self.__loggerTrabalhoProducaoDao.info(f'Trabalho concluido reconhecido: {nomeTrabalhoConcluido}')
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
        trabalhos = self.pegaTrabalhosBanco()
        for trabalho in trabalhos:
            if texto1PertenceTexto2(nomeTrabalhoConcluido[1:-1], trabalho.nomeProducao):
                listaPossiveisDicionariosTrabalhos.append(trabalho)
        return listaPossiveisDicionariosTrabalhos
    
    def insereTrabalhoProducao(self, trabalhoProducao: TrabalhoProducao, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        if variavelExiste(trabalhoProducao):
            personagem = self.__personagemEmUso if personagem is None else personagem
            trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
            if trabalhoProducaoDao.insereTrabalhoProducao(trabalhoProducao, modificaServidor):
                self.__loggerTrabalhoProducaoDao.info(f'({trabalhoProducao}) inserido no banco com sucesso!')
                return True
            self.__loggerTrabalhoProducaoDao.error(f'Erro ao inserir ({trabalhoProducao}) no banco: {trabalhoProducaoDao.pegaErro()}')
            return False
        
    def pegaTrabalhosProducaoParaProduzirProduzindo(self, personagem: Personagem = None) -> list[TrabalhoProducao]:
        personagem = self.__personagemEmUso if personagem is None else personagem
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
        trabalhosProducaoProduzirProduzindo = trabalhoProducaoDao.pegaTrabalhosProducaoParaProduzirProduzindo()
        if trabalhosProducaoProduzirProduzindo is None:
            self.__loggerTrabalhoProducaoDao.error(f'Erro ao bucar trabalhos para produção com estado 0 ou 1: {trabalhoProducaoDao.pegaErro()}')
            return None
        return trabalhosProducaoProduzirProduzindo

    def retornaTrabalhoConcluido(self, nomeTrabalhoConcluido: str) -> TrabalhoProducao:
        listaPossiveisTrabalhos = self.retornaListaPossiveisTrabalhoRecuperado(nomeTrabalhoConcluido)
        if tamanhoIgualZero(listaPossiveisTrabalhos):
            return None
        for possivelTrabalho in listaPossiveisTrabalhos:
            trabalhosProducao = self.pegaTrabalhosProducaoParaProduzirProduzindo()
            if variavelExiste(trabalhosProducao):
                for trabalhoProduzirProduzindo in trabalhosProducao:
                    nomeEhIgualEEstadoEhProduzindo = trabalhoProduzirProduzindo.ehProduzindo() and textoEhIgual(trabalhoProduzirProduzindo.nome, possivelTrabalho.nome)
                    if nomeEhIgualEEstadoEhProduzindo:
                        trabalhoProduzirProduzindo.estado = CODIGO_CONCLUIDO
                        self.__loggerTrabalhoProducaoDao.info(f'({trabalhoProduzirProduzindo}) encontrado na lista de produção')
                        return trabalhoProduzirProduzindo
        else:
            self.__loggerTrabalhoProducaoDao.warning(f'({nomeTrabalhoConcluido}) concluido não encontrado na lista de produção...')
            trabalhoProducaoConcluido = TrabalhoProducao()
            trabalhoProducaoConcluido.idTrabalho = listaPossiveisTrabalhos[0].id
            trabalhoProducaoConcluido.recorrencia = False
            trabalhoProducaoConcluido.tipo_licenca = CHAVE_LICENCA_NOVATO
            trabalhoProducaoConcluido.estado = CODIGO_CONCLUIDO
            self.insereTrabalhoProducao(trabalhoProducaoConcluido)
            return trabalhoProducaoConcluido
        
    def removeTrabalhoProducao(self, trabalho: TrabalhoProducao, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
        if trabalhoProducaoDao.removeTrabalhoProducao(trabalho, modificaServidor):
            self.__loggerTrabalhoProducaoDao.info(f'({trabalho}) removido do banco com sucesso!')
            return True
        self.__loggerTrabalhoProducaoDao.error(f'Erro ao remover ({trabalho}) do banco: {trabalhoProducaoDao.pegaErro()}')
        return False
    
    def modificaTrabalhoProducao(self, trabalho: TrabalhoProducao, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        trabalhoProducao = TrabalhoProducao()
        trabalhoProducao.id = trabalho.id
        trabalhoProducao.idTrabalho = trabalho.idTrabalho
        trabalhoProducao.recorrencia = trabalho.recorrencia
        trabalhoProducao.tipo_licenca = trabalho.tipo_licenca
        trabalhoProducao.estado = trabalho.estado
        personagem = self.__personagemEmUso if personagem is None else personagem
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
        if trabalhoProducaoDao.modificaTrabalhoProducao(trabalhoProducao, modificaServidor):
            self.__loggerTrabalhoProducaoDao.info(f'({trabalhoProducao}) modificado no banco com sucesso!')
            return True
        self.__loggerTrabalhoProducaoDao.error(f'Erro ao modificar ({trabalhoProducao}) no banco: {trabalhoProducaoDao.pegaErro()}')
        return False


    def modificaTrabalhoConcluidoListaProduzirProduzindo(self, trabalhoProducaoConcluido):
        if trabalhoEhProducaoRecursos(trabalhoProducaoConcluido):
            trabalhoProducaoConcluido.recorrencia = True
        if trabalhoProducaoConcluido.recorrencia:
            print(f'Trabalho recorrente.')
            self.removeTrabalhoProducao(trabalhoProducaoConcluido)
            return
        print(f'Trabalho sem recorrencia.')
        self.modificaTrabalhoProducao(trabalhoProducaoConcluido)

    def modificaExperienciaProfissao(self, trabalhoProducao):
        profissaoDao = ProfissaoDaoSqlite(self.__personagemEmUso)
        profissoes = profissaoDao.pegaProfissoes()
        if not variavelExiste(profissoes):
            logger = logging.getLogger('profissaoDao')
            logger.error(f'Erro ao buscar profissões: {profissaoDao.pegaErro()}')
            print(f'Erro ao buscar profissões: {profissaoDao.pegaErro()}')
            return
        for profissao in profissoes:
            if textoEhIgual(profissao.nome, trabalhoProducao.profissao):
                experiencia = profissao.experiencia + trabalhoProducao.experiencia
                profissao.setExperiencia(experiencia)
                profissaoDao = ProfissaoDaoSqlite(self.__personagemEmUso)
                if profissaoDao.modificaProfissao(profissao, True):
                    print(f'Experiência de {profissao.nome} atualizada para {experiencia}  com sucesso!')
                    return
                logger = logging.getLogger('profissaoDao')
                logger.error(f'Erro ao modificar profissão: {profissaoDao.pegaErro()}')
                print(f'Erro ao modificar profissão: {profissaoDao.pegaErro()}')
                return

    def retornaListaTrabalhoProduzido(self, trabalhoProducaoConcluido):
        '''
        Função que recebe um objeto TrabalhoProducao
        '''
        listaTrabalhoEstoqueConcluido = []
        trabalhoEstoque = None
        if trabalhoEhProducaoRecursos(trabalhoProducaoConcluido):
            if trabalhoEhProducaoLicenca(trabalhoProducaoConcluido):
                trabalhoEstoque = TrabalhoEstoque()
                trabalhoEstoque.nome = CHAVE_LICENCA_APRENDIZ
                trabalhoEstoque.profissao = ''
                trabalhoEstoque.nivel = 0
                trabalhoEstoque.quantidade = 2
                trabalhoEstoque.raridade = 'Recurso'
                trabalhoEstoque.trabalhoId = trabalhoProducaoConcluido.idTrabalho
            else:
                if trabalhoEhMelhoriaEssenciaComum(trabalhoProducaoConcluido):
                    trabalhoEstoque = TrabalhoEstoque()
                    trabalhoEstoque.nome = 'Essência composta'
                    trabalhoEstoque.profissao = ''
                    trabalhoEstoque.nivel = 0
                    trabalhoEstoque.quantidade = 5
                    trabalhoEstoque.raridade = 'Recurso'
                    trabalhoEstoque.trabalhoId = trabalhoProducaoConcluido.idTrabalho
                elif trabalhoEhMelhoriaEssenciaComposta(trabalhoProducaoConcluido):
                    trabalhoEstoque = TrabalhoEstoque()
                    trabalhoEstoque.nome = 'Essência de energia'
                    trabalhoEstoque.profissao = ''
                    trabalhoEstoque.nivel = 0
                    trabalhoEstoque.quantidade = 1
                    trabalhoEstoque.raridade = 'Recurso'
                    trabalhoEstoque.trabalhoId = trabalhoProducaoConcluido.idTrabalho
                elif trabalhoEhMelhoriaSubstanciaComum(trabalhoProducaoConcluido):
                    trabalhoEstoque = TrabalhoEstoque()
                    trabalhoEstoque.nome = 'Substância composta'
                    trabalhoEstoque.profissao = ''
                    trabalhoEstoque.nivel = 0
                    trabalhoEstoque.quantidade = 5
                    trabalhoEstoque.raridade = 'Recurso'
                    trabalhoEstoque.trabalhoId = trabalhoProducaoConcluido.idTrabalho
                elif trabalhoEhMelhoriaSubstanciaComposta(trabalhoProducaoConcluido):
                    trabalhoEstoque = TrabalhoEstoque()
                    trabalhoEstoque.nome = 'Substância energética'
                    trabalhoEstoque.profissao = ''
                    trabalhoEstoque.nivel = 0
                    trabalhoEstoque.quantidade = 1
                    trabalhoEstoque.raridade = 'Recurso'
                    trabalhoEstoque.trabalhoId = trabalhoProducaoConcluido.idTrabalho
                elif trabalhoEhMelhoriaCatalisadorComum(trabalhoProducaoConcluido):
                    trabalhoEstoque = TrabalhoEstoque()
                    trabalhoEstoque.nome = 'Catalisador amplificado'
                    trabalhoEstoque.profissao = ''
                    trabalhoEstoque.nivel = 0
                    trabalhoEstoque.quantidade = 5
                    trabalhoEstoque.raridade = 'Recurso'
                    trabalhoEstoque.trabalhoId = trabalhoProducaoConcluido.idTrabalho
                elif trabalhoEhMelhoriaCatalisadorComposto(trabalhoProducaoConcluido):
                    trabalhoEstoque = TrabalhoEstoque()
                    trabalhoEstoque.nome = 'Catalisador de energia'
                    trabalhoEstoque.profissao = ''
                    trabalhoEstoque.nivel = 0
                    trabalhoEstoque.quantidade = 1
                    trabalhoEstoque.raridade = 'Recurso'
                    trabalhoEstoque.trabalhoId = trabalhoProducaoConcluido.idTrabalho
                if variavelExiste(trabalhoEstoque):
                    if textoEhIgual(trabalhoProducaoConcluido.tipo_licenca, CHAVE_LICENCA_APRENDIZ):
                        trabalhoEstoque.quantidade = trabalhoEstoque.quantidade * 2
            if variavelExiste(trabalhoEstoque):
                listaTrabalhoEstoqueConcluido.append(trabalhoEstoque)
            if trabalhoEhColecaoRecursosComuns(trabalhoProducaoConcluido) or trabalhoEhColecaoRecursosAvancados(trabalhoProducaoConcluido):
                    nivelColecao = 1
                    if trabalhoEhColecaoRecursosAvancados(trabalhoProducaoConcluido):
                        nivelColecao = 8
                    trabalhos = self.pegaTrabalhosBanco()
                    for trabalho in trabalhos:
                        condicoes = textoEhIgual(trabalho.profissao, trabalhoProducaoConcluido.profissao) and trabalho.nivel == nivelColecao and textoEhIgual(trabalho.raridade, CHAVE_RARIDADE_COMUM)
                        if condicoes:
                            trabalhoEstoque = TrabalhoEstoque()
                            trabalhoEstoque.nome = trabalho.nome
                            trabalhoEstoque.profissao = trabalho.profissao
                            trabalhoEstoque.nivel = trabalho.nivel
                            trabalhoEstoque.quantidade = 1
                            trabalhoEstoque.raridade = trabalho.raridade
                            trabalhoEstoque.trabalhoId = trabalho.id
                            listaTrabalhoEstoqueConcluido.append(trabalhoEstoque)
                    for trabalhoEstoque in listaTrabalhoEstoqueConcluido:
                        tipoRecurso = retornaChaveTipoRecurso(trabalhoEstoque)
                        if variavelExiste(tipoRecurso):
                            if tipoRecurso == CHAVE_RCT:
                                trabalhoEstoque.quantidade = 2
                            if tipoRecurso == CHAVE_RAT or tipoRecurso == CHAVE_RCS:
                                trabalhoEstoque.quantidade = 3
                            elif tipoRecurso == CHAVE_RAS or tipoRecurso == CHAVE_RCP:
                                trabalhoEstoque.quantidade = 4
                            elif tipoRecurso == CHAVE_RAP:
                                trabalhoEstoque.quantidade = 5
                            if textoEhIgual(trabalhoProducaoConcluido.tipo_licenca, CHAVE_LICENCA_APRENDIZ):
                                trabalhoEstoque.quantidade = trabalhoEstoque.quantidade * 2
                        else:
                            print(f'Tipo de recurso não encontrado!')
            if tamanhoIgualZero(listaTrabalhoEstoqueConcluido):
                    trabalhoEstoque = TrabalhoEstoque()
                    trabalhoEstoque.nome = trabalhoProducaoConcluido.nome
                    trabalhoEstoque.profissao = trabalhoProducaoConcluido.profissao
                    trabalhoEstoque.nivel = trabalhoProducaoConcluido.nivel
                    trabalhoEstoque.quantidade = 0
                    trabalhoEstoque.raridade = trabalhoProducaoConcluido.raridade
                    trabalhoEstoque.trabalhoId = trabalhoProducaoConcluido.idTrabalho
                    tipoRecurso = retornaChaveTipoRecurso(trabalhoEstoque)
                    if variavelExiste(tipoRecurso):
                        if tipoRecurso == CHAVE_RCS or tipoRecurso == CHAVE_RCT:
                            trabalhoEstoque.quantidade = 1
                        elif tipoRecurso == CHAVE_RCP or tipoRecurso == CHAVE_RAP or tipoRecurso == CHAVE_RAS or tipoRecurso == CHAVE_RAT:
                            trabalhoEstoque.quantidade = 2
                        if textoEhIgual(trabalhoProducaoConcluido.tipo_licenca, CHAVE_LICENCA_APRENDIZ):
                            trabalhoEstoque.quantidade = trabalhoEstoque.quantidade * 2
                        listaTrabalhoEstoqueConcluido.append(trabalhoEstoque)
                    else:
                        print(f'Tipo de recurso não encontrado!')
        else:
            trabalhoEstoque = TrabalhoEstoque()
            trabalhoEstoque.nome = trabalhoProducaoConcluido.nome
            trabalhoEstoque.profissao = trabalhoProducaoConcluido.profissao
            trabalhoEstoque.nivel = trabalhoProducaoConcluido.nivel
            trabalhoEstoque.quantidade = 1
            trabalhoEstoque.raridade = trabalhoProducaoConcluido.raridade
            trabalhoEstoque.trabalhoId = trabalhoProducaoConcluido.idTrabalho
            listaTrabalhoEstoqueConcluido.append(trabalhoEstoque)
        print(f'Lista de dicionários trabalhos concluídos:')
        for trabalhoEstoqueConcluido in listaTrabalhoEstoqueConcluido:
                print(trabalhoEstoqueConcluido)
        return listaTrabalhoEstoqueConcluido

    def modificaQuantidadeTrabalhoEstoque(self, listaTrabalhoEstoqueConcluido, trabalhoEstoque):
        listaTrabalhoEstoqueConcluidoModificado = listaTrabalhoEstoqueConcluido
        for trabalhoEstoqueConcluido in listaTrabalhoEstoqueConcluido:
            if textoEhIgual(trabalhoEstoqueConcluido.nome, trabalhoEstoque.nome):
                novaQuantidade = trabalhoEstoque.quantidade + trabalhoEstoqueConcluido.quantidade
                trabalhoEstoque.quantidade = novaQuantidade
                print(trabalhoEstoque)
                estoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
                if estoqueDao.modificaTrabalhoEstoque(trabalhoEstoque):
                    print(f'Quantidade do trabalho ({trabalhoEstoque.nome}) atualizada para {novaQuantidade}.')
                    del listaTrabalhoEstoqueConcluidoModificado[listaTrabalhoEstoqueConcluido.index(trabalhoEstoqueConcluido)]
                    continue
                logger = logging.getLogger('estoqueDao')
                logger.error(f'Erro ao modificar trabalho no estoque: {estoqueDao.pegaErro()}')
                print(f'Erro ao modificar trabalho no estoque: {estoqueDao.pegaErro()}')
        return listaTrabalhoEstoqueConcluidoModificado, trabalhoEstoque

    def atualizaEstoquePersonagem(self, trabalhoEstoqueConcluido):
        loggerEstoque = logging.getLogger('estoqueDao')
        listaTrabalhoEstoqueConcluido = self.retornaListaTrabalhoProduzido(trabalhoEstoqueConcluido)
        if tamanhoIgualZero(listaTrabalhoEstoqueConcluido):
            return
        estoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
        estoque = estoqueDao.pegaEstoque()
        if variavelExiste(estoque):
            if tamanhoIgualZero(estoque):
                for trabalhoEstoqueConcluido in listaTrabalhoEstoqueConcluido:
                    trabalhoEstoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
                    if trabalhoEstoqueDao.insereTrabalhoEstoque(trabalhoEstoqueConcluido):
                        loggerEstoque.info(f'({trabalhoEstoqueConcluido}) inserido com sucesso!')
                        continue
                    loggerEstoque.error(f'Erro ao inserir trabalho ({trabalhoEstoqueConcluido}): {trabalhoEstoqueDao.pegaErro()}')
                return
            for trabalhoEstoque in estoque:
                listaTrabalhoEstoqueConcluido, trabalhoEstoque = self.modificaQuantidadeTrabalhoEstoque(listaTrabalhoEstoqueConcluido, trabalhoEstoque)
            if tamanhoIgualZero(listaTrabalhoEstoqueConcluido):
                return
            for trabalhoEstoqueConcluido in listaTrabalhoEstoqueConcluido:
                trabalhoEstoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
                if trabalhoEstoqueDao.insereTrabalhoEstoque(trabalhoEstoqueConcluido):
                    loggerEstoque.info(f'({trabalhoEstoqueConcluido}) inserido com sucesso!')
                    continue
                loggerEstoque.error(f'Erro ao inserir trabalho ({trabalhoEstoqueConcluido}): {trabalhoEstoqueDao.pegaErro()}')
            return
        loggerEstoque.error(f'Erro ao pegar trabalhos no estoque: {estoqueDao.pegaErro()}')

    def retornaProfissaoTrabalhoProducaoConcluido(self, trabalhoProducaoConcluido):
        profissaoDao = ProfissaoDaoSqlite(self.__personagemEmUso)
        profissoes = profissaoDao.pegaProfissoes()
        logger = logging.getLogger('profissaoDao')
        if variavelExiste(profissoes):
            for profissao in profissoes:
                if textoEhIgual(profissao.nome, trabalhoProducaoConcluido.profissao):
                    return profissao
            logger.warning(f'Erro ao buscar profissões ({self.__personagemEmUso}): lista de profissões vazia!')
            return None
        logger.error(f'Erro ao buscar profissões ({self.__personagemEmUso}): {profissaoDao.pegaErro()}')
        return None

    def verificaProducaoTrabalhoRaro(self, trabalhoProducaoConcluido):
        profissao = self.retornaProfissaoTrabalhoProducaoConcluido(trabalhoProducaoConcluido)
        if variavelExiste(profissao) and trabalhoProducaoConcluido.ehMelhorado():
            trabalhos = self.pegaTrabalhosBanco()
            for trabalho in trabalhos:
                trabalhoNecessarioEhIgualNomeTrabalhoConcluido = textoEhIgual(trabalho.trabalhoNecessario, trabalhoProducaoConcluido.nome)
                if trabalhoNecessarioEhIgualNomeTrabalhoConcluido:
                    return self.defineNovoTrabalhoProducaoRaro(profissao, trabalho)
        return None

    def defineNovoTrabalhoProducaoRaro(self, profissao, trabalho):
        licencaProducaoIdeal = CHAVE_LICENCA_NOVATO if profissao.pegaExperienciaMaximaPorNivel() >= profissao.pegaExperienciaMaxima() else CHAVE_LICENCA_INICIANTE
        trabalhoProducaoRaro = TrabalhoProducao()
        trabalhoProducaoRaro.dicionarioParaObjeto(trabalho.__dict__)
        trabalhoProducaoRaro.id = str(uuid.uuid4())
        trabalhoProducaoRaro.idTrabalho = trabalho.id
        trabalhoProducaoRaro.experiencia = trabalho.experiencia * 1.5
        trabalhoProducaoRaro.recorrencia = False
        trabalhoProducaoRaro.tipo_licenca = licencaProducaoIdeal
        trabalhoProducaoRaro.estado = CODIGO_PARA_PRODUZIR
        return trabalhoProducaoRaro

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
            referenciaEncontrada = self._imagem.verificaRecompensaDisponivel()
            if variavelExiste(referenciaEncontrada):
                print(f'Referência encontrada!')
                clickMouseEsquerdo(1, referenciaEncontrada[0], referenciaEncontrada[1])
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
        sleep(2)
        if menu == MENU_LOJA_MILAGROSA:
            clickEspecifico(1,'down')
            clickEspecifico(1,'enter')
            return False
        if menu == MENU_RECOMPENSAS_DIARIAS:
            self.recuperaPresente()
            return True
        print(f'Recompensa diária já recebida!')
        return True

    def deslogaPersonagem(self):
        menu = self.retornaMenu()
        while not ehMenuJogar(menu):
            tentativas = 0
            erro = self.verificaErro()
            while erroEncontrado(erro):
                if ehErroConectando(erro):
                    if tentativas > 10:
                        clickEspecifico(2, 'enter')
                        tentativas = 0
                    tentativas += 1
                erro = self.verificaErro()
                continue
            if ehMenuInicial(menu):
                encerraSecao()
                break
            if ehMenuJogar(menu):
                break
            if ehMenuEscolhaPersonagem(menu):
                clickEspecifico(1, 'f1')
                break
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
            if self.reconheceMenuRecompensa(menu):
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
        if menu == MENU_DESCONHECIDO:
            pass
        elif menu == MENU_TRABALHOS_ATUAIS:
            estadoTrabalho = self._imagem.retornaEstadoTrabalho()
            if estadoTrabalho == CODIGO_CONCLUIDO:
                nomeTrabalhoConcluido = self.reconheceRecuperaTrabalhoConcluido()
                if variavelExiste(nomeTrabalhoConcluido):
                    trabalhoProducaoConcluido = self.retornaTrabalhoConcluido(nomeTrabalhoConcluido)
                    if variavelExiste(trabalhoProducaoConcluido):
                        self.modificaTrabalhoConcluidoListaProduzirProduzindo(trabalhoProducaoConcluido)
                        self.modificaExperienciaProfissao(trabalhoProducaoConcluido)
                        self.atualizaEstoquePersonagem(trabalhoProducaoConcluido)
                        trabalhoProducaoRaro = self.verificaProducaoTrabalhoRaro(trabalhoProducaoConcluido)
                        self.insereTrabalhoProducao(trabalhoProducaoRaro)
                    else:
                        print(f'Trabalho produção concluido não reconhecido.')
                else:
                    print(f'Nome trabalho concluído não reconhecido.')
            elif estadoTrabalho == CODIGO_PRODUZINDO:
                if not self.existeEspacoProducao():
                    print(f'Todos os espaços de produção ocupados.')
                    self.__confirmacao = False
                else:
                    clickContinuo(3,'up')
                    clickEspecifico(1,'left')
            elif estadoTrabalho == CODIGO_PARA_PRODUZIR:
                clickContinuo(3,'up')
                clickEspecifico(1,'left')
        elif menu == MENU_RECOMPENSAS_DIARIAS or menu == MENU_LOJA_MILAGROSA:
            self.recebeTodasRecompensas(menu)
            personagens = self.pegaPersonagens()
            for personagem in personagens:
                if not personagem.estado :
                    personagem.alternaEstado()
                    self.modificaPersonagem(personagem)
            self.__confirmacao = False
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
            self.__confirmacao = False
        if ehErroOutraConexao(self.verificaErro()):
            self.__confirmacao = False
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
                if not self.__confirmacao:
                    return False
                menu = self.retornaMenu()
            else:
                return True
        elif ehErroOutraConexao(erro):
            self._unicaConexao = False
        return False

    def retornaListaTrabalhosRarosVendidosOrdenada(self, listaTrabalhosRarosVendidos):
        print(f'Definindo lista trabalhos raros vendidos ordenada...')
        listaTrabalhosRarosVendidosOrdenada = []
        for trabalhosRarosVendidos in listaTrabalhosRarosVendidos:
            if tamanhoIgualZero(listaTrabalhosRarosVendidosOrdenada):
                listaTrabalhosRarosVendidosOrdenada.append(trabalhosRarosVendidos)
                continue
            for trabalhoRaroVendidoOrdenado in listaTrabalhosRarosVendidosOrdenada:
                if textoEhIgual(trabalhoRaroVendidoOrdenado.nome, trabalhosRarosVendidos.nome):
                    trabalhoRaroVendidoOrdenado.quantidade = trabalhoRaroVendidoOrdenado.quantidade + 1
                    break
            else:
                listaTrabalhosRarosVendidosOrdenada.append(trabalhosRarosVendidos)
        listaTrabalhosRarosVendidosOrdenada = sorted(listaTrabalhosRarosVendidosOrdenada, key=lambda trabalho: (trabalho.quantidade, trabalho.nivel, trabalho.nome), reverse = True)
        for trabalhoRaroVendido in listaTrabalhosRarosVendidosOrdenada:
            print(trabalhoRaroVendido)
        return listaTrabalhosRarosVendidosOrdenada

    # def verificaTrabalhoRaroNecessario(self, verificacoes, dicionarioProdutoRaroVendido):
    #     print(f' Verificando quantidade de ({dicionarioProdutoRaroVendido[CHAVE_NOME]}) no estoque...')
    #     quantidadeTrabalhoRaroNoEstoque = retornaQuantidadeTrabalhoNoEstoque(dicionarioProdutoRaroVendido)
    #     quantidadeTrabalhoRaroNecessario = CODIGO_QUANTIDADE_MINIMA_TRABALHO_RARO_EM_ESTOQUE - quantidadeTrabalhoRaroNoEstoque
    #     if quantidadeTrabalhoRaroNecessario > 0:
    #         print(f' Quantidade de ({dicionarioProdutoRaroVendido[CHAVE_NOME]}) no estoque é ({quantidadeTrabalhoRaroNoEstoque}).')
    #         print(f' Verificando se ({dicionarioProdutoRaroVendido[CHAVE_NOME]}) já está sendo produzido...')
    #         quantidadeTrabalhoRaroProduzirOuProduzindo = retornaQuantidadeTrabalhoListaProduzirProduzindo(dicionarioProdutoRaroVendido[CHAVE_NOME])
    #         quantidadeTrabalhoRaroNecessario = quantidadeTrabalhoRaroNecessario - quantidadeTrabalhoRaroProduzirOuProduzindo
    #         if quantidadeTrabalhoRaroNecessario > 0:
    #             print(f' Existem {quantidadeTrabalhoRaroProduzirOuProduzindo} unidades de ({dicionarioProdutoRaroVendido[CHAVE_NOME]}) na lista para produzir/produzindo.')
                
    #             print(f' Atributos do trabalho raro mais vendido:')
    #             for atributo in dicionarioProdutoRaroVendido:
    #                 print(f' {atributo} - {dicionarioProdutoRaroVendido[atributo]}.')
                
    #             if CHAVE_TRABALHO_NECESSARIO in dicionarioProdutoRaroVendido:
    #                 listaTrabalhosMelhoradosNecessarios = dicionarioProdutoRaroVendido[CHAVE_TRABALHO_NECESSARIO].split(',')
    #                 if not tamanhoIgualZero(listaTrabalhosMelhoradosNecessarios):
    #                     print(f' Lista de trabalhos MELHORADOS necessários: ({listaTrabalhosMelhoradosNecessarios}).')
    #                     if len(listaTrabalhosMelhoradosNecessarios) == 1:
    #                         dicionarioProfissao = retornaDicionarioProfissaoTrabalho(dicionarioProdutoRaroVendido)
    #                         if not tamanhoIgualZero(dicionarioProfissao):
    #                             _, _, xpMaximo = retornaNivelXpMinimoMaximo(dicionarioProfissao)
    #                             licencaProducaoIdeal = CHAVE_LICENCA_PRINCIPIANTE
    #                             if xpMaximo >= 830000:
    #                                 licencaProducaoIdeal = CHAVE_LICENCA_INICIANTE
    #                             nomeTrabalhoMelhoradoNecessario = listaTrabalhosMelhoradosNecessarios[0]
    #                             dicionarioTrabalhoBuscado = {
    #                                 CHAVE_NOME:nomeTrabalhoMelhoradoNecessario,
    #                                 CHAVE_RARIDADE:CHAVE_RARIDADE_MELHORADO}
    #                             print(f' Verificando quantidade de ({nomeTrabalhoMelhoradoNecessario}) no estoque...')
    #                             quantidadeTrabalhoMelhoradoNecessarioNoEstoque = retornaQuantidadeTrabalhoNoEstoque(dicionarioTrabalhoBuscado)
    #                             print(f' Quantidade de ({nomeTrabalhoMelhoradoNecessario}) no estoque é ({quantidadeTrabalhoMelhoradoNecessarioNoEstoque}).')
    #                             if quantidadeTrabalhoMelhoradoNecessarioNoEstoque >= quantidadeTrabalhoRaroNecessario:
    #                                 if quantidadeTrabalhoMelhoradoNecessarioNoEstoque > 0:
    #                                     print(f' Adicionando ({quantidadeTrabalhoRaroNecessario}) unidades de ({dicionarioProdutoRaroVendido[CHAVE_NOME]}) a lista para produzir/produzindo...')
    #                                     dicionarioProdutoRaroVendido[LC.CHAVE_RECORRENCIA] = False
    #                                     dicionarioProdutoRaroVendido[CHAVE_LICENCA] = licencaProducaoIdeal
    #                                     dicionarioProdutoRaroVendido[CHAVE_ESTADO] = CODIGO_PARA_PRODUZIR
    #                                     for x in range(quantidadeTrabalhoRaroNecessario):
    #                                         dicionarioProdutoRaroVendido = adicionaTrabalhoDesejo(dicionarioPersonagemAtributos, dicionarioProdutoRaroVendido)
    #                                         dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO].append(dicionarioProdutoRaroVendido)
                                        
    #                             elif quantidadeTrabalhoMelhoradoNecessarioNoEstoque < quantidadeTrabalhoRaroNecessario and quantidadeTrabalhoMelhoradoNecessarioNoEstoque >= 0:
    #                                 print(f' Adicionando ({quantidadeTrabalhoMelhoradoNecessarioNoEstoque}) unidades de ({dicionarioProdutoRaroVendido[CHAVE_NOME]}) a lista para produzir/produzindo...')
    #                                 dicionarioProdutoRaroVendido[LC.CHAVE_RECORRENCIA] = False
    #                                 dicionarioProdutoRaroVendido[CHAVE_LICENCA] = licencaProducaoIdeal
    #                                 dicionarioProdutoRaroVendido[CHAVE_ESTADO] = CODIGO_PARA_PRODUZIR
    #                                 for x in range(quantidadeTrabalhoMelhoradoNecessarioNoEstoque):
    #                                     dicionarioProdutoRaroVendido = adicionaTrabalhoDesejo(dicionarioPersonagemAtributos, dicionarioProdutoRaroVendido)
    #                                     dicionarioPersonagemAtributos[CHAVE_LISTA_DESEJO].append(dicionarioProdutoRaroVendido)
                                    
    #                                 quantidadeTrabalhoMelhoradoNecessarioFaltante = quantidadeTrabalhoRaroNecessario - quantidadeTrabalhoMelhoradoNecessarioNoEstoque
    #                                 quantidadeTrabalhoMelhoradoNecessarioNaListaProduzirProduzindo = retornaQuantidadeTrabalhoListaProduzirProduzindo(nomeTrabalhoMelhoradoNecessario)
    #                                 quantidadeTrabalhoMelhoradoNecessarioFaltante = quantidadeTrabalhoMelhoradoNecessarioFaltante - quantidadeTrabalhoMelhoradoNecessarioNaListaProduzirProduzindo
    #                                 print(f' Verificando se ({nomeTrabalhoMelhoradoNecessario}) já está sendo produzido...')
    #                                 print(f' Existem ({quantidadeTrabalhoMelhoradoNecessarioNaListaProduzirProduzindo}) unidades de ({nomeTrabalhoMelhoradoNecessario}) na lista para produzir/produzindo.')
    #                                 if quantidadeTrabalhoMelhoradoNecessarioFaltante <= 0:
    #                                     print(f' Passando para o próximo trabalho...')
                                        
    #                                 else:
    #                                     verificacoes += 1
    #                                     verificaTrabalhoMelhoradoNecessario(licencaProducaoIdeal, nomeTrabalhoMelhoradoNecessario, quantidadeTrabalhoMelhoradoNecessarioFaltante)
    #                     elif len(listaTrabalhosMelhoradosNecessarios) == 2:
    #                         print(f' Falta desenvolver...')
    #                         print(f' Passando para o próximo trabalho...')
                            
    #                 else:
    #                     print(f' Lista de trabalhos raros necessários do trabalho ({dicionarioProdutoRaroVendido[CHAVE_NOME]}) está vazia.')
    #                     print(f' Passando para o próximo trabalho...')
                        
    #             else:
    #                 print(f' Trabalho ({dicionarioProdutoRaroVendido[CHAVE_NOME]}) não possui CHAVE_TRABALHO_NECESSARIO.')
    #                 print(f' Passando para o próximo trabalho...')
                    
    #         else:
    #             print(f' Existem ({quantidadeTrabalhoRaroProduzirOuProduzindo}) unidades de ({dicionarioProdutoRaroVendido[CHAVE_NOME]}) sendo produzidos!')
    #             print(f' Passando para o próximo trabalho...')
                       
    #     else:
    #         print(f' Existem ({quantidadeTrabalhoRaroNoEstoque}) unidades do produto mais vendido ({dicionarioProdutoRaroVendido[CHAVE_NOME]}) no estoque.')
    #         print(f' Passando para o próximo trabalho...')
    #     return verificacoes

    def produzProdutoMaisVendido(self, listaTrabalhosRarosVendidos):
        listaTrabalhosRarosVendidosOrdenada = self.retornaListaTrabalhosRarosVendidosOrdenada(listaTrabalhosRarosVendidos)
        verificacoes = 0
        for trabalhoRaroVendido in listaTrabalhosRarosVendidosOrdenada:
            print(f'{verificacoes + 1} verificações.')
            if verificacoes >= 4:
                break
            # verificacoes = self.verificaTrabalhoRaroNecessario(verificacoes, trabalhoRaroVendido)
        print(f'Fim do processo de verificação de produto mais vendido...')

    def pegaTrabalhoPorId(self, id: str) -> Trabalho | None:
        trabalhoDao = TrabalhoDaoSqlite()
        trabalhoEncontrado = trabalhoDao.pegaTrabalhoPorId(id)
        if trabalhoEncontrado is None:
            self.__loggerTrabalhoDao.error(f'Erro ao buscar trabalho ({trabalhoEncontrado}) no banco: {trabalhoDao.pegaErro()}')
            return None
        if trabalhoEncontrado.nome is None:
            self.__loggerTrabalhoDao.warning(f'({trabalhoEncontrado}) não encontrado no banco: {trabalhoDao.pegaErro()}')
            return None
        return trabalhoEncontrado
            

    def retornaListaTrabalhosRarosVendidos(self):
        print(f'Definindo lista produtos raros vendidos...')
        trabalhosRarosVendidos = []
        trabalhoVendidoDao = VendaDaoSqlite(self.__personagemEmUso)
        vendas = trabalhoVendidoDao.pegaVendas()
        if variavelExiste(vendas):
            for trabalhoVendido in vendas:
                trabalhoEncontrado = self.pegaTrabalhoPorId(trabalhoVendido.trabalhoId)
                if variavelExiste(trabalhoEncontrado):
                    if variavelExiste(trabalhoEncontrado.nome):
                        trabalhoEhRaroETrabalhoNaoEhProducaoDeRecursos = trabalhoEncontrado.ehRaro() and not trabalhoEhProducaoRecursos(trabalhoEncontrado)
                        if trabalhoEhRaroETrabalhoNaoEhProducaoDeRecursos:
                            trabalhosRarosVendidos.append(trabalhoVendido)
                            continue
                    self.__loggerTrabalhoDao.warning(f'({trabalhoVendido}) não foi encontrado na lista de trabalhos!')
            return trabalhosRarosVendidos
        self.__loggerVendaDao.error(f'Erro ao buscar trabalhos vendidos: {trabalhoVendidoDao.pegaErro()}')
        return trabalhosRarosVendidos

    def verificaProdutosRarosMaisVendidos(self):
        listaTrabalhosRarosVendidos = self.retornaListaTrabalhosRarosVendidos()
        if tamanhoIgualZero(listaTrabalhosRarosVendidos):
            print(f'Lista de trabalhos raros vendidos está vazia!')
            return
        self.produzProdutoMaisVendido(listaTrabalhosRarosVendidos)

    def defineChaveListaProfissoesNecessarias(self):
        print(f'Verificando profissões necessárias...')
        self.__listaProfissoesNecessarias.clear()
        profissaoDao = ProfissaoDaoSqlite(self.__personagemEmUso)
        profissoes = profissaoDao.pegaProfissoes()
        if not variavelExiste(profissoes):
            logger = logging.getLogger('profissaoDao')
            logger.error(f'Erro ao buscar profissões: {profissaoDao.pegaErro()}')
            print(f'Erro ao buscar profissões: {profissaoDao.pegaErro()}')
            return
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
        trabalhosProducao = trabalhoProducaoDao.pegaTrabalhosProducao()
        if not variavelExiste(trabalhosProducao):
            logger = logging.getLogger('trabalhoProducaoDao')
            logger.error(f'Erro ao bucar trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
            print(f'Erro ao buscar trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
            return
        for profissao in profissoes:
            for trabalhoProducaoDesejado in trabalhosProducao:
                chaveProfissaoEhIgualEEstadoEhParaProduzir = textoEhIgual(profissao.nome, trabalhoProducaoDesejado.profissao) and trabalhoProducaoDesejado.ehParaProduzir()
                if chaveProfissaoEhIgualEEstadoEhParaProduzir:
                    self.__listaProfissoesNecessarias.append(profissao)
                    break
        else:
            self.__listaProfissoesNecessarias = sorted(self.__listaProfissoesNecessarias,key=lambda profissao:profissao.prioridade,reverse=True)
            for profissaoNecessaria in self.__listaProfissoesNecessarias:
                print(f'{profissaoNecessaria}')

    def retornaContadorEspacosProducao(self, contadorEspacosProducao, nivel):
        contadorNivel = 0
        profissaoDao = ProfissaoDaoSqlite(self.__personagemEmUso)
        profissoes = profissaoDao.pegaProfissoes()
        if not variavelExiste(profissoes):
            logger = logging.getLogger('profissaoDao')
            logger.error(f'Erro ao buscar profissões: {profissaoDao.pegaErro()}')
            print(f'Erro ao buscar profissões: {profissaoDao.pegaErro()}')
            return
        for profissao in profissoes:
            if profissao.pegaNivel() >= nivel:
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
        profissaoDao = ProfissaoDaoSqlite(self.__personagemEmUso)
        profissoes = profissaoDao.pegaProfissoes()
        if not variavelExiste(profissoes):
            logger = logging.getLogger('profissaoDao')
            logger.error(f'Erro ao buscar profissões: {profissaoDao.pegaErro()}')
            print(f'Erro ao buscar profissões: {profissaoDao.pegaErro()}')
            return quantidadeEspacosProducao
        for profissao in profissoes:
            nivel = profissao.pegaNivel()
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
        if self.__personagemEmUso.espacoProducao != quantidadeEspacoProducao:
            self.__personagemEmUso.setEspacoProducao(quantidadeEspacoProducao)
            self.modificaPersonagem(self.__personagemEmUso)

    def retornaListaTrabalhosProducaoRaridadeEspecifica(self, dicionarioTrabalho, raridade):
        listaTrabalhosProducaoRaridadeEspecifica = []
        trabalhosProducao = self.pegaTrabalhosProducaoParaProduzirProduzindo()
        if variavelExiste(trabalhosProducao):
            for trabalhoProducao in trabalhosProducao:
                raridadeEhIgualProfissaoEhIgualEstadoEhParaProduzir = textoEhIgual(trabalhoProducao.raridade, raridade) and textoEhIgual(trabalhoProducao.profissao, dicionarioTrabalho[CHAVE_PROFISSAO]) and trabalhoProducao.ehParaProduzir()
                if raridadeEhIgualProfissaoEhIgualEstadoEhParaProduzir:
                    for trabalhoProducaoRaridadeEspecifica in listaTrabalhosProducaoRaridadeEspecifica:
                        if textoEhIgual(trabalhoProducaoRaridadeEspecifica.nome, trabalhoProducao.nome):
                            break
                    else:
                        print(f'Trabalho {raridade} encontado: {trabalhoProducao.nome}')
                        listaTrabalhosProducaoRaridadeEspecifica.append(trabalhoProducao)
            if tamanhoIgualZero(listaTrabalhosProducaoRaridadeEspecifica):
                print(f'Nem um trabalho {raridade} na lista!')
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
            if len(nomeTrabalhoReconhecido) >= 29:
                nomeTrabalhoReconhecido = nomeTrabalhoReconhecido[:28]
            for trabalhoProducaoPriorizada in dicionarioTrabalho[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA]:
                if trabalhoProducaoPriorizada.nomeProducao:
                    nomeTrabalhoProducaoDesejado = trabalhoProducaoPriorizada.nome.replace('-','')
                    nomeProducaoTrabalhoProducaoDesejado = trabalhoProducaoPriorizada.nomeProducao.replace('-','')
                    if len(trabalhoProducaoPriorizada.nome) >= 29:
                        nomeTrabalhoProducaoDesejado = nomeTrabalhoProducaoDesejado[:28]
                    if len(trabalhoProducaoPriorizada.nomeProducao) >= 29:
                        nomeProducaoTrabalhoProducaoDesejado = nomeProducaoTrabalhoProducaoDesejado[:28]
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
        print(f'Trabalho negado: {nomeTrabalhoReconhecido}')
        return dicionarioTrabalho

    def incrementaChavePosicaoTrabalho(self, dicionarioTrabalho):
        dicionarioTrabalho[CHAVE_POSICAO] += 1
        return dicionarioTrabalho

    def defineDicionarioTrabalhoComumMelhorado(self, dicionarioTrabalho):
        nomeTrabalhoReconhecidoAux = ''
        nomeTrabalhoReconhecido = ''
        print(f'Buscando trabalho {dicionarioTrabalho[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA][0].raridade}.')
        contadorParaBaixo = 0
        if not primeiraBusca(dicionarioTrabalho):
            contadorParaBaixo = dicionarioTrabalho[CHAVE_POSICAO]
            clickEspecifico(contadorParaBaixo, 'down')
        while not chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
            erro = self.verificaErro()
            if erroEncontrado(erro):
                self.__confirmacao = False
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
                    print(f'Trabalho na lista: {trabalhoProducao.nome}')
                    if texto1PertenceTexto2(nomeTrabalhoReconhecido, trabalhoProducao.nomeProducao):
                        clickEspecifico(1, 'enter')
                        dicionarioTrabalho[CHAVE_POSICAO] = contadorParaBaixo - 1
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
                    print(f'Trabalho {dicionarioTrabalho[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA][0].raridade} não reconhecido!')
                    break
                else:
                    clickEspecifico(1, 'down')
                    dicionarioTrabalho[CHAVE_POSICAO] = contadorParaBaixo
                    contadorParaBaixo += 1
        return dicionarioTrabalho

    def defineCloneTrabalhoProducao(self, trabalhoProducaoEncontrado):
        cloneTrabalhoProducao = TrabalhoProducao()
        cloneTrabalhoProducao.dicionarioParaObjeto(trabalhoProducaoEncontrado.__dict__)
        cloneTrabalhoProducao.id = str(uuid.uuid4())
        cloneTrabalhoProducao.idTrabalho = trabalhoProducaoEncontrado.idTrabalho
        cloneTrabalhoProducao.recorrencia = False
        self.__loggerTrabalhoProducaoDao.info(f'({cloneTrabalhoProducao.id}|{cloneTrabalhoProducao.idTrabalho}|{cloneTrabalhoProducao.nome}|{cloneTrabalhoProducao.nomeProducao}|{cloneTrabalhoProducao.experiencia}|{cloneTrabalhoProducao.nivel}|{cloneTrabalhoProducao.profissao}|{cloneTrabalhoProducao.raridade}|{cloneTrabalhoProducao.trabalhoNecessario}|{cloneTrabalhoProducao.recorrencia}|{cloneTrabalhoProducao.tipo_licenca}|{cloneTrabalhoProducao.estado}) foi clonado')
        return cloneTrabalhoProducao
    

    def clonaTrabalhoProducaoEncontrado(self, trabalhoProducaoEncontrado):
        print(f'Recorrencia está ligada.')
        cloneTrabalhoProducaoEncontrado = self.defineCloneTrabalhoProducao(trabalhoProducaoEncontrado)
        self.insereTrabalhoProducao(cloneTrabalhoProducaoEncontrado)

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
        nivelTrabalhoProducao = trabalhoProducao.nivel
        nivelRecurso = 1
        recursoTerciario = 0
        if textoEhIgual(trabalhoProducao.profissao, CHAVE_PROFISSAO_ARMA_DE_LONGO_ALCANCE):
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
        chaveProfissao = limpaRuidoTexto(trabalhoProducao.profissao)
        nomeRecursoPrimario, nomeRecursoSecundario, nomeRecursoTerciario = self.retornaNomesRecursos(chaveProfissao, nivelRecurso)
        return TrabalhoRecurso(trabalhoProducao.profissao, trabalhoProducao.nivel, nomeRecursoTerciario, nomeRecursoSecundario, nomeRecursoPrimario, recursoTerciario)

    def removeTrabalhoProducaoEstoque(self, trabalhoProducao):
        estoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
        estoque = estoqueDao.pegaEstoque()
        if not variavelExiste(estoque):
            logger = logging.getLogger('estoqueDao')
            logger.error(f'Erro ao pegar trabalhos no estoque: {estoqueDao.pegaErro()}')
            print(f'Erro ao pegar trabalhos no estoque: {estoqueDao.pegaErro()}')
            return
        if trabalhoProducao.ehComum():
            if trabalhoEhProducaoRecursos(trabalhoProducao):
                print(f'Trabalho é recurso de produção!')
                print(f'Nome recurso produzido: {trabalhoProducao.nome}')
                dicionarioRecurso = {
                    CHAVE_NOME:trabalhoProducao.nome,
                    CHAVE_PROFISSAO:trabalhoProducao.profissao,
                    CHAVE_NIVEL:trabalhoProducao.nivel}
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
                for trabalhoEstoque in estoque:
                    for recursoBuscado in listaNomeRecursoBuscado:
                        if textoEhIgual(trabalhoEstoque.nome, recursoBuscado[0]):
                            novaQuantidade = trabalhoEstoque.quantidade - recursoBuscado[1]
                            print(f'Quantidade de {trabalhoEstoque.nome} atualizada de {trabalhoEstoque.quantidade} para {novaQuantidade}.')
                            trabalhoEstoque.quantidade = novaQuantidade
                            estoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
                            if estoqueDao.modificaTrabalhoEstoque(trabalhoEstoque):
                                print(f'Quantidade do trabalho ({trabalhoEstoque.nome}) atualizada para {novaQuantidade}.')
                                continue
                            logger = logging.getLogger('estoqueDao')
                            logger.error(f'Erro ao modificar trabalho no estoque: {estoqueDao.pegaErro()}')
                            print(f'Erro ao modificar trabalho no estoque: {estoqueDao.pegaErro()}')
                    if textoEhIgual(trabalhoEstoque.nome, trabalhoProducao.tipo_licenca):
                        novaQuantidade = trabalhoEstoque.quantidade - 1
                        print(f'Quantidade de {trabalhoEstoque.nome} atualizada de {trabalhoEstoque.quantidade} para {novaQuantidade}.')
                        trabalhoEstoque.quantidade = novaQuantidade
                        estoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
                        if estoqueDao.modificaTrabalhoEstoque(trabalhoEstoque):
                            print(f'Quantidade do trabalho ({trabalhoEstoque.nome}) atualizada para {novaQuantidade}.')
                            continue
                        logger = logging.getLogger('estoqueDao')
                        logger.error(f'Erro ao modificar trabalho no estoque: {estoqueDao.pegaErro()}')
                        print(f'Erro ao modificar trabalho no estoque: {estoqueDao.pegaErro()}')
            else:
                trabalhoRecurso = self.retornaTrabalhoRecurso(trabalhoProducao)
                for trabalhoEstoque in estoque:
                    novaQuantidade = None
                    if textoEhIgual(trabalhoEstoque.nome, trabalhoRecurso.pegaPrimario()):
                        novaQuantidade = trabalhoEstoque.quantidade - trabalhoRecurso.pegaQuantidadePrimario()
                    elif textoEhIgual(trabalhoEstoque.nome, trabalhoRecurso.pegaSecundario()):
                        novaQuantidade = trabalhoEstoque.quantidade - trabalhoRecurso.pegaQuantidadeSecundario()
                    elif textoEhIgual(trabalhoEstoque.nome, trabalhoRecurso.pegaTerciario()):
                        novaQuantidade = trabalhoEstoque.quantidade - trabalhoRecurso.pegaQuantidadeTerciario()
                    elif textoEhIgual(trabalhoEstoque.nome, trabalhoProducao.tipo_licenca):
                        novaQuantidade = trabalhoEstoque.quantidade - 1
                    if variavelExiste(novaQuantidade):
                        logger = logging.getLogger('estoqueDao')
                        trabalhoEstoque.quantidade = novaQuantidade
                        estoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
                        if estoqueDao.modificaTrabalhoEstoque(trabalhoEstoque):
                            logger.info(f'Quantidade do trabalho ({trabalhoEstoque}) atualizada para {novaQuantidade}.')
                            continue
                        logger.error(f'Erro ao modificar trabalho ({trabalhoEstoque}) no estoque: {estoqueDao.pegaErro()}')
        elif trabalhoProducao.ehMelhorado() or trabalhoProducao.ehRaro():
            if not trabalhoEhProducaoRecursos(trabalhoProducao):
                listaTrabalhosNecessarios = trabalhoProducao.trabalhoNecessario.split(',')
                for trabalhoNecessario in listaTrabalhosNecessarios:
                    for trabalhoEstoque in estoque:
                        if textoEhIgual(trabalhoNecessario, trabalhoEstoque.nome):
                            novaQuantidade = trabalhoEstoque.quantidade - 1
                            trabalhoEstoque.quantidade = novaQuantidade
                            estoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
                            if estoqueDao.modificaTrabalhoEstoque(trabalhoEstoque):
                                print(f'Quantidade do trabalho ({trabalhoEstoque.nome}) atualizada para {novaQuantidade}.')
                                break
                            logger = logging.getLogger('estoqueDao')
                            logger.error(f'Erro ao modificar trabalho no estoque: {estoqueDao.pegaErro()}')
                            print(f'Erro ao modificar trabalho no estoque: {estoqueDao.pegaErro()}')
                            break
            
    def iniciaProcessoDeProducao(self, dicionarioTrabalho):
        primeiraBusca = True
        trabalhoProducaoEncontrado = dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO]
        while True:
            menu = self.retornaMenu()
            if menuTrabalhosAtuaisReconhecido(menu):
                if variavelExiste(trabalhoProducaoEncontrado):
                    if trabalhoProducaoEncontrado.ehRecorrente():
                        self.clonaTrabalhoProducaoEncontrado(trabalhoProducaoEncontrado)
                        self.verificaNovamente = True
                        break
                    self.modificaTrabalhoProducao(trabalhoProducaoEncontrado)
                    self.removeTrabalhoProducaoEstoque(trabalhoProducaoEncontrado)
                    clickContinuo(12,'up')
                    self.verificaNovamente = True
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
                print(f"Buscando: {trabalhoProducaoEncontrado.tipo_licenca}")
                textoReconhecido = self._imagem.retornaTextoLicencaReconhecida()
                if variavelExiste(textoReconhecido):
                    print(f'Licença reconhecida: {textoReconhecido}')
                    if texto1PertenceTexto2('Licença de Artesanato', textoReconhecido):
                        primeiraBusca = True
                        listaCiclo = []
                        while not texto1PertenceTexto2(textoReconhecido, trabalhoProducaoEncontrado.tipo_licenca):
                            listaCiclo.append(textoReconhecido)
                            clickEspecifico(1, "right")
                            textoReconhecido = self._imagem.retornaTextoLicencaReconhecida()
                            if variavelExiste(textoReconhecido):
                                print(f'Licença reconhecida: {textoReconhecido}.')
                                if textoEhIgual(textoReconhecido, 'nenhumitem'):
                                    if textoEhIgual(trabalhoProducaoEncontrado.tipo_licenca, CHAVE_LICENCA_NOVATO):
                                        if not textoEhIgual(listaCiclo[-1], 'nenhumitem'):
                                            print(f'Sem licenças de produção...')
                                            self.__personagemEmUso.alternaEstado()
                                            self.modificaPersonagem(self.__personagemEmUso)
                                            clickEspecifico(3, 'f1')
                                            clickContinuo(10, 'up')
                                            clickEspecifico(1, 'left')
                                            return dicionarioTrabalho
                                    else:
                                        print(f'{trabalhoProducaoEncontrado.tipo_licenca} não encontrado!')
                                        print(f'Licença buscada agora é {CHAVE_LICENCA_NOVATO}!')
                                        trabalhoProducaoEncontrado.tipo_licenca = CHAVE_LICENCA_NOVATO
                                        dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = trabalhoProducaoEncontrado
                                else:
                                    if len(listaCiclo) > 10:
                                        print(f'{trabalhoProducaoEncontrado.tipo_licenca} não encontrado!')
                                        print(f'Licença buscada agora é {CHAVE_LICENCA_NOVATO}!')
                                        trabalhoProducaoEncontrado.tipo_licenca = CHAVE_LICENCA_NOVATO
                                        dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = trabalhoProducaoEncontrado          
                            else:
                                erro = self.verificaErro()
                                if ehErroOutraConexao(erro):
                                    self._unicaConexao = False
                                print(f'Erro ao reconhecer licença!')
                                break
                            primeiraBusca = False
                        else:
                            trabalhoProducaoEncontrado.estado = CODIGO_PRODUZINDO
                            if primeiraBusca:
                                clickEspecifico(1, "f1")
                            else:
                                clickEspecifico(1, "f2")
                    else:
                        print(f'Sem licenças de produção...')
                        self.__personagemEmUso.alternaEstado()
                        self.modificaPersonagem(self.__personagemEmUso)
                        clickEspecifico(3, 'f1')
                        clickContinuo(10, 'up')
                        clickEspecifico(1, 'left')
                        return dicionarioTrabalho
                else:
                    print(f'Erro ao reconhecer licença!')
                    return dicionarioTrabalho
            elif menuEscolhaEquipamentoReconhecido(menu) or menuAtributosEquipamentoReconhecido(menu):
                print(f'Clica f2.')
                clickEspecifico(1, 'f2')
            else:
                return dicionarioTrabalho
            print(f'Tratando possíveis erros...')
            tentativas = 1
            erro = self.verificaErro()
            while erroEncontrado(erro):
                if ehErroRecursosInsuficiente(erro):
                    self.__loggerTrabalhoProducaoDao.warning(f'Não possue recursos necessários ({trabalhoProducaoEncontrado.id} | {trabalhoProducaoEncontrado})')
                    self.__confirmacao = False
                    self.removeTrabalhoProducao(trabalhoProducaoEncontrado)
                    erro = self.verificaErro()
                    continue
                if ehErroEspacoProducaoInsuficiente(erro) or ehErroOutraConexao(erro) or ehErroConectando(erro) or ehErroRestauraConexao(erro):
                    self.__confirmacao = False
                    if ehErroOutraConexao(erro):
                        self._unicaConexao = False
                        erro = self.verificaErro()
                        continue
                    if ehErroConectando(erro):
                        if tentativas > 10:
                            clickEspecifico(1, 'enter')
                            tentativas = 0
                        tentativas+=1
                erro = self.verificaErro()
            if not self.__confirmacao:
                break
            primeiraBusca = False
        return dicionarioTrabalho

    def retornaListaPossiveisTrabalhos(self, nomeTrabalhoConcluido):
        listaPossiveisTrabalhos = []
        trabalhos = self.pegaTrabalhosBanco()
        for trabalho in trabalhos:
            if texto1PertenceTexto2(nomeTrabalhoConcluido[1:-1], trabalho.nomeProducao):
                trabalhoEncontrado = TrabalhoProducao()
                trabalhoEncontrado.dicionarioParaObjeto(trabalho.__dict__)
                trabalhoEncontrado.id = str(uuid.uuid4())
                trabalhoEncontrado.idTrabalho = trabalho.id
                trabalhoEncontrado.recorrencia = False
                trabalhoEncontrado.tipo_licenca = CHAVE_LICENCA_NOVATO
                trabalhoEncontrado.estado = CODIGO_CONCLUIDO
                listaPossiveisTrabalhos.append(trabalhoEncontrado)
        return listaPossiveisTrabalhos

    def retornaTrabalhoProducaoConcluido(self, nomeTrabalhoConcluido):
        listaPossiveisTrabalhosProducao = self.retornaListaPossiveisTrabalhos(nomeTrabalhoConcluido)
        if not tamanhoIgualZero(listaPossiveisTrabalhosProducao):
            trabalhosProducao = self.pegaTrabalhosProducaoParaProduzirProduzindo()
            if not variavelExiste(trabalhosProducao):
                return listaPossiveisTrabalhosProducao[0]
            for possivelTrabalhoProducao in listaPossiveisTrabalhosProducao:
                for trabalhoProduzirProduzindo in trabalhosProducao:
                    condicoes = trabalhoProduzirProduzindo.ehProduzindo() and textoEhIgual(trabalhoProduzirProduzindo.nome, possivelTrabalhoProducao.nome)
                    if condicoes:
                        return trabalhoProduzirProduzindo
            else:
                print(f'Trabalho concluído ({listaPossiveisTrabalhosProducao[0].nome}) não encontrado na lista produzindo...')
                return listaPossiveisTrabalhosProducao[0]
        return None

    
    def existeEspacoProducao(self):
        espacoProducao = self.__personagemEmUso.espacoProducao
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
        trabalhosProducao = trabalhoProducaoDao.pegaTrabalhosProducao()
        if not variavelExiste(trabalhosProducao):
            logger = logging.getLogger('trabalhoProducaoDao')
            logger.error(f'Erro ao bucar trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
            return False
        for trabalhoProducao in trabalhosProducao:
            if trabalhoProducao.ehProduzindo():
                espacoProducao -= 1
                if espacoProducao <= 0:
                    print(f'{espacoProducao} espaços de produção.')
                    return False
        print(f'{espacoProducao} espaços de produção.')
        return True

    def iniciaBuscaTrabalho(self):
        dicionarioTrabalho = {CHAVE_TRABALHO_PRODUCAO_ENCONTRADO: None}
        self.defineChaveListaProfissoesNecessarias()
        for profissaoNecessaria in self.__listaProfissoesNecessarias:
            if not self.__confirmacao or not self._unicaConexao:
                break
            if not self.existeEspacoProducao():
                continue
            dicionarioTrabalho[CHAVE_POSICAO] = -1
            while self.__confirmacao:
                self.verificaNovamente = False
                self.vaiParaMenuProduzir()
                if not self.__confirmacao or not self._unicaConexao or not self.existeEspacoProducao():
                    break
                if self._profissaoModificada:
                    self.verificaEspacoProducao()
                profissaoDao = ProfissaoDaoSqlite(self.__personagemEmUso)
                profissoes = profissaoDao.pegaProfissoes()
                if not variavelExiste(profissoes):
                    logger = logging.getLogger('profissaoDao')
                    logger.error(f'Erro ao buscar profissões: {profissaoDao.pegaErro()}')
                    print(f'Erro ao buscar profissões: {profissaoDao.pegaErro()}')
                    break
                for profissao in profissoes:
                    if profissao.nome == profissaoNecessaria.nome:
                        posicao = profissoes.index(profissao) + 1 
                entraProfissaoEspecifica(profissaoNecessaria, posicao)
                print(f'Verificando profissão: {profissaoNecessaria.nome}')
                dicionarioTrabalho[CHAVE_PROFISSAO] = profissaoNecessaria.nome
                dicionarioTrabalho = self.veficaTrabalhosProducaoListaDesejos(dicionarioTrabalho)
                if self.__confirmacao:
                    if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
                        dicionarioTrabalho = self.iniciaProcessoDeProducao(dicionarioTrabalho)
                    elif ehMenuTrabalhosDisponiveis(self.retornaMenu()):
                        saiProfissaoVerificada(dicionarioTrabalho)
                    if self._unicaConexao and self._espacoBolsa:
                        if self._imagem.retornaEstadoTrabalho() == CODIGO_CONCLUIDO:
                            nomeTrabalhoConcluido = self.reconheceRecuperaTrabalhoConcluido()
                            if variavelExiste(nomeTrabalhoConcluido):
                                trabalhoProducaoConcluido = self.retornaTrabalhoProducaoConcluido(nomeTrabalhoConcluido)
                                if variavelExiste(trabalhoProducaoConcluido):
                                    self.modificaTrabalhoConcluidoListaProduzirProduzindo(trabalhoProducaoConcluido)
                                    self.modificaExperienciaProfissao(trabalhoProducaoConcluido)
                                    self.atualizaEstoquePersonagem(trabalhoProducaoConcluido)
                                    trabalhoProducaoRaro = self.verificaProducaoTrabalhoRaro(trabalhoProducaoConcluido)
                                    self.insereTrabalhoProducao(trabalhoProducaoRaro)
                                else:
                                    print(f'Dicionário trabalho concluido não reconhecido.')
                            else:
                                print(f'Dicionário trabalho concluido não reconhecido.')
                            self.verificaNovamente = True
                        elif not self.existeEspacoProducao():
                            break
                        dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = None
                        clickContinuo(3,'up')
                        clickEspecifico(1,'left')
                        sleep(1.5)
                if not self.verificaNovamente:
                    break
        else:
            if self._profissaoModificada:
                self.verificaEspacoProducao()
            print(f'Fim da lista de profissões...')

    def veficaTrabalhosProducaoListaDesejos(self, dicionarioTrabalho):
        listaDeListasTrabalhosProducao = self.retornaListaDeListasTrabalhosProducao(dicionarioTrabalho)
        for listaTrabalhosProducao in listaDeListasTrabalhosProducao:
            if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not self.__confirmacao:
                return dicionarioTrabalho
            dicionarioTrabalho[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA] = listaTrabalhosProducao
            for trabalhoProducaoPriorizado in dicionarioTrabalho[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA]:
                if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not self.__confirmacao:
                    return dicionarioTrabalho
                if trabalhoProducaoPriorizado.ehEspecial() or trabalhoProducaoPriorizado.ehRaro():
                    print(f'Trabalho desejado: {trabalhoProducaoPriorizado.nome}.')
                    posicaoAux = -1
                    if dicionarioTrabalho[CHAVE_POSICAO] != -1:
                        posicaoAux = dicionarioTrabalho[CHAVE_POSICAO]
                    dicionarioTrabalho[CHAVE_POSICAO] = 0
                    while naoFizerQuatroVerificacoes(dicionarioTrabalho):
                        nomeTrabalhoReconhecido = self.retornaNomeTrabalhoPosicaoTrabalhoRaroEspecial(dicionarioTrabalho)
                        print(f'Trabalho {trabalhoProducaoPriorizado.raridade} reconhecido: {nomeTrabalhoReconhecido}.')
                        if nomeTrabalhoReconhecido is None:
                            break
                        if texto1PertenceTexto2(nomeTrabalhoReconhecido[:-1], trabalhoProducaoPriorizado.nomeProducao):
                            erro = self.verificaErro()
                            if erroEncontrado(erro) and (ehErroOutraConexao(erro) or ehErroConectando(erro) or ehErroRestauraConexao(erro)):
                                self.__confirmacao = False
                                dicionarioTrabalho[CHAVE_UNICA_CONEXAO] = False if ehErroOutraConexao(erro) else True
                                return dicionarioTrabalho
                            entraTrabalhoEncontrado(dicionarioTrabalho)
                            dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = trabalhoProducaoPriorizado
                            tipoTrabalho = 0
                            if trabalhoEhProducaoRecursos(dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO]):
                                tipoTrabalho = 1
                            dicionarioTrabalho = self.confirmaNomeTrabalhoProducao(dicionarioTrabalho, tipoTrabalho)
                            if not chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
                                clickEspecifico(1,'f1')
                                clickContinuo(dicionarioTrabalho[CHAVE_POSICAO] + 1, 'up')
                            continue
                        dicionarioTrabalho = self.incrementaChavePosicaoTrabalho(dicionarioTrabalho)
                    dicionarioTrabalho[CHAVE_POSICAO] = posicaoAux
                    continue
                if trabalhoProducaoPriorizado.ehMelhorado() or trabalhoProducaoPriorizado.ehComum():
                    dicionarioTrabalho = self.defineDicionarioTrabalhoComumMelhorado(dicionarioTrabalho)
                    if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not self.__confirmacao:
                        return dicionarioTrabalho
                    if listaDeListasTrabalhosProducao.index(listaTrabalhosProducao) + 1 >= len(listaDeListasTrabalhosProducao):
                        vaiParaMenuTrabalhoEmProducao()
                        break
                    vaiParaOTopoDaListaDeTrabalhosComunsEMelhorados(dicionarioTrabalho)
                    dicionarioTrabalho[CHAVE_POSICAO] = -1
                    break
        return dicionarioTrabalho

    def retornaListaDeListasTrabalhosProducao(self, dicionarioTrabalho):
        listaDeListaTrabalhos = []
        for raridade in LISTA_RARIDADES:
            listaTrabalhosProducao = self.retornaListaTrabalhosProducaoRaridadeEspecifica(dicionarioTrabalho, raridade)
            if tamanhoIgualZero(listaTrabalhosProducao):
                continue
            listaDeListaTrabalhos.append(listaTrabalhosProducao)
        return listaDeListaTrabalhos

    def retiraPersonagemJaVerificadoListaAtivo(self):
        """
        Esta função é responsável por redefinir a lista de personagens ativos, verificando a lista de personagens já verificados
        """        
        self.defineListaPersonagensAtivos()
        novaListaPersonagensAtivos = []
        for personagemAtivo in self.__listaPersonagemAtivo:
            for personagemRemovido in self.__listaPersonagemJaVerificado:
                if textoEhIgual(personagemAtivo.nome, personagemRemovido.nome):
                    break
            else:
                print(personagemAtivo)
                novaListaPersonagensAtivos.append(personagemAtivo)
        self.__listaPersonagemAtivo = novaListaPersonagensAtivos

    def logaContaPersonagem(self):
        confirmacao=False
        email=self.__listaPersonagemAtivo[0].email
        senha=self.__listaPersonagemAtivo[0].senha
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
                if variavelExiste(self.__personagemEmUso):
                    clickEspecifico(1, 'f2')
                    sleep(1)
                    print(f'Personagem ({self.__personagemEmUso.nome}) encontrado.')
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

    def retornaProfissaoPriorizada(self):
        profissaoDao = ProfissaoDaoSqlite(self.__personagemEmUso)
        profissoes = profissaoDao.pegaProfissoes()
        if variavelExiste(profissoes):
            for profissao in profissoes:
                if profissao.prioridade:
                    return profissao
            return None
        self.__loggerProfissaoDao.error(f'Erro ao buscar profissões: {profissaoDao.pegaErro()}')
        return None
    
    def pegaTrabalhosComumProfissaoNivelEspecifico(self, trabalho: Trabalho) -> list[Trabalho]:
        trabalhoDao = TrabalhoDaoSqlite()
        trabalhosComunsProfissaoNivelExpecifico = trabalhoDao.pegaTrabalhosComumProfissaoNivelEspecifico(trabalho)
        if trabalhosComunsProfissaoNivelExpecifico is None:
            self.__loggerTrabalhoDao.error(f'Erro ao buscar trabalhos específicos no banco: {trabalhoDao.pegaErro()}')
            return []
        return trabalhosComunsProfissaoNivelExpecifico

    def defineTrabalhoComumProfissaoPriorizada(self):
        profissaoPriorizada = self.retornaProfissaoPriorizada()
        if variavelExiste(profissaoPriorizada):
            nivelProfissao = profissaoPriorizada.pegaNivel()
            if nivelProfissao == 1 or nivelProfissao == 8:
                self.__loggerProfissaoDao.warning(f'Nível de produção é 1 ou 8')
                return 
            trabalhoBuscado = self.defineTrabalhoComumBuscado(profissaoPriorizada, nivelProfissao)
            trabalhosComunsProfissaoNivelExpecifico = self.pegaTrabalhosComumProfissaoNivelEspecifico(trabalhoBuscado)
            if tamanhoIgualZero(trabalhosComunsProfissaoNivelExpecifico):
                self.__loggerProfissaoDao.warning(f'Nem um trabalho nível ({trabalhoBuscado.nivel}), raridade (comum) e profissão ({trabalhoBuscado.profissao}) foi encontrado!')
                return
            while True:
                trabalhosQuantidade = self.defineListaTrabalhosQuantidade(trabalhosComunsProfissaoNivelExpecifico)
                trabalhosQuantidade = self.atualizaListaTrabalhosQuantidadeEstoque(trabalhosQuantidade)
                trabalhosQuantidade, quantidadeTotalTrabalhoProducao = self.atualizaListaTrabalhosQuantidadeTrabalhosProducao(trabalhosQuantidade)
                trabalhosQuantidade = sorted(trabalhosQuantidade, key=lambda trabalho: trabalho.quantidade)
                quantidadeTrabalhosEmProducaoEhMaiorIgualAoTamanhoListaTrabalhosComuns = quantidadeTotalTrabalhoProducao >= len(trabalhosComunsProfissaoNivelExpecifico)
                if quantidadeTrabalhosEmProducaoEhMaiorIgualAoTamanhoListaTrabalhosComuns:
                    break
                trabalhoComum = self.defineTrabalhoProducaoComum(trabalhosQuantidade)
                self.insereTrabalhoProducao(trabalhoComum)
            return
        self.__loggerProfissaoDao.warning(f'Nem uma profissão priorizada encontrada!')
        return

    def defineTrabalhoComumBuscado(self, profissaoPriorizada, nivelProfissao):
        trabalhoBuscado = Trabalho()
        trabalhoBuscado.profissao = profissaoPriorizada.nome
        trabalhoBuscado.nivel = trabalhoBuscado.pegaNivel(nivelProfissao)
        trabalhoBuscado.raridade = CHAVE_RARIDADE_COMUM
        return trabalhoBuscado

    def defineTrabalhoProducaoComum(self, trabalhosQuantidade):
        trabalhoComum = TrabalhoProducao()
        trabalhoComum.idTrabalho = trabalhosQuantidade[0].trabalhoId
        trabalhoComum.estado = 0
        trabalhoComum.recorrencia = False
        trabalhoComum.tipo_licenca = CHAVE_LICENCA_NOVATO
        return trabalhoComum

    def atualizaListaTrabalhosQuantidadeTrabalhosProducao(self, trabalhosQuantidade):
        quantidadeTotalTrabalhoProducao = 0
        for trabalhoQuantidade in trabalhosQuantidade:
            trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
            quantidade = trabalhoProducaoDao.pegaQuantidadeTrabalhoProducaoProduzirProduzindo(trabalhoQuantidade.trabalhoId)
            if variavelExiste(quantidade):
                trabalhoQuantidade.quantidade += quantidade
                quantidadeTotalTrabalhoProducao += quantidade
                continue
            self.__loggerTrabalhoProducaoDao.error(f'Erro ao pegar quantidade trabalho na lista de produções: {trabalhoProducaoDao.pegaErro()}')
        return trabalhosQuantidade, quantidadeTotalTrabalhoProducao

    def atualizaListaTrabalhosQuantidadeEstoque(self, trabalhosQuantidade):
        for trabalhoQuantidade in trabalhosQuantidade:
            trabalhoEstoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
            quantidade = trabalhoEstoqueDao.pegaQuantidadeTrabalho(trabalhoQuantidade.trabalhoId)
            if variavelExiste(quantidade):
                trabalhoQuantidade.quantidade += quantidade
                continue
            self.__loggerEstoqueDao.error(f'Erro ao pegar quantidade trabalho no estoque: {trabalhoEstoqueDao.pegaErro()}')
        return trabalhosQuantidade

    def defineListaTrabalhosQuantidade(self, trabalhosComunsProfissaoNivelExpecifico):
        trabalhosQuantidade = []
        for trabalhoComum in trabalhosComunsProfissaoNivelExpecifico:
            trabalhoQuantidade = TrabalhoEstoque()
            trabalhoQuantidade.trabalhoId = trabalhoComum.id
            trabalhoQuantidade.quantidade = 0
            trabalhosQuantidade.append(trabalhoQuantidade)
        return trabalhosQuantidade

    def iniciaProcessoBusca(self):
        while True:
            self.verificaAlteracaoListaTrabalhos()
            self.verificaAlteracaoPersonagem()
            self.retiraPersonagemJaVerificadoListaAtivo()
            listaPersonagensAtivosEstaVazia = tamanhoIgualZero(self.__listaPersonagemAtivo)
            if listaPersonagensAtivosEstaVazia:
                self.__listaPersonagemJaVerificado.clear()
                continue
            self.definePersonagemEmUso()
            if variavelExiste(self.__personagemEmUso):
                self.modificaAtributoUso()
                print(f'Personagem ({self.__personagemEmUso.nome}) ESTÁ EM USO.')
                self.inicializaChavesPersonagem()
                print('Inicia busca...')
                if self.vaiParaMenuProduzir():
                    self.defineTrabalhoComumProfissaoPriorizada()
                    trabalhosProducao = self.pegaTrabalhosProducaoParaProduzirProduzindo()
                    if not variavelExiste(trabalhosProducao):
                        continue
                    if tamanhoIgualZero(trabalhosProducao):
                        print(f'Lista de trabalhos desejados vazia.')
                        self.__personagemEmUso.alternaEstado()
                        self.modificaPersonagem(self.__personagemEmUso)
                        continue
                    if self._autoProducaoTrabalho:
                        self.verificaProdutosRarosMaisVendidos()
                    self.iniciaBuscaTrabalho()
                if self._unicaConexao:
                    if haMaisQueUmPersonagemAtivo(self.__listaPersonagemAtivo):
                        clickMouseEsquerdo(1, 2, 35)
                self.__listaPersonagemJaVerificado.append(self.__personagemEmUso)
                continue
            if tamanhoIgualZero(self.__listaPersonagemJaVerificado):
                if self.configuraLoginPersonagem():
                    self.entraPersonagemAtivo()
                continue
            if textoEhIgual(self.__listaPersonagemJaVerificado[-1].email, self.__listaPersonagemAtivo[0].senha):
                self.entraPersonagemAtivo()
                continue
            if self.configuraLoginPersonagem():
                self.entraPersonagemAtivo()

    def insereTrabalho(self, trabalho: Trabalho, modificaServidor: bool = True) -> bool:
        trabalhoDao = TrabalhoDaoSqlite()
        if trabalhoDao.insereTrabalho(trabalho, modificaServidor):
            self.__loggerTrabalhoDao.info(f'({trabalho}) inserido no banco com sucesso!')
            return True
        self.__loggerTrabalhoDao.error(f'Erro ao inserir ({trabalho}) no banco: {trabalhoDao.pegaErro()}')
        return False

    def removeTrabalho(self, trabalho: Trabalho, modificaServidor: bool = True) -> bool:
        trabalhoDao = TrabalhoDaoSqlite()
        if trabalhoDao.removeTrabalho(trabalho, modificaServidor):
            self.__loggerTrabalhoDao.info(f'({trabalho}) removido do banco com sucesso!')
            return True
        self.__loggerTrabalhoDao.error(f'Erro ao remover ({trabalho}) do banco: {trabalhoDao.pegaErro()}')
        return False

    def verificaAlteracaoListaTrabalhos(self):
        if self.__repositorioTrabalho.estaPronto:
            for trabalho in self.__repositorioTrabalho.pegaDadosModificados():
                if trabalho.nome is None:
                    self.removeTrabalho(trabalho, False)
                    continue
                trabalhoEncontrado = self.pegaTrabalhoPorId(trabalho.id)
                if trabalhoEncontrado is None:
                    continue
                if trabalhoEncontrado.id == trabalho.id:
                    self.modificaTrabalho(trabalho, False)
                    continue
                self.insereTrabalho(trabalho, False)
            self.__repositorioTrabalho.limpaLista()
    
    def modificaPersonagem(self, personagem: Personagem, modificaServidor: bool = True):
        personagemDao = PersonagemDaoSqlite()
        if personagemDao.modificaPersonagem(personagem, modificaServidor):
            self.__loggerPersonagemDao.info(f'({personagem}) modificado no banco com sucesso!')
            return
        self.__loggerPersonagemDao.error(f'Erro ao modificar ({personagem}) no banco: {personagemDao.pegaErro()}')

    def inserePersonagem(self, personagem: Personagem, modificaServidor: bool = True):
        personagemDao = PersonagemDaoSqlite()
        if personagemDao.inserePersonagem(personagem, modificaServidor):
            self.__loggerPersonagemDao.info(f'({personagem}) inserido no banco com sucesso!')
            return
        self.__loggerPersonagemDao.error(f'Erro ao inserir ({personagem}) no banco: {personagemDao.pegaErro()}')
        
    def concluiRemoveTrabalhoEstoque(self, trabalhoEstoque, modificaServidor = True):
        trabalhoEstoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
        if trabalhoEstoqueDao.removeTrabalhoEstoque(trabalhoEstoque, modificaServidor):
            self.__loggerEstoqueDao.info(f'({trabalhoEstoque}) removido com sucesso!')
            return
        self.__loggerEstoqueDao.error(f'Erro ao remover ({trabalhoEstoque}): {trabalhoEstoqueDao.pegaErro()}')

    def concluiModificaTrabalhoEstoque(self, trabalhoEstoque, modificaServidor = True):
        estoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
        if estoqueDao.modificaTrabalhoEstoque(trabalhoEstoque, modificaServidor):
            self.__loggerEstoqueDao.info(f'({trabalhoEstoque}) modificado com sucesso!')
            return
        self.__loggerEstoqueDao.error(f'Erro ao modificar ({trabalhoEstoque}): {estoqueDao.pegaErro()}')
        
    def concluiInsereTrabalhoEstoque(self, trabalhoEstoque, modificaServidor = True, personagem = None):
        if personagem is None:
            personagem = self.__personagemEmUso
        trabalhoEstoqueDao = EstoqueDaoSqlite(personagem)
        if trabalhoEstoqueDao.insereTrabalhoEstoque(trabalhoEstoque, modificaServidor):
            self.__loggerEstoqueDao.info(f'({trabalhoEstoque}) inserido com sucesso!')
            return
        self.__loggerEstoqueDao.error(f'Erro ao inserir ({trabalhoEstoque}): {trabalhoEstoqueDao.pegaErro()}')
        
    def concluiModificaProfissao(self, profissao, modificaServidor = True, personagem = None):
        if personagem is None:
            personagem = self.__personagemEmUso
        profissaoDao = ProfissaoDaoSqlite(personagem)
        if profissaoDao.modificaProfissao(profissao, modificaServidor):
            self.__loggerProfissaoDao.info(f'({profissao}) modificado no banco com sucesso!')
            return True
        self.__loggerProfissaoDao.error(f'Erro ao modificar ({profissao}) no banco: {profissaoDao.pegaErro()}')
        return False
    
    def concluiRemovePersonagem(self, personagem, modificaServirdor = True):
        personagemDao = PersonagemDaoSqlite()
        if personagemDao.removePersonagem(personagem, modificaServirdor):
            self.__loggerPersonagemDao.info(f'({personagem}) removido no banco com sucesso!')
            return
        self.__loggerPersonagemDao.error(f'Erro ao remover ({personagem}) do banco: {personagemDao.pegaErro()}')
        
    def concluiInsereProfissao(self, profissao, modificaServidor = True, personagem = None):
        if personagem is None:
            personagem = self.__personagemEmUso
        profissaoDao = ProfissaoDaoSqlite(personagem)
        if profissaoDao.insereProfissao(profissao, modificaServidor):
            self.__loggerProfissaoDao.info(f'({profissao}) inserido no banco com sucesso!')
            return
        self.__loggerProfissaoDao.error(f'Erro ao inserir ({profissao}) no banco: {profissaoDao.pegaErro()}')

    def pegaPersonagemPorId(self, id: str) -> Personagem:
        persoangemDao = PersonagemDaoSqlite()
        personagemEncontrado = persoangemDao.pegaPersonagemPorId(id)
        if personagemEncontrado == None:
            self.__loggerPersonagemDao.error(f'Erro ao buscar personagem por id: {persoangemDao.pegaErro()}')
            return None
        return personagemEncontrado

    def verificaAlteracaoPersonagem(self):
        if self.__repositorioPersonagem.estaPronto:
            dicionarios = self.__repositorioPersonagem.pegaDadosModificados()
            for dicionario in dicionarios:
                personagemModificado = Personagem()
                personagemModificado.id = dicionario['id']
                if CHAVE_LISTA_TRABALHOS_PRODUCAO in dicionario:
                    trabalhoProducao = TrabalhoProducao()
                    if dicionario[CHAVE_LISTA_TRABALHOS_PRODUCAO] == None:
                        trabalhoProducao.id = dicionario['idTrabalhoProducao']
                        self.removeTrabalhoProducao(trabalhoProducao, personagemModificado, False)
                        continue
                    trabalhoProducao.dicionarioParaObjeto(dicionario[CHAVE_LISTA_TRABALHOS_PRODUCAO])
                    if trabalhoProducao.idTrabalho is None or trabalhoProducao.tipo_licenca is None or trabalhoProducao.estado is None or trabalhoProducao.recorrencia is None:
                        continue
                    trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagemModificado)
                    trabalhoProducaoEncontrado = trabalhoProducaoDao.pegaTrabalhoProducaoPorId(trabalhoProducao)
                    if trabalhoProducaoEncontrado == None:
                        self.__loggerTrabalhoProducaoDao.error(f'Erro ao buscar trabalho em produção por id: {trabalhoProducaoDao.pegaErro()}')
                        continue
                    if trabalhoProducaoEncontrado.id == trabalhoProducao.id:
                        self.modificaTrabalhoProducao(trabalhoProducao, personagemModificado, False)
                        continue
                    self.insereTrabalhoProducao(trabalhoProducao, personagemModificado, False)
                    continue
                if CHAVE_LISTA_ESTOQUE in dicionario:
                    trabalhoEstoque = TrabalhoEstoque()
                    if dicionario[CHAVE_LISTA_ESTOQUE] == None:
                        trabalhoEstoque.id = dicionario['idTrabalhoProducao']
                        trabalhoEstoqueDao = EstoqueDaoSqlite(personagemModificado)
                        trabalhoEstoqueEncontrado = trabalhoEstoqueDao.pegaTrabalhoEstoquePorId(trabalhoEstoque.id)
                        if variavelExiste(trabalhoEstoqueEncontrado):
                            if trabalhoEstoqueEncontrado.id == trabalhoEstoque.id:
                                self.concluiRemoveTrabalhoEstoque(trabalhoEstoqueEncontrado, False)
                                continue
                            self.__loggerEstoqueDao.warning(f'({trabalhoEstoque.id}) não foi encontrado no banco!')
                            continue
                        self.__loggerEstoqueDao.error(f'Erro ao buscar ({trabalhoEstoque.id}) por id: {trabalhoEstoqueDao.pegaErro()}')
                        continue
                    trabalhoEstoque.dicionarioParaObjeto(dicionario[CHAVE_LISTA_ESTOQUE])
                    trabalhoEstoqueDao = EstoqueDaoSqlite(personagemModificado)
                    trabalhoEstoqueEncontrado = trabalhoEstoqueDao.pegaTrabalhoEstoquePorId(trabalhoEstoque.id)
                    if variavelExiste(trabalhoEstoqueEncontrado):
                        if trabalhoEstoqueEncontrado.id == trabalhoEstoque.id:
                            trabalhoEstoqueEncontrado.setQuantidade(trabalhoEstoque.quantidade)
                            self.concluiModificaTrabalhoEstoque(trabalhoEstoqueEncontrado, False)
                            continue
                        self.concluiInsereTrabalhoEstoque(trabalhoEstoque, False, personagemModificado)
                        continue
                    self.__loggerEstoqueDao.error(f'Erro ao buscar ({trabalhoEstoque.id}) por id: {trabalhoEstoqueDao.pegaErro()}')
                    continue
                if CHAVE_LISTA_PROFISSAO in dicionario:
                    profissao = Profissao()
                    profissao.dicionarioParaObjeto(dicionario[CHAVE_LISTA_PROFISSAO])
                    profissaoDao = ProfissaoDaoSqlite(personagemModificado)
                    profissaoEncontrada = profissaoDao.pegaProfissaoPorId(profissao.id)
                    if variavelExiste(profissaoEncontrada):
                        if profissaoEncontrada.id == profissao.id:
                            self.concluiModificaProfissao(profissao, False, personagemModificado)
                            continue
                        self.concluiInsereProfissao(profissao, False, personagemModificado)
                        continue
                    self.__loggerProfissaoDao.error(f'Erro ao buscar ({profissao.id}) por id: {profissaoDao.pegaErro()}')
                    continue
                if dicionario['novoPersonagem'] is None:
                    personagemEncontrado = self.pegaPersonagemPorId(personagemModificado.id)
                    if personagemEncontrado is None:
                        continue
                    if personagemEncontrado.nome is None:
                        self.__loggerPersonagemDao.warning(f'({personagemModificado}) não encontrado no banco!')
                        continue
                    personagemEncontrado.dicionarioParaObjeto(dicionario)
                    self.modificaPersonagem(personagemEncontrado, False)
                    continue
                personagemModificado.dicionarioParaObjeto(dicionario['novoPersonagem'])
                self.inserePersonagem(personagemModificado, False)
                continue
            self.__repositorioPersonagem.limpaLista()
        
    def sincronizaListaTrabalhos(self):
        repositorioTrabalho = RepositorioTrabalho()        
        trabalhosServidor = repositorioTrabalho.pegaTodosTrabalhos()
        if variavelExiste(trabalhosServidor):
            for trabalhoServidor in trabalhosServidor:
                limpaTela()
                print(f'Sincronizando trabalhos...')
                print(f'Trabalhos: {(trabalhosServidor.index(trabalhoServidor)+1)/len(trabalhosServidor):.2%}')
                trabalhoEncontradoBanco = self.pegaTrabalhoPorId(trabalhoServidor.id)
                if variavelExiste(trabalhoEncontradoBanco):
                    if trabalhoEncontradoBanco.id == trabalhoServidor.id:
                        self.modificaTrabalho(trabalhoServidor, False)
                        continue
                    self.insereTrabalho(trabalhoServidor, False)  
            trabalhosBanco = self.pegaTrabalhosBanco()
            novaLista = []
            for trabalhoBanco in trabalhosBanco:
                for trabalhoServidor in trabalhosServidor:
                    if trabalhoBanco.id == trabalhoServidor.id:
                        break
                else:
                    novaLista.append(trabalhoBanco)
            for trabalhoBanco in novaLista:
                self.removeTrabalho(trabalhoBanco, False)
            return
        self.__loggerRepositorioTrabalho.error(f'Erro ao buscar trabalhos no servidor: {repositorioTrabalho.pegaErro()}')

    def pegaPersonagens(self) -> list[Personagem]:
        personagemDao = PersonagemDaoSqlite()
        personagensBanco = personagemDao.pegaPersonagens()
        if personagensBanco is None:                  
            self.__loggerPersonagemDao.error(f'Erro ao pegar personagens no banco: {personagemDao.pegaErro()}')
            return []
        return personagensBanco

    def sincronizaListaPersonagens(self):
        repositorioPersonagem = RepositorioPersonagem()
        personagensServidor = repositorioPersonagem.pegaTodosPersonagens()
        if variavelExiste(personagensServidor):
            for personagemServidor in personagensServidor:
                limpaTela()
                print(f'Sincronizando personagens...')
                print(f'Personagens: {(personagensServidor.index(personagemServidor)+1)/len(personagensServidor):.2%}')
                personagemEncontradoBanco = self.pegaPersonagemPorId(personagemServidor.id)
                if variavelExiste(personagemEncontradoBanco):
                    if personagemEncontradoBanco.id == personagemServidor.id:
                        self.modificaPersonagem(personagemServidor, False)
                        continue
                    self.inserePersonagem(personagemServidor, False)
                    continue
            personagensBanco = self.pegaPersonagens()
            novaLista = []
            for personagemBanco in personagensBanco:
                for personagemServidor in personagensServidor:
                    if personagemBanco.id == personagemServidor.id:
                        break
                else:
                    novaLista.append(personagemBanco)
            for personagemBanco in novaLista:
                self.concluiRemovePersonagem(personagemBanco, False)                    
            return
        self.__loggerRepositorioPersonagem.error(f'Erro ao pegar personagens no servidor: {repositorioPersonagem.pegaErro()}')

    def sincronizaListaProfissoes(self):
        personagens = self.pegaPersonagens()
        for personagem in personagens:
            repositorioProfissao = RepositorioProfissao(personagem)
            profissoesServidor = repositorioProfissao.pegaTodasProfissoes()
            if variavelExiste(profissoesServidor):
                for profissaoServidor in profissoesServidor:
                    limpaTela()
                    print(f'Sincronizando profissões...')
                    print(f'Personagens: {(personagens.index(personagem)+1)/len(personagens):.2%}')
                    print(f'Profissões: {(profissoesServidor.index(profissaoServidor)+1)/len(profissoesServidor):.2%}')
                    profissaoDao = ProfissaoDaoSqlite(personagem)
                    profissaoEncontrada = profissaoDao.pegaProfissaoPorId(profissaoServidor.id)
                    if variavelExiste(profissaoEncontrada):
                        if profissaoEncontrada.id == profissaoServidor.id:
                            profissaoDao = ProfissaoDaoSqlite(personagem)
                            if profissaoDao.modificaProfissao(profissaoServidor, False):
                                self.__loggerProfissaoDao.info(f'({profissaoServidor}) sincronizado com sucesso!')
                            continue
                        profissaoDao = ProfissaoDaoSqlite(personagem)
                        if profissaoDao.insereProfissao(profissaoServidor, False):
                            self.__loggerProfissaoDao.info(f'({profissaoServidor}) inserido com sucesso!')
                        continue
                    self.__loggerProfissaoDao.error(f'Erro ao pegar profissão por id ({profissaoServidor}): {profissaoDao.pegaErro()}')
                profissaoDao = ProfissaoDaoSqlite(personagem)
                profissoesBanco = profissaoDao.pegaProfissoes()
                if variavelExiste(profissoesBanco):
                    novaLista = []
                    for profissaoBanco in profissoesBanco:
                        for profissaoServidor in profissoesServidor:
                            if profissaoBanco.id == profissaoServidor.id:
                                break
                        else:
                            novaLista.append(profissaoBanco)
                    for profissaoBanco in novaLista:
                        profissaoDao = ProfissaoDaoSqlite(personagem)
                        if profissaoDao.removeProfissao(profissaoBanco, False):
                            self.__loggerProfissaoDao.info(f'({profissaoBanco.nome}) removido do banco com sucesso!')
                            continue
                        self.__loggerProfissaoDao.error(f'Erro ao remover ({profissaoBanco.nome}) do banco: {profissaoDao.pegaErro()}')
                    continue
                self.__loggerProfissaoDao.error(f'Erro ao buscar trabalhos em produção no banco: {profissaoDao.pegaErro()}')
                continue
            self.__loggerRepositorioProfissao.error(f'Erro ao pegar profissões: {repositorioProfissao.pegaErro()}')
    
    def sincronizaTrabalhosProducao(self):
        personagens = self.pegaPersonagens()
        for personagem in personagens:
            self.personagemEmUso(personagem)
            repositorioTrabalhoProducao = RepositorioTrabalhoProducao(self.__personagemEmUso)
            trabalhosProducaoServidor = repositorioTrabalhoProducao.pegaTodosTrabalhosProducao()
            if variavelExiste(trabalhosProducaoServidor):
                for trabalhoProducaoServidor in trabalhosProducaoServidor:
                    limpaTela()
                    print(f'Sincronizando trabalhos para produção...')
                    print(f'Personagens: {(personagens.index(personagem)+1)/len(personagens):.2%}')
                    print(f'Trabalhos: {(trabalhosProducaoServidor.index(trabalhoProducaoServidor)+1)/len(trabalhosProducaoServidor):.2%}')
                    trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
                    trabalhoProducaoEncontradoBanco = trabalhoProducaoDao.pegaTrabalhoProducaoPorId(trabalhoProducaoServidor)
                    if variavelExiste(trabalhoProducaoEncontradoBanco):
                        if trabalhoProducaoEncontradoBanco.id == trabalhoProducaoServidor.id:
                            self.modificaTrabalhoProducao(trabalhoProducaoServidor, None, False)
                            continue
                        self.insereTrabalhoProducao(trabalhoProducaoServidor, False)
                        continue
                    self.__loggerTrabalhoProducaoDao.error(f'Erro ao buscar profissão ({trabalhoProducaoServidor}): {trabalhoProducaoDao.pegaErro()}')
                    continue
                trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
                trabalhosProducaoBanco = trabalhoProducaoDao.pegaTrabalhosProducao()
                if variavelExiste(trabalhosProducaoBanco):
                    novaLista = []
                    for trabalhoProducaoBanco in trabalhosProducaoBanco:
                        for trabalhoProducaoServidor in trabalhosProducaoServidor:
                            if trabalhoProducaoBanco.id == trabalhoProducaoServidor.id:
                                break
                        else:
                            novaLista.append(trabalhoProducaoBanco)
                    for trabalhoProducaoBanco in novaLista:
                        self.removeTrabalhoProducao(trabalhoProducaoBanco, None, False)
                    continue
                self.__loggerTrabalhoProducaoDao.error(f'Erro ao buscar trabalhos em produção no banco: {trabalhoProducaoDao.pegaErro()}')
                continue
            self.__loggerTrabalhoProducaoDao.error(f'Erro ao buscar trabalhos em produção no servidor: {repositorioTrabalhoProducao.pegaErro()}')

    def pegaPersonagens(self):
        repositorioPersonagem = RepositorioPersonagem()
        personagens = repositorioPersonagem.pegaTodosPersonagens()
        if variavelExiste(personagens):
            return personagens
        self.__loggerRepositorioPersonagem.error(f'Erro ao pegar personagens no servidor: {repositorioPersonagem.pegaErro()}')
        return []

    def pegaTrabalhosBanco(self) -> list[Trabalho]:
        trabalhoDao = TrabalhoDaoSqlite()
        trabalhos = trabalhoDao.pegaTrabalhos()
        if variavelExiste(trabalhos):
            return trabalhos
        self.__loggerTrabalhoDao.error(f'Erro ao pegar trabalhos no banco: {trabalhoDao.pegaErro()}')
        return []
    
    def pegaTrabalhoPorNome(self, nomeTrabalho: str) -> Trabalho | None:
        trabalhoDao = TrabalhoDaoSqlite()
        trabalhoEncontrado = trabalhoDao.pegaTrabalhoPorNome(nomeTrabalho)
        if trabalhoEncontrado is None:
            self.__loggerTrabalhoDao.error(f'Erro ao pegar ({nomeTrabalho}) por nome no banco: {trabalhoDao.pegaErro()}')
            return None
        if trabalhoEncontrado.nome is None:
            self.__loggerTrabalhoDao.warning(f'({nomeTrabalho}) não encontrado no banco!')
            return None
        return trabalhoEncontrado


    def sincronizaTrabalhosVendidos(self):
        personagens = self.pegaPersonagens()
        for personagem in personagens:

            pass
        

    def sincronizaDados(self):
        # self.sincronizaListaTrabalhos()
        # self.sincronizaListaPersonagens()
        self.sincronizaListaProfissoes()
        # self.sincronizaTrabalhosVendidos()

    def preparaPersonagem(self):
        self.abreStreamTrabalhos()
        self.abreStreamPersonagens()
        sincroniza = input(f'Sincronizar listas? (S/N) ')
        if sincroniza is not None and sincroniza.lower() == 's':
            self.sincronizaListaTrabalhos()
            self.sincronizaListaPersonagens
            self.sincronizaTrabalhosProducao()
            self.sincronizaListaProfissoes()
        clickAtalhoEspecifico('alt', 'tab')
        clickAtalhoEspecifico('win', 'left')
        self.iniciaProcessoBusca()

    def abreStreamPersonagens(self):
        if self.__repositorioPersonagem.abreStream():
            self.__loggerRepositorioPersonagem.info(f'Stream repositório personagem iniciada!')
            return
        self.__loggerRepositorioPersonagem.error(f'Erro ao iniciar stream repositório personagem: {self.__repositorioPersonagem.pegaErro()}')

    def abreStreamTrabalhos(self):
        if self.__repositorioTrabalho.abreStream():
            self.__loggerRepositorioTrabalho.info(f'Stream repositório trabalhos iniciada!')
            return
        self.__loggerRepositorioTrabalho.error(f'Erro ao iniciar stream repositório trabalhos: {self.__repositorioTrabalho.pegaErro()}')

    def modificaTrabalho(self, trabalho: Trabalho, modificaServidor: bool = True) -> bool:
        trabalhoDao = TrabalhoDaoSqlite()
        if trabalhoDao.modificaTrabalho(trabalho, modificaServidor):
            self.__loggerTrabalhoDao.info(f'({trabalho}) modificado no banco com sucesso!')
            return True
        self.__loggerTrabalhoDao.error(f'Erro ao modificar ({trabalho}) no banco: {trabalhoDao.pegaErro()}')
        return False

    def pegaTodosTrabalhosEstoque(self):
        limpaTela()
        estoqueDao = EstoqueDaoSqlite()
        estoque = estoqueDao.pegaTodosTrabalhosEstoque()
        if not variavelExiste(estoque):
            print(f'Erro ao buscar todos trabalhos em estoque: {estoqueDao.pegaErro()}')
            input(f'Clique para continuar...')
            return
        for trabalhoEstoque in estoque:
            print(trabalhoEstoque)
        input(f'Clique para continuar...')

    def pegaTodosTrabalhosVendidos(self):
        limpaTela()
        vendaDao = VendaDaoSqlite()
        vendas = vendaDao.pegaTodosTrabalhosVendidos()
        if not variavelExiste(vendas):
            print(f'Erro ao buscar todas as vendas: {vendaDao.pegaErro()}')
            input(f'Clique para continuar...')
            return
        print(f'{"NOME".ljust(113)} | {"DATA".ljust(10)} | {"ID TRABALHO".ljust(36)} | {"VALOR".ljust(5)} | UND')
        for trabalhoVendido in vendas:
            print(trabalhoVendido)
        input(f'Clique para continuar...')

    def pegaTodosTrabalhosProducao(self):
        limpaTela()
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite()
        trabalhosProducao = trabalhoProducaoDao.pegaTodosTrabalhosProducao()
        if not variavelExiste(trabalhosProducao):
            print(f'Erro ao buscar todas os trabalhos em produção: {trabalhoProducaoDao.pegaErro()}')
            input(f'Clique para continuar...')
            return
        # print(f'{"NOME".ljust(113)} | {"DATA".ljust(10)} | {"ID TRABALHO".ljust(36)} | {"VALOR".ljust(5)} | UND')
        for trabalhoProducao in trabalhosProducao:
            print(trabalhoProducao)
        input(f'Clique para continuar...')

    def pegaTodasProfissoes(self):
        limpaTela()
        profissaoDao = ProfissaoDaoSqlite()
        profissoes = profissaoDao.pegaTodasProfissoes()
        if not variavelExiste(profissoes):
            print(f'Erro ao buscar todas as profissões: {profissaoDao.pegaErro()}')
            input(f'Clique para continuar...')
        for profissao in profissoes:
            
            print(profissao)
        input(f'Clique para continuar...')

if __name__=='__main__':
    Aplicacao().preparaPersonagem()