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
        self._imagem = ManipulaImagem()
        self.__listaPersonagemJaVerificado = []
        self.__listaPersonagemAtivo = []
        self.__listaProfissoesNecessarias = []
        self.__personagemEmUso = None
        self.__repositorioTrabalho = RepositorioTrabalho()

    def defineListaPersonagemMesmoEmail(self):
        listaDicionarioPersonagemMesmoEmail = []
        if variavelExiste(self.__personagemEmUso):
            personagemDao = PersonagemDaoSqlite()
            personagens = personagemDao.pegaPersonagens()
            if not variavelExiste(personagens):
                logger = logging.getLogger('personagemDao')
                logger.error(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
                print(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
                return listaDicionarioPersonagemMesmoEmail
            for personagem in personagens:
                if textoEhIgual(personagem.email, self.__personagemEmUso.email):
                    listaDicionarioPersonagemMesmoEmail.append(personagem)
        return listaDicionarioPersonagemMesmoEmail

    def modificaAtributoUso(self): 
        listaPersonagemMesmoEmail = self.defineListaPersonagemMesmoEmail()
        personagemDao = PersonagemDaoSqlite()
        personagens = personagemDao.pegaPersonagens()
        if not variavelExiste(personagens):
            logger = logging.getLogger('personagemDao')
            logger.error(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
            print(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
            return
        for personagem in personagens:
            for personagemMesmoEmail in listaPersonagemMesmoEmail:
                if textoEhIgual(personagem.id, personagemMesmoEmail.id):
                    if not personagem.uso:
                        personagem.alternaUso()
                        personagemDao = PersonagemDaoSqlite()
                        if personagemDao.modificaPersonagem(personagem):
                            uso = 'verdadeiro' if personagem.uso else 'falso'
                            print(f'{personagem.nome}: Uso modificado para {uso} com sucesso!')
                            break
                        logger = logging.getLogger('personagemDao')
                        logger.error(f'Erro ao modificar personagem: {personagemDao.pegaErro()}')
                        print(f'Erro: {personagemDao.pegaErro()}')
                    break
            else:
                if personagem.uso:
                    personagem.alternaUso()
                    personagemDao = PersonagemDaoSqlite()
                    if personagemDao.modificaPersonagem(personagem):
                        uso = personagem.uso
                        print(f'{personagem.nome}: Uso modificado para {uso} com sucesso!')
                        continue
                    logger = logging.getLogger('personagemDao')
                    logger.error(f'Erro ao modificar personagem: {personagemDao.pegaErro()}')
                    print(f'Erro: {personagemDao.pegaErro()}')

    def confirmaNomePersonagem(self, personagemReconhecido):
        '''
        Esta função é responsável por confirmar se o nome do personagem reconhecido está na lista de personagens ativos atual
        Argumentos:
            personagemReconhecido {string} -- Valor reconhecido via processamento de imagem
        '''
        for personagemAtivo in self.__listaPersonagemAtivo:
            if textoEhIgual(personagemReconhecido, personagemAtivo.nome):
                print(f'Personagem {personagemReconhecido} confirmado!')
                self.__personagemEmUso = personagemAtivo
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
        personagemDao = PersonagemDaoSqlite()
        personagens = personagemDao.pegaPersonagens()
        if not variavelExiste(personagens):
            logger = logging.getLogger('personagemDao')
            logger.error(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
            print(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
            return
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
                    if texto1PertenceTexto2('personagem',textoMenu):
                        print(f'Menu escolha de personagem...')
                        return MENU_ESCOLHA_PERSONAGEM
                    if texto1PertenceTexto2('artesanato',textoMenu):
                        textoMenu = self._imagem.retornaTextoMenuReconhecido(266, 242, 150)
                        if variavelExiste(textoMenu):
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
                print(f'Menu não reconhecido...')
                self.verificaErro()
                return MENU_DESCONHECIDO
            clickAtalhoEspecifico('win','left')
            clickAtalhoEspecifico('win','left')
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
        logger = logging.getLogger('vendaDao')
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
                    logger.info(f'({trabalhoVendido}) inserido com sucesso!')
                    return trabalhoVendido
                logger.error(f'Erro ao inserir ({trabalhoVendido}): {vendaDAO.pegaErro()}')
        return None

    def retornaChaveIdTrabalho(self, textoCarta):
        trabalhoDao = TrabalhoDaoSqlite()
        trabalhos = trabalhoDao.pegaTrabalhos()
        if variavelExiste(trabalhos):
            for trabalho in trabalhos:
                if texto1PertenceTexto2(trabalho.nome, textoCarta):
                    return trabalho.id
            return ''
        logger = logging.getLogger('trabalhoDao')
        logger.error(f'Erro ao buscar trabalhos no banco: {trabalhoDao.pegaErro()}')
        print(f'Erro ao buscar trabalhos no banco: {trabalhoDao.pegaErro()}')
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
        trabalhoDao = TrabalhoDaoSqlite()
        trabalhos = trabalhoDao.pegaTrabalhos()
        if variavelExiste(trabalhos):
            for trabalho in trabalhos:
                if texto1PertenceTexto2(nomeTrabalhoConcluido[1:-1], trabalho.nomeProducao):
                    listaPossiveisDicionariosTrabalhos.append(trabalho)
            return listaPossiveisDicionariosTrabalhos
        logger = logging.getLogger('trabalhoDao')
        logger.error(f'Erro ao buscar trabalhos no banco: {trabalhoDao.pegaErro()}')
        return listaPossiveisDicionariosTrabalhos
    
    def insereTrabalhoProducao(self, trabalhoProducao):
        if variavelExiste(trabalhoProducao):
            logger = logging.getLogger('trabalhoProducaoDao')
            trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
            if trabalhoProducaoDao.insereTrabalhoProducao(trabalhoProducao):
                logger.info(f'({trabalhoProducao}) inserido com sucesso!')
                return True
            logger.error(f'Erro ao inserir ({trabalhoProducao}): {trabalhoProducaoDao.pegaErro()}')
            return False

    def retornaTrabalhoConcluido(self, nomeTrabalhoConcluido):
        listaPossiveisTrabalhos = self.retornaListaPossiveisTrabalhoRecuperado(nomeTrabalhoConcluido)
        if tamanhoIgualZero(listaPossiveisTrabalhos):
            return None
        for possivelTrabalho in listaPossiveisTrabalhos:
            trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
            trabalhosProducao = trabalhoProducaoDao.pegaTrabalhosProducaoParaProduzirProduzindo()
            if variavelExiste(trabalhosProducao):
                for trabalhoProduzirProduzindo in trabalhosProducao:
                    nomeEhIgualEEhProduzindo = trabalhoProduzirProduzindo.ehProduzindo() and textoEhIgual(trabalhoProduzirProduzindo.nome, possivelTrabalho.nome)
                    if nomeEhIgualEEhProduzindo:
                        trabalhoProduzirProduzindo.estado = CODIGO_CONCLUIDO
                        trabalhoProduzirProduzindo.trabalhoId = possivelTrabalho.id
                        trabalhoProduzirProduzindo.nomeProducao = possivelTrabalho.nomeProducao
                        return trabalhoProduzirProduzindo
            else:
                logger = logging.getLogger('trabalhoProducaoDao')
                logger.error(f'Erro ao bucar trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
                continue
        else:
            print(f'Trabalho concluído ({listaPossiveisTrabalhos[0].nome}) não encontrado na lista produzindo...')
            trabalhoProducaoConcluido = TrabalhoProducao()
            trabalhoProducaoConcluido.dicionarioParaObjeto(listaPossiveisTrabalhos[0].__dict__)
            trabalhoProducaoConcluido.trabalhoId = listaPossiveisTrabalhos[0].id
            trabalhoProducaoConcluido.recorrencia = False
            trabalhoProducaoConcluido.tipo_licenca = CHAVE_LICENCA_NOVATO
            trabalhoProducaoConcluido.estado = CODIGO_CONCLUIDO
            self.insereTrabalhoProducao(trabalhoProducaoConcluido)
            return trabalhoProducaoConcluido

    def modificaTrabalhoConcluidoListaProduzirProduzindo(self, trabalhoProducaoConcluido):
        logger = logging.getLogger('trabalhoProducaoDao')
        if trabalhoEhProducaoRecursos(trabalhoProducaoConcluido):
            trabalhoProducaoConcluido.recorrencia = True
        if trabalhoProducaoConcluido.recorrencia:
            print(f'Trabalho recorrente.')
            trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
            if trabalhoProducaoDao.removeTrabalhoProducao(trabalhoProducaoConcluido):
                logger.info(f'({trabalhoProducaoConcluido}) removido com sucesso!')
                return trabalhoProducaoConcluido
            logger.error(f'Erro ao remover ({trabalhoProducaoConcluido}): {trabalhoProducaoDao.pegaErro()}')
            return trabalhoProducaoConcluido
        print(f'Trabalho sem recorrencia.')
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
        if trabalhoProducaoDao.modificaTrabalhoProducao(trabalhoProducaoConcluido):
            logger.info(f'({trabalhoProducaoConcluido}) modificado com sucesso!.')
            return trabalhoProducaoConcluido
        logger.error(f'Erro ao modificar ({trabalhoProducaoConcluido}): {trabalhoProducaoDao.pegaErro()}')
        return trabalhoProducaoConcluido

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
                trabalhoEstoque.trabalhoId = trabalhoProducaoConcluido.trabalhoId
            else:
                if trabalhoEhMelhoriaEssenciaComum(trabalhoProducaoConcluido):
                    trabalhoEstoque = TrabalhoEstoque()
                    trabalhoEstoque.nome = 'Essência composta'
                    trabalhoEstoque.profissao = ''
                    trabalhoEstoque.nivel = 0
                    trabalhoEstoque.quantidade = 5
                    trabalhoEstoque.raridade = 'Recurso'
                    trabalhoEstoque.trabalhoId = trabalhoProducaoConcluido.trabalhoId
                elif trabalhoEhMelhoriaEssenciaComposta(trabalhoProducaoConcluido):
                    trabalhoEstoque = TrabalhoEstoque()
                    trabalhoEstoque.nome = 'Essência de energia'
                    trabalhoEstoque.profissao = ''
                    trabalhoEstoque.nivel = 0
                    trabalhoEstoque.quantidade = 1
                    trabalhoEstoque.raridade = 'Recurso'
                    trabalhoEstoque.trabalhoId = trabalhoProducaoConcluido.trabalhoId
                elif trabalhoEhMelhoriaSubstanciaComum(trabalhoProducaoConcluido):
                    trabalhoEstoque = TrabalhoEstoque()
                    trabalhoEstoque.nome = 'Substância composta'
                    trabalhoEstoque.profissao = ''
                    trabalhoEstoque.nivel = 0
                    trabalhoEstoque.quantidade = 5
                    trabalhoEstoque.raridade = 'Recurso'
                    trabalhoEstoque.trabalhoId = trabalhoProducaoConcluido.trabalhoId
                elif trabalhoEhMelhoriaSubstanciaComposta(trabalhoProducaoConcluido):
                    trabalhoEstoque = TrabalhoEstoque()
                    trabalhoEstoque.nome = 'Substância energética'
                    trabalhoEstoque.profissao = ''
                    trabalhoEstoque.nivel = 0
                    trabalhoEstoque.quantidade = 1
                    trabalhoEstoque.raridade = 'Recurso'
                    trabalhoEstoque.trabalhoId = trabalhoProducaoConcluido.trabalhoId
                elif trabalhoEhMelhoriaCatalisadorComum(trabalhoProducaoConcluido):
                    trabalhoEstoque = TrabalhoEstoque()
                    trabalhoEstoque.nome = 'Catalisador amplificado'
                    trabalhoEstoque.profissao = ''
                    trabalhoEstoque.nivel = 0
                    trabalhoEstoque.quantidade = 5
                    trabalhoEstoque.raridade = 'Recurso'
                    trabalhoEstoque.trabalhoId = trabalhoProducaoConcluido.trabalhoId
                elif trabalhoEhMelhoriaCatalisadorComposto(trabalhoProducaoConcluido):
                    trabalhoEstoque = TrabalhoEstoque()
                    trabalhoEstoque.nome = 'Catalisador de energia'
                    trabalhoEstoque.profissao = ''
                    trabalhoEstoque.nivel = 0
                    trabalhoEstoque.quantidade = 1
                    trabalhoEstoque.raridade = 'Recurso'
                    trabalhoEstoque.trabalhoId = trabalhoProducaoConcluido.trabalhoId
                if variavelExiste(trabalhoEstoque):
                    if textoEhIgual(trabalhoProducaoConcluido.tipo_licenca, CHAVE_LICENCA_APRENDIZ):
                        trabalhoEstoque.quantidade = trabalhoEstoque.quantidade * 2
            if variavelExiste(trabalhoEstoque):
                listaTrabalhoEstoqueConcluido.append(trabalhoEstoque)
            if trabalhoEhColecaoRecursosComuns(trabalhoProducaoConcluido) or trabalhoEhColecaoRecursosAvancados(trabalhoProducaoConcluido):
                    nivelColecao = 1
                    if trabalhoEhColecaoRecursosAvancados(trabalhoProducaoConcluido):
                        nivelColecao = 8
                    trabalhoDao = TrabalhoDaoSqlite()
                    trabalhos = trabalhoDao.pegaTrabalhos()
                    if not variavelExiste(trabalhos):
                        logger = logging.getLogger('trabalhoDao')
                        logger.error(f'Erro ao buscar trabalhos no banco: {trabalhoDao.pegaErro()}')
                        print(f'Erro ao buscar trabalhos no banco: {trabalhoDao.pegaErro()}')
                        return listaTrabalhoEstoqueConcluido
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
                    trabalhoEstoque.trabalhoId = trabalhoProducaoConcluido.trabalhoId
                    tipoRecurso = retornaChaveTipoRecurso(trabalhoEstoque)
                    if variavelExiste(tipoRecurso):
                        if tipoRecurso == CHAVE_RCS or tipoRecurso == CHAVE_RCT:
                            trabalhoEstoque.quantidade = 1
                        elif tipoRecurso == CHAVE_RCP or tipoRecurso == CHAVE_RAP or tipoRecurso == CHAVE_RAS or tipoRecurso == CHAVE_RAT:
                            trabalhoEstoque.quantidade = 2
                        if textoEhIgual(trabalhoProducaoConcluido[CHAVE_TIPO_LICENCA], CHAVE_LICENCA_APRENDIZ):
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
            trabalhoEstoque.trabalhoId = trabalhoProducaoConcluido.trabalhoId
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
        if variavelExiste(profissao):
            if trabalhoProducaoConcluido.ehMelhorado():
                trabalhoDao = TrabalhoDaoSqlite()
                trabalhos = trabalhoDao.pegaTrabalhos()
                if variavelExiste(trabalhos):
                    for trabalho in trabalhos:
                        trabalhoNecessarioEhIgualNomeTrabalhoConcluido = textoEhIgual(trabalho.trabalhoNecessario, trabalhoProducaoConcluido.nome)
                        if trabalhoNecessarioEhIgualNomeTrabalhoConcluido:
                            licencaProducaoIdeal = CHAVE_LICENCA_NOVATO if profissao.pegaExperienciaMaximaPorNivel() >= profissao.pegaExperienciaMaxima() else CHAVE_LICENCA_INICIANTE
                            trabalhoProducaoRaro = TrabalhoProducao()
                            trabalhoProducaoRaro.dicionarioParaObjeto(trabalho.__dict__)
                            trabalhoProducaoRaro.id = str(uuid.uuid4())
                            trabalhoProducaoRaro.trabalhoId = trabalho.id
                            trabalhoProducaoRaro.experiencia = trabalho.experiencia * 1.5
                            trabalhoProducaoRaro.recorrencia = False
                            trabalhoProducaoRaro.tipo_licenca = licencaProducaoIdeal
                            trabalhoProducaoRaro.estado = CODIGO_PARA_PRODUZIR
                            return trabalhoProducaoRaro
                    return None
                logger = logging.getLogger('trabalhoDao')
                logger.error(f'Erro ao buscar trabalhos no banco: {trabalhoDao.pegaErro()}')
        return None

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
            personagemDao = PersonagemDaoSqlite()
            personagens = personagemDao.pegaPersonagens()
            if not variavelExiste(personagens):
                logger = logging.getLogger('personagemDao')
                logger.error(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
                print(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
                return
            for personagem in personagens:
                if not personagem.estado :
                    personagem.alternaEstado()
                    personagemDao = PersonagemDaoSqlite()
                    if personagemDao.modificaPersonagem(personagem):
                        estado = 'verdadeiro' if personagem.estado else 'falso'
                        print(f'{personagem.nome}: Estado modificado para {estado} com sucesso!')
                        continue
                    logger = logging.getLogger('personagemDao')
                    logger.error(f'Erro ao modificar personagem: {personagemDao.pegaErro()}')
                    print(f'Erro: {personagemDao.pegaErro()}')
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

    def retornaListaTrabalhosRarosVendidos(self):
        print(f'Definindo lista produtos raros vendidos...')
        trabalhosRarosVendidos = []
        trabalhoVendidoDao = VendaDaoSqlite(self.__personagemEmUso)
        vendas = trabalhoVendidoDao.pegaVendas()
        if variavelExiste(vendas):
            for trabalhoVendido in vendas:
                trabalhoDao = TrabalhoDaoSqlite()
                trabalhoEncontrado = trabalhoDao.pegaTrabalhoEspecificoPorId(trabalhoVendido.trabalhoId)
                logger = logging.getLogger('trabalhoDao')
                if variavelExiste(trabalhoEncontrado):
                    if variavelExiste(trabalhoEncontrado.nome):
                        trabalhoEhRaroETrabalhoNaoEhProducaoDeRecursos = trabalhoEncontrado.ehRaro() and not trabalhoEhProducaoRecursos(trabalhoEncontrado)
                        if trabalhoEhRaroETrabalhoNaoEhProducaoDeRecursos:
                            trabalhosRarosVendidos.append(trabalhoVendido)
                            continue
                    logger.warning(f'Trabalho ({trabalhoVendido}) não foi encontrado na lista de trabalhos!')
                    continue
                logger.error(f'Erro ao buscar trabalho especifico ({trabalhoVendido}) no banco: {trabalhoDao.pegaErro()}')
                return trabalhosRarosVendidosOrdenados
            trabalhosRarosVendidosOrdenados = sorted(trabalhosRarosVendidos, key = lambda trabalho: (trabalho.profissao, trabalho.nivel, trabalho.nome))
            return trabalhosRarosVendidosOrdenados
        logger = logging.getLogger('vendasDao')
        logger.error(f'Erro ao buscar trabalhos vendidos: {trabalhoVendidoDao.pegaErro()}')
        return trabalhosRarosVendidosOrdenados

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
            personagemDao = PersonagemDaoSqlite()
            if personagemDao.modificaPersonagem(self.__personagemEmUso):
                print(f'{self.__personagemEmUso.nome}: Espaço de produção modificado para {self.__personagemEmUso.espacoProducao} com sucesso!')
                return
            logger = logging.getLogger('personagemDao')
            logger.error(f'Erro ao modificar personagem: {personagemDao.pegaErro()}')
            print(f'Erro ao modificar personagem: {personagemDao.pegaErro()}')

    def retornaListaTrabalhosProducaoRaridadeEspecifica(self, dicionarioTrabalho, raridade):
        listaTrabalhosProducaoRaridadeEspecifica = []
        print(f'Buscando trabalho {raridade} na lista...')
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
        trabalhosProducao = trabalhoProducaoDao.pegaTrabalhosProducaoParaProduzirProduzindo()
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
        logger = logging.getLogger('trabalhoProducaoDao')
        logger.error(f'Erro ao bucar trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
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
        return cloneTrabalhoProducao
    

    def clonaTrabalhoProducaoEncontrado(self, dicionarioTrabalho, trabalhoProducaoEncontrado):
        print(f'Recorrencia está ligada.')
        cloneTrabalhoProducaoEncontrado = self.defineCloneTrabalhoProducao(trabalhoProducaoEncontrado)
        dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = cloneTrabalhoProducaoEncontrado
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
                    logger = logging.getLogger('trabalhoProducaoDao')
                    if trabalhoProducaoEncontrado.ehRecorrente():
                        self.clonaTrabalhoProducaoEncontrado(dicionarioTrabalho, trabalhoProducaoEncontrado)
                        self.verificaNovamente = True
                        break
                    trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
                    if trabalhoProducaoDao.modificaTrabalhoProducao(trabalhoProducaoEncontrado):
                        estado = 'produzir' if trabalhoProducaoEncontrado.estado  == 0 else 'produzindo' if trabalhoProducaoEncontrado.estado  == 1 else 'concluido'
                        logger.info(f'({trabalhoProducaoEncontrado}) modificado para {estado} com sucesso!.')
                    else:
                        logger.error(f'Erro ao modificar ({trabalhoProducaoEncontrado}): {trabalhoProducaoDao.pegaErro()}')
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
                                            personagemDao = PersonagemDaoSqlite()
                                            if personagemDao.modificaPersonagem(self.__personagemEmUso):
                                                estado = 'verdadeiro' if self.__personagemEmUso.estado  else 'falso'
                                                print(f'{self.__personagemEmUso.nome}: Estado modificado para {estado} com sucesso!')
                                            else:
                                                logger = logging.getLogger('personagemDao')
                                                logger.error(f'Erro ao modificar personagem: {personagemDao.pegaErro()}')
                                                print(f'Erro ao modificar personagem: {personagemDao.pegaErro()}')
                                            clickEspecifico(3, 'f1')
                                            clickContinuo(10, 'up')
                                            clickEspecifico(1, 'left')
                                            return dicionarioTrabalho
                                    else:
                                        print(f'{trabalhoProducaoEncontrado.tipo_licenca} não encontrado!')
                                        print(f'Licença buscada agora é Licença de produção do iniciante!')
                                        trabalhoProducaoEncontrado.tipo_licenca = CHAVE_LICENCA_NOVATO
                                        dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = trabalhoProducaoEncontrado
                                else:
                                    if len(listaCiclo) > 10:
                                        print(f'{trabalhoProducaoEncontrado.tipo_licenca} não encontrado!')
                                        print(f'Licença buscada agora é Licença de produção do iniciante!')
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
                        personagemDao = PersonagemDaoSqlite()
                        if personagemDao.modificaPersonagem(self.__personagemEmUso):
                            estado = 'verdadeiro' if self.__personagemEmUso.estado  else 'falso'
                            print(f'{self.__personagemEmUso.nome}: Estado modificado para {estado} com sucesso!')
                        else:
                            logger = logging.getLogger('personagemDao')
                            logger.error(f'Erro ao modificar personagem: {personagemDao.pegaErro()}')   
                            print(f'Erro ao modificar personagem: {personagemDao.pegaErro()}')
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
            logger = logging.getLogger('trabalhoProducaoDao')
            while erroEncontrado(erro):
                if ehErroRecursosInsuficiente(erro):
                    self.__confirmacao = False
                    trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
                    if trabalhoProducaoDao.removeTrabalhoProducao(trabalhoProducaoEncontrado):
                        logger.info(f'({trabalhoProducaoEncontrado}) removido com sucesso!')
                        erro = self.verificaErro()
                        continue
                    logger.error(f'Erro ao remover ({trabalhoProducaoEncontrado}): {trabalhoProducaoDao.pegaErro()}')
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
        trabalhoDao = TrabalhoDaoSqlite()
        trabalhos = trabalhoDao.pegaTrabalhos()
        if not variavelExiste(trabalhos):
            logger = logging.getLogger('trabalhoDao')
            logger.error(f'Erro ao buscar trabalhos no banco: {trabalhoDao.pegaErro()}')
            print(f'Erro ao buscar trabalhos no banco: {trabalhoDao.pegaErro()}')
            return listaPossiveisTrabalhos
        for trabalho in trabalhos:
            if texto1PertenceTexto2(nomeTrabalhoConcluido[1:-1], trabalho.nomeProducao):
                trabalhoEncontrado = TrabalhoProducao()
                trabalhoEncontrado.dicionarioParaObjeto(trabalho.__dict__)
                trabalhoEncontrado.id = str(uuid.uuid4())
                trabalhoEncontrado.trabalhoId = trabalho.id
                trabalhoEncontrado.recorrencia = False
                trabalhoEncontrado.tipo_licenca = CHAVE_LICENCA_NOVATO
                trabalhoEncontrado.estado = CODIGO_CONCLUIDO
                listaPossiveisTrabalhos.append(trabalhoEncontrado)
        return listaPossiveisTrabalhos

    def retornaTrabalhoProducaoConcluido(self, nomeTrabalhoConcluido):
        listaPossiveisTrabalhosProducao = self.retornaListaPossiveisTrabalhos(nomeTrabalhoConcluido)
        if not tamanhoIgualZero(listaPossiveisTrabalhosProducao):
            trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
            trabalhosProducao = trabalhoProducaoDao.pegaTrabalhosProducaoParaProduzirProduzindo()
            if not variavelExiste(trabalhosProducao):
                logger = logging.getLogger('trabalhoProducaoDao')
                logger.error(f'Erro ao bucar trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
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
                listaDeListasTrabalhosProducao = self.retornaListaDeListasTrabalhosProducao(dicionarioTrabalho)
                for listaTrabalhosProducao in listaDeListasTrabalhosProducao:
                    if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not self.__confirmacao:
                        break
                    dicionarioTrabalho[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA] = listaTrabalhosProducao
                    for trabalhoProducaoPriorizado in dicionarioTrabalho[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA]:
                        if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not self.__confirmacao:
                            break
                        if trabalhoProducaoPriorizado.ehEspecial() or trabalhoProducaoPriorizado.ehRaro():
                            print(f'Trabalho desejado: {trabalhoProducaoPriorizado.nome}.')
                            posicaoAux = -1
                            if dicionarioTrabalho[CHAVE_POSICAO] != -1:
                                posicaoAux = dicionarioTrabalho[CHAVE_POSICAO]
                            dicionarioTrabalho[CHAVE_POSICAO] = 0
                            while naoFizerQuatroVerificacoes(dicionarioTrabalho) and not chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
                                nomeTrabalhoReconhecido = self.retornaNomeTrabalhoPosicaoTrabalhoRaroEspecial(dicionarioTrabalho)
                                print(f'Trabalho {trabalhoProducaoPriorizado.raridade} reconhecido: {nomeTrabalhoReconhecido}.')
                                if variavelExiste(nomeTrabalhoReconhecido):
                                    if texto1PertenceTexto2(nomeTrabalhoReconhecido[:-1], trabalhoProducaoPriorizado.nomeProducao):
                                        erro = self.verificaErro()
                                        if erroEncontrado(erro):
                                            if ehErroOutraConexao(erro) or ehErroConectando(erro) or ehErroRestauraConexao(erro):
                                                self.__confirmacao = False
                                                if ehErroOutraConexao(erro):
                                                    dicionarioTrabalho[CHAVE_UNICA_CONEXAO] = False
                                        else:
                                            entraTrabalhoEncontrado(dicionarioTrabalho)
                                        if self.__confirmacao:
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
                            if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not self.__confirmacao:
                                break
                            continue
                        if trabalhoProducaoPriorizado.ehMelhorado() or trabalhoProducaoPriorizado.ehComum():
                            dicionarioTrabalho = self.defineDicionarioTrabalhoComumMelhorado(dicionarioTrabalho)
                            if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not self.__confirmacao:
                                break
                            elif listaDeListasTrabalhosProducao.index(listaTrabalhosProducao) + 1 >= len(listaDeListasTrabalhosProducao):
                                vaiParaMenuTrabalhoEmProducao()
                            else:
                                vaiParaOTopoDaListaDeTrabalhosComunsEMelhorados(dicionarioTrabalho)
                if self.__confirmacao:
                    if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
                        dicionarioTrabalho = self.iniciaProcessoDeProducao(dicionarioTrabalho)
                    else:
                        saiProfissaoVerificada(dicionarioTrabalho)
                    if self._unicaConexao and self._espacoBolsa:
                        if self._imagem.retornaEstadoTrabalho() == CODIGO_CONCLUIDO:
                            nomeTrabalhoConcluido = self.reconheceRecuperaTrabalhoConcluido()
                            if variavelExiste(nomeTrabalhoConcluido):
                                trabalhoProducaoConcluido = self.retornaTrabalhoProducaoConcluido(nomeTrabalhoConcluido)
                                if variavelExiste(trabalhoProducaoConcluido):
                                    trabalhoProducaoConcluido = self.modificaTrabalhoConcluidoListaProduzirProduzindo(trabalhoProducaoConcluido)
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

    def iniciaProcessoBusca(self):
        while True:
            self.verificaAlteracaoListaTrabalhos()
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
                    # while defineTrabalhoComumProfissaoPriorizada():
                    #     continue
                    trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
                    trabalhosProducao = trabalhoProducaoDao.pegaTrabalhosProducaoParaProduzirProduzindo()
                    if not variavelExiste(trabalhosProducao):
                        logger = logging.getLogger('trabalhoProducaoDao')
                        logger.error(f'Erro ao bucar trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
                        continue
                    if tamanhoIgualZero(trabalhosProducao):
                        print(f'Lista de trabalhos desejados vazia.')
                        self.__personagemEmUso.alternaEstado()
                        personagemDao = PersonagemDaoSqlite()
                        if personagemDao.modificaPersonagem(self.__personagemEmUso):
                            estado = 'verdadeiro' if self.__personagemEmUso.estado  else 'falso'
                            print(f'{self.__personagemEmUso.nome}: Estado modificado para {estado} com sucesso!')
                            continue
                        logger = logging.getLogger('personagemDao')
                        logger.error(f'Erro ao modificar personagem: {personagemDao.pegaErro()}')
                        print(f'Erro modificar personagem: {personagemDao.pegaErro()}')
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

    def verificaAlteracaoListaTrabalhos(self):
        if self.__repositorioTrabalho.estaPronto:
            print(f'Lista de trabalhos foi alterada!')
            for trabalho in self.__repositorioTrabalho.pegaDadosModificados():
                trabalhoDao = TrabalhoDaoSqlite()
                trabalhoEncontrado = trabalhoDao.pegaTrabalhoEspecificoPorId(trabalho)
                if trabalhoEncontrado is None:
                    print(f'Trabalho não encontrado no banco!')
                    if trabalho.nome is not None:
                        print(f'Deve inserir novo trabalho no banco!')
                        trabalhoDao = TrabalhoDaoSqlite()
                        if trabalhoDao.insereTrabalho(trabalho, False):
                            print(f'{trabalho.nome} inserido com sucesso!')
                            continue
                        logger = logging.getLogger('trabalhoDao')
                        logger.error(f'Erro ao inserir trabalho: {trabalhoDao.pegaErro()}')
                        print(f'Erro ao inserir trabalho: {trabalhoDao.pegaErro()}')
                    continue
                if trabalho.nome is None:
                    print(f'Deve remover trabalho do banco!')
                    trabalhoDao = TrabalhoDaoSqlite()
                    if trabalhoDao.removeTrabalho(trabalho, False):
                        print(f'Trabalho removido com sucesso!')
                        continue
                    logger = logging.getLogger('trabalhoDao')
                    logger.error(f'Erro ao remover trabalho: {trabalhoDao.pegaErro()}')
                    print(f'Erro ao remover trabalho: {trabalhoDao.pegaErro()}')
                    continue
                print(f'Deve modificar trabalho no banco!')
                trabalhoDao = TrabalhoDaoSqlite()
                if trabalhoDao.modificaTrabalhoPorId(trabalho, False):
                    print(f'{trabalho.nome} modificado com sucesso!')
                    continue
                logger = logging.getLogger('trabalhoDao')
                logger.error(f'Erro ao modificar trabalho: {trabalhoDao.pegaErro()}')
                print(f'Erro ao modificar trabalho: {trabalhoDao.pegaErro()}')
            self.__repositorioTrabalho.limpaLista()
        
    def sincronizaListaTrabalhos(self):
        loggerTrabalho = logging.getLogger('trabalhoDAO')
        loggerEstoque = logging.getLogger('estoqueDAO')
        loggerProducao = logging.getLogger('trabalhoProducaoDAO')
        loggerVenda = logging.getLogger('vendaDAO')
        repositorioTrabalho = RepositorioTrabalho()        
        trabalhosServidor = repositorioTrabalho.pegaTodosTrabalhos()
        if not variavelExiste(trabalhosServidor):
            print(f'Erro ao buscar trabalhos no servidor: {repositorioTrabalho.pegaErro()}')
            return
        trabalhoDao = TrabalhoDaoSqlite()
        trabalhosBanco = trabalhoDao.pegaTrabalhos()
        if not variavelExiste(trabalhosBanco):
            print(f'Erro ao buscar trabalhos no banco: {trabalhoDao.pegaErro()}')
            return
        for trabalhoServidor in trabalhosServidor:
            trabalhoDao = TrabalhoDaoSqlite()
            trabalhoEncontradoBanco = trabalhoDao.pegaTrabalhoEspecificoPorNomeProfissaoRaridade(trabalhoServidor)
            if variavelExiste(trabalhoEncontradoBanco):
                if variavelExiste(trabalhoEncontradoBanco.nome):
                    if trabalhoServidor.id != trabalhoEncontradoBanco.id:
                        print(f'Sincronizando ids...')
                        trabalhoDao = TrabalhoDaoSqlite()
                        if trabalhoDao.modificaTrabalhoPorNomeProfissaoRaridade(trabalhoServidor):
                            loggerTrabalho.info(f'ID do trabalho modificado de: ({trabalhoEncontradoBanco}) -> ({trabalhoServidor})')
                            trabalhoEstoqueDAO = EstoqueDaoSqlite()
                            if trabalhoEstoqueDAO.modificaIdTrabalhoEstoque(trabalhoServidor.id, trabalhoEncontradoBanco.id):
                                loggerEstoque.info(f'Id do trabalho em estoque modificado: ({trabalhoEncontradoBanco}) -> ({trabalhoServidor})')
                            else:
                                loggerEstoque.error(f'Erro ao modificar o id do trabalho ({trabalhoEncontradoBanco}): {trabalhoEstoqueDAO.pegaErro()}')
                            trabalhoProducaoDAO = TrabalhoProducaoDaoSqlite()
                            if trabalhoProducaoDAO.modificaIdTrabalhoEmProducao(trabalhoServidor.id, trabalhoEncontradoBanco.id):
                                loggerProducao.info(f'Id do trabalho em produção modificado: ({trabalhoEncontradoBanco}) -> ({trabalhoServidor})')
                            else:
                                loggerProducao.error(f'Erro ao modificar o id do trabalho ({trabalhoEncontradoBanco}): {trabalhoProducaoDAO.pegaErro()}')
                            vendaDAO = VendaDaoSqlite()
                            if vendaDAO.modificaIdTrabalhoVendido(trabalhoServidor.id, trabalhoEncontradoBanco.id):
                                loggerVenda.info(f'Id do trabalho em vendas modificado: ({trabalhoEncontradoBanco}) -> ({trabalhoServidor})')
                            else:
                                loggerVenda.error(f'Erro ao modificar o id do trabalho ({trabalhoEncontradoBanco}): {vendaDAO.pegaErro()}')
                            continue
                        loggerTrabalho.error(f'Erro ao modificar o id do trabalho ({trabalhoEncontradoBanco}): {trabalhoDao.pegaErro()}')
                    continue
                trabalhoDao = TrabalhoDaoSqlite()
                if trabalhoDao.insereTrabalho(trabalhoServidor, False):
                    loggerTrabalho.info(f'({trabalhoServidor}) inserido no banco!')
                    continue
                loggerTrabalho.error(f'Erro ao inserir trabalho ({trabalhoServidor}) no banco: {trabalhoDao.pegaErro()}')

    def sincronizaListaPersonagens(self):
        repositorioPersonagem = RepositorioPersonagem()
        personagensServidor = repositorioPersonagem.pegaTodosPersonagens()
        if not variavelExiste(personagensServidor):
            print(f'Erro ao buscar lista de personagens no servidor: {repositorioPersonagem.pegaErro()}')
            input(f'Clique para continuar...')
            return
        personagemDao = PersonagemDaoSqlite()
        personagensBanco = personagemDao.pegaPersonagens()
        if not variavelExiste(personagensBanco):
            print(f'Erro ao buscar lista de personagens no banco: {personagemDao.pegaErro()}')
            input(f'Clique para continuar...')
            return
        for personagemServidor in personagensServidor:
            personagemDao = PersonagemDaoSqlite()
            personagemEncontrado = personagemDao.pegaPersonagemEspecificoPorNome(personagemServidor)
            if not variavelExiste(personagemEncontrado):
                print(f'Erro ao buscar trabalho especifico no banco: {personagemDao.pegaErro()}')
                continue
            if personagemEncontrado.nome == None:
                personagemDao = PersonagemDaoSqlite()
                if personagemDao.inserePersonagem(personagemServidor, False):
                    print(f'{personagemServidor.nome} inserido no banco com sucesso!')
                    continue
                print(f'Erro ao inserir {personagemServidor.nome} no banco: {personagemDao.pegaErro()}')
                continue
            if personagemServidor.id != personagemEncontrado.id:
                print(f'Sincronizando ids...')
                personagemDao = PersonagemDaoSqlite()
                if personagemDao.modificaPersonagemPorNome(personagemServidor):
                    print(f'ID do personagem: {personagemServidor.nome} modificado de: {personagemEncontrado.id} -> {personagemServidor.id}')
                    trabalhoEstoqueDAO = EstoqueDaoSqlite()
                    if trabalhoEstoqueDAO.modificaIdPersonagemTrabalhoEstoque(personagemServidor.id, personagemEncontrado.id):
                        print(f'idPersonagem do trabalho em estoque modificado: {personagemEncontrado.id} -> {personagemServidor.id}')
                    else:
                        print(f'Erro ao modificar o idPersonagem do trabalho no estoque: {trabalhoEstoqueDAO.pegaErro()}')
                    trabalhoProducaoDAO = TrabalhoProducaoDaoSqlite()
                    if trabalhoProducaoDAO.modificaIdPersonagemTrabalhoEmProducao(personagemServidor.id, personagemEncontrado.id):
                        print(f'idPersonagem do trabalho em produção modificado: {personagemEncontrado.id} -> {personagemServidor.id}')
                    else:
                        print(f'Erro ao modificar o idPersonagem do trabalho em produção: {trabalhoProducaoDAO.pegaErro()}')
                    vendaDAO = VendaDaoSqlite()
                    if vendaDAO.modificaIdPersonagemTrabalhoVendido(personagemServidor.id, personagemEncontrado.id):
                        print(f'idPersonagem do trabalho em vendas modificado: {personagemEncontrado.id} -> {personagemServidor.id}')
                    else:
                        print(f'Erro ao modificar o idPersonagem do trabalho em vendas: {vendaDAO.pegaErro()}')
                    continue
                print(f'Erro ao modificar o id do personagem {personagemEncontrado.id}: {personagemDao.pegaErro()}')

    def sincronizaListaProfissoes(self):
        logger = logging.getLogger('profissaoDao')
        limpaTela()
        print(f'{('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
        personagemDao = PersonagemDaoSqlite()
        personagens = personagemDao.pegaPersonagens()
        if not variavelExiste(personagens):
            print(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
            input(f'Clique para continuar...')
        for personagem in personagens:
            print(personagem)
            repositorioProfissao = RepositorioProfissao(personagem)
            profissoes = repositorioProfissao.pegaTodasProfissoes()
            if not variavelExiste(profissoes):
                print(f'Erro ao buscar profissões no servidor: {repositorioProfissao.pegaErro()}')
                continue
            for profissao in profissoes:
                print(profissao)
                profissaoDao = ProfissaoDaoSqlite(personagem)
                profissaoEncontrada = profissaoDao.pegaProfissaoPorId(profissao)
                if not variavelExiste(profissaoEncontrada):
                    logger.error(f'Erro ao buscar profissão ({profissao}): {profissaoDao.pegaErro()}')
                    continue
                if variavelExiste(profissaoEncontrada.nome):
                    profissaoDao = ProfissaoDaoSqlite(personagem)
                    if profissaoDao.modificaProfissao(profissao):
                        logger.info(f'({profissao}) modificado com sucesso!')
                        continue
                    logger.error(f'Erro ao modificar ({profissao}): {profissaoDao.pegaErro()}')
        input(f'Clique para continuar...')

    def sincronizaTrabalhosProducao(self):
        loggerTrabalhoProducaoDAO = logging.getLogger('trabalhoProducaoDao')
        loggerRepositorioTrabalhoProducao = logging.getLogger('repositorioTrabalhoProducao')
        limpaTela()
        print(f'{('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
        personagemDao = PersonagemDaoSqlite()
        personagens = personagemDao.pegaPersonagens()
        if not variavelExiste(personagens):
            print(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
            input(f'Clique para continuar...')
        for personagem in personagens:
            print(personagem)
            repositorioTrabalhoProducao = RepositorioTrabalhoProducao(personagem)
            trabalhosProducao = repositorioTrabalhoProducao.pegaTodosTrabalhosProducao()
            if not variavelExiste(trabalhosProducao):
                loggerRepositorioTrabalhoProducao.error(f'Erro ao buscar trabalhos em produção no servidor: {repositorioTrabalhoProducao.pegaErro()}')
                continue
            for trabalhoProducao in trabalhosProducao:
                print(trabalhoProducao)
                trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
                trabalhoProducaoEncontrada = trabalhoProducaoDao.pegaTrabalhoProducaoPorId(trabalhoProducao)
                if not variavelExiste(trabalhoProducaoEncontrada):
                    loggerTrabalhoProducaoDAO.error(f'Erro ao buscar profissão ({trabalhoProducao}): {trabalhoProducaoDao.pegaErro()}')
                    continue
                if variavelExiste(trabalhoProducaoEncontrada.nome):
                    trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
                    if trabalhoProducaoDao.modificaTrabalhoProducao(trabalhoProducao):
                        loggerTrabalhoProducaoDAO.info(f'({trabalhoProducao}) modificado no banco com sucesso!')
                        continue
                    loggerTrabalhoProducaoDAO.error(f'Erro ao modificar ({trabalhoProducao}): {trabalhoProducaoDao.pegaErro()}')
                    continue
                self.insereTrabalhoProducao(trabalhoProducaoEncontrada)
        input(f'Clique para continuar...')

    def sincronizaTrabalhosVendidos(self):
        loggerTrabalhoVendidoDAO = logging.getLogger('trabalhoVendidoDao')
        loggerRepositorioVendas = logging.getLogger('repositorioVendas')
        limpaTela()
        print(f'{('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
        personagemDao = PersonagemDaoSqlite()
        personagens = personagemDao.pegaPersonagens()
        if variavelExiste(personagens):
            for personagem in personagens:
                print(personagem)
                repositorioVendas = RepositorioVendas(personagem)
                trabalhosVendidos = repositorioVendas.pegaTodasVendas()
                if variavelExiste(trabalhosVendidos):
                    for trabalhoVendido in trabalhosVendidos:
                        print(trabalhoVendido)
                        vendasDao = VendaDaoSqlite(personagem)
                        trabalhoVendidoEncontrado = vendasDao.pegaTrabalhoVendidoPorId(trabalhoVendido)
                        if variavelExiste(trabalhoVendidoEncontrado):
                            if variavelExiste(trabalhoVendidoEncontrado.nomeProduto):
                                vendasDao = VendaDaoSqlite(personagem)
                                if vendasDao.modificaTrabalhoVendido(trabalhoVendido, False):
                                    loggerTrabalhoVendidoDAO.info(f'({trabalhoVendido}) modificado no banco com sucesso!')
                                    continue
                                loggerTrabalhoVendidoDAO.error(f'Erro ao modificar ({trabalhoVendido}): {vendasDao.pegaErro()}')
                                continue
                            vendasDao = VendaDaoSqlite(personagem)
                            if vendasDao.insereTrabalhoVendido(trabalhoVendido, False):
                                loggerTrabalhoVendidoDAO.info(f'({trabalhoVendido}) inserido no banco com sucesso!')
                                continue
                            loggerTrabalhoVendidoDAO.error(f'Erro ao inserir ({trabalhoVendido}): {vendasDao.pegaErro()}')
                            continue
                        loggerTrabalhoVendidoDAO.error(f'Erro ao buscar trabalho vendido específico ({trabalhoVendido}): {vendasDao.pegaErro()}')
                        continue
                    continue
                loggerRepositorioVendas.error(f'Erro ao buscar lista de vendas no servidor: {repositorioVendas.pegaErro()}')
                return
            input(f'Clique para continuar...')
            return
        print(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')

    def sincronizaDados(self):
        self.sincronizaListaTrabalhos()
        self.sincronizaListaPersonagens()
        self.sincronizaListaProfissoes()
        self.sincronizaTrabalhosProducao()
        self.sincronizaTrabalhosVendidos()

    def preparaPersonagem(self):
        if self.__repositorioTrabalho.abreStream():
            print(f'Stream repositório trabalhos iniciada!')
        else:
            print(f'Erro ao iniciar stream repositório trabalhos: {self.__repositorioTrabalho.pegaErro()}')
            logger = logging.getLogger('repositorioTrabalho')
            logger.error(f'Erro ao iniciar stream repositório trabalhos: {self.__repositorioTrabalho.pegaErro()}')
        clickAtalhoEspecifico('alt', 'tab')
        clickAtalhoEspecifico('win', 'left')
        self.iniciaProcessoBusca()

    def modificaProfissao(self):
        while True:
            limpaTela()
            personagemDao = PersonagemDaoSqlite()
            personagens = personagemDao.pegaPersonagens()
            if not variavelExiste(personagens):
                print(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
                input(f'Clique para continuar...')
                break
            print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
            for personagem in personagens:
                print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
            opcaoPersonagem = input(f'Opção:')
            if int(opcaoPersonagem) == 0:
                break
            while True:
                limpaTela()
                profissaoDao = ProfissaoDaoSqlite(personagens[int(opcaoPersonagem) - 1])
                profissoes = profissaoDao.pegaProfissoes()
                if not variavelExiste(profissoes):
                    print(f'Erro ao buscar profissões: {profissaoDao.pegaErro()}')
                    input(f'Clique para continuar...')
                    break
                if len(profissoes) == 0:
                    profissaoDao = ProfissaoDaoSqlite(personagens[int(opcaoPersonagem) - 1])
                    if profissaoDao.insereListaProfissoes():
                        print(f'Profissões inseridas com sucesso!')
                        input(f'Clique para continuar...')
                    else:
                        print(f'Erro ao inserir profissões: {profissaoDao.pegaErro()}')
                        input(f'Clique para continuar...')
                        break
                    continue
                print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(40)} | {('NOME').ljust(22)} | {str('EXP').ljust(6)} | PRIORIDADE')
                for profissao in profissoes:
                    print(f'{str(profissoes.index(profissao) + 1).ljust(6)} | {profissao}')
                opcaoProfissao = input(f'Opção: ')
                if int(opcaoProfissao) == 0:
                    break
                novoNome = input(f'Novo nome: ')
                novaExperiencia = input(f'Nova experiência: ')
                profissaoModificado = profissoes[int(opcaoProfissao)-1]
                if tamanhoIgualZero(novoNome):
                    novoNome = profissaoModificado.nome
                profissaoModificado.nome = novoNome
                if tamanhoIgualZero(novaExperiencia):
                    novaExperiencia = profissaoModificado.experiencia
                profissaoModificado.setExperiencia(novaExperiencia)
                alternaPrioridade = input(f'Alternar prioridade? (S/N) ')
                if alternaPrioridade.lower() == 's':
                    profissaoModificado.alternaPrioridade()
                profissaoDao = ProfissaoDaoSqlite(personagens[int(opcaoPersonagem)-1])
                if profissaoDao.modificaProfissao(profissaoModificado, True):
                    print(f'{profissaoModificado.nome} modificado com sucesso!')
                    input(f'Clique para continuar...')
                    continue
                logger = logging.getLogger('profissaoDao')
                logger.error(f'Erro ao modificar profissão: {profissaoDao.pegaErro()}')
                print(f'Erro ao modificar profissão: {profissaoDao.pegaErro()}')
                input(f'Clique para continuar...')

    def insereNovoTrabalho(self):
        while True:
            limpaTela()
            trabalhoDao = TrabalhoDaoSqlite()
            trabalhos = trabalhoDao.pegaTrabalhos()
            if not variavelExiste(trabalhos):
                print(f'Erro ao buscar trabalhos no banco: {trabalhoDao.pegaErro()}')
                break
            print(f'{('NOME').ljust(44)} | {('PROFISSÃO').ljust(22)} | {('RARIDADE').ljust(9)} | NÍVEL')
            for trabalho in trabalhos:
                print(f'{trabalho} | {trabalho.trabalhoNecessario}')
            opcaoTrabalho = input(f'Adicionar novo trabalho? (S/N)')
            try:
                if opcaoTrabalho.lower() == 'n':
                    break
                limpaTela()
                raridades = ['Comum', 'Melhorado', 'Raro', 'Especial']
                for raridade in raridades:
                    print(f'{raridades.index(raridade) + 1} - {raridade}')
                opcaoRaridade = input(f'Opção raridade: ')
                try:
                    if int(opcaoRaridade) == 0:
                        continue
                    limpaTela()
                    raridade = raridades[int(opcaoRaridade) - 1]
                    profissoes = [CHAVE_PROFISSAO_ARMA_DE_LONGO_ALCANCE, CHAVE_PROFISSAO_ARMA_CORPO_A_CORPO, CHAVE_PROFISSAO_ARMADURA_DE_TECIDO, CHAVE_PROFISSAO_ARMADURA_LEVE, CHAVE_PROFISSAO_ARMADURA_PESADA, CHAVE_PROFISSAO_ANEIS, CHAVE_PROFISSAO_AMULETOS, CHAVE_PROFISSAO_CAPOTES, CHAVE_PROFISSAO_BRACELETES]
                    for profissao in profissoes:
                        print(f'{profissoes.index(profissao) + 1} - {profissao}')
                    opcaoProfissao = input(f'Opção de profissao: ')
                    if int(opcaoProfissao) == 0:
                        continue
                    limpaTela()
                    profissao = profissoes[int(opcaoProfissao) - 1]
                    nome = input(f'Nome: ')
                    nomeProducao = input(f'Nome produção: ')
                    experiencia = input(f'Experiência: ')
                    nivel = input(f'Nível: ')
                    trabalhoNecessario = input(f'Trabalhos necessarios: ')
                    novoTrabalho = Trabalho(str(uuid.uuid4()), nome, nomeProducao, int(experiencia), int(nivel), profissao, raridade, trabalhoNecessario)
                    trabalhoDao = TrabalhoDaoSqlite()
                    if trabalhoDao.insereTrabalho(novoTrabalho):
                        print(f'{novoTrabalho.nome} inserido com sucesso!')
                        input(f'Clique para continuar...')
                        continue
                    logger = logging.getLogger('trabalhoDao')
                    logger.error(f'Erro ao inserir trabalho: {trabalhoDao.pegaErro()}')
                    print(f'Erro ao inserir trabalho: {trabalhoDao.pegaErro()}')
                    input(f'Clique para continuar...')
                except Exception as erro:
                    print(f'Opção inválida!')
                    input(f'Clique para continuar...')
            except Exception as erro:
                print(f'Opção inválida!')
                input(f'Clique para continuar...')

    def modificaTrabalho(self):
        while True:
            limpaTela()
            trabalhoDao = TrabalhoDaoSqlite()
            trabalhos = trabalhoDao.pegaTrabalhos()
            if not variavelExiste(trabalhos):
                print(f'Erro ao buscar trabalhos no banco: {trabalhoDao.pegaErro()}')
                input(f'Clique para continuar...')
                break
            print(f'{('ÍNDICE').ljust(6)} - {('NOME').ljust(44)} | {('PROFISSÃO').ljust(22)} | {('RARIDADE').ljust(9)} | NÍVEL')
            for trabalho in trabalhos:
                print(f'{str(trabalhos.index(trabalho) + 1).ljust(6)} - {trabalho}')
            opcaoTrabalho = input(f'Opção trabalho: ')    
            if int(opcaoTrabalho) == 0:
                break
            trabalhoEscolhido = trabalhos[int(opcaoTrabalho) - 1]
            novoNome = input(f'Novo nome: ')
            if tamanhoIgualZero(novoNome):
                novoNome = trabalhoEscolhido.nome
            novoNomeProducao = input(f'Novo nome de produção: ')
            if tamanhoIgualZero(novoNomeProducao):
                novoNomeProducao = trabalhoEscolhido.nomeProducao
            novaExperiencia = input(f'Nova experiência: ')
            if tamanhoIgualZero(novaExperiencia):
                novaExperiencia = trabalhoEscolhido.experiencia
            novoNivel = input(f'Novo nível: ')
            if tamanhoIgualZero(novoNivel):
                novoNivel = trabalhoEscolhido.nivel
            novaProfissao = input(f'Nova profissão: ')
            if tamanhoIgualZero(novaProfissao):
                novaProfissao = trabalhoEscolhido.profissao
            novaRaridade = input(f'Nova raridade: ')
            if tamanhoIgualZero(novaRaridade):
                novaRaridade = trabalhoEscolhido.raridade
            novoTrabalhoNecessario = input(f'Novo trabalho necessário: ')
            if tamanhoIgualZero(novoTrabalhoNecessario):
                novoTrabalhoNecessario = trabalhoEscolhido.trabalhoNecessario
            trabalhoEscolhido.nome = novoNome
            trabalhoEscolhido.setNomeProducao(novoNomeProducao)
            trabalhoEscolhido.setExperiencia(novaExperiencia)
            trabalhoEscolhido.nivel = novoNivel
            trabalhoEscolhido.profissao = novaProfissao
            trabalhoEscolhido.raridade = novaRaridade
            trabalhoEscolhido.setTrabalhoNecessario(novoTrabalhoNecessario)
            trabalhoDao = TrabalhoDaoSqlite()
            if trabalhoDao.modificaTrabalhoPorId(trabalhoEscolhido):
                print(f'{trabalhoEscolhido.nome} modificado com sucesso!')
                input(f'Clique para continuar...')
                continue
            print(f'Erro ao modificar trabalho: {trabalhoDao.pegaErro()}')
            logger = logging.getLogger('trabalhoDao')
            logger.error(f'Erro ao modificar trabalho: {trabalhoDao.pegaErro()}')
            input(f'Clique para continuar...')

    def insereNovoTrabalhoProducao(self):
        while True:
            limpaTela()
            print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
            personagemDao = PersonagemDaoSqlite()
            personagens = personagemDao.pegaPersonagens()
            if not variavelExiste(personagens):
                print(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
                input(f'Clique para continuar...')
                break
            for personagem in personagens:
                print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
            opcaoPersonagem = input(f'Opção:')
            if int(opcaoPersonagem) == 0:
                break
            while True:
                limpaTela()
                personagem = personagens[int(opcaoPersonagem) - 1]
                print(f'{('NOME').ljust(44)} | {('PROFISSÃO').ljust(22)} | {('NÍVEL').ljust(5)} | {('ESTADO').ljust(10)} | {('LICENÇA').ljust(31)} | RECORRÊNCIA')
                trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
                trabalhos = trabalhoProducaoDao.pegaTrabalhosProducao()
                if not variavelExiste(trabalhos):
                    print(f'Erro ao buscar trabalhos em produção: {trabalhoProducaoDao.pegaErro()}')
                    input(f'Clique para continuar...')
                    break
                for trabalhoProducao in trabalhos:
                    print(trabalhoProducao)
                opcaoTrabalho = input(f'Adicionar novo trabalho? (S/N) ')    
                if (opcaoTrabalho).lower() == 'n':
                    break
                limpaTela()
                profissoes = [CHAVE_PROFISSAO_ARMA_DE_LONGO_ALCANCE, CHAVE_PROFISSAO_ARMA_CORPO_A_CORPO, CHAVE_PROFISSAO_ARMADURA_DE_TECIDO, CHAVE_PROFISSAO_ARMADURA_LEVE, CHAVE_PROFISSAO_ARMADURA_PESADA, CHAVE_PROFISSAO_ANEIS, CHAVE_PROFISSAO_AMULETOS, CHAVE_PROFISSAO_CAPOTES, CHAVE_PROFISSAO_BRACELETES]
                print(f'{('ÍNDICE').ljust(6)} - PROFISSÃO')
                for profissao in profissoes:
                    print(f'{str(profissoes.index(profissao) + 1).ljust(6)} - {profissao}')
                opcaoProfissao = input(f'Opção de profissao: ')
                if int(opcaoProfissao) == 0:
                    continue
                profissao = profissoes[int(opcaoProfissao) - 1]
                trabalhosFiltrados = []
                trabalhoDao = TrabalhoDaoSqlite()
                trabalhos = trabalhoDao.pegaTrabalhos()
                if not variavelExiste(trabalhos):
                    print(f'Erro ao buscar trabalhos: {trabalhoDao.pegaErro()}')
                    input(f'Clique para continuar...')
                    break
                for trabalho in trabalhos:
                    if trabalho.profissao == profissao:
                        trabalhosFiltrados.append(trabalho)
                print(f'{('INDICE').ljust(6)} | {('NOME').ljust(40)} | {('PROFISSÃO').ljust(20)} | NÍVEL')
                for trabalho in trabalhosFiltrados:
                    print(f'{str(trabalhosFiltrados.index(trabalho) + 1).ljust(6)} - {trabalho}')
                opcaoTrabalho = input(f'Trabalhos escolhido: ')
                if int(opcaoTrabalho) == 0:
                    continue
                trabalho = trabalhosFiltrados[int(opcaoTrabalho) - 1]
                licencas = [CHAVE_LICENCA_NOVATO, CHAVE_LICENCA_APRENDIZ, CHAVE_LICENCA_INICIANTE, CHAVE_LICENCA_MESTRE]
                for licenca in licencas:
                    print(f'{licencas.index(licenca) + 1} - {licenca}')
                opcaoLicenca = input(f'Licença escolhida: ')
                if int(opcaoLicenca) == 0:
                    continue
                licenca = licencas[int(opcaoLicenca) - 1]
                opcaoRecorrencia = input(f'Trabalho recorrente? (S/N)')
                recorrencia = True if (opcaoRecorrencia).lower() == 's' else False
                novoTrabalhoProducao = TrabalhoProducao()
                novoTrabalhoProducao.dicionarioParaObjeto(trabalho.__dict__)
                novoTrabalhoProducao.trabalhoId = trabalho.id
                novoTrabalhoProducao.recorrencia = recorrencia
                novoTrabalhoProducao.tipo_licenca = licenca
                novoTrabalhoProducao.estado = CODIGO_PARA_PRODUZIR
                trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
                self.insereTrabalhoProducao(trabalhoProducao)
                input(f'Clique para continuar...')
                
    def modificaPersonagem(self):
        while True:
            limpaTela()
            print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
            personagemDao = PersonagemDaoSqlite()
            personagens = personagemDao.pegaPersonagens()
            if not variavelExiste(personagens):
                print(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
                input(f'Clique para continuar...')
                break
            for personagem in personagens:
                print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
            opcaoPersonagem = input(f'Opção:')
            if int(opcaoPersonagem) == 0:
                break
            limpaTela()
            personagem = personagens[int(opcaoPersonagem) - 1]
            novoNome = input(f'Novo nome: ')
            if tamanhoIgualZero(novoNome):
                novoNome = personagem.nome
            personagem.nome = novoNome
            novoEspaco = input(f'Nova quantidade de produção: ')
            if tamanhoIgualZero(novoEspaco):
                novoEspaco = personagem.espacoProducao
            personagem.setEspacoProducao(novoEspaco)
            novoEstado = input(f'Modificar estado? (S/N) ')
            if novoEstado.lower() == 's':
                personagem.alternaEstado()
            novoUso = input(f'Modificar uso? (S/N) ')
            if novoUso.lower() == 's':
                personagem.alternaUso()
            novoAutoProducao = input(f'Modificar autoProducao? (S/N) ')
            if novoAutoProducao.lower() == 's':
                personagem.alternaAutoProducao()
            personagemDao = PersonagemDaoSqlite()
            if personagemDao.modificaPersonagem(personagem):
                print(f'{personagem.nome} modificado com sucesso!')
                input(f'Clique para continuar...')
                continue
            logger = logging.getLogger('personagemDao')
            logger.error(f'Erro ao modificar persoangem: {personagemDao.pegaErro()}')
            print(f'Erro ao modificar personagem: {personagemDao.pegaErro()}')
            input(f'Clique para continuar...')
            
    def removeTrabalho(self):
        while True:
            limpaTela()
            print(f'{('ÍNDICE').ljust(6)} - {('NOME').ljust(44)} | {('PROFISSÃO').ljust(22)} | {('RARIDADE').ljust(9)} | NÍVEL')
            trabalhoDao = TrabalhoDaoSqlite()
            trabalhos = trabalhoDao.pegaTrabalhos()
            if not variavelExiste(trabalhos):
                print(f'Erro ao buscar trabalhos: {trabalhoDao.pegaErro()}')
                input(f'Clique para continuar...')
                break
            for trabalho in trabalhos:
                print(f'{str(trabalhos.index(trabalho) + 1).ljust(6)} - {trabalho}')
            opcaoTrabalho = input(f'Opção trabalho: ')    
            if int(opcaoTrabalho) == 0:
                break
            trabalhoEscolhido = trabalhos[int(opcaoTrabalho) - 1]
            trabalhoDao = TrabalhoDaoSqlite()
            if trabalhoDao.removeTrabalho(trabalhoEscolhido):
                print(f'{trabalhoEscolhido.nome} removido com sucesso!')
                input(f'Clique para continuar...')
                continue
            logger = logging.getLogger('trabalhoDao')
            logger.error(f'Erro ao remover trabalho: {trabalhoDao.pegaErro()}')
            print(f'Erro ao remover trabalho: {trabalhoDao.pegaErro()}')
            input(f'Clique para continuar...')

    def modificaTrabalhoProducao(self):
        while True:
            limpaTela()
            print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
            personagemDao = PersonagemDaoSqlite()
            personagens = personagemDao.pegaPersonagens()
            if not variavelExiste(personagens):
                print(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
                input(f'Clique para continuar...')
                break
            for personagem in personagens:
                print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
            opcaoPersonagem = input(f'Opção: ')
            if int(opcaoPersonagem) == 0:
                break
            personagem = personagens[int(opcaoPersonagem) - 1]
            while True:
                limpaTela()
                trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
                trabalhosProducao = trabalhoProducaoDao.pegaTrabalhosProducao()
                if not variavelExiste(trabalhosProducao):
                    print(f'Erro ao buscar trabalhos em produção: {trabalhoProducaoDao.pegaErro()}')
                    input(f'Clique para continuar...')
                    break
                for trabalhoProducao in trabalhosProducao:
                    print(f'{str(trabalhosProducao.index(trabalhoProducao) + 1).ljust(6)} - {trabalhoProducao}')
                opcaoTrabalho = input(f'Opção trabalho: ')
                if int(opcaoTrabalho) == 0:
                    break
                limpaTela()
                trabalhoEscolhido = trabalhosProducao[int(opcaoTrabalho) - 1]
                licencas = [CHAVE_LICENCA_NOVATO, CHAVE_LICENCA_APRENDIZ, CHAVE_LICENCA_INICIANTE, CHAVE_LICENCA_MESTRE]
                for licenca in licencas:
                    print(f'{licencas.index(licenca) + 1} - {licenca}')
                novaLicenca = input(f'Nova licença: ')
                if tamanhoIgualZero(novaLicenca):
                    novaLicenca = trabalhoEscolhido.tipo_licenca
                else:
                    trabalhoEscolhido.tipo_licenca = licencas[int(novaLicenca) - 1]
                limpaTela()
                novaRecorrencia = input(f'Alterna recorrencia? (S/N) ')
                if novaRecorrencia.lower() == 's':
                    trabalhoEscolhido.alternaRecorrencia()
                limpaTela()
                novoEstado = input(f'Novo estado: (0 - PRODUZIR, 1 - PRODUZINDO, 2 - CONCLUÍDO)')
                if tamanhoIgualZero(novoEstado):
                    novoEstado = trabalhoEscolhido.estado 
                else:
                    trabalhoEscolhido.estado = int(novoEstado)
                trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
                if trabalhoProducaoDao.modificaTrabalhoProducao(trabalhoEscolhido):
                    print(f'{trabalhoEscolhido.nome} modificado com sucesso!')
                    input(f'Clique para continuar...')
                    continue
                logger = logging.getLogger('trabalhoProducaoDao')
                logger.error(f'Erro ao modificar trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
                print(f'Erro ao modificar trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
                input(f'Clique para continuar...')

    def removeTrabalhoProducao(self):
        while True:
            limpaTela()
            print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
            personagemDao = PersonagemDaoSqlite()
            personagens = personagemDao.pegaPersonagens()
            if not variavelExiste(personagens):
                print(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
                input(f'Clique para continuar...')
                break
            for personagem in personagens:
                print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
            opcaoPersonagem = input(f'Opção: ')
            if int(opcaoPersonagem) == 0:
                break
            personagem = personagens[int(opcaoPersonagem) - 1]
            while True: 
                limpaTela()
                print(f'{('ÍNDICE').ljust(6)} - {('NOME').ljust(40)} | {('PROFISSÃO').ljust(21)} | {('NÍVEL').ljust(5)} | {('ESTADO').ljust(10)} | LICENÇA')
                trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
                trabalhosProducao = trabalhoProducaoDao.pegaTrabalhosProducao()
                if not variavelExiste(trabalhosProducao):
                    print(f'Erro ao buscar trabalhos em produção: {trabalhoProducaoDao.pegaErro()}')
                    input(f'Clique para continuar...')
                    break
                for trabalhoProducao in trabalhosProducao:
                    print(f'{str(trabalhosProducao.index(trabalhoProducao) + 1).ljust(6)} - {trabalhoProducao}')
                opcaoTrabalho = input(f'Opcção trabalho: ')
                if int(opcaoTrabalho) == 0:
                    break
                trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
                trabalhoRemovido = trabalhosProducao[int(opcaoTrabalho) - 1]
                if trabalhoProducaoDao.removeTrabalhoProducao(trabalhoRemovido):
                    print(f'{trabalhoRemovido.nome} removido com sucesso!')
                    input(f'Clique para continuar...')
                    continue
                logger = logging.getLogger('trabalhoProducaoDao')
                logger.error(f'Erro ao remover trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
                print(f'Erro ao remover trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
                input(f'Clique para continuar...')

    def mostraVendas(self):
        while True:
            limpaTela()
            print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
            personagens = PersonagemDaoSqlite().pegaPersonagens()
            for personagem in personagens:
                print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
            opcaoPersonagem = input(f'Opção:')
            if int(opcaoPersonagem) == 0:
                break
            while True:
                limpaTela()
                personagem = personagens[int(opcaoPersonagem) - 1]
                trabalhoVendidoDao = VendaDaoSqlite(personagem)
                vendas = trabalhoVendidoDao.pegaVendas()
                if not variavelExiste(vendas):
                    logger = logging.getLogger('vendasDao')
                    logger.error(f'Erro ao buscar trabalhos vendidos: {trabalhoVendidoDao.pegaErro()}')
                    print(f'Erro ao buscar trabalhos vendidos: {trabalhoVendidoDao.pegaErro()}')
                    input(f'Clique para continuar...')
                    break
                print(f'{('NOME').ljust(112)} | {('DATA').ljust(10)} | {('ID TRABALHO').ljust(36)} | {('VALOR').ljust(5)} | QUANT')
                for trabalhoVendido in vendas:
                    print(trabalhoVendido)
                opcaoTrabalhoVendido = input(f'Opção trabalho vendido: ')
                if int(opcaoTrabalhoVendido) == 0:
                    break

    def inserePersonagem(self):
         while True:
            limpaTela()
            print(f'{('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
            personagemDao = PersonagemDaoSqlite()
            personagens = personagemDao.pegaPersonagens()
            if not variavelExiste(personagens):
                print(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
                input(f'Clique para continuar...')
                break
            for personagem in personagens:
                print(personagem)
            opcaoPersonagem = input(f'Inserir novo personagem? (S/N) ')
            if opcaoPersonagem.lower() == 'n':
                break
            nome = input(f'Nome: ')
            email = input(f'Email: ')
            senha = input(f'Senha: ')
            novoPersonagem = Personagem()
            novoPersonagem.nome = nome
            novoPersonagem.setEmail(email)
            novoPersonagem.setSenha(senha)
            personagemDao = PersonagemDaoSqlite()
            if personagemDao.inserePersonagem(novoPersonagem):
                print(f'Novo personagem {novoPersonagem.nome} inserido com sucesso!')
                input(f'Clique para continuar...')
                continue
            logger = logging.getLogger('personagemDao')
            logger.error(personagemDao.pegaErro())
            print(f'Erro ao inserir novo personagem: {personagemDao.pegaErro()}')
            input(f'Clique para continuar...')

    def removePersonagem(self):
        while True:
            limpaTela()
            print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
            personagemDao = PersonagemDaoSqlite()
            personagens = personagemDao.pegaPersonagens()
            if not variavelExiste(personagens):
                print(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
                input(f'Clique para continuar...')
                break
            for personagem in personagens:
                print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
            opcaoPersonagem = input(f'Opção:')
            if int(opcaoPersonagem) == 0:
                break
            personagem = personagens[int(opcaoPersonagem) - 1]
            personagemDao = PersonagemDaoSqlite()
            if personagemDao.removePersonagem(personagem):
                print(f'Personagem {personagem.nome} removido com sucesso!')
                input(f'Clique para continuar...')
                continue
            logger = logging.getLogger('personagemDao')
            logger.error(f'Erro ao remover personagem: {personagemDao.pegaErro()}')
            print(f'Erro ao remover personagem: {personagemDao.pegaErro()}')
            input(f'Clique para continuar...')
    
    def insereTrabalhoEstoque(self):
        while True:
            limpaTela()
            print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
            personagemDao = PersonagemDaoSqlite()
            personagens = personagemDao.pegaPersonagens()
            if not variavelExiste(personagens):
                print(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
                input(f'Clique para continuar...')
                break
            for personagem in personagens:
                print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
            opcaoPersonagem = input(f'Opção:')
            if int(opcaoPersonagem) == 0:
                break
            personagem = personagens[int(opcaoPersonagem) - 1]
            while True:
                limpaTela()
                print(f'{('NOME').ljust(40)} | {('PROFISSÃO').ljust(25)} | {('QNT').ljust(3)} | {('NÍVEL').ljust(5)} | {('RARIDADE').ljust(10)} | {'ID TRABALHO'}')
                trabalhoEstoqueDao = EstoqueDaoSqlite(personagem)
                estoque = trabalhoEstoqueDao.pegaEstoque()
                if not variavelExiste(estoque):
                    print(f'Erro ao buscar trabalhos no estoque: {trabalhoEstoqueDao.pegaErro()}')
                    input(f'Clique para continuar...')
                    break
                for trabalhoEstoque in estoque:
                    print(trabalhoEstoque)
                opcaoTrabalho = input(f'Inserir novo trabalho ao estoque? (S/N) ')
                if opcaoTrabalho.lower() == 'n':
                    break
                trabalhoDao = TrabalhoDaoSqlite()
                trabalhos = trabalhoDao.pegaTrabalhos()
                if not variavelExiste(trabalhos):
                    print(f'Erro ao buscar trabalhos: {trabalhoDao.pegaErro()}')
                    input(f'Clique para continuar...')
                    break
                print(f'{('ÍNDICE').ljust(6)} | {('NOME').ljust(44)} | {('PROFISSÃO').ljust(22)} | {('RARIDADE').ljust(9)} | NÍVEL')
                for trabalho in trabalhos:
                    print(f'{str(trabalhos.index(trabalho) + 1).ljust(6)} | {trabalho}')
                opcaoTrabalho = input(f'Opção trabalho: ')    
                if int(opcaoTrabalho) == 0:
                    break
                trabalho = trabalhos[int(opcaoTrabalho) - 1]
                quantidadeTrabalho = input(f'Quantidade trabalho: ')
                trabalhoEstoqueDao = EstoqueDaoSqlite(personagem)
                trabalhoEstoque = TrabalhoEstoque()
                trabalhoEstoque.nome = trabalho.nome
                trabalhoEstoque.profissao = trabalho.profissao
                trabalhoEstoque.nivel = trabalho.nivel
                trabalhoEstoque.quantidade = quantidadeTrabalho
                trabalhoEstoque.raridade = trabalho.raridade
                trabalhoEstoque.trabalhoId = trabalho.id
                if trabalhoEstoqueDao.insereTrabalhoEstoque(trabalhoEstoque):
                    print(f'Trabalho {trabalho.nome} inserido no estoque com sucesso!')
                    input(f'Clique para continuar...')
                    continue
                logger = logging.getLogger('estoqueDao')
                logger.error(f'Erro ao inserir trabalho no estoque: {trabalhoEstoqueDao.pegaErro()}')
                print(f'Erro ao inserir trabalho no estoque: {trabalhoEstoqueDao.pegaErro()}')
                input(f'Clique para continuar...')
    
    def modificaTrabalhoEstoque(self):
        while True:
            limpaTela()
            print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
            personagemDao = PersonagemDaoSqlite()
            personagens = personagemDao.pegaPersonagens()
            if not variavelExiste(personagens):
                print(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
                input(f'Clique para continuar...')
                break
            for personagem in personagens:
                print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
            opcaoPersonagem = input(f'Opção:')
            if int(opcaoPersonagem) == 0:
                break
            personagem = personagens[int(opcaoPersonagem) - 1]
            while True:
                limpaTela()
                trabalhoEstoqueDao = EstoqueDaoSqlite(personagem)
                estoque = trabalhoEstoqueDao.pegaEstoque()
                if not variavelExiste(estoque):
                    print(f'Erro ao buscar trabalhos no estoque: {trabalhoEstoqueDao.pegaErro()}')
                    input(f'Clique para continuar...')
                    break
                print(f'{('ÍNDICE').ljust(6)} | {('NOME').ljust(40)} | {('PROFISSÃO').ljust(25)} | {('QNT').ljust(3)} | {('NÍVEL').ljust(5)} | {('RARIDADE').ljust(10)} | {'ID TRABALHO'}')
                for trabalhoEstoque in estoque:
                    print(f'{str(estoque.index(trabalhoEstoque) + 1).ljust(6)} | {trabalhoEstoque}')
                print(f'{('0').ljust(6)} | Sair')
                opcaoTrabalho = input(f'opção trabalho ')
                if int(opcaoTrabalho) == 0:
                    break
                trabalho = estoque[int(opcaoTrabalho) - 1]
                quantidadeTrabalho = input(f'Quantidade trabalho: ')
                if tamanhoIgualZero(quantidadeTrabalho):
                    quantidadeTrabalho = trabalho.quantidade
                trabalho.quantidade = quantidadeTrabalho
                trabalhoEstoqueDao = EstoqueDaoSqlite(personagem)
                if trabalhoEstoqueDao.modificaTrabalhoEstoque(trabalho):
                    print(f'Trabalho {trabalho.nome} modificado no estoque com sucesso!')
                    input(f'Clique para continuar...')
                    continue
                logger = logging.getLogger('estoqueDao')
                logger.error(f'Erro ao modificar trabalho no estoque: {trabalhoEstoqueDao.pegaErro()}')
                print(f'Erro ao modificar trabalho no estoque: {trabalhoEstoqueDao.pegaErro()}')
                input(f'Clique para continuar...')

    def removeTrabalhoEstoque(self):
        while True:
            limpaTela()
            print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
            personagemDao = PersonagemDaoSqlite()
            personagens = personagemDao.pegaPersonagens()
            if not variavelExiste(personagens):
                print(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
                input(f'Clique para continuar...')
                break
            for personagem in personagens:
                print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
            opcaoPersonagem = input(f'Opção:')
            if int(opcaoPersonagem) == 0:
                break
            personagem = personagens[int(opcaoPersonagem) - 1]
            while True:
                limpaTela()
                trabalhoEstoqueDao = EstoqueDaoSqlite(personagem)
                estoque = trabalhoEstoqueDao.pegaEstoque()
                if not variavelExiste(estoque):
                    print(f'Erro ao buscar trabalhos no estoque: {trabalhoEstoqueDao.pegaErro()}')
                    input(f'Clique para continuar...')
                    break
                print(f'{('ÍNDICE').ljust(6)} | {('NOME').ljust(40)} | {('PROFISSÃO').ljust(25)} | {('QNT').ljust(3)} | {('NÍVEL').ljust(5)} | {('RARIDADE').ljust(10)} | {'ID TRABALHO'}')
                for trabalhoEstoque in estoque:
                    print(f'{str(estoque.index(trabalhoEstoque) + 1).ljust(6)} | {trabalhoEstoque}')
                print(f'{('0').ljust(6)} | Sair')
                opcaoTrabalho = input(f'opção trabalho ')
                if int(opcaoTrabalho) == 0:
                    break
                trabalho = estoque[int(opcaoTrabalho) - 1]
                trabalhoEstoqueDao = EstoqueDaoSqlite(personagem)
                if trabalhoEstoqueDao.removeTrabalhoEstoque(trabalho):
                    print(f'Trabalho {trabalho.nome} removido do estoque com sucesso!')
                    input(f'Clique para continuar...')
                    continue
                logger = logging.getLogger('estoqueDao')
                logger.error(f'Erro ao remover trabalho do estoque: {trabalhoEstoqueDao.pegaErro()}')
                print(f'Erro ao remover trabalho do estoque: {trabalhoEstoqueDao.pegaErro()}')
                input(f'Clique para continuar...')

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
        print(f'{'NOME'.ljust(113)} | {'DATA'.ljust(10)} | {'ID TRABALHO'.ljust(36)} | {'VALOR'.ljust(5)} | UND')
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
        # print(f'{'NOME'.ljust(113)} | {'DATA'.ljust(10)} | {'ID TRABALHO'.ljust(36)} | {'VALOR'.ljust(5)} | UND')
        for trabalhoProducao in trabalhosProducao:
            print(trabalhoProducao)
        input(f'Clique para continuar...')

    def insereTrabalhoVendido(self):
        while True:
            limpaTela()
            print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
            personagemDao = PersonagemDaoSqlite()
            personagens = personagemDao.pegaPersonagens()
            if not variavelExiste(personagens):
                print(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
                input(f'Clique para continuar...')
                break
            for personagem in personagens:
                print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
            opcaoPersonagem = input(f'Opção:')
            if int(opcaoPersonagem) == 0:
                break
            personagem = personagens[int(opcaoPersonagem) - 1]
            while True:
                limpaTela()
                print(f'{'NOME'.ljust(113)} | {'DATA'.ljust(10)} | {'ID TRABALHO'.ljust(36)} | {'VALOR'.ljust(5)} | UND')
                trabalhoVendidoDao = VendaDaoSqlite(personagem)
                vendas = trabalhoVendidoDao.pegaVendas()
                if not variavelExiste(vendas):
                    print(f'Erro ao buscar trabalhos vendidos: {trabalhoVendidoDao.pegaErro()}')
                    input(f'Clique para continuar...')
                    break
                for trabalhoVendido in vendas:
                    print(trabalhoVendido)
                opcaoTrabalho = input(f'Inserir nova venda? (S/N) ')
                if opcaoTrabalho.lower() == 'n':
                    break
                trabalhoDao = TrabalhoDaoSqlite()
                trabalhos = trabalhoDao.pegaTrabalhos()
                if not variavelExiste(trabalhos):
                    print(f'Erro ao buscar trabalhos: {trabalhoDao.pegaErro()}')
                    input(f'Clique para continuar...')
                    break
                print(f'{('ÍNDICE').ljust(6)} | {('NOME').ljust(44)} | {('PROFISSÃO').ljust(22)} | {('RARIDADE').ljust(9)} | NÍVEL')
                for trabalho in trabalhos:
                    print(f'{str(trabalhos.index(trabalho) + 1).ljust(6)} | {trabalho}')
                opcaoTrabalho = input(f'Opção trabalho: ')    
                if int(opcaoTrabalho) == 0:
                    break
                trabalho = trabalhos[int(opcaoTrabalho) - 1]
                data = input(f'Data da venda: ')
                quantidade = input(f'Quantidade trabalho vendido: ')
                valor = input(f'Valor do trabalho vendido: ')
                trabalhoVendidoDao = VendaDaoSqlite(personagem)
                trabalhoVendido = TrabalhoVendido()
                trabalhoVendido.nome = trabalho.nome
                trabalhoVendido.dataVenda = data
                trabalhoVendido.nomePersonagem = personagem.id
                trabalhoVendido.quantidadeProduto = quantidade
                trabalhoVendido.trabalhoId = trabalho.id
                trabalhoVendido.valorProduto = valor
                if trabalhoVendidoDao.insereTrabalhoVendido(trabalhoVendido):
                    print(f'Nova venda inserida com sucesso!')
                    input(f'Clique para continuar...')
                    continue
                logger = logging.getLogger('vendasDao')
                logger.error(f'Erro ao inserir nova venda: {trabalhoVendidoDao.pegaErro()}')
                print(f'Erro ao inserir nova venda: {trabalhoVendidoDao.pegaErro()}')
                input(f'Clique para continuar...')

    def removeTrabalhoVendido(self):
        while True:
            limpaTela()
            personagemDao = PersonagemDaoSqlite()
            personagens = personagemDao.pegaPersonagens()
            if not variavelExiste(personagens):
                print(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
                input(f'Clique para continuar...')
                break
            print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
            for personagem in personagens:
                print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
            opcaoPersonagem = input(f'Opção:')
            if int(opcaoPersonagem) == 0:
                break
            personagem = personagens[int(opcaoPersonagem) - 1]
            while True:
                limpaTela()
                trabalhoVendidoDao = VendaDaoSqlite(personagem)
                vendas = trabalhoVendidoDao.pegaVendas()
                if not variavelExiste(vendas):
                    print(f'Erro ao buscar trabalhos vendidos: {trabalhoVendidoDao.pegaErro()}')
                    input(f'Clique para continuar...')
                    break
                print(f'{('ÍNDICE').ljust(6)} | {'NOME'.ljust(113)} | {'DATA'.ljust(10)} | {'ID TRABALHO'.ljust(36)} | {'VALOR'.ljust(5)} | UND')
                for trabalhoVendido in vendas:
                    print(f'{str(vendas.index(trabalhoVendido) + 1).ljust(6)} | {trabalhoVendido}')
                opcaoTrabalho = input(f'Opção trabalho: ')    
                if int(opcaoTrabalho) == 0:
                    break
                trabalhoVendidoDao = VendaDaoSqlite(personagem)
                if trabalhoVendidoDao.removeTrabalhoVendido(vendas[int(opcaoTrabalho) - 1]):
                    print(f'Trabalho vendido removido com sucesso!')
                    input(f'Clique para continuar...')
                    continue
                logger = logging.getLogger('vendasDao')
                logger.error(f'Erro ao remover trabalho vendido: {trabalhoVendidoDao.pegaErro()}')
                print(f'Erro ao remover trabalho vendido: {trabalhoVendidoDao.pegaErro()}')
                input(f'Clique para continuar...')
    
    def modificaTrabalhoVendido(self):
        while True:
            limpaTela()
            personagemDao = PersonagemDaoSqlite()
            personagens = personagemDao.pegaPersonagens()
            if not variavelExiste(personagens):
                print(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
                input(f'Clique para continuar...')
                break
            print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
            for personagem in personagens:
                print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
            opcaoPersonagem = input(f'Opção:')
            if int(opcaoPersonagem) == 0:
                break
            personagem = personagens[int(opcaoPersonagem) - 1]
            while True:
                limpaTela()
                trabalhoVendidoDao = VendaDaoSqlite(personagem)
                vendas = trabalhoVendidoDao.pegaVendas()
                if not variavelExiste(vendas):
                    print(f'Erro ao buscar trabalhos vendidos: {trabalhoVendidoDao.pegaErro()}')
                    input(f'Clique para continuar...')
                    break
                print(f'{('ÍNDICE').ljust(6)} | {'NOME'.ljust(113)} | {'DATA'.ljust(10)} | {'ID TRABALHO'.ljust(36)} | {'VALOR'.ljust(5)} | UND')
                for trabalhoVendido in vendas:
                    print(f'{str(vendas.index(trabalhoVendido) + 1).ljust(6)} | {trabalhoVendido}')
                opcaoTrabalho = input(f'Opção trabalho: ')    
                if int(opcaoTrabalho) == 0:
                    break
                trabalhoVendidoModificado = vendas[int(opcaoTrabalho) - 1]
                nome = input(f'Nome do trabalho: ')
                if tamanhoIgualZero(nome):
                    nome = trabalhoVendidoModificado.nome
                data = input(f'Data da venda: ')
                if tamanhoIgualZero(data):
                    data = trabalhoVendidoModificado.dataVenda
                quantidade = input(f'Quantidade vendida: ')
                if tamanhoIgualZero(quantidade):
                    quantidade = trabalhoVendidoModificado.quantidadeProduto
                valor = input(f'Valor da venda: ')
                if tamanhoIgualZero(valor):
                    valor = trabalhoVendidoModificado.valorProduto
                trabalhoVendidoModificado.nome = nome
                trabalhoVendidoModificado.setData(data)
                trabalhoVendidoModificado.quantidade = quantidade
                trabalhoVendidoModificado.setValor(valor)
                trabalhoVendidoDao = VendaDaoSqlite(personagem)
                if trabalhoVendidoDao.modificaTrabalhoVendido(trabalhoVendidoModificado):
                    print(f'Trabalho vendido modificado com sucesso!')
                    input(f'Clique para continuar...')
                    continue
                logger = logging.getLogger('vendasDao')
                logger.error(f'Erro ao modificar trabalho vendido: {trabalhoVendidoDao.pegaErro()}')
                print(f'Erro ao modificar trabalho vendido: {trabalhoVendidoDao.pegaErro()}')
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

    def redefineListaDeProfissoes(self):
        while True:
            limpaTela()
            personagemDao = PersonagemDaoSqlite()
            personagens = personagemDao.pegaPersonagens()
            if not variavelExiste(personagens):
                print(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
                input(f'Clique para continuar...')
                break
            print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
            for personagem in personagens:
                print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
            opcaoPersonagem = input(f'Opção:')
            if int(opcaoPersonagem) == 0:
                break
            profissaoDao = ProfissaoDaoSqlite(personagens[int(opcaoPersonagem) - 1])
            profissaoDao.limpaListaProfissoes(True)

    def testeFuncao(self):
        trabalhoTeste = 'Pulseiras da Inacessibilidade'
        personagemTeste = Personagem()
        personagemTeste.id = '266719b6-8b25-4dc9-8d7a-ea7ef395a136'
        self.__personagemEmUso = personagemTeste
        trabalhoProducaoConcluido = self.retornaTrabalhoConcluido(trabalhoTeste)
        if variavelExiste(trabalhoProducaoConcluido):
            trabalhoProducaoRaro = self.verificaProducaoTrabalhoRaro(trabalhoProducaoConcluido)
            pass
        input(f'Clique para continuar')

    def teste(self):
        while True:
            limpaTela()
            print(f'MENU')
            print(f'01 - Adiciona trabalho')
            print(f'02 - Adiciona trabalho produção')
            print(f'03 - Modifica personagem')
            print(f'04 - Modifica profissao')
            print(f'05 - Remove trabalho')
            print(f'06 - Modifica trabalho produção')
            print(f'07 - Remove trabalho produção')
            print(f'08 - Mostra vendas')
            print(f'09 - Modifica trabalho')
            print(f'10 - Remove personagem')
            print(f'11 - Insere personagem')
            print(f'12 - Insere trabalho no estoque')
            print(f'13 - Modifica trabalho no estoque')
            print(f'14 - Remove trabalho no estoque')
            print(f'15 - Pega todos trabalhos no estoque')
            print(f'16 - Insere trabalho vendido')
            print(f'17 - Modifica trabalho vendido')
            print(f'18 - Remove trabalho vendido')
            print(f'19 - Pega todos trabalhos vendidos')
            print(f'20 - Pega todos trabalhos producao')
            print(f'21 - Sincroniza dados')
            print(f'22 - Pega todas profissões')
            print(f'23 - Redefine profissões')
            print(f'24 - Teste de funções')
            print(f'0 - Sair')
            try:
                opcaoMenu = input(f'Opção escolhida: ')
                if int(opcaoMenu) == 0:
                    break
                if int(opcaoMenu) == 1:
                    self.insereNovoTrabalho()
                    continue
                if int(opcaoMenu) == 2:
                    self.insereNovoTrabalhoProducao()
                    continue
                if int(opcaoMenu) == 3:
                    self.modificaPersonagem()
                    continue
                if int(opcaoMenu) == 4:
                    self.modificaProfissao()
                    continue
                if int(opcaoMenu) == 5:
                    self.removeTrabalho()
                    continue
                if int(opcaoMenu) == 6:
                    self.modificaTrabalhoProducao()
                    continue
                if int(opcaoMenu) == 7:
                    self.removeTrabalhoProducao()
                    continue
                if int(opcaoMenu) == 8:
                    self.mostraVendas()
                    continue
                if int(opcaoMenu) == 9:
                    self.modificaTrabalho()
                    continue
                if int(opcaoMenu) == 10:
                    self.removePersonagem()
                    continue
                if int(opcaoMenu) == 11:
                    self.inserePersonagem()
                    continue
                if int(opcaoMenu) == 12:
                    self.insereTrabalhoEstoque()
                    continue
                if int(opcaoMenu) == 13:
                    self.modificaTrabalhoEstoque()
                    continue
                if int(opcaoMenu) == 14:
                    self.removeTrabalhoEstoque()
                    continue
                if int(opcaoMenu) == 15:
                    self.pegaTodosTrabalhosEstoque()
                    continue
                if int(opcaoMenu) == 16:
                    # insere trabalho vendido
                    self.insereTrabalhoVendido()
                    continue
                if int(opcaoMenu) == 17:
                    # modifica trabalho vendido
                    self.modificaTrabalhoVendido()
                    continue
                if int(opcaoMenu) == 18:
                    # remove trabalho vendido
                    self.removeTrabalhoVendido()
                    continue
                if int(opcaoMenu) == 19:
                    # pega todos trabalhos vendidos
                    self.pegaTodosTrabalhosVendidos()
                    continue
                if int(opcaoMenu) == 20:
                    # pega todos trabalhos produção
                    self.pegaTodosTrabalhosProducao()
                    continue
                if int(opcaoMenu) == 21:
                    # pega todos trabalhos vendidos
                    self.sincronizaDados()
                    continue
                if int(opcaoMenu) == 22:
                    # pega todos trabalhos vendidos
                    self.pegaTodasProfissoes()
                    continue
                if int(opcaoMenu) == 23:
                    # pega todos trabalhos vendidos
                    self.redefineListaDeProfissoes()
                    continue
                if int(opcaoMenu) == 24:
                    # pega todos trabalhos vendidos
                    self.testeFuncao()
                    continue
            except Exception as erro:
                logger = logging.getLogger(__name__)
                logger.exception(erro)
                print(f'Opção inválida! Erro: {erro}')
                input(f'Clique para continuar...')

if __name__=='__main__':
    Aplicacao().preparaPersonagem()
    # print(self.imagem.reconheceTextoNomePersonagem(self.imagem.abreImagem('tests/imagemTeste/testeMenuTrabalhoProducao.png'), 1))