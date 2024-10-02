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

class Aplicacao:
    def __init__(self) -> None:
        logging.basicConfig(level = logging.INFO, filename = 'aplicacao.log', encoding='utf-8', format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt = '%d/%m/%Y %I:%M:%S %p')
        self._imagem = ManipulaImagem()
        self.__listaPersonagemJaVerificado = []
        self.__listaPersonagemAtivo = []
        self.__listaProfissoesNecessarias = []
        self.__personagemEmUso = None

    def defineListaPersonagemMesmoEmail(self):
        listaDicionarioPersonagemMesmoEmail = []
        if variavelExiste(self.__personagemEmUso):
            for personagem in PersonagemDaoSqlite().pegaPersonagens():
                if textoEhIgual(personagem.pegaEmail(), self.__personagemEmUso.pegaEmail()):
                    listaDicionarioPersonagemMesmoEmail.append(personagem)
        return listaDicionarioPersonagemMesmoEmail

    def modificaAtributoUso(self): 
        listaPersonagemMesmoEmail = self.defineListaPersonagemMesmoEmail()
        for personagem in PersonagemDaoSqlite().pegaPersonagens():
            for personagemMesmoEmail in listaPersonagemMesmoEmail:
                if textoEhIgual(personagem.pegaId(), personagemMesmoEmail.pegaId()):
                    if not personagem.pegaUso():
                        personagem.alternaUso()
                        personagemDao = PersonagemDaoSqlite()
                        if personagemDao.modificaPersonagem(personagem):
                            uso = 'verdadeiro' if personagem.pegaUso() else 'falso'
                            print(f'{personagem.pegaNome()}: Uso modificado para {uso} com sucesso!')
                            break
                        logger = logging.getLogger('personagemDao')
                        logger.error(f'Erro ao modificar personagem: {personagemDao.pegaErro()}')
                        print(f'Erro: {personagemDao.pegaErro()}')
                    break
            else:
                if personagem.pegaUso():
                    personagem.alternaUso()
                    personagemDao = PersonagemDaoSqlite()
                    if personagemDao.modificaPersonagem(personagem):
                        uso = personagem.pegaUso()
                        print(f'{personagem.pegaNome()}: Uso modificado para {uso} com sucesso!')
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
            if textoEhIgual(personagemReconhecido, personagemAtivo.pegaNome()):
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
        listaPersonagem = PersonagemDaoSqlite().pegaPersonagens()
        self.__listaPersonagemAtivo.clear()
        for personagem in listaPersonagem:
            if personagem.ehAtivo():
                self.__listaPersonagemAtivo.append(personagem)

    def inicializaChavesPersonagem(self):
        self._autoProducaoTrabalho = self.__personagemEmUso.pegaAutoProducao()
        self._unicaConexao = True
        self._espacoBolsa = True
        self.__confirmacao = True
        self._profissaoModificada = False
        self.__vendaDaoSqlite = VendaDaoSqlite(self.__personagemEmUso)

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
        textoCarta = self._imagem.retornaTextoCorrespondenciaReconhecido()
        if variavelExiste(textoCarta):
            trabalhoFoiVendido = texto1PertenceTexto2('Item vendido', textoCarta)
            if trabalhoFoiVendido:
                print(f'Produto vendido')
                textoCarta = re.sub("Item vendido", "", textoCarta)
                trabalhoVendido = TrabalhoVendido(str(uuid.uuid4()), textoCarta, str(datetime.date.today()), self.__personagemEmUso.pegaId(), self.retornaQuantidadeTrabalhoVendido(textoCarta), self.retornaChaveIdTrabalho(textoCarta), self.retornaValorTrabalhoVendido(textoCarta))
                vendaDAO = VendaDaoSqlite(self.__personagemEmUso)
                if vendaDAO.insereVenda(trabalhoVendido):
                    print(f'Nova venda {trabalhoVendido.pegaNome()} cadastrada com sucesso!')
                    return trabalhoVendido
                logger = logging.getLogger('vendaDao')
                logger.error(f'Erro ao inserir nova venda: {vendaDAO.pegaErro()}')
                print(f'Erro ao inserir nova venda: {vendaDAO.pegaErro()}')
            else:
                print(f'Erro...')
        return None

    def retornaChaveIdTrabalho(self, textoCarta):
        for trabalho in TrabalhoDaoSqlite().pegaTrabalhos():
            if texto1PertenceTexto2(trabalho.pegaNome(), textoCarta):
                return trabalho.pegaId()
        return ''

    def atualizaQuantidadeTrabalhoEstoque(self, venda):
        for trabalhoEstoque in EstoqueDaoSqlite(self.__personagemEmUso).pegaEstoque():
            if textoEhIgual(trabalhoEstoque.pegaTrabalhoId(), venda.pegaTrabalhoId()):
                novaQuantidade = trabalhoEstoque.pegaQuantidade() - venda.pegaQuantidadeProduto()
                trabalhoEstoque.setQuantidade(novaQuantidade)
                estoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
                if estoqueDao.modificaTrabalhoEstoque(trabalhoEstoque):
                    print(f'Quantidade do trabalho ({trabalhoEstoque.pegaNome()}) atualizada para {novaQuantidade}.')
                    return
                logger = logging.getLogger('estoqueDao')
                logger.error(f'Erro ao modificar trabalho no estoque: {estoqueDao.pegaErro()}')
                print(f'Erro ao modificar trabalho no estoque: {estoqueDao.pegaErro()}')
        print(f'Trabalho ({venda.pegaNome()}) não encontrado no estoque.')

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
        for trabalho in TrabalhoDaoSqlite().pegaTrabalhos():
            if texto1PertenceTexto2(nomeTrabalhoConcluido[1:-1], trabalho.pegaNomeProducao()):
                listaPossiveisDicionariosTrabalhos.append(trabalho)
        return listaPossiveisDicionariosTrabalhos

    def retornaTrabalhoConcluido(self, nomeTrabalhoConcluido):
        listaPossiveisTrabalhos = self.retornaListaPossiveisTrabalhoRecuperado(nomeTrabalhoConcluido)
        if not tamanhoIgualZero(listaPossiveisTrabalhos):
            for possivelTrabalho in listaPossiveisTrabalhos:
                for trabalhoProduzirProduzindo in TrabalhoProducaoDaoSqlite(self.__personagemEmUso).pegaTrabalhosProducaoParaProduzirProduzindo():
                    condicoes = trabalhoProduzirProduzindo.ehProduzindo() and textoEhIgual(trabalhoProduzirProduzindo.pegaNome(), possivelTrabalho.pegaNome())
                    if condicoes:
                        trabalhoProduzirProduzindo.setEstado(CODIGO_CONCLUIDO)
                        trabalhoProduzirProduzindo.setTrabalhoId(possivelTrabalho.pegaId())
                        trabalhoProduzirProduzindo.setNomeProducao(possivelTrabalho.pegaNomeProducao())
                        return trabalhoProduzirProduzindo
            else:
                print(f'Trabalho concluído ({listaPossiveisTrabalhos[0].pegaNome()}) não encontrado na lista produzindo...')
                trabalhoProducaoConcluido = TrabalhoProducao(str(uuid.uuid4()), listaPossiveisTrabalhos[0].pegaId(), listaPossiveisTrabalhos[0].pegaNome(), listaPossiveisTrabalhos[0].pegaNomeProducao(), listaPossiveisTrabalhos[0].pegaExperiencia(), listaPossiveisTrabalhos[0].pegaNivel(), listaPossiveisTrabalhos[0].pegaProfissao(), listaPossiveisTrabalhos[0].pegaRaridade(), listaPossiveisTrabalhos[0].pegaTrabalhoNecessario(), False, CHAVE_LICENCA_NOVATO, CODIGO_CONCLUIDO)
                trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
                if trabalhoProducaoDao.insereTrabalhoProducao(trabalhoProducaoConcluido):
                    print(f'{trabalhoProducaoConcluido.pegaNome()} adicionado com sucesso!')
                    return trabalhoProducaoConcluido
                logger = logging.getLogger('trabalhoProducaoDao')
                logger.error(f'Erro ao inserir trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
                print(f'Erro ao inserir trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
                return trabalhoProducaoConcluido
        return None

    def modificaTrabalhoConcluidoListaProduzirProduzindo(self, trabalhoProducaoConcluido):
        if trabalhoEhProducaoRecursos(trabalhoProducaoConcluido):
            trabalhoProducaoConcluido.setRecorrencia(True)
        if trabalhoProducaoConcluido.pegaRecorrencia():
            print(f'Trabalho recorrente.')
            trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
            if trabalhoProducaoDao.removeTrabalhoProducao(trabalhoProducaoConcluido):
                print(f'Trabalho ({trabalhoProducaoConcluido.pegaNome()}) removido com sucesso!')
                return trabalhoProducaoConcluido
            logger = logging.getLogger('trabalhoProducaoDao')
            logger.error(f'Erro ao remover trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
            print(f'Erro ao remover trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
            return trabalhoProducaoConcluido
        print(f'Trabalho sem recorrencia.')
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
        if trabalhoProducaoDao.modificaTrabalhoProducao(trabalhoProducaoConcluido):
            print(f'Trabalho ({trabalhoProducaoConcluido.pegaNome()}) modificado para concluído.')
            return trabalhoProducaoConcluido
        logger = logging.getLogger('trabalhoProducaoDao')
        logger.error(f'Erro ao modificar trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
        print(f'Erro ao modificar trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
        return trabalhoProducaoConcluido

    def modificaExperienciaProfissao(self, trabalhoProducao):
        for profissao in ProfissaoDaoSqlite(self.__personagemEmUso).pegaProfissoes():
            if textoEhIgual(profissao.pegaNome(), trabalhoProducao.pegaProfissao()):
                experiencia = profissao.pegaExperiencia() + trabalhoProducao.pegaExperiencia()
                profissao.setExperiencia(experiencia)
                profissaoDao = ProfissaoDaoSqlite(self.__personagemEmUso)
                if profissaoDao.modificaProfissao(profissao):
                    print(f'Experiência de {profissao.pegaNome()} atualizada para {experiencia}  com sucesso!')
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
                    for trabalho in TrabalhoDaoSqlite().pegaTrabalhos():
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
            trabalhoEstoque = TrabalhoEstoque(str(uuid.uuid4()), trabalhoProducaoConcluido.pegaNome(), trabalhoProducaoConcluido.pegaProfissao(), trabalhoProducaoConcluido.pegaNivel(), 1, trabalhoProducaoConcluido.pegaRaridade(), trabalhoProducaoConcluido.pegaTrabalhoId())
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
                estoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
                if estoqueDao.modificaTrabalhoEstoque(trabalhoEstoque):
                    print(f'Quantidade do trabalho ({trabalhoEstoque.pegaNome()}) atualizada para {novaQuantidade}.')
                    continue
                logger = logging.getLogger('estoqueDao')
                logger.error(f'Erro ao modificar trabalho no estoque: {estoqueDao.pegaErro()}')
                print(f'Erro ao modificar trabalho no estoque: {estoqueDao.pegaErro()}')
        return listaTrabalhoEstoqueConcluido, trabalhoEstoque

    def atualizaEstoquePersonagem(self, trabalhoEstoqueConcluido):
        listaTrabalhoEstoqueConcluido = self.retornaListaTrabalhoProduzido(trabalhoEstoqueConcluido)
        if not tamanhoIgualZero(listaTrabalhoEstoqueConcluido):
            listaEstoque = EstoqueDaoSqlite(self.__personagemEmUso).pegaEstoque()
            if tamanhoIgualZero(listaEstoque):
                for trabalhoEstoqueConcluido in listaTrabalhoEstoqueConcluido:
                    trabalhoEstoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
                    if trabalhoEstoqueDao.insereTrabalhoEstoque(trabalhoEstoqueConcluido):
                        print(f'{trabalhoEstoqueConcluido.pegaNome()} adicionado com sucesso!')
                        continue
                    logger = logging.getLogger('estoqueDao')
                    logger.error(f'Erro ao inserir trabalho no estoque: {trabalhoEstoqueDao.pegaErro()}')
                    print(f'Erro ao inserir trabalho no estoque: {trabalhoEstoqueDao.pegaErro()}')
                return
            for trabalhoEstoque in listaEstoque:
                listaTrabalhoEstoqueConcluido, trabalhoEstoque = self.modificaQuantidadeTrabalhoEstoque(listaTrabalhoEstoqueConcluido, trabalhoEstoque)
            if not tamanhoIgualZero(listaTrabalhoEstoqueConcluido):
                for trabalhoEstoqueConcluido in listaTrabalhoEstoqueConcluido:
                    trabalhoEstoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
                    if trabalhoEstoqueDao.insereTrabalhoEstoque(trabalhoEstoqueConcluido):
                        print(f'{trabalhoEstoqueConcluido.pegaNome()} adicionado com sucesso!')
                        continue
                    logger = logging.getLogger('estoqueDao')
                    logger.error(f'Erro ao inserir trabalho no estoque: {trabalhoEstoqueDao.pegaErro()}')
                    print(f'Erro ao inserir trabalho no estoque: {trabalhoEstoqueDao.pegaErro()}')

    def retornaProfissaoTrabalhoProducaoConcluido(self, trabalhoProducaoConcluido):
        for profissao in ProfissaoDaoSqlite(self.__personagemEmUso).pegaProfissoes():
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
            licencaProducaoIdeal = CHAVE_LICENCA_INICIANTE
            if xpMaximo >= 830000:
                licencaProducaoIdeal = CHAVE_LICENCA_NOVATO
            if textoEhIgual(trabalhoProducaoConcluido.pegaRaridade(), CHAVE_RARIDADE_MELHORADO):
                print(f'Trabalhos MELHORADO. Profissão {trabalhoProducaoConcluido.pegaProfissao()}. Nível {trabalhoProducaoConcluido.pegaNivel()}.')
                for trabalho in TrabalhoDaoSqlite().pegaTrabalhos():
                    condicoes = (textoEhIgual(trabalho.pegaProfissao(), trabalhoProducaoConcluido.pegaProfissao())
                        and textoEhIgual(trabalho.pegaRaridade(), CHAVE_RARIDADE_RARO)
                        and trabalho.pegaNivel() == trabalhoProducaoConcluido.pegaNivel())
                    if condicoes:    
                        if textoEhIgual(trabalho.pegaTrabalhoNecessario(), trabalhoProducaoConcluido.pegaNome()):
                            experiencia = trabalho.pegaExperiencia() * 1.5
                            trabalhoProducaoRaro = TrabalhoProducao('', trabalho.pegaTrabalhoId(), trabalho.pegaNome(), trabalho.pegaNomeProducao(), experiencia, trabalho.pegaNivel(), trabalho.pegaProfissao(), trabalho.pegaRaridade(), trabalho.pegaTrabalhoNecessario(), False, licencaProducaoIdeal, trabalho.pegaEstado())
                            break
        if variavelExiste(trabalhoProducaoRaro):
            trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
            if trabalhoProducaoDao.insereTrabalhoProducao(trabalhoProducaoRaro):
                print(f'{trabalhoProducaoRaro.pegaNome()} adicionado com sucesso!')
                return 
            logger = logging.getLogger('trabalhoProducaoDao')
            logger.error(f'Erro ao inserir trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
            print(f'Erro ao inserir trabalho de produção: {trabalhoProducaoDao.pegaErro()}')

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
            for personagem in PersonagemDaoSqlite().pegaPersonagens():
                if not personagem.pegaEstado():
                    personagem.alternaEstado()
                    personagemDao = PersonagemDaoSqlite()
                    if personagemDao.modificaPersonagem(personagem):
                        estado = 'verdadeiro' if personagem.pegaEstado() else 'falso'
                        print(f'{personagem.pegaNome()}: Estado modificado para {estado} com sucesso!')
                    else:
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
                if textoEhIgual(trabalhoRaroVendidoOrdenado.pegaNome(), trabalhosRarosVendidos.pegaNome()):
                    trabalhoRaroVendidoOrdenado.setQuantidade(trabalhoRaroVendidoOrdenado.pegaQuantidade() + 1)
                    break
            else:
                listaTrabalhosRarosVendidosOrdenada.append(trabalhosRarosVendidos)
        listaTrabalhosRarosVendidosOrdenada = sorted(listaTrabalhosRarosVendidosOrdenada, key=lambda trabalho: (trabalho.pegaQuantidade(), trabalho.pegaNivel(), trabalho.pegaNome()), reverse = True)
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
        listaTrabalhosRarosVendidos = []
        for trabalhoVendido in VendaDaoSqlite(self.__personagemEmUso).pegaVendas():
            for trabalho in TrabalhoDaoSqlite().pegaTrabalhos():
                raridadeEhRaroIdPersonagemEhPersonagemEmUsoTrabalhoNaoEhProducaoDeRecursos = (
                    textoEhIgual(trabalho.pegaRaridade(), CHAVE_RARIDADE_RARO)
                    and texto1PertenceTexto2(trabalho.pegaNome(), trabalhoVendido.pegaNome())
                    and textoEhIgual(trabalhoVendido.pegaNomePersonagem(), self.__personagemEmUso.pegaId())
                    and not trabalhoEhProducaoRecursos(trabalho))
                if raridadeEhRaroIdPersonagemEhPersonagemEmUsoTrabalhoNaoEhProducaoDeRecursos:
                    print(trabalhoVendido)
                    listaTrabalhosRarosVendidos.append(trabalhoVendido)
                    break
        listaTrabalhosRarosVendidosOrdenados = sorted(listaTrabalhosRarosVendidos, key = lambda trabalho: (trabalho.pegaProfissao(), trabalho.pegaNivel(), trabalho.pegaNome()))
        return listaTrabalhosRarosVendidosOrdenados

    def verificaProdutosRarosMaisVendidos(self):
        listaTrabalhosRarosVendidos = self.retornaListaTrabalhosRarosVendidos()
        if tamanhoIgualZero(listaTrabalhosRarosVendidos):
            print(f'Lista de trabalhos raros vendidos está vazia!')
            return
        self.produzProdutoMaisVendido(listaTrabalhosRarosVendidos)

    def defineChaveListaProfissoesNecessarias(self):
        print(f'Verificando profissões necessárias...')
        self.__listaProfissoesNecessarias.clear()
        for profissao in ProfissaoDaoSqlite(self.__personagemEmUso).pegaProfissoes():
            for trabalhoProducaoDesejado in TrabalhoProducaoDaoSqlite(self.__personagemEmUso).pegaTrabalhosProducao():
                chaveProfissaoEhIgualEEstadoEhParaProduzir = textoEhIgual(profissao.pegaNome(), trabalhoProducaoDesejado.pegaProfissao()) and trabalhoProducaoDesejado.ehParaProduzir()
                if chaveProfissaoEhIgualEEstadoEhParaProduzir:
                    self.__listaProfissoesNecessarias.append(profissao)
                    break
        else:
            self.__listaProfissoesNecessarias = sorted(self.__listaProfissoesNecessarias,key=lambda profissao:profissao.pegaPrioridade(),reverse=True)
            for profissaoNecessaria in self.__listaProfissoesNecessarias:
                print(f'{profissaoNecessaria}')

    def retornaContadorEspacosProducao(self, contadorEspacosProducao, nivel):
        contadorNivel = 0
        for dicionarioProfissao in ProfissaoDaoSqlite(self.__personagemEmUso).pegaProfissoes():
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
        for dicionarioProfissao in ProfissaoDaoSqlite(self.__personagemEmUso).pegaProfissoes():
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
        if self.__personagemEmUso.pegaEspacoProducao() != quantidadeEspacoProducao:
            self.__personagemEmUso.setEspacoProducao(quantidadeEspacoProducao)
            personagemDao = PersonagemDaoSqlite()
            if personagemDao.modificaPersonagem(self.__personagemEmUso):
                print(f'{self.__personagemEmUso.pegaNome()}: Espaço de produção modificado para {self.__personagemEmUso.pegaEspacoProducao()} com sucesso!')
                return
            logger = logging.getLogger('personagemDao')
            logger.error(f'Erro ao modificar personagem: {personagemDao.pegaErro()}')
            print(f'Erro: {personagemDao.pegaErro()}')

    def retornaListaDicionariosTrabalhosProducaoRaridadeEspecifica(self, dicionarioTrabalho, raridade):
        listaTrabalhosProducaoRaridadeEspecifica = []
        print(f'Buscando trabalho {raridade} na lista...')
        for trabalhoProducao in TrabalhoProducaoDaoSqlite(self.__personagemEmUso).pegaTrabalhosProducaoParaProduzirProduzindo():
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
        return TrabalhoProducao(str(uuid.uuid4()), trabalhoProducaoEncontrado.pegaTrabalhoId(),trabalhoProducaoEncontrado.pegaNome(), trabalhoProducaoEncontrado.pegaNomeProducao(), trabalhoProducaoEncontrado.pegaExperiencia(), trabalhoProducaoEncontrado.pegaNivel(), trabalhoProducaoEncontrado.pegaProfissao(), trabalhoProducaoEncontrado.pegaRaridade(), trabalhoProducaoEncontrado.pegaTrabalhoNecessario(), trabalhoProducaoEncontrado.pegaRecorrencia(), trabalhoProducaoEncontrado.pegaLicenca(), trabalhoProducaoEncontrado.pegaEstado())

    def clonaTrabalhoProducaoEncontrado(self, dicionarioTrabalho, trabalhoProducaoEncontrado):
        print(f'Recorrencia está ligada.')
        cloneTrabalhoProducaoEncontrado = self.defineCloneDicionarioTrabalhoDesejado(trabalhoProducaoEncontrado)
        dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = cloneTrabalhoProducaoEncontrado
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
        if trabalhoProducaoDao.insereTrabalhoProducao(cloneTrabalhoProducaoEncontrado):
            print(f'{trabalhoProducaoEncontrado.pegaNome()} adicionado com sucesso!')
            return
        logger = logging.getLogger('trabalhoProducaoDao')
        logger.error(f'Erro ao inserir trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
        print(f'Erro ao inserir trabalho de produção: {trabalhoProducaoDao.pegaErro()}')

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

    def removeTrabalhoProducaoEstoque(self, trabalhoProducao):
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
                for trabalhoEstoque in EstoqueDaoSqlite(self.__personagemEmUso).pegaEstoque():
                    for recursoBuscado in listaNomeRecursoBuscado:
                        if textoEhIgual(trabalhoEstoque.pegaNome(), recursoBuscado[0]):
                            novaQuantidade = trabalhoEstoque.pegaQuantidade() - recursoBuscado[1]
                            if novaQuantidade < 0:
                                novaQuantidade = 0
                            print(f'Quantidade de {trabalhoEstoque.pegaNome()} atualizada de {trabalhoEstoque.pegaQuantidade()} para {novaQuantidade}.')
                            trabalhoEstoque.setQuantidade(novaQuantidade)
                            estoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
                            if estoqueDao.modificaTrabalhoEstoque(trabalhoEstoque):
                                print(f'Quantidade do trabalho ({trabalhoEstoque.pegaNome()}) atualizada para {novaQuantidade}.')
                                continue
                            logger = logging.getLogger('estoqueDao')
                            logger.error(f'Erro ao modificar trabalho no estoque: {estoqueDao.pegaErro()}')
                            print(f'Erro ao modificar trabalho no estoque: {estoqueDao.pegaErro()}')
                    if textoEhIgual(trabalhoEstoque.pegaNome(), trabalhoProducao.pegaLicenca()):
                        novaQuantidade = trabalhoEstoque.pegaQuantidade() - 1
                        if novaQuantidade < 0:
                            novaQuantidade = 0
                        print(f'Quantidade de {trabalhoEstoque.pegaNome()} atualizada de {trabalhoEstoque.pegaQuantidade()} para {novaQuantidade}.')
                        trabalhoEstoque.setQuantidade(novaQuantidade)
                        estoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
                        if estoqueDao.modificaTrabalhoEstoque(trabalhoEstoque):
                            print(f'Quantidade do trabalho ({trabalhoEstoque.pegaNome()}) atualizada para {novaQuantidade}.')
                            continue
                        logger = logging.getLogger('estoqueDao')
                        logger.error(f'Erro ao modificar trabalho no estoque: {estoqueDao.pegaErro()}')
                        print(f'Erro ao modificar trabalho no estoque: {estoqueDao.pegaErro()}')
            else:
                trabalhoRecurso = self.retornaTrabalhoRecurso(trabalhoProducao)
                for trabalhoEstoque in EstoqueDaoSqlite(self.__personagemEmUso).pegaEstoque():
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
                        estoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
                        if estoqueDao.modificaTrabalhoEstoque(trabalhoEstoque):
                            print(f'Quantidade do trabalho ({trabalhoEstoque.pegaNome()}) atualizada para {novaQuantidade}.')
                            continue
                        logger = logging.getLogger('estoqueDao')
                        logger.error(f'Erro ao modificar trabalho no estoque: {estoqueDao.pegaErro()}')
                        print(f'Erro ao modificar trabalho no estoque: {estoqueDao.pegaErro()}')
        elif trabalhoProducao.ehMelhorado() or trabalhoProducao.ehRaro():
            if not trabalhoEhProducaoRecursos(trabalhoProducao):
                listaTrabalhosNecessarios = trabalhoProducao.pegaTrabalhoNecessario().split(',')
                for trabalhoNecessario in listaTrabalhosNecessarios:
                    for trabalhoEstoque in EstoqueDaoSqlite(self.__personagemEmUso).pegaEstoque():
                        if textoEhIgual(trabalhoNecessario, trabalhoEstoque.pegaNome()):
                            novaQuantidade = trabalhoEstoque.pegaQuantidade() - 1
                            if novaQuantidade < 0:
                                novaQuantidade = 0
                            print(f'Quantidade de {trabalhoEstoque.pegaNome()} atualizada para {novaQuantidade}.')
                            trabalhoEstoque.setQuantidade(novaQuantidade)
                            estoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
                            if estoqueDao.modificaTrabalhoEstoque(trabalhoEstoque):
                                print(f'Quantidade do trabalho ({trabalhoEstoque.pegaNome()}) atualizada para {novaQuantidade}.')
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
                        self.clonaTrabalhoProducaoEncontrado(dicionarioTrabalho, trabalhoProducaoEncontrado)
                        self.verificaNovamente = True
                        break
                    trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
                    if trabalhoProducaoDao.modificaTrabalhoProducao(trabalhoProducaoEncontrado):
                        estado = 'produzir' if trabalhoProducaoEncontrado.pegaEstado() == 0 else 'produzindo' if trabalhoProducaoEncontrado.pegaEstado() == 1 else 'concluido'
                        print(f'Trabalho ({trabalhoProducaoEncontrado.pegaNome()}) modificado para {estado}.')
                    else:
                        logger = logging.getLogger('trabalhoProducaoDao')
                        logger.error(f'Erro ao modificar trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
                        print(f'Erro ao modificar trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
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
                print(f"Buscando: {trabalhoProducaoEncontrado.pegaLicenca()}")
                textoReconhecido = self._imagem.retornaTextoLicencaReconhecida()
                if variavelExiste(textoReconhecido):
                    print(f'Licença reconhecida: {textoReconhecido}')
                    if texto1PertenceTexto2('Licença de Artesanato', textoReconhecido):
                        primeiraBusca = True
                        listaCiclo = []
                        while not texto1PertenceTexto2(textoReconhecido, trabalhoProducaoEncontrado.pegaLicenca()):
                            listaCiclo.append(textoReconhecido)
                            clickEspecifico(1, "right")
                            textoReconhecido = self._imagem.retornaTextoLicencaReconhecida()
                            if variavelExiste(textoReconhecido):
                                print(f'Licença reconhecida: {textoReconhecido}.')
                                if textoEhIgual(textoReconhecido, 'nenhumitem'):
                                    if textoEhIgual(trabalhoProducaoEncontrado.pegaLicenca(), CHAVE_LICENCA_NOVATO):
                                        if not textoEhIgual(listaCiclo[-1], 'nenhumitem'):
                                            print(f'Sem licenças de produção...')
                                            self.__personagemEmUso.alternaEstado()
                                            personagemDao = PersonagemDaoSqlite()
                                            if personagemDao.modificaPersonagem(self.__personagemEmUso):
                                                estado = 'verdadeiro' if self.__personagemEmUso.pegaEstado() else 'falso'
                                                print(f'{self.__personagemEmUso.pegaNome()}: Estado modificado para {estado} com sucesso!')
                                            else:
                                                logger = logging.getLogger('personagemDao')
                                                logger.error(f'Erro ao modificar personagem: {personagemDao.pegaErro()}')
                                                print(f'Erro: {personagemDao.pegaErro()}')
                                            clickEspecifico(3, 'f1')
                                            clickContinuo(10, 'up')
                                            clickEspecifico(1, 'left')
                                            return dicionarioTrabalho
                                    else:
                                        print(f'{trabalhoProducaoEncontrado.pegaLicenca()} não encontrado!')
                                        print(f'Licença buscada agora é Licença de produção do iniciante!')
                                        trabalhoProducaoEncontrado.setLicenca(CHAVE_LICENCA_NOVATO)
                                        dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = trabalhoProducaoEncontrado
                                else:
                                    if len(listaCiclo) > 10:
                                        print(f'{trabalhoProducaoEncontrado.pegaLicenca()} não encontrado!')
                                        print(f'Licença buscada agora é Licença de produção do iniciante!')
                                        trabalhoProducaoEncontrado.setLicenca(CHAVE_LICENCA_NOVATO)
                                        dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = trabalhoProducaoEncontrado          
                            else:
                                erro = self.verificaErro()
                                if ehErroOutraConexao(erro):
                                    self._unicaConexao = False
                                print(f'Erro ao reconhecer licença!')
                                break
                            primeiraBusca = False
                        else:
                            trabalhoProducaoEncontrado.setEstado(CODIGO_PRODUZINDO)
                            if primeiraBusca:
                                clickEspecifico(1, "f1")
                            else:
                                clickEspecifico(1, "f2")
                    else:
                        print(f'Sem licenças de produção...')
                        self.__personagemEmUso.alternaEstado()
                        personagemDao = PersonagemDaoSqlite()
                        if personagemDao.modificaPersonagem(self.__personagemEmUso):
                            estado = 'verdadeiro' if self.__personagemEmUso.pegaEstado() else 'falso'
                            print(f'{self.__personagemEmUso.pegaNome()}: Estado modificado para {estado} com sucesso!')
                        else:
                            logger = logging.getLogger('personagemDao')
                            logger.error(f'Erro ao modificar personagem: {personagemDao.pegaErro()}')   
                            print(f'Erro: {personagemDao.pegaErro()}')
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
                    self.__confirmacao = False
                    trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
                    if trabalhoProducaoDao.removeTrabalhoProducao(trabalhoProducaoEncontrado):
                        print(f'Trabalho ({trabalhoProducaoEncontrado.pegaNome()}) removido com sucesso!')
                        erro = self.verificaErro()
                        continue
                    logger = logging.getLogger('trabalhoProducaoDao')
                    logger.error(f'Erro ao remover trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
                    print(f'Erro ao remover trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
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
        for trabalho in TrabalhoDaoSqlite().pegaTrabalhos():
            if texto1PertenceTexto2(nomeTrabalhoConcluido[1:-1], trabalho.pegaNomeProducao()):
                trabalhoEncontrado = TrabalhoProducao('', trabalho.pegaId(), trabalho.pegaNome(), trabalho.pegaNomeProducao(), trabalho.pegaExperiencia(), trabalho.pegaNivel(), trabalho.pegaProfissao(), trabalho.pegaRaridade(), trabalho.pegaTrabalhoNecessario(), False, CHAVE_LICENCA_NOVATO, CODIGO_CONCLUIDO)
                listaPossiveisTrabalhos.append(trabalhoEncontrado)
        return listaPossiveisTrabalhos

    def retornaTrabalhoProducaoConcluido(self, nomeTrabalhoConcluido):
        listaPossiveisTrabalhosProducao = self.retornaListaPossiveisTrabalhos(nomeTrabalhoConcluido)
        if not tamanhoIgualZero(listaPossiveisTrabalhosProducao):
            for possivelTrabalhoProducao in listaPossiveisTrabalhosProducao:
                for dicionarioTrabalhoProduzirProduzindo in TrabalhoProducaoDaoSqlite(self.__personagemEmUso).pegaTrabalhosProducaoParaProduzirProduzindo():
                    condicoes = dicionarioTrabalhoProduzirProduzindo.ehProduzindo() and textoEhIgual(dicionarioTrabalhoProduzirProduzindo.pegaNome(), possivelTrabalhoProducao.pegaNome())
                    if condicoes:
                        return dicionarioTrabalhoProduzirProduzindo
            else:
                print(f'Trabalho concluído ({listaPossiveisTrabalhosProducao[0].pegaNome()}) não encontrado na lista produzindo...')
                return listaPossiveisTrabalhosProducao[0]
        return None

    
    def existeEspacoProducao(self):
        espacoProducao = self.__personagemEmUso.pegaEspacoProducao()
        for trabalhoProducao in TrabalhoProducaoDaoSqlite(self.__personagemEmUso).pegaTrabalhosProducao():
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
                profissoes = ProfissaoDaoSqlite(self.__personagemEmUso).pegaProfissoes()
                for profissao in profissoes:
                    if profissao.pegaNome() == profissaoNecessaria.pegaNome():
                        posicao = profissoes.index(profissao) + 1 
                entraProfissaoEspecifica(profissaoNecessaria, posicao)
                print(f'Verificando profissão: {profissaoNecessaria.pegaNome()}')
                dicionarioTrabalho[CHAVE_PROFISSAO] = profissaoNecessaria.pegaNome()
                listaDeListasTrabalhosProducao = self.retornaListaDeListasTrabalhosProducao(dicionarioTrabalho)
                for listaTrabalhosProducao in listaDeListasTrabalhosProducao:
                    if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not self.__confirmacao:
                        break
                    dicionarioTrabalho[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA] = listaTrabalhosProducao
                    for trabalhoProducaoPriorizado in dicionarioTrabalho[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA]:
                        if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not self.__confirmacao:
                            break
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
                                    self.verificaProducaoTrabalhoRaro(trabalhoProducaoConcluido)
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

    def retiraPersonagemJaVerificadoListaAtivo(self):
        """
        Esta função é responsável por redefinir a lista de personagens ativos, verificando a lista de personagens já verificados
        """        
        self.defineListaPersonagensAtivos()
        novaListaPersonagensAtivos = []
        for personagemAtivo in self.__listaPersonagemAtivo:
            for personagemRemovido in self.__listaPersonagemJaVerificado:
                if textoEhIgual(personagemAtivo.pegaNome(), personagemRemovido.pegaNome()):
                    break
            else:
                print(personagemAtivo)
                novaListaPersonagensAtivos.append(personagemAtivo)
        self.__listaPersonagemAtivo = novaListaPersonagensAtivos

    def logaContaPersonagem(self):
        confirmacao=False
        email=self.__listaPersonagemAtivo[0].pegaEmail()
        senha=self.__listaPersonagemAtivo[0].pegaSenha()
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
                    print(f'Personagem ({self.__personagemEmUso.pegaNome()}) encontrado.')
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
            self.retiraPersonagemJaVerificadoListaAtivo()
            listaPersonagensAtivosEstaVazia = tamanhoIgualZero(self.__listaPersonagemAtivo)
            if listaPersonagensAtivosEstaVazia:
                self.__listaPersonagemJaVerificado.clear()
                continue
            self.definePersonagemEmUso()
            if variavelExiste(self.__personagemEmUso):
                self.modificaAtributoUso()
                print(f'Personagem ({self.__personagemEmUso.pegaNome()}) ESTÁ EM USO.')
                self.inicializaChavesPersonagem()
                print('Inicia busca...')
                if self.vaiParaMenuProduzir():
                    # while defineTrabalhoComumProfissaoPriorizada():
                    #     continue
                    if tamanhoIgualZero(TrabalhoProducaoDaoSqlite(self.__personagemEmUso).pegaTrabalhosProducaoParaProduzirProduzindo()):
                        print(f'Lista de trabalhos desejados vazia.')
                        self.__personagemEmUso.alternaEstado()
                        personagemDao = PersonagemDaoSqlite()
                        if personagemDao.modificaPersonagem(self.__personagemEmUso):
                            estado = 'verdadeiro' if self.__personagemEmUso.pegaEstado() else 'falso'
                            print(f'{self.__personagemEmUso.pegaNome()}: Estado modificado para {estado} com sucesso!')
                            continue
                        logger = logging.getLogger('personagemDao')
                        logger.error(f'Erro ao modificar personagem: {personagemDao.pegaErro()}')
                        print(f'Erro: {personagemDao.pegaErro()}')
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
            if textoEhIgual(self.__listaPersonagemJaVerificado[-1].pegaEmail(), self.__listaPersonagemAtivo[0].pegaEmail()):
                self.entraPersonagemAtivo()
                continue
            if self.configuraLoginPersonagem():
                self.entraPersonagemAtivo()
        
    def preparaPersonagem(self):
        clickAtalhoEspecifico('alt', 'tab')
        clickAtalhoEspecifico('win', 'left')
        self.iniciaProcessoBusca()

    def modificaProfissao(self):
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
                profissoes = ProfissaoDaoSqlite(personagens[int(opcaoPersonagem) - 1]).pegaProfissoes()
                if len(profissoes) == 0:
                    ProfissaoDaoSqlite(personagens[int(opcaoPersonagem) - 1]).insereListaProfissoes()
                    profissoes = ProfissaoDaoSqlite(personagens[int(opcaoPersonagem) - 1]).pegaProfissoes()
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
                    novoNome = profissaoModificado.pegaNome()
                profissaoModificado.setNome(novoNome)
                if tamanhoIgualZero(novaExperiencia):
                    novaExperiencia = profissaoModificado.pegaExperiencia()
                profissaoModificado.setExperiencia(int(novaExperiencia))
                alternaPrioridade = input(f'Alternar prioridade? (S/N) ')
                if alternaPrioridade.lower() == 's':
                    profissaoModificado.alternaPrioridade()
                profissaoDao = ProfissaoDaoSqlite(personagens[int(opcaoPersonagem)-1])
                if profissaoDao.modificaProfissao(profissaoModificado):
                    print(f'Profissão {profissaoModificado.pegaNome()} modificado com sucesso!')
                    continue
                logger = logging.getLogger('profissaoDao')
                logger.error(f'Erro ao modificar profissão: {profissaoDao.pegaErro()}')
                print(f'Erro ao modificar profissão: {profissaoDao.pegaErro()}')

    def insereNovoTrabalho(self):
        while True:
            limpaTela()
            trabalhos = TrabalhoDaoSqlite().pegaTrabalhos()
            print(f'{('NOME').ljust(44)} | {('PROFISSÃO').ljust(22)} | {('RARIDADE').ljust(9)} | NÍVEL')
            for trabalho in trabalhos:
                print(trabalho)
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
                        print(f'{novoTrabalho.pegaNome()} adicionado com sucesso!')
                        continue
                    print(f'Erro: {trabalhoDao.pegaErro()}')
                    logger.error(f'Erro ao inserir novo trabalho: {trabalhoDao.pegaErro()}')
                except Exception as erro:
                    logger = logging.getLogger(__name__)
                    logger.exception(erro)
                    print(f'Opção inválida!')
                    input(f'Clique para continuar...')
            except Exception as erro:
                logger = logging.getLogger(__name__)
                logger.exception(erro)
                print(f'Opção inválida!')
                input(f'Clique para continuar...')

    def modificaTrabalho(self):
        while True:
            limpaTela()
            trabalhos = TrabalhoDaoSqlite().pegaTrabalhos()
            print(f'{('ÍNDICE').ljust(6)} - {('NOME').ljust(44)} | {('PROFISSÃO').ljust(22)} | {('RARIDADE').ljust(9)} | NÍVEL')
            for trabalho in trabalhos:
                print(f'{str(trabalhos.index(trabalho) + 1).ljust(6)} - {trabalho}')
            opcaoTrabalho = input(f'Opção trabalho: ')    
            if int(opcaoTrabalho) == 0:
                break
            trabalhoEscolhido = trabalhos[int(opcaoTrabalho) - 1]
            novoNome = input(f'Novo nome: ')
            if tamanhoIgualZero(novoNome):
                novoNome = trabalhoEscolhido.pegaNome()
            novoNomeProducao = input(f'Novo nome de produção: ')
            if tamanhoIgualZero(novoNomeProducao):
                novoNomeProducao = trabalhoEscolhido.pegaNomeProducao()
            novaExperiencia = input(f'Nova experiência: ')
            if tamanhoIgualZero(novaExperiencia):
                novaExperiencia = trabalhoEscolhido.pegaExperiencia()
            novoNivel = input(f'Novo nível: ')
            if tamanhoIgualZero(novoNivel):
                novoNivel = trabalhoEscolhido.pegaNivel()
            novaProfissao = input(f'Nova profissão: ')
            if tamanhoIgualZero(novaProfissao):
                novaProfissao = trabalhoEscolhido.pegaProfissao()
            novaRaridade = input(f'Nova raridade: ')
            if tamanhoIgualZero(novaRaridade):
                novaRaridade = trabalhoEscolhido.pegaRaridade()
            novoTrabalhoNecessario = input(f'Novo trabalho necessário: ')
            if tamanhoIgualZero(novoTrabalhoNecessario):
                novoTrabalhoNecessario = trabalhoEscolhido.pegaTrabalhoNecessario()
            trabalhoEscolhido.setNome(novoNome)
            trabalhoEscolhido.setNomeProducao(novoNomeProducao)
            trabalhoEscolhido.setExperiencia(novaExperiencia)
            trabalhoEscolhido.setNivel(novoNivel)
            trabalhoEscolhido.setProfissao(novaProfissao)
            trabalhoEscolhido.setRaridade(novaRaridade)
            trabalhoEscolhido.setTrabalhoNecessario(novoTrabalhoNecessario)
            trabalhoDao = TrabalhoDaoSqlite()
            if trabalhoDao.modificaTrabalho(trabalhoEscolhido):
                print(f'{trabalhoEscolhido.pegaNome()} modificado com sucesso!')
            else:
                print(f'Erro: {trabalhoDao.pegaErro()}')
                logging.error(f'Erro ao modificar trabalho: {trabalhoDao.pegaErro()}')
            input(f'Clique para continuar...')

    def insereNovoTrabalhoProducao(self):
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
                print(f'{('NOME').ljust(40)} | {('PROFISSÃO').ljust(22)} | {('NÍVEL').ljust(5)} | {('ESTADO').ljust(10)} | {('LICENÇA').ljust(31)} | RECORRÊNCIA')
                for trabalhoProducao in TrabalhoProducaoDaoSqlite(personagem).pegaTrabalhosProducaoParaProduzirProduzindo():
                    print(trabalhoProducao)
                opcaoTrabalho = input(f'Adicionar novo trabalho? (S/N)')    
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
                for trabalho in TrabalhoDaoSqlite().pegaTrabalhos():
                    if trabalho.pegaProfissao() == profissao:
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
                novoTrabalhoProducao = TrabalhoProducao(str(uuid.uuid4()), trabalho.pegaId(), trabalho.pegaNome(), trabalho.pegaNomeProducao(), trabalho.pegaExperiencia(), trabalho.pegaNivel(), trabalho.pegaProfissao(), trabalho.pegaRaridade(), trabalho.pegaTrabalhoNecessario(), recorrencia, licenca, 0)
                trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
                if trabalhoProducaoDao.insereTrabalhoProducao(novoTrabalhoProducao):
                    print(f'{novoTrabalhoProducao.pegaNome()} adicionado com sucesso!')
                    continue
                logger = logging.getLogger('trabalhoProducaoDao')
                logger.error(f'Erro ao inserir trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
                print(f'Erro ao inserir trabalho de produção: {trabalhoProducaoDao.pegaErro()}')

    def modificaPersonagem(self):
        while True:
            limpaTela()
            print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
            personagens = PersonagemDaoSqlite().pegaPersonagens()
            for personagem in personagens:
                print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
            opcaoPersonagem = input(f'Opção:')
            if int(opcaoPersonagem) == 0:
                break
            limpaTela()
            personagem = personagens[int(opcaoPersonagem) - 1]
            novoNome = input(f'Novo nome: ')
            if tamanhoIgualZero(novoNome):
                novoNome = personagem.pegaNome()
            personagem.setNome(novoNome)
            novoEspaco = input(f'Nova quantidade: ')
            if tamanhoIgualZero(novoEspaco):
                novoEspaco = personagem.pegaEspacoProducao()
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
                print(f'{personagem.pegaNome()}: Modificado com sucesso!')
                continue
            logger = logging.getLogger('personagemDao')
            logger.error(f'Erro ao modificar persoangem: {personagemDao.pegaErro()}')
            print(f'Erro: {personagemDao.pegaErro()}')
            
    def removeTrabalho(self):
        while True:
            limpaTela()
            trabalhos = TrabalhoDaoSqlite().pegaTrabalhos()
            print(f'{('ÍNDICE').ljust(6)} - {('NOME').ljust(44)} | {('PROFISSÃO').ljust(22)} | {('RARIDADE').ljust(9)} | NÍVEL')
            for trabalho in trabalhos:
                print(f'{str(trabalhos.index(trabalho) + 1).ljust(6)} - {trabalho}')
            opcaoTrabalho = input(f'Opção trabalho: ')    
            if int(opcaoTrabalho) == 0:
                break
            trabalhoEscolhido = trabalhos[int(opcaoTrabalho) - 1]
            trabalhoDao = TrabalhoDaoSqlite()
            if trabalhoDao.removeTrabalho(trabalhoEscolhido):
                print(f'{trabalhoEscolhido.pegaNome()} excluído com sucesso!')
            else:
                print(f'Erro: {trabalhoDao.pegaErro()}')
                logging.error(f'Erro ao remover trabalho: {trabalhoDao.pegaErro()}')
            input(f'Clique para continuar...')

    def modificaTrabalhoProducao(self):
        while True:
            limpaTela()
            print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
            personagens = PersonagemDaoSqlite().pegaPersonagens()
            for personagem in personagens:
                print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
            opcaoPersonagem = input(f'Opção: ')
            if int(opcaoPersonagem) == 0:
                break
            personagem = personagens[int(opcaoPersonagem) - 1]
            while True:
                limpaTela()
                trabalhosProducao = TrabalhoProducaoDaoSqlite(personagem).pegaTrabalhosProducao()
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
                    novaLicenca = trabalhoEscolhido.pegaLicenca()
                else:
                    trabalhoEscolhido.setLicenca(licencas[int(novaLicenca) - 1])
                limpaTela()
                novaRecorrencia = input(f'Alterna recorrencia? (S/N) ')
                if novaRecorrencia.lower() == 's':
                    trabalhoEscolhido.alternaRecorrencia()
                limpaTela()
                novoEstado = input(f'Novo estado: (0 - PRODUZIR, 1 - PRODUZINDO, 2 - CONCLUÍDO)')
                if tamanhoIgualZero(novoEstado):
                    novoEstado = trabalhoEscolhido.pegaEstado()
                else:
                    trabalhoEscolhido.setEstado(int(novoEstado))
                trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
                if trabalhoProducaoDao.modificaTrabalhoProducao(trabalhoEscolhido):
                    print(f'{trabalhoEscolhido.pegaNome()} modificado com sucesso!')
                    continue
                logger = logging.getLogger('trabalhoProducaoDao')
                logger.error(f'Erro ao modificar trabalho de produção: {trabalhoProducaoDao.pegaErro()}')
                print(f'Erro ao modificar trabalho de produção: {trabalhoProducaoDao.pegaErro()}')

    def removeTrabalhoProducao(self):
        while True:
            limpaTela()
            print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
            personagens = PersonagemDaoSqlite().pegaPersonagens()
            for personagem in personagens:
                print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
            opcaoPersonagem = input(f'Opção: ')
            if int(opcaoPersonagem) == 0:
                break
            personagem = personagens[int(opcaoPersonagem) - 1]
            while True: 
                limpaTela()
                print(f'{('ÍNDICE').ljust(6)} - {('NOME').ljust(40)} | {('PROFISSÃO').ljust(21)} | {('NÍVEL').ljust(5)} | {('ESTADO').ljust(10)} | LICENÇA')
                trabalhosProducao = TrabalhoProducaoDaoSqlite(personagem).pegaTrabalhosProducao()
                for trabalhoProducao in trabalhosProducao:
                    print(f'{str(trabalhosProducao.index(trabalhoProducao) + 1).ljust(6)} - {trabalhoProducao}')
                opcaoTrabalho = input(f'Opcção trabalho: ')
                if int(opcaoTrabalho) == 0:
                    break
                trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
                trabalhoRemovido = trabalhosProducao[int(opcaoTrabalho) - 1]
                if trabalhoProducaoDao.removeTrabalhoProducao(trabalhoRemovido):
                    print(f'{trabalhoRemovido.pegaNome()} removido com sucesso!')
                else:
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
                self.__vendaDaoSqlite = VendaDaoSqlite(personagem)
                vendas = VendaDaoSqlite(personagem).pegaVendas()
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
            personagens = PersonagemDaoSqlite().pegaPersonagens()
            for personagem in personagens:
                print(personagem)
            opcaoPersonagem = input(f'Inserir novo personagem? (S/N) ')
            if opcaoPersonagem.lower() == 'n':
                break
            nome = input(f'Nome: ')
            email = input(f'Email: ')
            senha = input(f'Senha: ')
            novoPersonagem = Personagem(str(uuid.uuid4()), nome, email, senha, 1, False, False, False)
            personagemDao = PersonagemDaoSqlite()
            if personagemDao.inserePersonagem(novoPersonagem):
                print(f'Novo personagem {novoPersonagem.pegaNome()} inserido com sucesso!')
                continue
            logger = logging.getLogger('personagemDao')
            logger.error(personagemDao.pegaErro())
            print(f'Erro ao inserir novo personagem: {personagemDao.pegaErro()}')

    def removePersonagem(self):
        while True:
            limpaTela()
            print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
            personagens = PersonagemDaoSqlite().pegaPersonagens()
            for personagem in personagens:
                print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
            opcaoPersonagem = input(f'Opção:')
            if int(opcaoPersonagem) == 0:
                break
            personagem = personagens[int(opcaoPersonagem) - 1]
            personagemDao = PersonagemDaoSqlite()
            if personagemDao.removePersonagem(personagem):
                print(f'Personagem {personagem.pegaNome()} removido com sucesso!')
                continue
            logger = logging.getLogger('personagemDao')
            logger.error(f'Erro ao remover personagem: {personagemDao.pegaErro()}')
            print(f'Erro ao remover personagem: {personagemDao.pegaErro()}')
    
    def insereTrabalhoEstoque(self):
        while True:
            limpaTela()
            print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
            personagens = PersonagemDaoSqlite().pegaPersonagens()
            for personagem in personagens:
                print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
            opcaoPersonagem = input(f'Opção:')
            if int(opcaoPersonagem) == 0:
                break
            personagem = personagens[int(opcaoPersonagem) - 1]
            while True:
                limpaTela()
                print(f'{('NOME').ljust(40)} | {('PROFISSÃO').ljust(25)} | {('QNT').ljust(3)} | {('NÍVEL').ljust(5)} | {('RARIDADE').ljust(10)} | {'ID TRABALHO'}')
                for trabalhoEstoque in EstoqueDaoSqlite(personagem).pegaEstoque():
                    print(trabalhoEstoque)
                opcaoTrabalho = input(f'Inserir novo trabalho ao estoque? (S/N) ')
                if opcaoTrabalho.lower() == 'n':
                    break
                trabalhos = TrabalhoDaoSqlite().pegaTrabalhos()
                print(f'{('ÍNDICE').ljust(6)} | {('NOME').ljust(44)} | {('PROFISSÃO').ljust(22)} | {('RARIDADE').ljust(9)} | NÍVEL')
                for trabalho in trabalhos:
                    print(f'{str(trabalhos.index(trabalho) + 1).ljust(6)} | {trabalho}')
                opcaoTrabalho = input(f'Opção trabalho: ')    
                if int(opcaoTrabalho) == 0:
                    break
                trabalho = trabalhos[int(opcaoTrabalho) - 1]
                quantidadeTrabalho = input(f'Quantidade trabalho: ')
                trabalhoEstoqueDao = EstoqueDaoSqlite(personagem)
                if trabalhoEstoqueDao.insereTrabalhoEstoque(TrabalhoEstoque(str(uuid.uuid4()), trabalho.pegaNome(), trabalho.pegaProfissao(), trabalho.pegaNivel(), quantidadeTrabalho, trabalho.pegaRaridade(), trabalho.pegaId())):
                    print(f'Trabalho {trabalho.pegaNome()} inserido no estoque com sucesso!')
                    continue
                logger = logging.getLogger('estoqueDao')
                logger.error(f'Erro ao inserir trabalho no estoque: {trabalhoEstoqueDao.pegaErro()}')
                print(f'Erro ao inserir trabalho no estoque: {trabalhoEstoqueDao.pegaErro()}')
    
    def modificaTrabalhoEstoque(self):
        while True:
            limpaTela()
            print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
            personagens = PersonagemDaoSqlite().pegaPersonagens()
            for personagem in personagens:
                print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
            opcaoPersonagem = input(f'Opção:')
            if int(opcaoPersonagem) == 0:
                break
            personagem = personagens[int(opcaoPersonagem) - 1]
            while True:
                limpaTela()
                print(f'{('ÍNDICE').ljust(6)} | {('NOME').ljust(40)} | {('PROFISSÃO').ljust(25)} | {('QNT').ljust(3)} | {('NÍVEL').ljust(5)} | {('RARIDADE').ljust(10)} | {'ID TRABALHO'}')
                estoque = EstoqueDaoSqlite(personagem).pegaEstoque()
                for trabalhoEstoque in estoque:
                    print(f'{str(estoque.index(trabalhoEstoque) + 1).ljust(6)} | {trabalhoEstoque}')
                print(f'{('0').ljust(6)} | Sair')
                opcaoTrabalho = input(f'opção trabalho ')
                if int(opcaoTrabalho) == 0:
                    break
                trabalho = estoque[int(opcaoTrabalho) - 1]
                quantidadeTrabalho = input(f'Quantidade trabalho: ')
                if tamanhoIgualZero(quantidadeTrabalho):
                    quantidadeTrabalho = trabalho.pegaQuantidade()
                trabalho.setQuantidade(int(quantidadeTrabalho))
                trabalhoEstoqueDao = EstoqueDaoSqlite(personagem)
                if trabalhoEstoqueDao.modificaTrabalhoEstoque(trabalho):
                    print(f'Trabalho {trabalho.pegaNome()} modificado no estoque com sucesso!')
                    continue
                logger = logging.getLogger('estoqueDao')
                logger.error(f'Erro ao modificar trabalho no estoque: {trabalhoEstoqueDao.pegaErro()}')
                print(f'Erro ao modificar trabalho no estoque: {trabalhoEstoqueDao.pegaErro()}')

    def removeTrabalhoEstoque(self):
        while True:
            limpaTela()
            print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
            personagens = PersonagemDaoSqlite().pegaPersonagens()
            for personagem in personagens:
                print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
            opcaoPersonagem = input(f'Opção:')
            if int(opcaoPersonagem) == 0:
                break
            personagem = personagens[int(opcaoPersonagem) - 1]
            while True:
                limpaTela()
                print(f'{('ÍNDICE').ljust(6)} | {('NOME').ljust(40)} | {('PROFISSÃO').ljust(25)} | {('QNT').ljust(3)} | {('NÍVEL').ljust(5)} | {('RARIDADE').ljust(10)} | {'ID TRABALHO'}')
                estoque = EstoqueDaoSqlite(personagem).pegaEstoque()
                for trabalhoEstoque in estoque:
                    print(f'{str(estoque.index(trabalhoEstoque) + 1).ljust(6)} | {trabalhoEstoque}')
                print(f'{('0').ljust(6)} | Sair')
                opcaoTrabalho = input(f'opção trabalho ')
                if int(opcaoTrabalho) == 0:
                    break
                trabalho = estoque[int(opcaoTrabalho) - 1]
                trabalhoEstoqueDao = EstoqueDaoSqlite(personagem)
                if trabalhoEstoqueDao.removeTrabalhoEstoque(trabalho):
                    print(f'Trabalho {trabalho.pegaNome()} removido do estoque com sucesso!')
                    continue
                logger = logging.getLogger('estoqueDao')
                logger.error(f'Erro ao remover trabalho do estoque: {trabalhoEstoqueDao.pegaErro()}')
                print(f'Erro ao remover trabalho do estoque: {trabalhoEstoqueDao.pegaErro()}')

    def pegaTodosTrabalhosEstoque(self):
        limpaTela()
        for trabalhoEstoque in EstoqueDaoSqlite().pegaTodosTrabalhosEstoque():
            print(trabalhoEstoque)
        input(f'Clique para continuar...')

    def pegaTodosTrabalhosVendidos(self):
        limpaTela()
        print(f'{'NOME'.ljust(113)} | {'DATA'.ljust(10)} | {'ID TRABALHO'.ljust(36)} | {'VALOR'.ljust(5)} | UND')
        for trabalhoVendido in VendaDaoSqlite().pegaTodosTrabalhosVendidos():
            print(trabalhoVendido)
        input(f'Clique para continuar...')

    def teste(self):
        while True:
            limpaTela()
            print(f'MENU')
            print(f'1 - Adiciona trabalho')
            print(f'2 - Adiciona trabalho produção')
            print(f'3 - Modifica personagem')
            print(f'4 - Modifica profissao')
            print(f'5 - Remove trabalho')
            print(f'6 - Modifica trabalho produção')
            print(f'7 - Remove trabalho produção')
            print(f'8 - Mostra vendas')
            print(f'9 - Modifica trabalho')
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
                    continue
                if int(opcaoMenu) == 17:
                    # modifica trabalho vendido
                    continue
                if int(opcaoMenu) == 18:
                    # remove trabalho vendido
                    # self.removeTrabalhoVendidos()
                    continue
                if int(opcaoMenu) == 19:
                    # pega todos trabalhos vendidos
                    self.pegaTodosTrabalhosVendidos()
                    continue
            except Exception as erro:
                logger = logging.getLogger(__name__)
                logger.exception(erro)
                print(f'Opção inválida! Erro: {erro}')
                input(f'Clique para continuar...')

if __name__=='__main__':
    Aplicacao().preparaPersonagem()
    # print(self.imagem.reconheceTextoNomePersonagem(self.imagem.abreImagem('tests/imagemTeste/testeMenuTrabalhoProducao.png'), 1))