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

class Aplicacao:
    def __init__(self) -> None:
        logging.basicConfig(level = logging.DEBUG, filename = 'logs/aplicacao.log', encoding='utf-8', format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt = '%d/%m/%Y %I:%M:%S %p')
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
        self.__listaPersonagemJaVerificado: list[Personagem] = []
        self.__listaPersonagemAtivo: list[Personagem] = []
        self.__listaProfissoesNecessarias: list[Profissao] = []
        self.__personagemEmUso: Personagem = None
        self.__repositorioTrabalho = RepositorioTrabalho()
        self.__repositorioPersonagem = RepositorioPersonagem()

    def personagemEmUso(self, personagem):
        self.__personagemEmUso = personagem

    def defineListaPersonagemMesmoEmail(self) -> list[Personagem]:
        listaPersonagens: list[Personagem] = []
        personagens: list[Personagem] = self.pegaPersonagens()
        for personagem in personagens:
            if textoEhIgual(personagem.email, self.__personagemEmUso.email):
                listaPersonagens.append(personagem)
        return listaPersonagens

    def modificaAtributoUso(self) -> None: 
        listaPersonagemMesmoEmail: list[Personagem] = self.defineListaPersonagemMesmoEmail()
        personagens: list[Personagem] = self.pegaPersonagens()
        for personagem in personagens:
            if self.verificaPersonagemMesmoEmail(listaPersonagemMesmoEmail, personagem) and personagem.uso:
                personagem.alternaUso()
                self.modificaPersonagem(personagem)

    def verificaPersonagemMesmoEmail(self, listaPersonagemMesmoEmail: list[Personagem], personagem: Personagem) -> bool:
        for personagemMesmoEmail in listaPersonagemMesmoEmail:
            if textoEhIgual(personagem.id, personagemMesmoEmail.id) and not personagem.uso:
                personagem.alternaUso()
                self.modificaPersonagem(personagem)
                return False
        return True

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

    def defineListaPersonagensAtivos(self) -> None:
        '''
        Esta função é responsável por preencher a lista de personagens ativos, recuperando os dados do banco
        '''
        print(f'Definindo lista de personagem ativo')
        personagens: list[Personagem] = self.pegaPersonagens()
        self.__listaPersonagemAtivo.clear()
        for personagem in personagens:
            if personagem.ehAtivo():
                self.__listaPersonagemAtivo.append(personagem)

    def inicializaChavesPersonagem(self):
        self.__autoProducaoTrabalho: bool = self.__personagemEmUso.autoProducao
        self.__unicaConexao: bool = True
        self.__espacoBolsa: bool = True
        self.__confirmacao: bool = True
        self.__profissaoModificada: bool = False

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

    def retornaMenu(self) -> int | None:
        print(f'Reconhecendo menu.')
        textoMenu = self._imagem.retornaTextoSair()
        if texto1PertenceTexto2('sair', textoMenu):
            print(f'Menu jogar...')
            return MENU_JOGAR
        textoMenu = self._imagem.retornaTextoMenuReconhecido()
        if textoMenu is None:
            print(f'Menu não reconhecido...')
            self.verificaErro()
            return MENU_DESCONHECIDO
        if texto1PertenceTexto2('interagir',textoMenu):
            print(f'Menu principal...')
            return MENU_PRINCIPAL
        if texto1PertenceTexto2('conquistas',textoMenu):
            print(f'Menu personagem...')
            return MENU_PERSONAGEM
        if texto1PertenceTexto2('ofertadiaria',textoMenu):
            print(f'Menu oferta diária...')
            return MENU_OFERTA_DIARIA
        if texto1PertenceTexto2('Loja Milagrosa',textoMenu):
            print(f'Menu loja milagrosa...')
            return MENU_LOJA_MILAGROSA
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
                if texto1PertenceTexto2('fechar',textoMenu):
                    print(f'Menu produzir...')
                    return MENU_PROFISSOES
                if texto1PertenceTexto2('voltar',textoMenu):
                    print(f'Menu trabalhos diponíveis...')
                    return MENU_TRABALHOS_DISPONIVEIS
        if texto1PertenceTexto2('noticias',textoMenu):
            print(f'Menu notícias...')
            return MENU_NOTICIAS
        if self._imagem.verificaMenuReferencia():
            print(f'Menu tela inicial...')
            return MENU_INICIAL
        if texto1PertenceTexto2('parâmetros',textoMenu):
            if texto1PertenceTexto2('requisitos',textoMenu):
                print(f'Menu atributo do trabalho...')
                return MENU_TRABALHOS_ATRIBUTOS
            print(f'Menu licenças...')
            return MENU_LICENSAS
        if texto1PertenceTexto2('Recompensa',textoMenu):
            print(f'Menu trabalho específico...')
            return MENU_TRABALHO_ESPECIFICO
        if texto1PertenceTexto2('recompensasdiarias',textoMenu):
            print(f'Menu recompensas diárias...')
            return MENU_RECOMPENSAS_DIARIAS
        if texto1PertenceTexto2('meu',textoMenu):
            print(f'Menu meu perfil...')
            return MENU_MEU_PERFIL           
        if texto1PertenceTexto2('Bolsa',textoMenu):
            print(f'Menu bolsa...')
            return MENU_BOLSA
        clickMouseEsquerdo(1,35,35)
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
    
    def pegaTrabalhosRarosVendidos(self, personagem: Personagem = None) -> list[TrabalhoVendido]:
        personagem = self.__personagemEmUso if personagem is None else personagem
        trabalhoVendidoDao = VendaDaoSqlite(personagem)
        trabalhosVendidos = trabalhoVendidoDao.pegaTrabalhosRarosVendidos()
        if trabalhosVendidos is None:
            self.__loggerVendaDao.error(f'Erro ao buscar trabalhos vendidos raros: {trabalhoVendidoDao.pegaErro()}')
            return []
        return trabalhosVendidos
    
    def insereTrabalhoVendido(self, trabalho: TrabalhoVendido, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        vendaDAO = VendaDaoSqlite(personagem)
        if vendaDAO.insereTrabalhoVendido(trabalho, modificaServidor):
            self.__loggerVendaDao.info(f'({trabalho}) inserido no banco com sucesso!')
            return True
        self.__loggerVendaDao.error(f'Erro ao inserir ({trabalho}) no banco: {vendaDAO.pegaErro()}')
        return False
    
    def modificaTrabalhoVendido(self, trabalho: TrabalhoVendido, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        vendaDAO = VendaDaoSqlite(personagem)
        if vendaDAO.modificaTrabalhoVendido(trabalho, modificaServidor):
            self.__loggerVendaDao.info(f'({trabalho}) modificado no banco com sucesso!')
            return True
        self.__loggerVendaDao.error(f'Erro ao modificar ({trabalho}) no banco: {vendaDAO.pegaErro()}')
        return False
    
    def removeTrabalhoVendido(self, trabalho: TrabalhoVendido, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        vendaDAO = VendaDaoSqlite(personagem)
        if vendaDAO.removeTrabalhoVendido(trabalho, modificaServidor):
            self.__loggerVendaDao.info(f'({trabalho}) removido do banco com sucesso!')
            return True
        self.__loggerVendaDao.error(f'Erro ao remover ({trabalho}) do banco: {vendaDAO.pegaErro()}')
        return False
    
    def pegaTrabalhosVendidos(self, personagem: Personagem = None) -> list[TrabalhoVendido]:
        personagem = self.__personagemEmUso if personagem is None else personagem
        trabalhoVendidoDao = VendaDaoSqlite(personagem)
        vendas = trabalhoVendidoDao.pegaTrabalhosVendidos()
        if vendas is None:
            self.__loggerVendaDao.error(f'Erro ao buscar trabalhos vendidos: {trabalhoVendidoDao.pegaErro()}')
            return []
        return vendas

    def retornaConteudoCorrespondencia(self) -> TrabalhoVendido | None:
        textoCarta = self._imagem.retornaTextoCorrespondenciaReconhecido()
        if variavelExiste(textoCarta):
            trabalhoFoiVendido = texto1PertenceTexto2('Item vendido', textoCarta)
            if trabalhoFoiVendido:
                print(f'Produto vendido')
                textoCarta = re.sub("Item vendido", "", textoCarta).strip()
                trabalho = TrabalhoVendido()
                trabalho.descricao = textoCarta
                trabalho.dataVenda = str(datetime.date.today())
                trabalho.setQuantidade(self.retornaQuantidadeTrabalhoVendido(textoCarta))
                trabalho.idTrabalho = self.retornaChaveIdTrabalho(textoCarta)
                trabalho.setValor(self.retornaValorTrabalhoVendido(textoCarta))
                self.insereTrabalhoVendido(trabalho)
                return trabalho
        return None

    def retornaChaveIdTrabalho(self, textoCarta):
        trabalhos = self.pegaTrabalhosBanco()
        for trabalho in trabalhos:
            if texto1PertenceTexto2(trabalho.nome, textoCarta):
                return trabalho.id
        return ''
    
    def pegaTrabalhosEstoque(self, personagem: Personagem = None) -> list[TrabalhoEstoque]:
        personagem = self.__personagemEmUso if personagem is None else personagem
        estoqueDao = EstoqueDaoSqlite(personagem)
        trabalhosEstoque = estoqueDao.pegaTrabalhosEstoque()
        if trabalhosEstoque is None:
            self.__loggerEstoqueDao.error(f'Erro ao buscar trabalhos em estoque: {estoqueDao.pegaErro()}')
            return []
        return trabalhosEstoque

    def atualizaQuantidadeTrabalhoEstoque(self, trabalho: TrabalhoVendido):
        estoque = self.pegaTrabalhosEstoque()
        for trabalhoEstoque in estoque:
            if textoEhIgual(trabalhoEstoque.trabalhoId, trabalho.idTrabalho):
                novaQuantidade = 0 if trabalhoEstoque.quantidade - trabalho.quantidade < 0 else trabalhoEstoque.quantidade - trabalho.quantidade
                trabalhoEstoque.quantidade = novaQuantidade
                if self.modificaTrabalhoEstoque(trabalhoEstoque):
                    self.__loggerEstoqueDao.debug(f'Quantidade de ({trabalhoEstoque}) atualizada para {novaQuantidade}.')
                return
        self.__loggerEstoqueDao.warning(f'({trabalho}) não encontrado no estoque.')

    def recuperaCorrespondencia(self, ):
        while self._imagem.existeCorrespondencia():
            clickEspecifico(1, 'enter')
            trabalhoVendido = self.retornaConteudoCorrespondencia()
            if variavelExiste(trabalhoVendido):
                self.atualizaQuantidadeTrabalhoEstoque(trabalhoVendido)
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
                    if not self.listaProfissoesFoiModificada():
                        self.__profissaoModificada = True
                    clickContinuo(3, 'up')
                    return nomeTrabalhoConcluido
                if ehErroEspacoBolsaInsuficiente(erro):
                    self.__espacoBolsa = False
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
    
    def insereTrabalhoProducao(self, trabalho: TrabalhoProducao, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        if variavelExiste(trabalho):
            personagem = self.__personagemEmUso if personagem is None else personagem
            trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
            if trabalhoProducaoDao.insereTrabalhoProducao(trabalho, modificaServidor):
                self.__loggerTrabalhoProducaoDao.info(f'({trabalho}) inserido no banco com sucesso!')
                return True
            self.__loggerTrabalhoProducaoDao.error(f'Erro ao inserir ({trabalho}) no banco: {trabalhoProducaoDao.pegaErro()}')
            return False
        
    def pegaTrabalhosProducaoParaProduzirProduzindo(self, personagem: Personagem = None) -> list[TrabalhoProducao]:
        personagem = self.__personagemEmUso if personagem is None else personagem
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
        trabalhosProducaoProduzirProduzindo = trabalhoProducaoDao.pegaTrabalhosProducaoParaProduzirProduzindo()
        if trabalhosProducaoProduzirProduzindo is None:
            self.__loggerTrabalhoProducaoDao.error(f'Erro ao bucar trabalhos para produção com estado para produzir ou produzindo: {trabalhoProducaoDao.pegaErro()}')
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
        personagem = self.__personagemEmUso if personagem is None else personagem
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
        if trabalhoProducaoDao.modificaTrabalhoProducao(trabalho, modificaServidor):
            self.__loggerTrabalhoProducaoDao.info(f'({trabalho}) modificado no banco com sucesso!')
            return True
        self.__loggerTrabalhoProducaoDao.error(f'Erro ao modificar ({trabalho}) no banco: {trabalhoProducaoDao.pegaErro()}')
        return False


    def modificaTrabalhoConcluidoListaProduzirProduzindo(self, trabalhoProducaoConcluido: TrabalhoProducao):
        trabalho = self.pegaTrabalhoPorId(trabalhoProducaoConcluido.idTrabalho)
        if trabalho is None or trabalho.nome is None:
            return
        if trabalhoEhProducaoRecursos(trabalho):
            trabalhoProducaoConcluido.recorrencia = True
        if trabalhoProducaoConcluido.recorrencia:
            print(f'Trabalho recorrente.')
            self.removeTrabalhoProducao(trabalhoProducaoConcluido)
            return
        print(f'Trabalho sem recorrencia.')
        self.modificaTrabalhoProducao(trabalhoProducaoConcluido)

    def insereListaProfissoes(self, personagem: Personagem =None) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        profissaoDao = ProfissaoDaoSqlite(personagem)
        if profissaoDao.insereListaProfissoes():
            return True
        return False

    def pegaProfissoes(self, personagem: Personagem = None) -> list[Personagem]:
        personagem = self.__personagemEmUso if personagem is None else personagem
        profissaoDao: ProfissaoDaoSqlite = ProfissaoDaoSqlite(personagem)
        profissoes: list[Profissao] = profissaoDao.pegaProfissoes()
        if profissoes is None:
            self.__loggerProfissaoDao.error(f'Erro ao buscar profissões: {profissaoDao.pegaErro()}')
            return []
        if tamanhoIgualZero(profissoes):
            self.__loggerProfissaoDao.warning(f'Erro ao buscar profissões ({self.__personagemEmUso}): lista de profissões vazia!')
        return profissoes
    
    def modificaProfissao(self, profissao: Profissao, personagem: Personagem = None, modificaServidor = True) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        profissaoDao = ProfissaoDaoSqlite(personagem)
        if profissaoDao.modificaProfissao(profissao, modificaServidor):
            self.__loggerProfissaoDao.info(f'({profissao}) modificado no banco com sucesso!')
            return True
        self.__loggerProfissaoDao.error(f'Erro ao modificar ({profissao}) no banco: {profissaoDao.pegaErro()}')
        return False

    def modificaExperienciaProfissao(self, trabalho: TrabalhoProducao) -> bool:
        profissoes: list[Profissao] = self.pegaProfissoes()
        trabalhoEncontado: Trabalho = self.pegaTrabalhoPorId(trabalho.idTrabalho)
        if trabalhoEncontado is None or trabalhoEncontado.nome is None:
            return False
        trabalhoEncontado.experiencia = trabalhoEncontado.experiencia * 1.5 if textoEhIgual(trabalho.tipo_licenca, CHAVE_LICENCA_INICIANTE) else trabalhoEncontado.experiencia
        for profissao in profissoes:
            if textoEhIgual(profissao.nome, trabalhoEncontado.profissao):
                experiencia = profissao.experiencia + trabalhoEncontado.experiencia
                profissao.setExperiencia(experiencia)
                if self.modificaProfissao(profissao):
                    print(f'Experiência de {profissao.nome} atualizada para {experiencia} com sucesso!')
                return True
        return False

    def retornaListaTrabalhoProduzido(self, trabalhoProducaoConcluido: TrabalhoProducao):
        '''
        Função que recebe um objeto TrabalhoProducao
        '''
        listaTrabalhoEstoqueConcluido = []
        trabalhoEstoque = None
        trabalho = self.pegaTrabalhoPorId(trabalhoProducaoConcluido.idTrabalho)
        if trabalho is None:
            return listaTrabalhoEstoqueConcluido
        if trabalho.nome is None:
            self.__loggerTrabalhoDao.warning(f'({trabalhoProducaoConcluido}) não foi encontrado na lista de trabalhos!')
            return listaTrabalhoEstoqueConcluido
        if trabalhoEhProducaoRecursos(trabalho):
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
                if self.modificaTrabalhoEstoque(trabalhoEstoque):
                    self.__loggerEstoqueDao.debug(f'Quantidade de ({trabalhoEstoque.nome}) atualizada para {novaQuantidade}.')
                    del listaTrabalhoEstoqueConcluidoModificado[listaTrabalhoEstoqueConcluido.index(trabalhoEstoqueConcluido)]
        return listaTrabalhoEstoqueConcluidoModificado, trabalhoEstoque

    def atualizaEstoquePersonagem(self, trabalhoEstoqueConcluido):
        listaTrabalhoEstoqueConcluido = self.retornaListaTrabalhoProduzido(trabalhoEstoqueConcluido)
        if tamanhoIgualZero(listaTrabalhoEstoqueConcluido):
            return
        estoque = self.pegaTrabalhosEstoque()
        if tamanhoIgualZero(estoque):
            for trabalhoEstoqueConcluido in listaTrabalhoEstoqueConcluido:
                self.insereTrabalhoEstoque(trabalhoEstoqueConcluido)
            return
        for trabalhoEstoque in estoque:
            listaTrabalhoEstoqueConcluido, trabalhoEstoque = self.modificaQuantidadeTrabalhoEstoque(listaTrabalhoEstoqueConcluido, trabalhoEstoque)
        if tamanhoIgualZero(listaTrabalhoEstoqueConcluido):
            return
        for trabalhoEstoqueConcluido in listaTrabalhoEstoqueConcluido:
            self.insereTrabalhoEstoque(trabalhoEstoqueConcluido)

    def retornaProfissaoTrabalhoProducaoConcluido(self, trabalhoProducaoConcluido: TrabalhoProducao) -> Profissao | None:
        profissoes: list[Profissao] = self.pegaProfissoes()
        for profissao in profissoes:
            if textoEhIgual(profissao.nome, trabalhoProducaoConcluido.profissao):
                return profissao
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

    def retornaListaPersonagemRecompensaRecebida(self, listaPersonagemPresenteRecuperado: list[str] = []) -> list[str]:
        nomePersonagemReconhecido: str = self._imagem.retornaTextoNomePersonagemReconhecido(posicao= 0)
        if nomePersonagemReconhecido is None:
            print(f'Erro ao reconhecer nome...')
            return listaPersonagemPresenteRecuperado
        print(f'{nomePersonagemReconhecido} foi adicionado a lista!')
        listaPersonagemPresenteRecuperado.append(nomePersonagemReconhecido)
        return listaPersonagemPresenteRecuperado

    def recuperaPresente(self) -> None:
        evento: int = 0
        print(f'Buscando recompensa diária...')
        while evento < 2:
            sleep(2)
            referenciaEncontrada: list[float] = self._imagem.verificaRecompensaDisponivel()
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

    def reconheceMenuRecompensa(self, menu: int) -> bool:
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

    def deslogaPersonagem(self) -> None:
        menu: int = self.retornaMenu()
        while not ehMenuJogar(menu):
            tentativas: int = 0
            erro: int = self.verificaErro()
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
                menu = self.retornaMenu()
                continue
            if ehMenuEscolhaPersonagem(menu):
                clickEspecifico(cliques= 1, teclaEspecifica= 'f1')
                menu = self.retornaMenu()
                continue
            clickMouseEsquerdo(clicks= 1, xTela= 2, yTela= 35)
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

    def recebeTodasRecompensas(self, menu: int) -> None:
        listaPersonagemPresenteRecuperado: list[str] = self.retornaListaPersonagemRecompensaRecebida()
        while True:
            if self.reconheceMenuRecompensa(menu= menu):
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
            menu: int = self.retornaMenu()

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
            for personagem in self.pegaPersonagens():
                if personagem.estado:
                    continue
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
            self.__unicaConexao = False

    def vaiParaMenuProduzir(self) -> bool:
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
            self.__unicaConexao = False
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

    def pegaTrabalhoPorNomeProfissaoRaridade(self, trabalho: Trabalho) -> Trabalho | None:
        trabalhoDao = TrabalhoDaoSqlite()
        trabalhoEncontrado = trabalhoDao.pegaTrabalhoPorNomeProfissaoRaridade(trabalho)
        if trabalhoEncontrado is None:
            self.__loggerTrabalhoDao.error(f'Erro ao buscar trabalho por nome, profissao e raridade ({trabalho.nome}, {trabalho.profissao}, {trabalho.raridade}) no banco: {trabalhoDao.pegaErro()}')
            return None
        if trabalhoEncontrado.nome is None:
            self.__loggerTrabalhoDao.warning(f'({trabalho.nome}) não foi encontrado no banco!')
            return None
        return trabalhoEncontrado

    def pegaTrabalhosPorProfissaoRaridade(self, trabalho: Trabalho) -> list[Trabalho]:
        trabalhoDao = TrabalhoDaoSqlite()
        trabalhos = trabalhoDao.pegaTrabalhosPorProfissaoRaridade(trabalho)
        if trabalhos is None:
            self.__loggerTrabalhoDao.error(f'Erro ao buscar trabalhos por profissão e raridade ({trabalho.profissao}, {trabalho.raridade}) no banco: {trabalhoDao.pegaErro()}')
            return []
        return trabalhos

    def pegaTrabalhoPorId(self, id: str) -> Trabalho | None:
        trabalhoDao = TrabalhoDaoSqlite()
        trabalhoEncontrado = trabalhoDao.pegaTrabalhoPorId(id)
        if trabalhoEncontrado is None:
            self.__loggerTrabalhoDao.error(f'Erro ao buscar trabalho por id ({id}) no banco: {trabalhoDao.pegaErro()}')
            return None
        return trabalhoEncontrado
            

    def retornaListaTrabalhosRarosVendidos(self):
        print(f'Definindo lista produtos raros vendidos...')
        trabalhosRarosVendidos = []
        trabalhosVendidos: list[TrabalhoVendido] = self.pegaTrabalhosVendidos()
        for trabalhoVendido in trabalhosVendidos:
            trabalhoEncontrado = self.pegaTrabalhoPorId(trabalhoVendido.trabalhoId)
            if trabalhoEncontrado is None:
                continue
            if trabalhoEncontrado.nome is None:
                self.__loggerTrabalhoDao.warning(f'({trabalhoVendido}) não foi encontrado na lista de trabalhos!')
                continue
            trabalhoEhRaroETrabalhoNaoEhProducaoDeRecursos = trabalhoEncontrado.ehRaro() and not trabalhoEhProducaoRecursos(trabalhoEncontrado)
            if trabalhoEhRaroETrabalhoNaoEhProducaoDeRecursos:
                trabalhosRarosVendidos.append(trabalhoVendido)
        return trabalhosRarosVendidos

    def verificaProdutosRarosMaisVendidos(self):
        listaTrabalhosRarosVendidos = self.retornaListaTrabalhosRarosVendidos()
        if tamanhoIgualZero(listaTrabalhosRarosVendidos):
            print(f'Lista de trabalhos raros vendidos está vazia!')
            return
        self.produzProdutoMaisVendido(listaTrabalhosRarosVendidos)

    def pegaTodosTrabalhosProducao(self) -> list[TrabalhoProducao]:
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite()
        trabalhosProducao = trabalhoProducaoDao.pegaTodosTrabalhosProducao()
        if trabalhosProducao is None:
            self.__loggerTrabalhoProducaoDao.error(f'Erro ao buscar todos os trabalhos para produção: {trabalhoProducaoDao.pegaErro()}')
            return []
        return trabalhosProducao


    def pegaTrabalhosProducao(self, personagem: Personagem = None) -> list[TrabalhoProducao]:
        personagem = self.__personagemEmUso if personagem is None else personagem
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
        trabalhosProducao = trabalhoProducaoDao.pegaTrabalhosProducao()
        if trabalhosProducao is None:
            self.__loggerTrabalhoProducaoDao.error(f'Erro ao buscar trabalhos para produção: {trabalhoProducaoDao.pegaErro()}')
            return []
        return trabalhosProducao

    def defineChaveListaProfissoesNecessarias(self) -> None:
        print(f'Verificando profissões necessárias...')
        self.limpaListaProfissoesNecessarias()
        self.defineListaProfissoesNecessarias()
        self.ordenaListaProfissoesNecessarias()
        self.mostraListaProfissoesNecessarias()

    def defineListaProfissoesNecessarias(self) -> None:
        profissoes: list[Profissao] = self.pegaProfissoes()
        trabalhosProducao: list[TrabalhoProducao] = self.pegaTrabalhosProducao()
        for profissao in profissoes:
            for trabalhoProducao in trabalhosProducao:
                chaveProfissaoEhIgualEEstadoEhParaProduzir: bool = textoEhIgual(profissao.nome, trabalhoProducao.profissao) and trabalhoProducao.ehParaProduzir()
                if chaveProfissaoEhIgualEEstadoEhParaProduzir:
                    self.insereItemListaProfissoesNecessarias(profissao)
                    break

    def ordenaListaProfissoesNecessarias(self) -> None:
        self.__listaProfissoesNecessarias = sorted(self.__listaProfissoesNecessarias, key=lambda profissao: profissao.prioridade, reverse= True)

    def mostraListaProfissoesNecessarias(self) -> None:
        print(f'{CHAVE_NOME.upper().ljust(22)} | {"EXP".ljust(6)} | {CHAVE_PRIORIDADE.upper().ljust(10)}')
        for profissaoNecessaria in self.__listaProfissoesNecessarias:
            nome = 'Indefinido' if profissaoNecessaria.nome is None else profissaoNecessaria.nome
            experiencia = 'Indefinido' if profissaoNecessaria.experiencia is None else str(profissaoNecessaria.experiencia)
            prioridade = 'Verdadeiro' if profissaoNecessaria.prioridade else 'Falso'
            print(f'{(nome).ljust(22)} | {experiencia.ljust(6)} | {prioridade.ljust(10)}')

    def insereItemListaProfissoesNecessarias(self, profissao: Profissao) -> None:
        self.__listaProfissoesNecessarias.append(profissao)

    def limpaListaProfissoesNecessarias(self) -> None:
        self.__listaProfissoesNecessarias.clear()

    def retornaContadorEspacosProducao(self, contadorEspacosProducao: int, nivel: int):
        contadorNivel: int = 0
        profissoes: list[Profissao] = self.pegaProfissoes()
        for profissao in profissoes:
            if profissao.pegaNivel() >= nivel:
                contadorNivel += 1
        print(f'Contador de profissões nível {nivel} ou superior: {contadorNivel}.')
        if contadorNivel > 0 and contadorNivel < 3:
            contadorEspacosProducao += 1
            return contadorEspacosProducao
        if contadorNivel >= 3:
            contadorEspacosProducao += 2
        return contadorEspacosProducao

    def retornaQuantidadeEspacosDeProducao(self) -> int:
        print(f'Define quantidade de espaços de produção...')
        quantidadeEspacosProducao: int = 2
        profissoes: list[Profissao] = self.pegaProfissoes()
        for profissao in profissoes:
            nivel: int = profissao.pegaNivel()
            if nivel >= 5:
                quantidadeEspacosProducao += 1
                break
        listaNiveis: list[int] = [10, 15, 20, 25]
        for nivel in listaNiveis:
            quantidadeEspacosProducao = self.retornaContadorEspacosProducao(quantidadeEspacosProducao, nivel)
        print(f'Espaços de produção disponíveis: {quantidadeEspacosProducao}.')
        return quantidadeEspacosProducao

    def verificaEspacoProducao(self):
        quantidadeEspacoProducao: int = self.retornaQuantidadeEspacosDeProducao()
        if self.__personagemEmUso.espacoProducao != quantidadeEspacoProducao:
            self.__personagemEmUso.setEspacoProducao(quantidadeEspacoProducao)
            self.modificaPersonagem()

    def retornaListaTrabalhosProducaoRaridadeEspecifica(self, dicionarioTrabalho: dict, raridade: str) -> list[TrabalhoProducao]:
        listaTrabalhosProducaoRaridadeEspecifica: list[TrabalhoProducao] = []
        trabalhosProducao: list[TrabalhoProducao] = self.pegaTrabalhosProducaoParaProduzirProduzindo()
        if trabalhosProducao is None:
            return listaTrabalhosProducaoRaridadeEspecifica
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

    def retornaFrameTelaTrabalhoEspecifico(self) -> str | None:
        clickEspecifico(1, 'down')
        clickEspecifico(1, 'enter')
        nomeTrabalhoReconhecido: str = self._imagem.retornaNomeConfirmacaoTrabalhoProducaoReconhecido(tipoTrabalho= 0)
        clickEspecifico(1, 'f1')
        clickEspecifico(1, 'up')
        return nomeTrabalhoReconhecido

    def confirmaNomeTrabalhoProducao(self, dicionarioTrabalho: dict, tipoTrabalho: int):
        print(f'Confirmando nome do trabalho...')
        dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = None
        if tipoTrabalho == 0:
            nomeTrabalhoReconhecido: str = self.retornaFrameTelaTrabalhoEspecifico()
        else:
            nomeTrabalhoReconhecido: str = self._imagem.retornaNomeConfirmacaoTrabalhoProducaoReconhecido(tipoTrabalho= tipoTrabalho)
        if nomeTrabalhoReconhecido is None:
            self.__loggerTrabalhoProducaoDao.info(f'Trabalho negado: Não reconhecido')
            return dicionarioTrabalho
        if CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA in dicionarioTrabalho:
            nomeTrabalhoReconhecido = nomeTrabalhoReconhecido[:28] if len(nomeTrabalhoReconhecido) >= 29 else nomeTrabalhoReconhecido
            listaTrabalhoProducaoPriorizada: list[TrabalhoProducao] = dicionarioTrabalho[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA]
            for trabalhoProducao in listaTrabalhoProducaoPriorizada:
                trabalhoEncontrado: Trabalho = self.pegaTrabalhoPorId(trabalhoProducao.idTrabalho)
                if trabalhoEncontrado is None:
                    continue
                nomeTrabalho = self.padronizaTexto(trabalhoEncontrado.nome)
                nomeProducaoTrabalho: str = self.padronizaTexto(trabalhoEncontrado.nomeProducao)
                if trabalhoEhProducaoRecursos(trabalhoEncontrado):
                    if texto1PertenceTexto2(nomeTrabalhoReconhecido, nomeProducaoTrabalho):
                        dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = trabalhoProducao
                        self.__loggerTrabalhoProducaoDao.info(f'Trabalho confirmado: {nomeTrabalhoReconhecido.ljust(30)} | {nomeProducaoTrabalho.ljust(30)}')
                        return dicionarioTrabalho
                    continue
                if textoEhIgual(nomeTrabalhoReconhecido, nomeTrabalho):
                    dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = trabalhoProducao
                    self.__loggerTrabalhoProducaoDao.info(f'Trabalho confirmado: {nomeTrabalhoReconhecido.ljust(30)} | {nomeTrabalho.ljust(30)}')
                    return dicionarioTrabalho
                if textoEhIgual(nomeTrabalhoReconhecido, nomeProducaoTrabalho):
                    dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = trabalhoProducao
                    self.__loggerTrabalhoProducaoDao.info(f'Trabalho confirmado: {nomeTrabalhoReconhecido.ljust(30)} | {nomeProducaoTrabalho.ljust(30)}')
                    return dicionarioTrabalho
        self.__loggerTrabalhoProducaoDao.info(f'Trabalho negado: {nomeTrabalhoReconhecido.ljust(30)}')
        return dicionarioTrabalho

    def padronizaTexto(self, texto: str) -> str:
        textoPadronizado: str = texto.replace('-','')
        textoPadronizado = textoPadronizado[:28] if len(textoPadronizado) >= 29 else textoPadronizado
        return textoPadronizado

    def incrementaChavePosicaoTrabalho(self, dicionarioTrabalho):
        dicionarioTrabalho[CHAVE_POSICAO] += 1
        return dicionarioTrabalho

    def reconheceTextoTrabalhoComumMelhorado(self, trabalho: dict, contadorParaBaixo: int):
        yinicialNome: int = (2 * 70) + 285
        if primeiraBusca(trabalho):
            clickEspecifico(cliques= 3, teclaEspecifica= 'down')
            return self._imagem.retornaNomeTrabalhoReconhecido(yinicialNome, 1)
        if contadorParaBaixo == 3:
            return self._imagem.retornaNomeTrabalhoReconhecido(yinicialNome, 1)
        if contadorParaBaixo == 4:
            yinicialNome = (3 * 70) + 285
            return self._imagem.retornaNomeTrabalhoReconhecido(yinicialNome, 1)
        if contadorParaBaixo > 4:
            return self._imagem.retornaNomeTrabalhoReconhecido(530, 1)

    def defineDicionarioTrabalhoComumMelhorado(self, dicionarioTrabalho: dict) -> dict:
        nomeTrabalhoReconhecidoAux: str = ''
        nomeTrabalhoReconhecido: str = ''
        print(f'Buscando trabalho {dicionarioTrabalho[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA][0].raridade}.')
        contadorParaBaixo: int = 0
        if not primeiraBusca(dicionarioTrabalho):
            contadorParaBaixo = dicionarioTrabalho[CHAVE_POSICAO]
            clickEspecifico(contadorParaBaixo, 'down')
        while not chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
            erro = self.verificaErro()
            if erroEncontrado(erro):
                self.__confirmacao = False
                break
            nomeTrabalhoReconhecido = self.reconheceTextoTrabalhoComumMelhorado(dicionarioTrabalho, contadorParaBaixo)
            contadorParaBaixo = 3 if primeiraBusca(dicionarioTrabalho) else contadorParaBaixo
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
                        tipoTrabalho: int = 1 if trabalhoEhProducaoRecursos(dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO]) else 0
                        dicionarioTrabalho = self.confirmaNomeTrabalhoProducao(dicionarioTrabalho, tipoTrabalho)
                        if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
                            break
                        clickEspecifico(1, 'f1')
                else:
                    clickEspecifico(1, 'down')
                    dicionarioTrabalho[CHAVE_POSICAO] = contadorParaBaixo
                    contadorParaBaixo += 1
                continue
            if not primeiraBusca(dicionarioTrabalho) and dicionarioTrabalho[CHAVE_POSICAO] > 5:
                print(f'Trabalho {dicionarioTrabalho[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA][0].raridade} não reconhecido!')
                break
            clickEspecifico(1, 'down')
            dicionarioTrabalho[CHAVE_POSICAO] = contadorParaBaixo
            contadorParaBaixo += 1
        return dicionarioTrabalho

    def defineCloneTrabalhoProducao(self, trabalhoProducaoEncontrado: TrabalhoProducao) -> TrabalhoProducao:
        cloneTrabalhoProducao = TrabalhoProducao()
        cloneTrabalhoProducao.dicionarioParaObjeto(trabalhoProducaoEncontrado.__dict__)
        cloneTrabalhoProducao.id = str(uuid.uuid4())
        cloneTrabalhoProducao.idTrabalho = trabalhoProducaoEncontrado.idTrabalho
        cloneTrabalhoProducao.recorrencia = False
        self.__loggerTrabalhoProducaoDao.info(f'({trabalhoProducaoEncontrado.id}|{cloneTrabalhoProducao.idTrabalho}|{cloneTrabalhoProducao.nome}|{cloneTrabalhoProducao.nomeProducao}|{cloneTrabalhoProducao.experiencia}|{cloneTrabalhoProducao.nivel}|{cloneTrabalhoProducao.profissao}|{cloneTrabalhoProducao.raridade}|{cloneTrabalhoProducao.trabalhoNecessario}|{cloneTrabalhoProducao.recorrencia}|{cloneTrabalhoProducao.tipo_licenca}|{cloneTrabalhoProducao.estado}) foi clonado')
        return cloneTrabalhoProducao
    

    def clonaTrabalhoProducaoEncontrado(self, trabalhoProducaoEncontrado: TrabalhoProducao) -> None:
        print(f'Recorrencia está ligada.')
        cloneTrabalhoProducaoEncontrado: TrabalhoProducao = self.defineCloneTrabalhoProducao(trabalhoProducaoEncontrado)
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

    def defineTrabalhoRecurso(self, trabalho: Trabalho) -> TrabalhoRecurso:
        print(f'Define quantidade de recursos.')
        nivelTrabalhoProducao = trabalho.nivel
        nivelRecurso = 1
        recursoTerciario = 0
        chaveProfissao = limpaRuidoTexto(trabalho.profissao)
        if textoEhIgual(trabalho.profissao, CHAVE_PROFISSAO_ARMA_DE_LONGO_ALCANCE):
            recursoTerciario = 1
        if nivelTrabalhoProducao <= 14:
            if nivelTrabalhoProducao == 10:
                recursoTerciario += 2
            elif nivelTrabalhoProducao == 12:
                recursoTerciario += 4
            elif nivelTrabalhoProducao == 14:
                recursoTerciario += 6
            nomeRecursoPrimario, nomeRecursoSecundario, nomeRecursoTerciario = self.retornaNomesRecursos(chaveProfissao, nivelRecurso)
            return TrabalhoRecurso(trabalho.profissao, trabalho.nivel, nomeRecursoTerciario, nomeRecursoSecundario, nomeRecursoPrimario, recursoTerciario)
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
        nomeRecursoPrimario, nomeRecursoSecundario, nomeRecursoTerciario = self.retornaNomesRecursos(chaveProfissao, nivelRecurso)
        return TrabalhoRecurso(trabalho.profissao, trabalho.nivel, nomeRecursoTerciario, nomeRecursoSecundario, nomeRecursoPrimario, recursoTerciario)

    def removeTrabalhoProducaoEstoque(self, trabalhoProducao: TrabalhoProducao) -> None:
        trabalho: Trabalho = self.pegaTrabalhoPorId(trabalhoProducao.idTrabalho)
        if trabalho is None or trabalho.nome is None:
            return
        if trabalho.ehComum():
            if trabalhoEhProducaoRecursos(trabalho):
                return self.atualizaRecursosEstoqueTrabalhoRecursoProduzindo(trabalhoProducao)
            return self.atualizaRecursosEstoqueTrabalhoComumProduzindo(trabalhoProducao)
        if trabalho.ehMelhorado() or trabalho.ehRaro():
            if trabalhoEhProducaoRecursos(trabalho):
                return
            return self.atualizaResursosEstoqueTrabalhoMelhoradoRaroProduzindo(trabalho)

    def atualizaResursosEstoqueTrabalhoMelhoradoRaroProduzindo(self, trabalho: Trabalho) -> None:
        listaIdsTrabalhosNecessarios: list[str] = trabalho.trabalhoNecessario.split(',')
        for idTrabalhoNecessario in listaIdsTrabalhosNecessarios:
            trabalhoEncontrado: TrabalhoEstoque = self.pegaTrabalhoEstoquePorIdTrabalho(id= idTrabalhoNecessario)
            if trabalhoEncontrado is None:
                continue
            if trabalhoEncontrado.trabalhoId == idTrabalhoNecessario:
                trabalhoEncontrado.setQuantidade(trabalhoEncontrado.quantidade - 1)
                if self.modificaTrabalhoEstoque(trabalhoEncontrado):
                    print(f'Quantidade do trabalho ({trabalhoEncontrado.trabalhoId}) atualizada para {trabalhoEncontrado.quantidade}.')
                return
            self.__loggerEstoqueDao.warning(f'({idTrabalhoNecessario}) não encontrado no estoque!')

    def atualizaRecursosEstoqueTrabalhoRecursoProduzindo(self, trabalhoProducao: TrabalhoProducao) -> None:
        trabalho: Trabalho = self.pegaTrabalhoPorId(trabalhoProducao.idTrabalho)
        if trabalho is None or trabalho.nome is None:
            return
        print(f'Trabalho é recurso de produção!')
        print(f'Nome recurso produzido: {trabalho.nome}')
        dicionarioRecurso = {
            CHAVE_NOME:trabalho.nome,
            CHAVE_PROFISSAO:trabalho.profissao,
            CHAVE_NIVEL:trabalho.nivel}
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
        for trabalhoEstoque in self.pegaTrabalhosEstoque():
            for recursoBuscado in listaNomeRecursoBuscado:
                if textoEhIgual(trabalhoEstoque.nome, recursoBuscado[0]):
                    novaQuantidade = trabalhoEstoque.quantidade - recursoBuscado[1]
                    print(f'Quantidade de {trabalhoEstoque.nome} atualizada de {trabalhoEstoque.quantidade} para {novaQuantidade}.')
                    trabalhoEstoque.quantidade = novaQuantidade
                    if self.modificaTrabalhoEstoque(trabalhoEstoque):
                        print(f'Quantidade do trabalho ({trabalhoEstoque.nome}) atualizada para {novaQuantidade}.')
            if textoEhIgual(trabalhoEstoque.nome, trabalhoProducao.tipo_licenca):
                novaQuantidade = trabalhoEstoque.quantidade - 1
                print(f'Quantidade de {trabalhoEstoque.nome} atualizada de {trabalhoEstoque.quantidade} para {novaQuantidade}.')
                trabalhoEstoque.quantidade = novaQuantidade
                if self.modificaTrabalhoEstoque(trabalhoEstoque):
                    print(f'Quantidade do trabalho ({trabalhoEstoque.nome}) atualizada para {novaQuantidade}.')

    def atualizaRecursosEstoqueTrabalhoComumProduzindo(self, trabalhoProducao: TrabalhoProducao) -> None:
        trabalho: Trabalho = self.pegaTrabalhoPorId(trabalhoProducao.idTrabalho)
        if trabalho is None or trabalho.nome is None:
            return
        trabalhoRecurso: TrabalhoRecurso = self.defineTrabalhoRecurso(trabalho)
        for trabalhoEstoque in self.pegaTrabalhosEstoque():
            if textoEhIgual(trabalhoEstoque.nome, trabalhoRecurso.pegaPrimario()):
                trabalhoEstoque.setQuantidade(trabalhoEstoque.quantidade - trabalhoRecurso.pegaQuantidadePrimario())
                if self.modificaTrabalhoEstoque(trabalhoEstoque):
                    print(f'Quantidade do trabalho ({trabalhoEstoque}) atualizada.')
                continue
            if textoEhIgual(trabalhoEstoque.nome, trabalhoRecurso.pegaSecundario()):
                trabalhoEstoque.setQuantidade(trabalhoEstoque.quantidade - trabalhoRecurso.pegaQuantidadeSecundario())
                if self.modificaTrabalhoEstoque(trabalhoEstoque):
                    print(f'Quantidade do trabalho ({trabalhoEstoque}) atualizada.')
                continue
            if textoEhIgual(trabalhoEstoque.nome, trabalhoRecurso.pegaTerciario()):
                trabalhoEstoque.setQuantidade(trabalhoEstoque.quantidade - trabalhoRecurso.pegaQuantidadeTerciario())
                if self.modificaTrabalhoEstoque(trabalhoEstoque):
                    print(f'Quantidade do trabalho ({trabalhoEstoque}) atualizada.')
                continue
            if textoEhIgual(trabalhoEstoque.nome, trabalhoProducao.tipo_licenca):
                trabalhoEstoque.setQuantidade(trabalhoEstoque.quantidade - 1)
                if self.modificaTrabalhoEstoque(trabalhoEstoque):
                    print(f'Quantidade do trabalho ({trabalhoEstoque}) atualizada.')
            
    def iniciaProcessoDeProducao(self, dicionarioTrabalho: dict) -> dict:
        primeiraBusca: bool = True
        trabalhoProducaoEncontrado: TrabalhoProducao = dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO]
        while True:
            print(f'Tratando possíveis erros...')
            tentativas: int = 1
            erro: int = self.verificaErro()
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
                        self.__unicaConexao = False
                        erro = self.verificaErro()
                        continue
                    if ehErroConectando(erro):
                        if tentativas > 10:
                            clickEspecifico(1, 'enter')
                            tentativas = 0
                        tentativas+=1
                erro = self.verificaErro()
            menu = self.retornaMenu()
            if menuTrabalhosAtuaisReconhecido(menu):
                if trabalhoProducaoEncontrado.ehRecorrente():
                    self.removeTrabalhoProducaoEstoque(trabalhoProducaoEncontrado)
                    self.clonaTrabalhoProducaoEncontrado(trabalhoProducaoEncontrado)
                    self.verificaNovamente = True
                    break
                self.modificaTrabalhoProducao(trabalhoProducaoEncontrado)
                self.removeTrabalhoProducaoEstoque(trabalhoProducaoEncontrado)
                clickContinuo(12,'up')
                self.verificaNovamente = True
                break
            if menuTrabalhoEspecificoReconhecido(menu):
                if primeiraBusca:
                    print(f'Entra menu licença.')
                    clickEspecifico(1, 'up')
                    clickEspecifico(1, 'enter')
                    continue
                print(f'Clica f2.')
                clickEspecifico(1, 'f2')
                continue
            if menuLicencasReconhecido(menu):
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
                                            self.modificaPersonagem()
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
                                    self.__unicaConexao = False
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
                        self.modificaPersonagem()
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

    
    def existeEspacoProducao(self) -> bool:
        espacoProducao: int = self.__personagemEmUso.espacoProducao
        trabalhosProducao: list[TrabalhoProducao] = self.pegaTrabalhosProducao()
        for trabalho in trabalhosProducao:
            if trabalho.ehProduzindo():
                espacoProducao -= 1
                if espacoProducao <= 0:
                    print(f'{espacoProducao} espaços de produção.')
                    return False
        print(f'{espacoProducao} espaços de produção.')
        return True
    
    def percorreListaProfissoesNecessarias(self) -> bool:
        dicionarioTrabalho: dict = {CHAVE_TRABALHO_PRODUCAO_ENCONTRADO: None}
        for profissaoNecessaria in self.__listaProfissoesNecessarias:
            if not self.__confirmacao or not self.__unicaConexao:
                return False
            if not self.existeEspacoProducao():
                return True
            dicionarioTrabalho[CHAVE_POSICAO] = -1
            self.verificaProfissaoNecessaria(dicionarioTrabalho, profissaoNecessaria)

    def verificaProfissaoNecessaria(self, dicionarioTrabalho: dict, profissaoNecessaria: Profissao) -> None:
        while self.__confirmacao:
            self.verificaNovamente: bool = False
            self.vaiParaMenuProduzir()
            if not self.__confirmacao or not self.__unicaConexao or not self.existeEspacoProducao():
                break
            if self.listaProfissoesFoiModificada():
                self.verificaEspacoProducao()
            posicao = self.retornaPosicaoProfissaoNecessaria(profissaoNecessaria)
            if posicao == 0:
                break
            entraProfissaoEspecifica(posicao)
            print(f'Verificando profissão: {profissaoNecessaria.nome}')
            dicionarioTrabalho[CHAVE_PROFISSAO] = profissaoNecessaria.nome
            dicionarioTrabalho = self.veficaTrabalhosProducaoListaDesejos(dicionarioTrabalho)
            if self.__confirmacao:
                if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
                    dicionarioTrabalho = self.iniciaProcessoDeProducao(dicionarioTrabalho)
                elif ehMenuTrabalhosDisponiveis(self.retornaMenu()):
                    saiProfissaoVerificada(dicionarioTrabalho)
                if self.__unicaConexao and self.__espacoBolsa:
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

    def retornaPosicaoProfissaoNecessaria(self, profissaoNecessaria: Profissao) -> int:
        profissoes: list[Profissao] = self.pegaProfissoes()
        for profissao in profissoes:
            if profissao.nome == profissaoNecessaria.nome:
                posicao = profissoes.index(profissao) + 1
                self.__loggerProfissaoDao.info(f'({profissaoNecessaria.nome}) encontrada na posição {posicao}')
                return posicao
        self.__loggerProfissaoDao.warning(f'Posição de ({profissaoNecessaria.nome}) não encontrada.')
        return 0

    def iniciaBuscaTrabalho(self) -> None:
        self.defineChaveListaProfissoesNecessarias()
        if self.percorreListaProfissoesNecessarias() and self.listaProfissoesFoiModificada():
            self.verificaEspacoProducao()

    def listaProfissoesFoiModificada(self) -> bool:
        return self.__profissaoModificada

    def veficaTrabalhosProducaoListaDesejos(self, dicionarioTrabalho: dict) -> dict:
        listaDeListasTrabalhosProducao: list[list[TrabalhoProducao]] = self.retornaListaDeListasTrabalhosProducao(dicionarioTrabalho)
        for listaTrabalhosProducao in listaDeListasTrabalhosProducao:
            dicionarioTrabalho[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA] = listaTrabalhosProducao
            for trabalhoProducaoPriorizado in listaTrabalhosProducao:
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
                            trabalhoEncontrado = self.pegaTrabalhoPorId(dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO].idTrabalho)
                            if trabalhoEncontrado is None:
                                continue
                            if trabalhoEncontrado.nome is None:
                                self.__loggerTrabalhoDao.warning(f'({dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO]}) não foi encontrado na lista de trabalhos!')
                                continue
                            tipoTrabalho = 1 if trabalhoEhProducaoRecursos(trabalhoEncontrado) else 0
                            dicionarioTrabalho = self.confirmaNomeTrabalhoProducao(dicionarioTrabalho, tipoTrabalho)
                            if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not self.__confirmacao:
                                return dicionarioTrabalho
                            clickEspecifico(1,'f1')
                            clickContinuo(dicionarioTrabalho[CHAVE_POSICAO] + 1, 'up')
                            dicionarioTrabalho = self.incrementaChavePosicaoTrabalho(dicionarioTrabalho)
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

    def retornaListaDeListasTrabalhosProducao(self, dicionarioTrabalho: dict) -> list[list[TrabalhoProducao]]:
        listaDeListaTrabalhos: list[list[TrabalhoProducao]] = []
        for raridade in LISTA_RARIDADES:
            listaTrabalhosProducao: list = self.retornaListaTrabalhosProducaoRaridadeEspecifica(dicionarioTrabalho, raridade)
            if tamanhoIgualZero(listaTrabalhosProducao):
                continue
            listaDeListaTrabalhos.append(listaTrabalhosProducao)
        return listaDeListaTrabalhos

    def retiraPersonagemJaVerificadoListaAtivo(self) -> None:
        """
        Esta função é responsável por redefinir a lista de personagens ativos, verificando a lista de personagens já verificados
        """        
        self.defineListaPersonagensAtivos()
        novaListaPersonagensAtivos: list[Personagem] = []
        print(f'{CHAVE_NOME.ljust(17).upper()} | {CHAVE_ESPACO_BOLSA.ljust(11).upper()} | {CHAVE_ESTADO.ljust(10).upper()} | {CHAVE_USO.ljust(10).upper()} | {CHAVE_AUTO_PRODUCAO.ljust(10).upper()}')
        for personagemAtivo in self.__listaPersonagemAtivo:
            for personagemRemovido in self.__listaPersonagemJaVerificado:
                if textoEhIgual(personagemAtivo.nome, personagemRemovido.nome):
                    break
            else:
                estado = 'Verdadeiro' if personagemAtivo.estado else 'Falso'
                uso = 'Verdadeiro' if personagemAtivo.uso else 'Falso'
                autoProducao = 'Verdadeiro' if personagemAtivo.autoProducao else 'Falso'
                print(f'{(personagemAtivo.nome).ljust(17)} | {str(personagemAtivo.espacoProducao).ljust(11)} | {estado.ljust(10)} | {uso.ljust(10)} | {autoProducao.ljust(10)}')
                novaListaPersonagensAtivos.append(personagemAtivo)
        self.__listaPersonagemAtivo = novaListaPersonagensAtivos

    def entraContaPersonagem(self) -> bool:
        print(f'Tentando logar conta personagem...')
        preencheCamposLogin(email= self.__listaPersonagemAtivo[0].email, senha= self.__listaPersonagemAtivo[0].senha)
        tentativas: int = 1
        erro: int = self.verificaErro()
        while erroEncontrado(erro):
            if ehErroConectando(erro) or ehErroRestauraConexao(erro):
                if tentativas>10:
                    clickEspecifico(cliques= 1, teclaEspecifica= 'enter')
                    tentativas = 1
                tentativas += 1
                erro = self.verificaErro()
                continue
            if ehErroUsuarioOuSenhaInvalida(erro= erro):
                return False
            print('Erro ao tentar logar...')
            erro = self.verificaErro()
        print(f'Login efetuado com sucesso!')
        return True

    def configuraEntraPersonagem(self) -> bool:
        self.vaiParaMenuJogar()
        return self.entraContaPersonagem()


    def vaiParaMenuJogar(self) -> None:
        menu: int = self.retornaMenu()
        while not ehMenuJogar(menu):
            self.verificaErroEncontrado()
            if ehMenuNoticias(menu) or ehMenuEscolhaPersonagem(menu):
                clickEspecifico(1, 'f1')
                menu = self.retornaMenu()
                continue
            if ehMenuInicial(menu):
                encerraSecao()
                menu = self.retornaMenu()
                continue
            clickMouseEsquerdo(clicks= 1, xTela= 2, yTela= 35)
            menu = self.retornaMenu()

    def verificaErroEncontrado(self) -> None:
        tentativas: int = 1
        erro: int = self.verificaErro()
        while erroEncontrado(erro):
            if ehErroConectando(erro):
                if tentativas > 10:
                    clickEspecifico(2, 'enter')
                    tentativas = 0
                tentativas += 1
            erro = self.verificaErro()

    def entraPersonagemAtivo(self) -> None:
        menu: int = self.retornaMenu()
        if ehMenuDesconhecido(menu): 
            clickMouseEsquerdo(clicks= 1, xTela= 2, yTela= 35)
            return
        if ehMenuJogar(menu= menu):
            print(f'Buscando personagem ativo...')
            clickEspecifico(cliques= 1, teclaEspecifica= 'enter')
            sleep(1)
            tentativas: int = 1
            erro: int = self.verificaErro()
            while erroEncontrado(erro= erro):
                if ehErroConectando(erro= erro):
                    if tentativas > 10:
                        clickEspecifico(cliques= 2, teclaEspecifica= 'enter')
                        tentativas = 0
                    tentativas += 1
                erro = self.verificaErro()
            clickEspecifico(cliques= 1, teclaEspecifica= 'f2')
            clickContinuo(cliques= 10, teclaEspecifica= 'left')   
            contadorPersonagem: int = 0
            personagemReconhecido: str = self._imagem.retornaTextoNomePersonagemReconhecido(posicao= 1)
            while variavelExiste(variavel= personagemReconhecido) and contadorPersonagem < 13:
                self.confirmaNomePersonagem(personagemReconhecido= personagemReconhecido)
                if variavelExiste(variavel= self.__personagemEmUso):
                    clickEspecifico(cliques= 1, teclaEspecifica= 'f2')
                    sleep(1)
                    print(f'Personagem ({self.__personagemEmUso.nome}) encontrado.')
                    tentativas: int = 1
                    erro: int = self.verificaErro()
                    while erroEncontrado(erro= erro):
                        if ehErroOutraConexao(erro= erro):
                            self.__unicaConexao = False
                            contadorPersonagem = 14
                            return
                        if ehErroConectando(erro= erro):
                            if tentativas > 10:
                                clickEspecifico(cliques= 2, teclaEspecifica= 'enter')
                                tentativas = 0
                            tentativas += 1
                        erro = self.verificaErro()
                        continue
                    print(f'Login efetuado com sucesso!')
                    return
                clickEspecifico(cliques= 1, teclaEspecifica= 'right')
                personagemReconhecido = self._imagem.retornaTextoNomePersonagemReconhecido(posicao= 1)
                contadorPersonagem += 1
            print(f'Personagem não encontrado!')
            if ehMenuEscolhaPersonagem(menu= self.retornaMenu()):
                clickEspecifico(cliques= 1, teclaEspecifica= 'f1')
                return
        if ehMenuInicial(menu): self.deslogaPersonagem()

    def retornaProfissaoPriorizada(self) -> Profissao | None:
        profissoes: list[Profissao] = self.pegaProfissoes()
        for profissao in profissoes:
            if profissao.prioridade:
                return profissao
        return None
    
    def pegaTrabalhosComumProfissaoNivelEspecifico(self, trabalho: Trabalho) -> list[Trabalho]:
        trabalhoDao = TrabalhoDaoSqlite()
        trabalhosComunsProfissaoNivelExpecifico = trabalhoDao.pegaTrabalhosComumProfissaoNivelEspecifico(trabalho)
        if trabalhosComunsProfissaoNivelExpecifico is None:
            self.__loggerTrabalhoDao.error(f'Erro ao buscar trabalhos específicos no banco: {trabalhoDao.pegaErro()}')
            return []
        return trabalhosComunsProfissaoNivelExpecifico
    
    def retornaListaIdsRecursosNecessarios(self, trabalho: Trabalho) -> list[str]:
        trabalhoDao = TrabalhoDaoSqlite()
        idsTrabalhos = trabalhoDao.retornaListaIdsRecursosNecessarios(trabalho)
        if idsTrabalhos is None:
            self.__loggerTrabalhoDao.error(f'Erro ao buscar ids de recursos necessários ({trabalho.profissao}, {trabalho.nivel}): {trabalhoDao.pegaErro()}')
            return []
        return idsTrabalhos
    
    def retornaListaDicionariosRecursosNecessarios(self, idsRecursos: list[str]) -> list[dict]:
        listaDicionarios = []
        for id in idsRecursos:
            quantidade = self.pegaQuantidadeTrabalhoEstoque(idTrabalho = id)
            dicionarioTrabalho = {CHAVE_ID_TRABALHO: id, CHAVE_QUANTIDADE: quantidade}
            listaDicionarios.append(dicionarioTrabalho)
        return listaDicionarios
    
    def pegaTrabalhosParaProduzirPorProfissaoRaridade(self, trabalho: TrabalhoProducao, personagem: Personagem = None) -> list[TrabalhoProducao]:
        personagem = self.__personagemEmUso if personagem is None else personagem
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
        trabalhosProduzindo = trabalhoProducaoDao.pegaTrabalhosParaProduzirPorProfissaoRaridade(trabalho)
        if trabalhosProduzindo is None:
            self.__loggerTrabalhoProducaoDao.error(f'Erro ao buscar trabalhos produzindo por profissão e raridade ({trabalho.profissao}, {trabalho.raridade}): {trabalhoProducaoDao.pegaErro()}')
            return []
        return trabalhosProduzindo

    def verificaRecursosNecessarios(self, trabalho: Trabalho) -> bool:
        if trabalho.ehComum():
            quantidadeRecursosContingencia: int = 0
            for trabalhoParaProduzir in self.pegaTrabalhosParaProduzirPorProfissaoRaridade(trabalho):
                quantidadeRecursosContingencia += trabalhoParaProduzir.pegaQuantidadeRecursosNecessarios() + 2
            quantidadeRecursosContingencia += trabalho.pegaQuantidadeRecursosNecessarios() + 2
            trabalho.nivel = 1 if trabalho.nivel < 16 else 8
            idsRecursosNecessarios: list[str] = self.retornaListaIdsRecursosNecessarios(trabalho)
            if len(idsRecursosNecessarios) < 3:
                return False
            dicionariosRecursosNecessarios: list[dict] = self.retornaListaDicionariosRecursosNecessarios(idsRecursosNecessarios)
            for dicionario in dicionariosRecursosNecessarios:
                if self.pegaQuantidadeTrabalhoEstoque(idTrabalho= dicionario[CHAVE_ID_TRABALHO]) < quantidadeRecursosContingencia:
                    return False
            return True
        return False

    def defineTrabalhoComumProfissaoPriorizada(self):
        profissaoPriorizada = self.retornaProfissaoPriorizada()
        if variavelExiste(profissaoPriorizada):
            nivelProfissao = profissaoPriorizada.pegaNivel()
            if nivelProfissao == 1 or nivelProfissao == 8:
                self.__loggerProfissaoDao.warning(f'Nível de produção é 1 ou 8')
                return 
            trabalhoBuscado:Trabalho = self.defineTrabalhoComumBuscado(profissaoPriorizada, nivelProfissao)
            trabalhosComunsProfissaoNivelExpecifico:list[Trabalho] = self.pegaTrabalhosComumProfissaoNivelEspecifico(trabalhoBuscado)
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
                    return
                trabalhoComum = self.defineTrabalhoProducaoComum(trabalhosQuantidade)
                existeRecursosNecessarios = self.verificaRecursosNecessarios(trabalhoBuscado)
                if existeRecursosNecessarios:
                    self.insereTrabalhoProducao(trabalhoComum)
                    continue
                return
        self.__loggerProfissaoDao.warning(f'Nem uma profissão priorizada encontrada!')
        return

    def defineTrabalhoComumBuscado(self, profissaoPriorizada, nivelProfissao):
        trabalhoBuscado = Trabalho()
        trabalhoBuscado.profissao = profissaoPriorizada.nome
        trabalhoBuscado.nivel = trabalhoBuscado.pegaNivel(nivelProfissao)
        trabalhoBuscado.raridade = CHAVE_RARIDADE_COMUM
        return trabalhoBuscado

    def defineTrabalhoProducaoComum(self, trabalhosQuantidade: list[TrabalhoEstoque]) -> TrabalhoProducao:
        trabalhoComum = TrabalhoProducao()
        trabalhoComum.idTrabalho = trabalhosQuantidade[0].trabalhoId
        trabalhoComum.estado = 0
        trabalhoComum.recorrencia = False
        trabalhoComum.tipo_licenca = CHAVE_LICENCA_NOVATO
        return trabalhoComum
    
    def pegaQuantidadeTrabalhoProducaoProduzirProduzindo(self, idTrabalho: str, personagem: Personagem = None) -> int:
        personagem = self.__personagemEmUso if personagem is None else personagem
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
        quantidade = trabalhoProducaoDao.pegaQuantidadeTrabalhoProducaoProduzirProduzindo(idTrabalho)
        if quantidade is None:
            self.__loggerTrabalhoProducaoDao.error(f'Erro ao buscar quantidade trabalho para produção por id ({idTrabalho}): {trabalhoProducaoDao.pegaErro()}')
            return 0
        return quantidade

    def atualizaListaTrabalhosQuantidadeTrabalhosProducao(self, trabalhosQuantidade: list[TrabalhoProducao]):
        quantidadeTotalTrabalhoProducao = 0
        for trabalhoQuantidade in trabalhosQuantidade:
            quantidade = self.pegaQuantidadeTrabalhoProducaoProduzirProduzindo(trabalhoQuantidade.trabalhoId)
            trabalhoQuantidade.quantidade += quantidade
            quantidadeTotalTrabalhoProducao += quantidade
        return trabalhosQuantidade, quantidadeTotalTrabalhoProducao
    
    def pegaQuantidadeTrabalhoEstoque(self, idTrabalho: str, personagem: Personagem = None) -> int:
        personagem = self.__personagemEmUso if personagem is None else personagem
        trabalhoEstoqueDao = EstoqueDaoSqlite(personagem)
        quantidade = trabalhoEstoqueDao.pegaQuantidadeTrabalho(idTrabalho)
        if quantidade is None:
            self.__loggerEstoqueDao.error(f'Erro ao buscar quantidade ({idTrabalho}) no estoque: {trabalhoEstoqueDao.pegaErro()}')
            return 0
        return quantidade

    def atualizaListaTrabalhosQuantidadeEstoque(self, trabalhosQuantidade: list[TrabalhoProducao]):
        for trabalhoQuantidade in trabalhosQuantidade:
            quantidade = self.pegaQuantidadeTrabalhoEstoque(trabalhoQuantidade.trabalhoId)
            trabalhoQuantidade.quantidade += quantidade
        return trabalhosQuantidade

    def defineListaTrabalhosQuantidade(self, trabalhosComunsProfissaoNivelExpecifico) -> list[TrabalhoEstoque]:
        trabalhosQuantidade: list[TrabalhoEstoque] = []
        for trabalhoComum in trabalhosComunsProfissaoNivelExpecifico:
            trabalhoQuantidade = TrabalhoEstoque()
            trabalhoQuantidade.trabalhoId = trabalhoComum.id
            trabalhoQuantidade.quantidade = 0
            trabalhosQuantidade.append(trabalhoQuantidade)
        return trabalhosQuantidade
    
    def listaPersonagemJaVerificadoEPersonagemAnteriorEAtualMesmoEmail(self) -> bool:
        if not tamanhoIgualZero(self.__listaPersonagemJaVerificado) and textoEhIgual(self.__listaPersonagemJaVerificado[-1].email, self.__listaPersonagemAtivo[0].email):
            self.entraPersonagemAtivo()
            return True
        return False
    
    def listaPersonagensAtivosEstaVazia(self) -> bool:
        if tamanhoIgualZero(self.__listaPersonagemAtivo):
            self.__listaPersonagemJaVerificado.clear()
            return True
        return False
    
    def personagemEmUsoExiste(self) -> bool:
        if self.__personagemEmUso is None: return False
        self.modificaAtributoUso()
        print(f'Personagem ({self.__personagemEmUso.nome}) ESTÁ EM USO.')
        self.inicializaChavesPersonagem()
        print('Inicia busca...')
        if self.vaiParaMenuProduzir():
            self.defineTrabalhoComumProfissaoPriorizada()
            trabalhosProducao = self.pegaTrabalhosProducaoParaProduzirProduzindo()
            if trabalhosProducao is None: return True
            if tamanhoIgualZero(trabalhosProducao):
                print(f'Lista de trabalhos desejados vazia.')
                self.__personagemEmUso.alternaEstado()
                self.modificaPersonagem()
                return True
            if self.__autoProducaoTrabalho: self.verificaProdutosRarosMaisVendidos()
            self.iniciaBuscaTrabalho()
            self.__listaPersonagemJaVerificado.append(self.__personagemEmUso)
            return False
        if self.__unicaConexao and haMaisQueUmPersonagemAtivo(self.__listaPersonagemAtivo): clickMouseEsquerdo(1, 2, 35)
        self.__listaPersonagemJaVerificado.append(self.__personagemEmUso)
        return True

    def iniciaProcessoBusca(self):
        while True:
            self.verificaAlteracaoListaTrabalhos()
            self.verificaAlteracaoPersonagem()
            self.retiraPersonagemJaVerificadoListaAtivo()
            if self.listaPersonagensAtivosEstaVazia(): continue
            self.definePersonagemEmUso()
            if self.personagemEmUsoExiste(): continue
            if self.listaPersonagemJaVerificadoEPersonagemAnteriorEAtualMesmoEmail(): continue
            if self.configuraEntraPersonagem(): self.entraPersonagemAtivo()

    def insereTrabalho(self, trabalho: Trabalho, modificaServidor: bool = True) -> bool:
        trabalhoDao = TrabalhoDaoSqlite()
        if trabalhoDao.insereTrabalho(trabalho, modificaServidor):
            self.__loggerTrabalhoDao.info(f'({trabalho.id.ljust(36)} | {trabalho}) inserido no banco com sucesso!')
            return True
        self.__loggerTrabalhoDao.error(f'Erro ao inserir ({trabalho.id.ljust(36)} | {trabalho}) no banco: {trabalhoDao.pegaErro()}')
        return False

    def removeTrabalho(self, trabalho: Trabalho, modificaServidor: bool = True) -> bool:
        trabalhoDao = TrabalhoDaoSqlite()
        if trabalhoDao.removeTrabalho(trabalho, modificaServidor):
            self.__loggerTrabalhoDao.info(f'({trabalho.id.ljust(36)} | {trabalho}) removido do banco com sucesso!')
            return True
        self.__loggerTrabalhoDao.error(f'Erro ao remover ({trabalho.id.ljust(36)} | {trabalho}) do banco: {trabalhoDao.pegaErro()}')
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
    
    def modificaPersonagem(self, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        personagemDao = PersonagemDaoSqlite()
        if personagemDao.modificaPersonagem(personagem, modificaServidor):
            self.__loggerPersonagemDao.info(f'({personagem}) modificado no banco com sucesso!')
            return True
        self.__loggerPersonagemDao.error(f'Erro ao modificar ({personagem}) no banco: {personagemDao.pegaErro()}')
        return False

    def inserePersonagem(self, personagem: Personagem, modificaServidor: bool = True) -> bool:
        personagemDao = PersonagemDaoSqlite()
        if personagemDao.inserePersonagem(personagem, modificaServidor):
            self.__loggerPersonagemDao.info(f'({personagem}) inserido no banco com sucesso!')
            return True
        self.__loggerPersonagemDao.error(f'Erro ao inserir ({personagem}) no banco: {personagemDao.pegaErro()}')
        return False
        
    def removeTrabalhoEstoque(self, trabalho: TrabalhoEstoque, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        trabalhoEstoqueDao = EstoqueDaoSqlite(personagem)
        if trabalhoEstoqueDao.removeTrabalhoEstoque(trabalho, modificaServidor):
            self.__loggerEstoqueDao.info(f'({trabalho}) removido do banco com sucesso!')
            return True
        self.__loggerEstoqueDao.error(f'Erro ao remover ({trabalho}) do banco: {trabalhoEstoqueDao.pegaErro()}')
        return False

    def modificaTrabalhoEstoque(self, trabalho: TrabalhoEstoque, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        estoqueDao = EstoqueDaoSqlite(personagem)
        if estoqueDao.modificaTrabalhoEstoque(trabalho, modificaServidor):
            self.__loggerEstoqueDao.info(f'({trabalho}) modificado no banco com sucesso!')
            return True
        self.__loggerEstoqueDao.error(f'Erro ao modificar ({trabalho}) no banco: {estoqueDao.pegaErro()}')
        return False
        
    def insereTrabalhoEstoque(self, trabalho: TrabalhoEstoque, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        trabalhoEstoqueDao = EstoqueDaoSqlite(personagem)
        if trabalhoEstoqueDao.insereTrabalhoEstoque(trabalho, modificaServidor):
            self.__loggerEstoqueDao.info(f'({trabalho}) inserido no banco com sucesso!')
            return True
        self.__loggerEstoqueDao.error(f'Erro ao inserir ({trabalho}) no banco: {trabalhoEstoqueDao.pegaErro()}')
        return False
    
    def removePersonagem(self, personagem: Personagem, modificaServirdor: bool = True) -> bool:
        personagemDao = PersonagemDaoSqlite()
        if personagemDao.removePersonagem(personagem, modificaServirdor):
            self.__loggerPersonagemDao.info(f'({personagem}) removido no banco com sucesso!')
            return True
        self.__loggerPersonagemDao.error(f'Erro ao remover ({personagem}) do banco: {personagemDao.pegaErro()}')
        return False
        
    def insereProfissao(self, profissao: Profissao, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        profissaoDao = ProfissaoDaoSqlite(personagem)
        if profissaoDao.insereProfissao(profissao, modificaServidor):
            self.__loggerProfissaoDao.info(f'({profissao}) inserido no banco com sucesso!')
            return True
        self.__loggerProfissaoDao.error(f'Erro ao inserir ({profissao}) no banco: {profissaoDao.pegaErro()}')
        return False

    def pegaPersonagemPorId(self, id: str) -> Personagem | None:
        persoangemDao = PersonagemDaoSqlite()
        personagemEncontrado = persoangemDao.pegaPersonagemPorId(id)
        if personagemEncontrado is None:
            self.__loggerPersonagemDao.error(f'Erro ao buscar personagem por id ({id}): {persoangemDao.pegaErro()}')
            return None
        return personagemEncontrado
    
    def pegaProfissaoPorId(self, id: str) -> Profissao | None:
        profissaoDao = ProfissaoDaoSqlite()
        profissaoEncontrada = profissaoDao.pegaProfissaoPorId(id)
        if profissaoEncontrada is None:
            self.__loggerProfissaoDao.error(f'Erro ao buscar por id ({id}): {profissaoDao.pegaErro()}')
            return None
        return profissaoEncontrada

    def pegaTrabalhoEstoquePorId(self, id: str) -> TrabalhoEstoque | None:
        trabalhoEstoqueDao: EstoqueDaoSqlite = EstoqueDaoSqlite()
        trabalhoEstoque: TrabalhoEstoque = trabalhoEstoqueDao.pegaTrabalhoEstoquePorId(id)
        if trabalhoEstoque is None:
            self.__loggerEstoqueDao.error(f'Erro ao buscar no trabalho no estoque por id ({id}): {trabalhoEstoqueDao.pegaErro()}')
            return None
        return trabalhoEstoque

    def pegaTrabalhoEstoquePorIdTrabalho(self, id: str) -> TrabalhoEstoque | None:
        trabalhoEstoqueDao: EstoqueDaoSqlite = EstoqueDaoSqlite()
        trabalhoEstoque: TrabalhoEstoque = trabalhoEstoqueDao.pegaTrabalhoEstoquePorIdTrabalho(id)
        if trabalhoEstoque is None:
            self.__loggerEstoqueDao.error(f'Erro ao buscar no trabalho no estoque por idTrabalho ({id}): {trabalhoEstoqueDao.pegaErro()}')
            return None
        return trabalhoEstoque

    def verificaAlteracaoPersonagem(self):
        if self.__repositorioPersonagem.estaPronto:
            dicionarios = self.__repositorioPersonagem.pegaDadosModificados()
            for dicionario in dicionarios:
                personagemModificado = Personagem()
                personagemModificado.id = dicionario[CHAVE_ID_PERSONAGEM]
                if CHAVE_LISTA_TRABALHOS_PRODUCAO in dicionario:
                    trabalhoProducao = TrabalhoProducao()
                    trabalhoProducao.id = dicionario[CHAVE_ID_TRABALHO]
                    if dicionario[CHAVE_LISTA_TRABALHOS_PRODUCAO] == None:
                        self.removeTrabalhoProducao(trabalhoProducao, personagemModificado, False)
                        continue
                    trabalhoProducaoEncontrado = self.pegaTrabalhoProducaoPorId(trabalhoProducao.id)
                    if variavelExiste(trabalhoProducaoEncontrado):
                        if trabalhoProducaoEncontrado.id == trabalhoProducao.id:
                            trabalhoProducaoEncontrado.dicionarioParaObjeto(dicionario[CHAVE_LISTA_TRABALHOS_PRODUCAO])
                            self.modificaTrabalhoProducao(trabalhoProducaoEncontrado, personagemModificado, False)
                            continue
                        trabalhoProducao.dicionarioParaObjeto(dicionario[CHAVE_LISTA_TRABALHOS_PRODUCAO])
                        self.insereTrabalhoProducao(trabalhoProducao, personagemModificado, False)
                    continue
                if CHAVE_LISTA_ESTOQUE in dicionario:
                    trabalhoEstoque = TrabalhoEstoque()
                    trabalhoEstoque.id = dicionario[CHAVE_ID_TRABALHO]
                    if dicionario[CHAVE_LISTA_ESTOQUE] == None:
                        trabalhoEstoqueEncontrado = self.pegaTrabalhoEstoquePorId(trabalhoEstoque.id)
                        if trabalhoEstoqueEncontrado.id == trabalhoEstoque.id:
                            self.removeTrabalhoEstoque(trabalhoEstoqueEncontrado, personagemModificado, False)
                            continue
                        self.__loggerEstoqueDao.warning(f'({trabalhoEstoque.id}) não foi encontrado no banco!')
                        continue
                    trabalhoEstoqueEncontrado: TrabalhoEstoque = self.pegaTrabalhoEstoquePorId(trabalhoEstoque.id)
                    if trabalhoEstoqueEncontrado is None:
                        continue
                    if trabalhoEstoqueEncontrado.id == trabalhoEstoque.id:
                        trabalhoEstoqueEncontrado.dicionarioParaObjeto(dicionario[CHAVE_LISTA_ESTOQUE])
                        self.modificaTrabalhoEstoque(trabalhoEstoqueEncontrado, personagemModificado, False)
                        continue
                    trabalhoEstoque.dicionarioParaObjeto(dicionario[CHAVE_LISTA_ESTOQUE])
                    self.insereTrabalhoEstoque(trabalhoEstoque, personagemModificado, False)
                    continue
                if CHAVE_LISTA_PROFISSAO in dicionario:
                    profissao = Profissao()
                    profissao.id = dicionario[CHAVE_ID_TRABALHO]
                    profissaoEncontrada = self.pegaProfissaoPorId(profissao.id)
                    if profissaoEncontrada is None:
                        continue
                    if profissaoEncontrada.id == profissao.id:
                        profissaoEncontrada.dicionarioParaObjeto(dicionario[CHAVE_LISTA_PROFISSAO])
                        self.modificaProfissao(profissaoEncontrada, personagemModificado, False)
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
                else:
                    personagemModificado.dicionarioParaObjeto(dicionario['novoPersonagem'])
                    self.inserePersonagem(personagemModificado, False)
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
        personagemDao: PersonagemDaoSqlite = PersonagemDaoSqlite()
        personagensBanco: list[Personagem] = personagemDao.pegaPersonagens()
        if personagensBanco is None:                  
            self.__loggerPersonagemDao.error(f'Erro ao buscar personagens no banco: {personagemDao.pegaErro()}')
            return []
        return personagensBanco

    def sincronizaListaPersonagens(self):
        personagensServidor: list[Personagem] = self.pegaPersonagensServidor()
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
        novaLista = []
        for personagemBanco in self.pegaPersonagens():
            for personagemServidor in personagensServidor:
                if personagemBanco.id == personagemServidor.id:
                    break
            else:
                novaLista.append(personagemBanco)
        for personagemBanco in novaLista:
            self.removePersonagem(personagemBanco, False)                    

    def removeProfissao(self, profissao: Profissao, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        profissaoDao = ProfissaoDaoSqlite(personagem)
        if profissaoDao.removeProfissao(profissao, modificaServidor):
            self.__loggerProfissaoDao.info(f'({profissao}) removido do banco com sucesso!')
            return True
        self.__loggerProfissaoDao.error(f'Erro ao remover ({profissao}) do banco: {profissaoDao.pegaErro()}')
        return False

    def sincronizaListaProfissoes(self):
        personagens: list[Personagem] = self.pegaPersonagens()
        for personagem in personagens:
            repositorioProfissao = RepositorioProfissao(personagem)
            profissoesServidor = repositorioProfissao.pegaTodasProfissoes()
            if variavelExiste(profissoesServidor):
                for profissaoServidor in profissoesServidor:
                    limpaTela()
                    print(f'Sincronizando profissões...')
                    print(f'Personagens: {(personagens.index(personagem)+1)/len(personagens):.2%}')
                    print(f'Profissões: {(profissoesServidor.index(profissaoServidor)+1)/len(profissoesServidor):.2%}')
                    profissaoEncontrada = self.pegaProfissaoPorId(profissaoServidor.id)
                    if profissaoEncontrada is None:
                        continue
                    if profissaoEncontrada.id == profissaoServidor.id:
                        if self.modificaProfissao(profissaoServidor, personagem, False):
                            self.__loggerProfissaoDao.info(f'({profissaoServidor}) sincronizado com sucesso!')
                        continue
                    self.insereProfissao(profissaoServidor, personagem, False)
                profissoesBanco: list[Profissao] = self.pegaProfissoes()
                novaLista = []
                for profissaoBanco in profissoesBanco:
                    for profissaoServidor in profissoesServidor:
                        if profissaoBanco.id == profissaoServidor.id:
                            break
                    else:
                        novaLista.append(profissaoBanco)
                for profissaoBanco in novaLista:
                    self.removeProfissao(profissaoBanco, personagem, False)
                continue
            self.__loggerRepositorioProfissao.error(f'Erro ao buscar profissões: {repositorioProfissao.pegaErro()}')
    
    def pegaTrabalhoProducaoPorId(self, id:  str) -> TrabalhoProducao:
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite()
        trabalhoProducaoEncontrado = trabalhoProducaoDao.pegaTrabalhoProducaoPorId(id)
        if trabalhoProducaoEncontrado is None:
            self.__loggerTrabalhoProducaoDao.error(f'Erro ao buscar trabalho para produção por id ({id}) no banco: {trabalhoProducaoDao.pegaErro()}')
            return None
        return trabalhoProducaoEncontrado

    def sincronizaTrabalhosProducao(self):
        personagens: list[Personagem] = self.pegaPersonagens()
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
                    trabalhoProducaoEncontradoBanco = self.pegaTrabalhoProducaoPorId(trabalhoProducaoServidor.id)
                    if variavelExiste(trabalhoProducaoEncontradoBanco):
                        if trabalhoProducaoEncontradoBanco.id == trabalhoProducaoServidor.id:
                            self.modificaTrabalhoProducao(trabalhoProducaoServidor, personagem, False)
                            continue
                        self.insereTrabalhoProducao(trabalhoProducaoServidor, personagem, False)
                    continue
                trabalhosProducaoBanco = self.pegaTrabalhosProducao(personagem)
                novaLista = []
                for trabalhoProducaoBanco in trabalhosProducaoBanco:
                    for trabalhoProducaoServidor in trabalhosProducaoServidor:
                        if trabalhoProducaoBanco.id == trabalhoProducaoServidor.id:
                            break
                    else:
                        novaLista.append(trabalhoProducaoBanco)
                for trabalhoProducaoBanco in novaLista:
                    self.removeTrabalhoProducao(trabalhoProducaoBanco, personagem, False)
                continue
            self.__loggerTrabalhoProducaoDao.error(f'Erro ao buscar trabalhos em produção no servidor: {repositorioTrabalhoProducao.pegaErro()}')

    def pegaPersonagensServidor(self) -> list[Personagem]:
        repositorioPersonagem: RepositorioPersonagem = RepositorioPersonagem()
        personagens: list[Personagem] = repositorioPersonagem.pegaTodosPersonagens()
        if personagens is None:
            self.__loggerRepositorioPersonagem.error(f'Erro ao buscar personagens no servidor: {repositorioPersonagem.pegaErro()}')
            return []
        return personagens

    def pegaTrabalhosBanco(self) -> list[Trabalho]:
        trabalhoDao = TrabalhoDaoSqlite()
        trabalhos = trabalhoDao.pegaTrabalhos()
        if trabalhos is None:
            self.__loggerTrabalhoDao.error(f'Erro ao buscar trabalhos no banco: {trabalhoDao.pegaErro()}')
            return []
        return trabalhos
    
    def pegaTrabalhoPorNome(self, nomeTrabalho: str) -> Trabalho | None:
        trabalhoDao = TrabalhoDaoSqlite()
        trabalhoEncontrado = trabalhoDao.pegaTrabalhoPorNome(nomeTrabalho)
        if trabalhoEncontrado is None:
            self.__loggerTrabalhoDao.error(f'Erro ao buscar por nome ({nomeTrabalho}) no banco: {trabalhoDao.pegaErro()}')
            return None
        if trabalhoEncontrado.nome is None:
            self.__loggerTrabalhoDao.warning(f'({nomeTrabalho}) não encontrado no banco!')
            return None
        return trabalhoEncontrado

    def sincronizaTrabalhosVendidos(self):
        personagens = self.pegaPersonagens()
        for personagem in personagens:

            pass

    def preparaPersonagem(self):
        try:
            self.abreStreamTrabalhos()
            self.abreStreamPersonagens()
            self.sincronizaListas()
            clickAtalhoEspecifico('alt', 'tab')
            clickAtalhoEspecifico('win', 'left')
            self.iniciaProcessoBusca()
        except Exception as e:
            print(e)
            if input(f'Tentar novamente? (S/N) \n').lower() == 's':
                self.preparaPersonagem()

    def sincronizaListas(self) -> None:
        sincroniza = input(f'Sincronizar listas? (S/N) ')
        if sincroniza is not None and sincroniza.lower() == 's':
            self.sincronizaListaTrabalhos()
            self.sincronizaListaPersonagens
            self.sincronizaListaProfissoes()
            self.sincronizaTrabalhosProducao()

    def abreStreamPersonagens(self) -> bool:
        if self.__repositorioPersonagem.abreStream():
            self.__loggerRepositorioPersonagem.info(f'Stream repositório personagem iniciada!')
            return True
        self.__loggerRepositorioPersonagem.error(f'Erro ao iniciar stream repositório personagem: {self.__repositorioPersonagem.pegaErro()}')
        return False

    def abreStreamTrabalhos(self) -> bool:
        if self.__repositorioTrabalho.abreStream():
            self.__loggerRepositorioTrabalho.info(f'Stream repositório trabalhos iniciada!')
            return True
        self.__loggerRepositorioTrabalho.error(f'Erro ao iniciar stream repositório trabalhos: {self.__repositorioTrabalho.pegaErro()}')
        return False

    def modificaTrabalho(self, trabalho: Trabalho, modificaServidor: bool = True) -> bool:
        trabalhoDao = TrabalhoDaoSqlite()
        if trabalhoDao.modificaTrabalho(trabalho, modificaServidor):
            self.__loggerTrabalhoDao.info(f'({trabalho.id.ljust(36)} | {trabalho}) modificado no banco com sucesso!')
            return True
        self.__loggerTrabalhoDao.error(f'Erro ao modificar ({trabalho.id.ljust(36)} | {trabalho}) no banco: {trabalhoDao.pegaErro()}')
        return False

if __name__=='__main__':
    Aplicacao().preparaPersonagem()