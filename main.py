from teclado import *
from constantes import *
from utilitarios import *
from imagem import ManipulaImagem
from time import sleep
import datetime
import uuid
import re

from modelos.trabalhoRecurso import TrabalhoRecurso
from modelos.trabalho import Trabalho
from modelos.trabalhoVendido import TrabalhoVendido
from modelos.trabalhoProducao import TrabalhoProducao
from modelos.trabalhoEstoque import TrabalhoEstoque
from modelos.personagem import Personagem
from modelos.profissao import Profissao
from modelos.logger import MeuLogger
from db.db import MeuBanco

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
from repositorio.repositorioEstoque import RepositorioEstoque
from repositorio.repositorioVendas import RepositorioVendas
from repositorio.repositorioUsuario import RepositorioUsuario
class Aplicacao:
    def __init__(self) -> None:
        self.__loggerAplicacao: MeuLogger = MeuLogger(nome= 'aplicacao')
        self.__loggerRepositorioTrabalho: MeuLogger = MeuLogger(nome= CHAVE_REPOSITORIO_TRABALHO)
        self.__loggerRepositorioProducao: MeuLogger = MeuLogger(nome= CHAVE_REPOSITORIO_TRABALHO_PRODUCAO)
        self.__loggerRepositorioPersonagem: MeuLogger = MeuLogger(nome= CHAVE_REPOSITORIO_PERSONAGEM)
        self.__loggerRepositorioProfissao: MeuLogger = MeuLogger(nome= CHAVE_REPOSITORIO_PROFISSAO)
        self.__loggerRepositorioVendas: MeuLogger = MeuLogger(nome= CHAVE_REPOSITORIO_VENDAS)
        self.__loggerRepositorioEstoque: MeuLogger = MeuLogger(nome= CHAVE_REPOSITORIO_ESTOQUE)
        self.__loggerPersonagemDao: MeuLogger = MeuLogger(nome= 'personagemDao')
        self.__loggerTrabalhoProducaoDao: MeuLogger = MeuLogger(nome= 'trabalhoProducaoDao')
        self.__loggerTrabalhoDao: MeuLogger = MeuLogger(nome= 'trabalhoDao')
        self.__loggerVendaDao: MeuLogger = MeuLogger(nome= 'vendaDao')
        self.__loggerProfissaoDao: MeuLogger = MeuLogger(nome= 'profissaoDao')
        self.__loggerEstoqueDao: MeuLogger = MeuLogger(nome= 'estoqueDao')
        self.__imagem = ManipulaImagem()
        self.__listaPersonagemJaVerificado: list[Personagem] = []
        self.__listaPersonagemAtivo: list[Personagem] = []
        self.__listaProfissoesNecessarias: list[Profissao] = []
        self.__personagemEmUso: Personagem = None
        self.__repositorioTrabalho = RepositorioTrabalho()
        self.__repositorioPersonagem: RepositorioPersonagem= RepositorioPersonagem()
        self.__repositorioProducao: RepositorioTrabalhoProducao= RepositorioTrabalhoProducao()
        self.__repositorioProfissao: RepositorioProfissao= RepositorioProfissao()
        self.__repositorioEstoque: RepositorioEstoque= RepositorioEstoque()
        self.__repositorioVendas: RepositorioVendas= RepositorioVendas()
        self.__repositorioUsuario: RepositorioUsuario= RepositorioUsuario()
        __meuBanco: MeuBanco= MeuBanco()
        try:
            __meuBanco.pegaConexao()
            __meuBanco.criaTabelas()
            self.__personagemDao: PersonagemDaoSqlite= PersonagemDaoSqlite(banco= __meuBanco)
            self.__profissaoDao: ProfissaoDaoSqlite= ProfissaoDaoSqlite(banco= __meuBanco)
            self.__estoqueDao: EstoqueDaoSqlite= EstoqueDaoSqlite(banco= __meuBanco)
            self.__trabalhoDao: TrabalhoDaoSqlite= TrabalhoDaoSqlite(banco= __meuBanco)
            self.__trabalhoProducaoDao: TrabalhoProducaoDaoSqlite= TrabalhoProducaoDaoSqlite(banco= __meuBanco)
            self.__vendasDao: VendaDaoSqlite= VendaDaoSqlite(banco= __meuBanco)
        except Exception as e:
            self.__loggerAplicacao.critical(menssagem= f'Erro: {e}')

    def personagemEmUso(self, personagem: Personagem = None):
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
                personagem.alternaUso
                self.modificaPersonagem(personagem)

    def verificaPersonagemMesmoEmail(self, listaPersonagemMesmoEmail: list[Personagem], personagem: Personagem) -> bool:
        for personagemMesmoEmail in listaPersonagemMesmoEmail:
            if textoEhIgual(personagem.id, personagemMesmoEmail.id) and not personagem.uso:
                personagem.alternaUso
                self.modificaPersonagem(personagem)
                return False
        return True

    def confirmaNomePersonagem(self, personagemReconhecido: str) -> None:
        '''
            Função para verificar o nome do personagem reconhecido está na lista atual de personagens ativos
            Args:
                personagemReconhecido (str): Valor reconhecido via processamento de imagem
        '''
        self.personagemEmUso()
        for personagemAtivo in self.__listaPersonagemAtivo:
            if texto1PertenceTexto2(texto1= personagemAtivo.nome, texto2= personagemReconhecido):
                self.__loggerAplicacao.debug(f'Personagem {personagemReconhecido.upper()} confirmado!')
                self.personagemEmUso(personagem= personagemAtivo)
                return
        self.__loggerAplicacao.debug(f'Personagem {personagemReconhecido} não encontrado na lista de personagens ativos atual!')

    def definePersonagemEmUso(self):
        '''
            Função para reconhecer o nome do personagem atual na posição 0
        '''
        nomeReconhecido: str= self.__imagem.retornaTextoNomePersonagemReconhecido(0)
        if nomeReconhecido is None:
            self.__loggerAplicacao.debug(f'Nome personagem não reconhecido na posição {0}!')
            return
        self.confirmaNomePersonagem(personagemReconhecido= nomeReconhecido)

    def defineListaPersonagensAtivos(self):
        '''
            Função para preencher a lista de personagens ativos
        '''
        self.__loggerAplicacao.debug(f'Definindo lista de personagens ativos')
        personagens: list[Personagem] = self.pegaPersonagens()
        self.__listaPersonagemAtivo.clear()
        for personagem in personagens:
            if personagem.ehAtivo:
                self.__listaPersonagemAtivo.append(personagem)

    def inicializaChavesPersonagem(self):
        self.__autoProducaoTrabalho: bool = self.__personagemEmUso.autoProducao
        self.__unicaConexao: bool = True
        self.__espacoBolsa: bool = True
        self.__confirmacao: bool = True
        self.__profissaoModificada: bool = False

    def retornaCodigoErroReconhecido(self, textoErroEncontrado: str) -> int:
        if textoErroEncontrado is None:
            return 0
        for posicaoTipoErro in range(len(CHAVE_LISTA_ERROS)):
            textoErro: str = limpaRuidoTexto(CHAVE_LISTA_ERROS[posicaoTipoErro])
            if textoErro in textoErroEncontrado:
                return posicaoTipoErro + 1
        return 0

    def verificaLicenca(self, dicionarioTrabalho):
        confirmacao = False
        if variavelExiste(dicionarioTrabalho):
            print(f"Buscando: {dicionarioTrabalho[CHAVE_TIPO_LICENCA]}")
            licencaReconhecida = self.__imagem.retornaTextoLicencaReconhecida()
            if variavelExiste(licencaReconhecida) and variavelExiste(dicionarioTrabalho[CHAVE_TIPO_LICENCA]):
                print(f'Licença reconhecida: {licencaReconhecida}.')
                primeiraBusca = True
                listaCiclo = []
                while not texto1PertenceTexto2(licencaReconhecida, dicionarioTrabalho[CHAVE_TIPO_LICENCA]):
                    clickEspecifico(1, "right")
                    listaCiclo.append(licencaReconhecida)
                    licencaReconhecida = self.__imagem.retornaTextoLicencaReconhecida()
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

    def verificaErro(self, textoErroEncontrado:str = None) -> int:
        textoErroEncontrado = self.__imagem.retornaTextoMenuReconhecido() if textoErroEncontrado is None else textoErroEncontrado
        sleep(0.5)
        print(f'Verificando erro...')
        CODIGO_ERRO = self.retornaCodigoErroReconhecido(textoErroEncontrado)
        if ehErroLicencaNecessaria(CODIGO_ERRO) or ehErroFalhaConexao(CODIGO_ERRO) or ehErroConexaoInterrompida(CODIGO_ERRO) or ehErroServidorEmManutencao(CODIGO_ERRO) or ehErroReinoIndisponivel(CODIGO_ERRO):
            clickEspecifico(2, "enter")
            if ehErroLicencaNecessaria(CODIGO_ERRO):
                self.verificaLicenca(None)
            return CODIGO_ERRO
        if ehErroOutraConexao(CODIGO_ERRO) or ehErroRecursosInsuficiente(CODIGO_ERRO) or ehErroTempoDeProducaoExpirada(CODIGO_ERRO) or ehErroExperienciaInsuficiente(CODIGO_ERRO) or ehErroEspacoProducaoInsuficiente(CODIGO_ERRO) or ehErroFalhaAoIniciarConexao(erro= CODIGO_ERRO):
            clickEspecifico(1,'enter')
            if ehErroOutraConexao(CODIGO_ERRO) or ehErroFalhaAoIniciarConexao(erro= CODIGO_ERRO):
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
        if ehErroMoedasMilagrosasInsuficientes(CODIGO_ERRO) or ehErroItemAVenda(erro= CODIGO_ERRO):
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
        textoMenu = self.__imagem.retornaTextoSair()
        if texto1PertenceTexto2('sair', textoMenu):
            print(f'Menu jogar...')
            return MENU_JOGAR
        textoMenu = self.__imagem.retornaTextoMenuReconhecido()
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
        if self.__imagem.verificaMenuReferencia():
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
        if texto1PertenceTexto2(texto1= 'Mercado', texto2= textoMenu) and texto1PertenceTexto2(texto1= 'Fechar', texto2= textoMenu):
            print(f'Menu mercado...')
            return MENU_MERCADO
        if texto1PertenceTexto2(texto1= 'Anuncio', texto2= textoMenu) and texto1PertenceTexto2(texto1= 'Cancelar', texto2= textoMenu):
            print(f'Menu anuncio...')
            return MENU_ANUNCIO        
        if texto1PertenceTexto2(texto1= 'Meus anuncios', texto2= textoMenu) and texto1PertenceTexto2(texto1= 'Voltar', texto2= textoMenu):
            print(f'Menu meus anuncios...')
            return MENU_MEUS_ANUNCIOS        
        if texto1PertenceTexto2('Bolsa',textoMenu):
            print(f'Menu bolsa...')
            return MENU_BOLSA
        clickMouseEsquerdo(1,35,35)
        self.verificaErro(textoErroEncontrado= textoMenu)
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
        trabalhosVendidos: list[TrabalhoVendido]= self.__vendasDao.pegaTrabalhosRarosVendidos(personagem= personagem)
        if trabalhosVendidos is None:
            self.__loggerVendaDao.error(f'Erro ao buscar trabalhos vendidos raros: {self.__vendasDao.pegaErro}')
            return []
        return trabalhosVendidos
    
    def insereTrabalhoVendido(self, trabalho: TrabalhoVendido, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        if self.__vendasDao.insereTrabalhoVendido(personagem= personagem, trabalho= trabalho, modificaServidor= modificaServidor):
            self.__loggerVendaDao.info(f'({personagem.id.ljust(36)} | {trabalho}) inserido no banco com sucesso!')
            return True
        self.__loggerVendaDao.error(f'Erro ao inserir ({personagem.id.ljust(36)} | {trabalho}) no banco: {self.__vendasDao.pegaErro}')
        return False
    
    def modificaTrabalhoVendido(self, trabalho: TrabalhoVendido, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        if self.__vendasDao.modificaTrabalhoVendido(personagem= personagem, trabalho= trabalho, modificaServidor= modificaServidor):
            self.__loggerVendaDao.info(f'({personagem.id.ljust(36)} | {trabalho}) modificado no banco com sucesso!')
            return True
        self.__loggerVendaDao.error(f'Erro ao modificar ({personagem.id.ljust(36)} | {trabalho}) no banco: {self.__vendasDao.pegaErro}')
        return False
    
    def removeTrabalhoVendido(self, trabalho: TrabalhoVendido, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        if self.__vendasDao.removeTrabalhoVendido(personagem= personagem, trabalho= trabalho, modificaServidor= modificaServidor):
            self.__loggerVendaDao.info(f'({personagem.id.ljust(36)} | {trabalho}) removido do banco com sucesso!')
            return True
        self.__loggerVendaDao.error(f'Erro ao remover ({personagem.id.ljust(36)} | {trabalho}) do banco: {self.__vendasDao.pegaErro}')
        return False
    
    def pegaTrabalhosVendidos(self, personagem: Personagem = None) -> list[TrabalhoVendido]:
        personagem = self.__personagemEmUso if personagem is None else personagem
        vendas: list[TrabalhoVendido]= self.__vendasDao.pegaTrabalhosVendidos(personagem= personagem)
        if vendas is None:
            self.__loggerVendaDao.error(f'Erro ao buscar trabalhos vendidos: {self.__vendasDao.pegaErro}')
            return []
        return vendas

    def retornaConteudoCorrespondencia(self) -> TrabalhoVendido | None:
        textoCarta = self.__imagem.retornaTextoCorrespondenciaReconhecido()
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
        trabalhosEstoque: list[TrabalhoEstoque]= self.__estoqueDao.pegaTrabalhosEstoque(personagem= personagem)
        if trabalhosEstoque is None:
            self.__loggerEstoqueDao.error(f'Erro ao buscar trabalhos em estoque no banco: {self.__estoqueDao.pegaErro}')
            return []
        return trabalhosEstoque

    def atualizaQuantidadeTrabalhoEstoque(self, trabalho: TrabalhoVendido):
        estoque = self.pegaTrabalhosEstoque()
        for trabalhoEstoque in estoque:
            if textoEhIgual(trabalhoEstoque.idTrabalho, trabalho.idTrabalho):
                novaQuantidade = 0 if trabalhoEstoque.quantidade - trabalho.quantidade < 0 else trabalhoEstoque.quantidade - trabalho.quantidade
                trabalhoEstoque.quantidade = novaQuantidade
                if self.modificaTrabalhoEstoque(trabalhoEstoque):
                    self.__loggerEstoqueDao.debug(f'Quantidade de ({trabalhoEstoque}) atualizada para {novaQuantidade}.')
                return
        self.__loggerEstoqueDao.warning(f'({trabalho}) não encontrado no estoque.')

    def ofertaTrabalho(self) -> None:
        for x in range(10):
            resultado: tuple = self.__imagem.retornaReferenciaLeiloeiro()
            if resultado is None: return
            clickMouseEsquerdo(clicks= 1, xTela= resultado[0], yTela= resultado[1] + 100)
            sleep(3)
            if ehMenuMercado(menu= self.retornaMenu()):
                clickEspecifico(cliques= 1, teclaEspecifica= 'down')
                clickEspecifico(cliques= 1, teclaEspecifica= 'enter')
                for y in range(15):
                    clickEspecifico(cliques= 1, teclaEspecifica= 'f2')
                    clickEspecifico(cliques= 1, teclaEspecifica= '6')
                    if ehErroItemAVenda(self.verificaErro()):
                        clickEspecifico(cliques= 2, teclaEspecifica= 'f1')
                        return
                    clickEspecifico(cliques= 1, teclaEspecifica= 'f2')
                    codigoMenu = self.retornaMenu()
                    if ehMenuAnuncio(menu = codigoMenu):
                        clickEspecifico(cliques= 3, teclaEspecifica= 'f1')
                        return
                    if not ehMenuMeusAnuncios(menu= codigoMenu):
                        return
                return

    def recuperaCorrespondencia(self):
        while self.__imagem.existeCorrespondencia():
            clickEspecifico(1, 'enter')
            trabalhoVendido = self.retornaConteudoCorrespondencia()
            if variavelExiste(trabalhoVendido):
                self.atualizaQuantidadeTrabalhoEstoque(trabalhoVendido)
            clickEspecifico(1,'f2')
            continue
        print(f'Caixa de correio vazia!')
        clickMouseEsquerdo(1, 2, 35)

    def reconheceRecuperaTrabalhoConcluido(self) -> str | None:
        erro: int = self.verificaErro()
        if nenhumErroEncontrado(erro= erro):
            nomeTrabalhoConcluido: str = self.__imagem.retornaNomeTrabalhoFrameProducaoReconhecido()
            clickEspecifico(cliques= 1, teclaEspecifica= 'down')
            clickEspecifico(cliques= 1, teclaEspecifica= 'f2')
            self.__loggerTrabalhoProducaoDao.info(f'Trabalho concluido reconhecido: {nomeTrabalhoConcluido}')
            if nomeTrabalhoConcluido is None:
                return None
            erro: int = self.verificaErro()
            if nenhumErroEncontrado(erro= erro):
                if not self.listaProfissoesFoiModificada():
                    self.__profissaoModificada = True
                clickContinuo(cliques= 3, teclaEspecifica= 'up')
                return nomeTrabalhoConcluido
            self.__loggerTrabalhoProducaoDao.warning(f'Codigo erro: {erro}')
            if ehErroEspacoBolsaInsuficiente(erro= erro):
                self.__espacoBolsa = False
                clickContinuo(cliques= 1, teclaEspecifica= 'up')
                clickEspecifico(cliques= 1, teclaEspecifica= 'left')
        return None

    def retornaListaPossiveisTrabalhoRecuperado(self, nomeTrabalhoConcluido):
        listaPossiveisDicionariosTrabalhos = []
        trabalhos = self.pegaTrabalhosBanco()
        for trabalho in trabalhos:
            if texto1PertenceTexto2(nomeTrabalhoConcluido[1:-1], trabalho.nomeProducao):
                listaPossiveisDicionariosTrabalhos.append(trabalho)
        return listaPossiveisDicionariosTrabalhos
    
    def insereTrabalhoProducao(self, trabalho: TrabalhoProducao, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        '''
            Função para inserir um objeto da classe TrabalhoProducao no banco de dados local e remoto.
            Args:
                trabalho (TrabalhoProducao): Objeto da classe TrabalhoProducao a ser inserido no banco.
                personagem (Personagem): Objeto da classe Personagem que contêm o "id" do personagem a qual o trabalho pertence. É None por padrão.
                modificaServidor (bool): Valor boleano que indica se o trabalho deve ser inserido no banco de dados remoto ou não. É True por padrão.
            Returns:
                bool: Verdadeiro caso o trabalho seja inserido com sucesso
        '''
        if trabalho is None:
            return True
        personagem = self.__personagemEmUso if personagem is None else personagem
        if self.__trabalhoProducaoDao.insereTrabalhoProducao(personagem= personagem, trabalhoProducao= trabalho, modificaServidor= modificaServidor):
            self.__loggerTrabalhoProducaoDao.info(f'({personagem.id.ljust(36)} | {trabalho}) inserido no banco com sucesso!')
            return True
        self.__loggerTrabalhoProducaoDao.error(f'Erro ao inserir ({personagem.id.ljust(36)} | {trabalho}) no banco: {self.__trabalhoProducaoDao.pegaErro}')
        return False
        
    def pegaTrabalhosProducaoParaProduzirProduzindo(self, personagem: Personagem = None) -> list[TrabalhoProducao] | None:
        personagem = self.__personagemEmUso if personagem is None else personagem
        trabalhosProducaoProduzirProduzindo = self.__trabalhoProducaoDao.pegaTrabalhosProducaoParaProduzirProduzindo(personagem= personagem)
        if trabalhosProducaoProduzirProduzindo is None:
            self.__loggerTrabalhoProducaoDao.error(f'Erro ao bucar trabalhos para produção com estado para produzir ou produzindo: {self.__trabalhoProducaoDao.pegaErro}')
            return None
        return trabalhosProducaoProduzirProduzindo
        
    def removeTrabalhoProducao(self, trabalho: TrabalhoProducao, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        if self.__trabalhoProducaoDao.removeTrabalhoProducao(personagem= personagem, trabalhoProducao= trabalho, modificaServidor= modificaServidor):
            self.__loggerTrabalhoProducaoDao.info(f'({personagem.id.ljust(36)} | {trabalho}) removido do banco com sucesso!')
            return True
        self.__loggerTrabalhoProducaoDao.error(f'Erro ao remover ({personagem.id.ljust(36)} | {trabalho}) do banco: {self.__trabalhoProducaoDao.pegaErro}')
        return False
    
    def modificaTrabalhoProducao(self, trabalho: TrabalhoProducao, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        if self.__trabalhoProducaoDao.modificaTrabalhoProducao(personagem= personagem, trabalho= trabalho, modificaServidor= modificaServidor):
            self.__loggerTrabalhoProducaoDao.info(f'({personagem.id.ljust(36)} | {trabalho}) modificado no banco com sucesso!')
            return True
        self.__loggerTrabalhoProducaoDao.error(f'Erro ao modificar ({personagem.id.ljust(36)} | {trabalho}) no banco: {self.__trabalhoProducaoDao.pegaErro}')
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
        trabalhoProducaoConcluido.estado = CODIGO_CONCLUIDO
        self.modificaTrabalhoProducao(trabalhoProducaoConcluido)

    def insereListaProfissoes(self, personagem: Personagem= None) -> bool:
        personagem: Personagem = self.__personagemEmUso if personagem is None else personagem
        if self.__profissaoDao.insereListaProfissoes(personagem= personagem):
            return True
        return False

    def pegaProfissoes(self, personagem: Personagem = None) -> list[Personagem]:
        '''
            Método para recuperar uma lista de objetos da classe Profissao do personagem atual no banco de dados local.
            Args:
                personagem (Personagem): Objeto da classe Personagem que contêm os atributos do personagem em uso.
            Returns:
                profissoes (list[Profissao]): Lista de objetos da classe Profissao encontrados no banco de dados.
        '''
        personagem = self.__personagemEmUso if personagem is None else personagem
        self.__loggerAplicacao.debug(menssagem= f'Pegando profissões de ({personagem.nome})')
        profissoes: list[Profissao] = self.__profissaoDao.pegaProfissoesPorIdPersonagem(personagem= personagem)
        if profissoes is None:
            self.__loggerProfissaoDao.error(f'Erro ao buscar profissões no banco ({self.__personagemEmUso.nome}): {self.__profissaoDao.pegaErro}')
            return []
        if ehVazia(profissoes):
            self.__loggerProfissaoDao.warning(f'Erro ao buscar profissões ({self.__personagemEmUso.nome}) no banco: Profissões está vazia!')
        return profissoes
    
    def modificaProfissao(self, profissao: Profissao, personagem: Personagem = None, modificaServidor = True) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        if self.__profissaoDao.modificaProfissao(personagem= personagem, profissao= profissao, modificaServidor= modificaServidor):
            self.__loggerProfissaoDao.info(f'({profissao}) modificado no banco com sucesso!')
            return True
        self.__loggerProfissaoDao.error(f'Erro ao modificar ({profissao}) no banco: {self.__profissaoDao.pegaErro}')
        return False

    def modificaExperienciaProfissao(self, trabalho: TrabalhoProducao) -> bool:
        profissoes: list[Profissao] = self.pegaProfissoes()
        trabalhoEncontado: Trabalho = self.pegaTrabalhoPorId(trabalho.idTrabalho)
        if trabalhoEncontado is None or trabalhoEncontado.nome is None:
            return False
        trabalhoEncontado.experiencia = trabalhoEncontado.experiencia * 1.5 if textoEhIgual(trabalho.tipoLicenca, CHAVE_LICENCA_INICIANTE) else trabalhoEncontado.experiencia
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
                trabalhoEstoque.idTrabalho = trabalhoProducaoConcluido.idTrabalho
            else:
                if trabalhoEhMelhoriaEssenciaComum(trabalhoProducaoConcluido):
                    trabalhoEstoque = TrabalhoEstoque()
                    trabalhoEstoque.nome = 'Essência composta'
                    trabalhoEstoque.profissao = ''
                    trabalhoEstoque.nivel = 0
                    trabalhoEstoque.quantidade = 5
                    trabalhoEstoque.raridade = 'Recurso'
                    trabalhoEstoque.idTrabalho = trabalhoProducaoConcluido.idTrabalho
                elif trabalhoEhMelhoriaEssenciaComposta(trabalhoProducaoConcluido):
                    trabalhoEstoque = TrabalhoEstoque()
                    trabalhoEstoque.nome = 'Essência de energia'
                    trabalhoEstoque.profissao = ''
                    trabalhoEstoque.nivel = 0
                    trabalhoEstoque.quantidade = 1
                    trabalhoEstoque.raridade = 'Recurso'
                    trabalhoEstoque.idTrabalho = trabalhoProducaoConcluido.idTrabalho
                elif trabalhoEhMelhoriaSubstanciaComum(trabalhoProducaoConcluido):
                    trabalhoEstoque = TrabalhoEstoque()
                    trabalhoEstoque.nome = 'Substância composta'
                    trabalhoEstoque.profissao = ''
                    trabalhoEstoque.nivel = 0
                    trabalhoEstoque.quantidade = 5
                    trabalhoEstoque.raridade = 'Recurso'
                    trabalhoEstoque.idTrabalho = trabalhoProducaoConcluido.idTrabalho
                elif trabalhoEhMelhoriaSubstanciaComposta(trabalhoProducaoConcluido):
                    trabalhoEstoque = TrabalhoEstoque()
                    trabalhoEstoque.nome = 'Substância energética'
                    trabalhoEstoque.profissao = ''
                    trabalhoEstoque.nivel = 0
                    trabalhoEstoque.quantidade = 1
                    trabalhoEstoque.raridade = 'Recurso'
                    trabalhoEstoque.idTrabalho = trabalhoProducaoConcluido.idTrabalho
                elif trabalhoEhMelhoriaCatalisadorComum(trabalhoProducaoConcluido):
                    trabalhoEstoque = TrabalhoEstoque()
                    trabalhoEstoque.nome = 'Catalisador amplificado'
                    trabalhoEstoque.profissao = ''
                    trabalhoEstoque.nivel = 0
                    trabalhoEstoque.quantidade = 5
                    trabalhoEstoque.raridade = 'Recurso'
                    trabalhoEstoque.idTrabalho = trabalhoProducaoConcluido.idTrabalho
                elif trabalhoEhMelhoriaCatalisadorComposto(trabalhoProducaoConcluido):
                    trabalhoEstoque = TrabalhoEstoque()
                    trabalhoEstoque.nome = 'Catalisador de energia'
                    trabalhoEstoque.profissao = ''
                    trabalhoEstoque.nivel = 0
                    trabalhoEstoque.quantidade = 1
                    trabalhoEstoque.raridade = 'Recurso'
                    trabalhoEstoque.idTrabalho = trabalhoProducaoConcluido.idTrabalho
                if variavelExiste(trabalhoEstoque):
                    if textoEhIgual(trabalhoProducaoConcluido.tipoLicenca, CHAVE_LICENCA_APRENDIZ):
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
                            trabalhoEstoque.idTrabalho = trabalho.id
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
                            if textoEhIgual(trabalhoProducaoConcluido.tipoLicenca, CHAVE_LICENCA_APRENDIZ):
                                trabalhoEstoque.quantidade = trabalhoEstoque.quantidade * 2
                        else:
                            print(f'Tipo de recurso não encontrado!')
            if ehVazia(listaTrabalhoEstoqueConcluido):
                    trabalhoEstoque = TrabalhoEstoque()
                    trabalhoEstoque.nome = trabalhoProducaoConcluido.nome
                    trabalhoEstoque.profissao = trabalhoProducaoConcluido.profissao
                    trabalhoEstoque.nivel = trabalhoProducaoConcluido.nivel
                    trabalhoEstoque.quantidade = 0
                    trabalhoEstoque.raridade = trabalhoProducaoConcluido.raridade
                    trabalhoEstoque.idTrabalho = trabalhoProducaoConcluido.idTrabalho
                    tipoRecurso = retornaChaveTipoRecurso(trabalhoEstoque)
                    if variavelExiste(tipoRecurso):
                        if tipoRecurso == CHAVE_RCS or tipoRecurso == CHAVE_RCT:
                            trabalhoEstoque.quantidade = 1
                        elif tipoRecurso == CHAVE_RCP or tipoRecurso == CHAVE_RAP or tipoRecurso == CHAVE_RAS or tipoRecurso == CHAVE_RAT:
                            trabalhoEstoque.quantidade = 2
                        if textoEhIgual(trabalhoProducaoConcluido.tipoLicenca, CHAVE_LICENCA_APRENDIZ):
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
            trabalhoEstoque.idTrabalho = trabalhoProducaoConcluido.idTrabalho
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
        if ehVazia(listaTrabalhoEstoqueConcluido):
            return
        estoque = self.pegaTrabalhosEstoque()
        if ehVazia(estoque):
            for trabalhoEstoqueConcluido in listaTrabalhoEstoqueConcluido:
                self.insereTrabalhoEstoque(trabalhoEstoqueConcluido)
            return
        for trabalhoEstoque in estoque:
            listaTrabalhoEstoqueConcluido, trabalhoEstoque = self.modificaQuantidadeTrabalhoEstoque(listaTrabalhoEstoqueConcluido, trabalhoEstoque)
        if ehVazia(listaTrabalhoEstoqueConcluido):
            return
        for trabalhoEstoqueConcluido in listaTrabalhoEstoqueConcluido:
            self.insereTrabalhoEstoque(trabalhoEstoqueConcluido)

    def retornaProfissaoTrabalhoProducaoConcluido(self, trabalhoConcluido: TrabalhoProducao) -> Profissao | None:
        '''
            Método para retornar um objeto da classe Profissao que contêm os atributos da profissão encontrada.
            Args:
                trabalhoConcluido (TrabalhoConcluido): Objeto da classe TrabalhoProducao que contêm os atributos do trabalho concluído.
            Returns:
                profissao (Profissao): Objeto da classe Profissao que contêm os atributos da profissão encontrada.
        '''
        profissoes: list[Profissao] = self.pegaProfissoes()
        for profissao in profissoes:
            if textoEhIgual(texto1= profissao.nome, texto2= trabalhoConcluido.profissao):
                return profissao
        return None

    def verificaProducaoTrabalhoRaro(self, trabalhoConcluido: TrabalhoProducao) -> TrabalhoProducao | None:
        '''
            Método para verificar se trabalho concluído é do tipo "Melhorado" e possui um trabalho do tipo "Raro"
            Args:
                trabalhoConcluido (TrabalhoProducao): Objeto da classe TrabalhoProducao que contêm os atributos do trabalho concluído.
            Returns:
                TrabalhoProducao: Obejto da classe TrabalhoProducao que contêm os atributos do trabalho do tipo "Raro" encontrado.
        '''
        if trabalhoConcluido.ehMelhorado:
            profissao: Profissao = self.retornaProfissaoTrabalhoProducaoConcluido(trabalhoConcluido)
            if profissao is None:
                return None
            trabalhos: list[Trabalho]= self.pegaTrabalhosBanco()
            for trabalho in trabalhos:
                trabalhoNecessarioEhIgualNomeTrabalhoConcluido = textoEhIgual(texto1= trabalho.trabalhoNecessario, texto2= trabalhoConcluido.nome)
                if trabalhoNecessarioEhIgualNomeTrabalhoConcluido:
                    return self.defineNovoTrabalhoProducaoRaro(profissao, trabalho)
        return None

    def defineNovoTrabalhoProducaoRaro(self, profissao: Profissao, trabalho: Trabalho) -> TrabalhoProducao:
        '''
            Função de define um novo objeto da classe TrabalhoProducao do tipo "Raro"
            Args:
                profissao (Profissao): Objeto da classe Profissao que contêm o atributo necessário "experiencia".
                trabalho (Trabalho): Obejto da classe Trabalho que contêm os atributos do trabalho encontrado.
            Returns:
                trabalhoRaro (TrabalhoProducao): Novo bjeto da classe TrabalhoProducao que contêm os atributos do trabalho do tipo "Raro" encontado.
        '''
        licencaProducaoIdeal = CHAVE_LICENCA_NOVATO if profissao.pegaExperienciaMaximaPorNivel >= profissao.pegaExperienciaMaxima else CHAVE_LICENCA_INICIANTE
        trabalhoRaro: TrabalhoProducao = TrabalhoProducao()
        trabalhoRaro.dicionarioParaObjeto(dicionario= trabalho.__dict__)
        trabalhoRaro.id = str(uuid.uuid4())
        trabalhoRaro.idTrabalho = trabalho.id
        trabalhoRaro.experiencia = trabalho.experiencia * 1.5
        trabalhoRaro.recorrencia = False
        trabalhoRaro.tipoLicenca = licencaProducaoIdeal
        trabalhoRaro.estado = CODIGO_PARA_PRODUZIR
        return trabalhoRaro

    def retornaListaPersonagemRecompensaRecebida(self, listaPersonagemPresenteRecuperado: list[str] = []) -> list[str]:
        nomePersonagemReconhecido: str = self.__imagem.retornaTextoNomePersonagemReconhecido(posicao= 0)
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
            referenciaEncontrada: list[float] = self.__imagem.verificaRecompensaDisponivel()
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

    def deslogaPersonagem(self, menu: int = None) -> None:
        menu = self.retornaMenu() if menu is None else menu
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
                return
            if ehMenuEscolhaPersonagem(menu):
                clickEspecifico(cliques= 1, teclaEspecifica= 'f1')
                return
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
            nomePersonagem = self.__imagem.retornaTextoNomePersonagemReconhecido(1)               
            while True:
                nomePersonagemPresenteado = None
                for nomeLista in listaPersonagemPresenteRecuperado:
                    if texto1PertenceTexto2(nomeLista, nomePersonagem) and nomePersonagem != None:
                        nomePersonagemPresenteado = nomeLista
                        break
                if nomePersonagemPresenteado != None:
                    clickEspecifico(1, 'right')
                    nomePersonagem = self.__imagem.retornaTextoNomePersonagemReconhecido(1)
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
                if self.__imagem.retornaExistePixelCorrespondencia():
                    vaiParaMenuCorrespondencia()
                    self.recuperaCorrespondencia()
                    self.ofertaTrabalho()
                print(f'Lista: {listaPersonagemPresenteRecuperado}.')
                self.deslogaPersonagem()
                if self.entraPersonagem(listaPersonagemPresenteRecuperado):
                    listaPersonagemPresenteRecuperado = self.retornaListaPersonagemRecompensaRecebida(listaPersonagemPresenteRecuperado)
                else:
                    print(f'Todos os personagens foram verificados!')
                    break
            menu: int = self.retornaMenu()

    def trataMenu(self, menu) -> None:
        if menu == MENU_DESCONHECIDO:
            return
        if ehMenuTrabalhosAtuais(menu= menu):
            estadoTrabalho: int = self.__imagem.retornaEstadoTrabalho()
            if estadoTrabalho == CODIGO_CONCLUIDO:
                nomeTrabalhoConcluido: str = self.reconheceRecuperaTrabalhoConcluido()
                if nomeTrabalhoConcluido is None:
                    self.__loggerTrabalhoProducaoDao.warning(f'Nome trabalho concluído não reconhecido.')
                    return
                trabalhoProducaoConcluido: TrabalhoProducao = self.retornaTrabalhoProducaoConcluido(nomeTrabalhoReconhecido= nomeTrabalhoConcluido)
                if trabalhoProducaoConcluido is None:
                    self.__loggerTrabalhoProducaoDao.warning(f'Trabalho produção concluido ({nomeTrabalhoConcluido}) não encontrado.')
                    return
                self.modificaTrabalhoConcluidoListaProduzirProduzindo(trabalhoProducaoConcluido= trabalhoProducaoConcluido)
                self.modificaExperienciaProfissao(trabalho= trabalhoProducaoConcluido)
                self.atualizaEstoquePersonagem(trabalhoEstoqueConcluido= trabalhoProducaoConcluido)
                trabalhoProducaoRaro: TrabalhoProducao = self.verificaProducaoTrabalhoRaro(trabalhoConcluido= trabalhoProducaoConcluido)
                self.insereTrabalhoProducao(trabalho= trabalhoProducaoRaro)
                return
            if estadoTrabalho == CODIGO_PRODUZINDO:
                if self.existeEspacoProducao():
                    clickContinuo(cliques= 3, teclaEspecifica= 'up')
                    clickEspecifico(cliques= 1, teclaEspecifica= 'left')
                    return
                print(f'Todos os espaços de produção ocupados.')
                self.__confirmacao = False
                return
            if estadoTrabalho == CODIGO_PARA_PRODUZIR:
                clickContinuo(cliques= 3, teclaEspecifica= 'up')
                clickEspecifico(cliques= 1, teclaEspecifica= 'left')
            return
        if ehMenuRecompensasDiarias(menu= menu) or ehMenuLojaMilagrosa(menu= menu):
            self.recebeTodasRecompensas(menu)
            for personagem in self.pegaPersonagens():
                if personagem.estado:
                    continue
                personagem.alternaEstado
                self.modificaPersonagem(personagem)
            self.__confirmacao = False
            return
        if ehMenuPrincipal(menu= menu):
            clickEspecifico(1,'num1')
            clickEspecifico(1,'num7')
            return
        if ehMenuPersonagem(menu= menu):
            clickEspecifico(1,'num7')
            return
        if ehMenuTrabalhosDisponiveis(menu= menu):
            clickEspecifico(1,'up')
            clickEspecifico(2,'left')
            return
        if ehMenuTrabalhoEspecifico(menu== menu):
            clickEspecifico(1,'f1')
            clickContinuo(3,'up')
            clickEspecifico(2,'left')
            return
        if ehMenuOfertaDiaria(menu= menu):
            clickEspecifico(1,'f1')
            return
        if ehMenuInicial(menu= menu):
            clickEspecifico(1,'f2')
            clickEspecifico(1,'num1')
            clickEspecifico(1,'num7')
            return
        self.__confirmacao = False

    def vaiParaMenuProduzir(self) -> bool:
        erro = self.verificaErro()
        if nenhumErroEncontrado(erro):
            menu = self.retornaMenu()
            if ehMenuInicial(menu):
                if self.__imagem.retornaExistePixelCorrespondencia():
                    vaiParaMenuCorrespondencia()
                    self.recuperaCorrespondencia()
                    self.ofertaTrabalho()
            while not ehMenuProduzir(menu):
                self.trataMenu(menu)
                if ehErroOutraConexao(self.verificaErro()):
                    self.__confirmacao = False
                    self.__unicaConexao = False
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
            if ehVazia(listaTrabalhosRarosVendidosOrdenada):
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
        trabalhoEncontrado = self.__trabalhoDao.pegaTrabalhoPorNomeProfissaoRaridade(trabalho)
        if trabalhoEncontrado is None:
            self.__loggerTrabalhoDao.error(f'Erro ao buscar trabalho por nome, profissao e raridade ({trabalho.nome}, {trabalho.profissao}, {trabalho.raridade}) no banco: {self.__trabalhoDao.pegaErro}')
            return None
        if trabalhoEncontrado.nome is None:
            self.__loggerTrabalhoDao.warning(f'({trabalho.nome}) não foi encontrado no banco!')
            return None
        return trabalhoEncontrado

    def pegaTrabalhosPorProfissaoRaridade(self, trabalho: Trabalho) -> list[Trabalho]:
        trabalhos = self.__trabalhoDao.pegaTrabalhosPorProfissaoRaridade(trabalho)
        if trabalhos is None:
            self.__loggerTrabalhoDao.error(f'Erro ao buscar trabalhos por profissão e raridade ({trabalho.profissao}, {trabalho.raridade}) no banco: {self.__trabalhoDao.pegaErro}')
            return []
        return trabalhos

    def pegaTrabalhoPorId(self, id: str) -> Trabalho | None:
        trabalhoEncontrado: Trabalho= self.__trabalhoDao.pegaTrabalhoPorId(idBuscado= id)
        if trabalhoEncontrado is None:
            self.__loggerTrabalhoDao.error(f'Erro ao buscar trabalho por id ({id}) no banco: {self.__trabalhoDao.pegaErro}')
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
            trabalhoEhRaroETrabalhoNaoEhProducaoDeRecursos = trabalhoEncontrado.ehRaro and not trabalhoEhProducaoRecursos(trabalhoEncontrado)
            if trabalhoEhRaroETrabalhoNaoEhProducaoDeRecursos:
                trabalhosRarosVendidos.append(trabalhoVendido)
        return trabalhosRarosVendidos

    def verificaProdutosRarosMaisVendidos(self):
        listaTrabalhosRarosVendidos = self.retornaListaTrabalhosRarosVendidos()
        if ehVazia(listaTrabalhosRarosVendidos):
            print(f'Lista de trabalhos raros vendidos está vazia!')
            return
        self.produzProdutoMaisVendido(listaTrabalhosRarosVendidos)

    def pegaTodosTrabalhosProducao(self) -> list[TrabalhoProducao]:
        trabalhosProducao = self.__trabalhoProducaoDao.pegaTodosTrabalhosProducao()
        if trabalhosProducao is None:
            self.__loggerTrabalhoProducaoDao.error(f'Erro ao buscar todos os trabalhos para produção: {self.__trabalhoProducaoDao.pegaErro}')
            return []
        return trabalhosProducao


    def pegaTrabalhosProducao(self, personagem: Personagem = None) -> list[TrabalhoProducao]:
        personagem = self.__personagemEmUso if personagem is None else personagem
        trabalhosProducao = self.__trabalhoProducaoDao.pegaTrabalhosProducao(personagem= personagem)
        if trabalhosProducao is None:
            self.__loggerTrabalhoProducaoDao.error(f'Erro ao buscar trabalhos para produção: {self.__trabalhoProducaoDao.pegaErro}')
            return []
        return trabalhosProducao

    def defineChaveListaProfissoesNecessarias(self) -> None:
        self.__loggerAplicacao.debug(f'Verificando profissões necessárias...')
        self.limpaListaProfissoesNecessarias()
        self.defineListaProfissoesNecessarias()
        self.ordenaListaProfissoesNecessarias()
        self.mostraListaProfissoesNecessarias()

    def defineListaProfissoesNecessarias(self) -> None:
        self.__loggerAplicacao.debug(f'Definindo profissões necessárias...')
        profissoes: list[Profissao] = self.pegaProfissoes()
        trabalhosProducao: list[TrabalhoProducao] = self.pegaTrabalhosProducao()
        if ehVazia(profissoes):
            self.__loggerProfissaoDao.warning(menssagem= f'Profissões está vazia!')
            return
        for profissao in profissoes:
            for trabalhoProducao in trabalhosProducao:
                chaveProfissaoEhIgualEEstadoEhParaProduzir: bool = textoEhIgual(profissao.nome, trabalhoProducao.profissao) and trabalhoProducao.ehParaProduzir
                if chaveProfissaoEhIgualEEstadoEhParaProduzir:
                    self.insereItemListaProfissoesNecessarias(profissao)
                    break

    def ordenaListaProfissoesNecessarias(self) -> None:
        self.__listaProfissoesNecessarias = sorted(self.__listaProfissoesNecessarias, key=lambda profissao: profissao.prioridade, reverse= True)

    def mostraListaProfissoesNecessarias(self) -> None:
        if ehVazia(self.__listaProfissoesNecessarias):
            self.__loggerAplicacao.debug(menssagem= f'Profissões necessárias está vazia!')
            return
        self.__loggerAplicacao.debug(menssagem= f'Profissões necessárias:')
        for profissaoNecessaria in self.__listaProfissoesNecessarias:
            nome: str= 'Indefinido' if profissaoNecessaria.nome is None else profissaoNecessaria.nome
            experiencia: str= 'Indefinido' if profissaoNecessaria.experiencia is None else str(profissaoNecessaria.experiencia)
            prioridade: str= 'Verdadeiro' if profissaoNecessaria.prioridade else 'Falso'
            self.__loggerAplicacao.debug(menssagem= f'{(nome).ljust(22)} | {experiencia.ljust(6)} | {prioridade.ljust(10)}')

    def insereItemListaProfissoesNecessarias(self, profissao: Profissao) -> None:
        self.__loggerAplicacao.debug(menssagem= f'({profissao.nome}) foi adicionado a lista de profissões necessárias')
        self.__listaProfissoesNecessarias.append(profissao)

    def limpaListaProfissoesNecessarias(self) -> None:
        self.__loggerAplicacao.debug(menssagem= f'Profissões necessárias foi limpa')
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

    def verificaEspacoProducao(self) -> None:
        quantidadeEspacoProducao: int = self.retornaQuantidadeEspacosDeProducao()
        if self.__personagemEmUso.espacoProducao == quantidadeEspacoProducao: return
        self.__personagemEmUso.setEspacoProducao(quantidadeEspacoProducao)
        self.modificaPersonagem()

    def retornaListaTrabalhosProducaoRaridadeEspecifica(self, nomeProfissao: str, raridade: str) -> list[TrabalhoProducao]:
        '''
            Função para definir a lista de trabalhos para produção com estado PARA_PRODUZIR(0), profissão e raridade recebidos por parâmetro
            Args:
                nomeProfissao (str): String que contêm o nome da profissão a ser verificada
                raridade (str): String que contêm a raridade a ser verificada
            Returns:
                listaTrabalhosProducaoRaridadeEspecifica (list[TrabalhoProducao]): Lista de trabalhos para produzir definida
        '''
        listaTrabalhosProducaoRaridadeEspecifica: list[TrabalhoProducao] = []
        trabalhosProducao: list[TrabalhoProducao] = self.pegaTrabalhosProducaoParaProduzirProduzindo()
        if trabalhosProducao is None: return listaTrabalhosProducaoRaridadeEspecifica
        for trabalhoProducao in trabalhosProducao:
            raridadeEhIgualProfissaoEhIgualEstadoEhParaProduzir = textoEhIgual(trabalhoProducao.raridade, raridade) and textoEhIgual(trabalhoProducao.profissao, nomeProfissao) and trabalhoProducao.ehParaProduzir
            if raridadeEhIgualProfissaoEhIgualEstadoEhParaProduzir:
                for trabalhoProducaoRaridadeEspecifica in listaTrabalhosProducaoRaridadeEspecifica:
                    if textoEhIgual(texto1= trabalhoProducaoRaridadeEspecifica.idTrabalho, texto2= trabalhoProducao.idTrabalho): 
                        self.__loggerAplicacao.debug(f'Trabalho {trabalhoProducao.nome} já está na lista!')
                        break
                else:
                    self.__loggerAplicacao.debug(f'Trabalho {raridade} inserido na lista: {trabalhoProducao.id.ljust(36)} | {trabalhoProducao.nome}')
                    listaTrabalhosProducaoRaridadeEspecifica.append(trabalhoProducao)
        if ehVazia(listaTrabalhosProducaoRaridadeEspecifica): self.__loggerAplicacao.debug(f'Nem um trabalho {raridade} na lista!')
        return listaTrabalhosProducaoRaridadeEspecifica

    def retornaNomeTrabalhoPosicaoTrabalhoRaroEspecial(self, dicionarioTrabalho):
        return self.__imagem.retornaNomeTrabalhoReconhecido((dicionarioTrabalho[CHAVE_POSICAO] * 72) + 289, 0)

    def retornaFrameTelaTrabalhoEspecifico(self) -> str | None:
        clickEspecifico(1, 'down')
        clickEspecifico(1, 'enter')
        nomeTrabalhoReconhecido: str = self.__imagem.retornaNomeConfirmacaoTrabalhoProducaoReconhecido(tipoTrabalho= 0)
        clickEspecifico(1, 'f1')
        clickEspecifico(1, 'up')
        return nomeTrabalhoReconhecido

    def confirmaNomeTrabalhoProducao(self, dicionario: dict, tipo: int):
        print(f'Confirmando nome do trabalho...')
        dicionario[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = None
        if tipo == 0:
            nomeTrabalhoReconhecido: str = self.retornaFrameTelaTrabalhoEspecifico()
        else:
            nomeTrabalhoReconhecido: str = self.__imagem.retornaNomeConfirmacaoTrabalhoProducaoReconhecido(tipoTrabalho= tipo)
        if nomeTrabalhoReconhecido is None:
            self.__loggerTrabalhoProducaoDao.info(f'Trabalho negado: Não reconhecido')
            return dicionario
        if CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA in dicionario:
            nomeTrabalhoReconhecido = nomeTrabalhoReconhecido[:24] if len(nomeTrabalhoReconhecido) >= 25 else nomeTrabalhoReconhecido
            listaTrabalhoProducaoPriorizada: list[TrabalhoProducao] = dicionario[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA]
            for trabalhoProducao in listaTrabalhoProducaoPriorizada:
                trabalhoEncontrado: Trabalho = self.pegaTrabalhoPorId(trabalhoProducao.idTrabalho)
                if trabalhoEncontrado is None:
                    continue
                nomeTrabalho = self.padronizaTexto(trabalhoEncontrado.nome)

                if trabalhoEhProducaoRecursos(trabalhoEncontrado):
                    nomeProducaoTrabalho: str = limpaRuidoTexto(trabalhoEncontrado.nomeProducao)
                    if texto1PertenceTexto2(nomeTrabalhoReconhecido, nomeProducaoTrabalho):
                        dicionario[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = trabalhoProducao
                        self.__loggerTrabalhoProducaoDao.info(f'Trabalho confirmado: {nomeTrabalhoReconhecido.ljust(30)} | {nomeProducaoTrabalho.ljust(30)}')
                        return dicionario
                    continue
                if textoEhIgual(nomeTrabalhoReconhecido, nomeTrabalho):
                    dicionario[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = trabalhoProducao
                    self.__loggerTrabalhoProducaoDao.info(f'Trabalho confirmado: {nomeTrabalhoReconhecido.ljust(30)} | {nomeTrabalho.ljust(30)}')
                    return dicionario
                nomeProducaoTrabalho: str = self.padronizaTexto(trabalhoEncontrado.nomeProducao)
                if textoEhIgual(nomeTrabalhoReconhecido, nomeProducaoTrabalho):
                    dicionario[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = trabalhoProducao
                    self.__loggerTrabalhoProducaoDao.info(f'Trabalho confirmado: {nomeTrabalhoReconhecido.ljust(30)} | {nomeProducaoTrabalho.ljust(30)}')
                    return dicionario
        self.__loggerTrabalhoProducaoDao.info(f'Trabalho negado: {nomeTrabalhoReconhecido.ljust(30)}')
        return dicionario

    def padronizaTexto(self, texto: str) -> str:
        textoPadronizado: str = texto.replace('-','')
        textoPadronizado = limpaRuidoTexto(texto= textoPadronizado)
        textoPadronizado = textoPadronizado[:24] if len(textoPadronizado) >= 25 else textoPadronizado
        return textoPadronizado

    def incrementaChavePosicaoTrabalho(self, dicionarioTrabalho):
        dicionarioTrabalho[CHAVE_POSICAO] += 1
        return dicionarioTrabalho

    def reconheceTextoTrabalhoComumMelhorado(self, trabalho: dict, contadorParaBaixo: int) -> str | None:
        yinicialNome: int = (2 * 70) + 285
        if primeiraBusca(trabalho):
            clickEspecifico(cliques= 3, teclaEspecifica= 'down')
            return self.__imagem.retornaNomeTrabalhoReconhecido(yinicialNome, 1)
        if contadorParaBaixo == 3:
            return self.__imagem.retornaNomeTrabalhoReconhecido(yinicialNome, 1)
        if contadorParaBaixo == 4:
            yinicialNome = (3 * 70) + 285
            return self.__imagem.retornaNomeTrabalhoReconhecido(yinicialNome, 1)
        if contadorParaBaixo > 4:
            return self.__imagem.retornaNomeTrabalhoReconhecido(530, 1)

    def defineDicionarioTrabalhoComumMelhorado(self, dicionarioTrabalho: dict) -> dict:
        trabalhosProducaoPriorizado: list[TrabalhoProducao]= dicionarioTrabalho[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA]
        self.__loggerAplicacao.debug(f'Buscando trabalho {trabalhosProducaoPriorizado[0].raridade}.')
        contadorParaBaixo: int= 0
        if not primeiraBusca(dicionarioTrabalho= dicionarioTrabalho):
            contadorParaBaixo = dicionarioTrabalho[CHAVE_POSICAO]
            clickEspecifico(cliques= contadorParaBaixo, teclaEspecifica= 'down')
        while not chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
            if erroEncontrado(erro= self.verificaErro()):
                self.__confirmacao = False
                return dicionarioTrabalho
            nomeTrabalhoReconhecido: str = self.reconheceTextoTrabalhoComumMelhorado(trabalho= dicionarioTrabalho, contadorParaBaixo= contadorParaBaixo)
            contadorParaBaixo = 3 if primeiraBusca(dicionarioTrabalho) else contadorParaBaixo
            fimLista: bool= False if contadorParaBaixo < 133 else True
            nomeReconhecidoNaoEstaVazioEnaoEhFimLista: bool= nomeTrabalhoReconhecido is not None and not fimLista
            if nomeReconhecidoNaoEstaVazioEnaoEhFimLista:
                self.__loggerAplicacao.debug(f'Trabalho reconhecido: {nomeTrabalhoReconhecido}')
                for trabalhoProducao in trabalhosProducaoPriorizado:
                    self.__loggerAplicacao.debug(f'Trabalho na lista: {trabalhoProducao.id.ljust(36)} | {trabalhoProducao.nome}')
                    if texto1PertenceTexto2(texto1= nomeTrabalhoReconhecido, texto2= trabalhoProducao.nomeProducao):
                        clickEspecifico(cliques= 1, teclaEspecifica= 'enter')
                        dicionarioTrabalho[CHAVE_POSICAO] = contadorParaBaixo - 1
                        dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO] = trabalhoProducao
                        contadorParaBaixo+= 1
                        tipoTrabalho: int= 1 if trabalhoEhProducaoRecursos(trabalho= dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO]) else 0
                        dicionarioTrabalho= self.confirmaNomeTrabalhoProducao(dicionario= dicionarioTrabalho, tipo= tipoTrabalho)
                        if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho= dicionarioTrabalho):
                            return dicionarioTrabalho
                        clickEspecifico(cliques= 1, teclaEspecifica= 'f1')
                clickEspecifico(cliques= 1, teclaEspecifica= 'down')
                dicionarioTrabalho[CHAVE_POSICAO]= contadorParaBaixo
                contadorParaBaixo+= 1
                continue
            if not primeiraBusca(dicionarioTrabalho) and dicionarioTrabalho[CHAVE_POSICAO] > 5:
                self.__loggerTrabalhoProducaoDao.warning(f'Trabalho {dicionarioTrabalho[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA][0].raridade} não reconhecido!')
                return dicionarioTrabalho
            clickEspecifico(cliques= 1, teclaEspecifica= 'down')
            dicionarioTrabalho[CHAVE_POSICAO] = contadorParaBaixo
            contadorParaBaixo += 1
        return dicionarioTrabalho

    def defineCloneTrabalhoProducao(self, trabalhoProducaoEncontrado: TrabalhoProducao) -> TrabalhoProducao:
        cloneTrabalhoProducao = TrabalhoProducao()
        cloneTrabalhoProducao.dicionarioParaObjeto(trabalhoProducaoEncontrado.__dict__)
        cloneTrabalhoProducao.id = str(uuid.uuid4())
        cloneTrabalhoProducao.idTrabalho = trabalhoProducaoEncontrado.idTrabalho
        cloneTrabalhoProducao.recorrencia = False
        self.__loggerTrabalhoProducaoDao.info(f'({trabalhoProducaoEncontrado.id}|{cloneTrabalhoProducao.idTrabalho}|{cloneTrabalhoProducao.nome}|{cloneTrabalhoProducao.nomeProducao}|{cloneTrabalhoProducao.experiencia}|{cloneTrabalhoProducao.nivel}|{cloneTrabalhoProducao.profissao}|{cloneTrabalhoProducao.raridade}|{cloneTrabalhoProducao.trabalhoNecessario}|{cloneTrabalhoProducao.recorrencia}|{cloneTrabalhoProducao.tipoLicenca}|{cloneTrabalhoProducao.estado}) foi clonado')
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
        if not ehVazia(listaDicionarioProfissao):
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
        if trabalho.ehComum:
            if trabalhoEhProducaoRecursos(trabalho):
                return self.atualizaRecursosEstoqueTrabalhoRecursoProduzindo(trabalhoProducao)
            return self.atualizaRecursosEstoqueTrabalhoComumProduzindo(trabalhoProducao)
        if trabalho.ehMelhorado or trabalho.ehRaro:
            if trabalhoEhProducaoRecursos(trabalho):
                return
            return self.atualizaResursosEstoqueTrabalhoMelhoradoRaroProduzindo(trabalho)

    def atualizaResursosEstoqueTrabalhoMelhoradoRaroProduzindo(self, trabalho: Trabalho) -> None:
        listaIdsTrabalhosNecessarios: list[str] = trabalho.trabalhoNecessario.split(',')
        for idTrabalhoNecessario in listaIdsTrabalhosNecessarios:
            trabalhoEncontrado: TrabalhoEstoque = self.pegaTrabalhoEstoquePorIdTrabalho(id= idTrabalhoNecessario)
            if trabalhoEncontrado is None:
                continue
            if trabalhoEncontrado.idTrabalho == idTrabalhoNecessario:
                trabalhoEncontrado.setQuantidade(trabalhoEncontrado.quantidade - 1)
                if self.modificaTrabalhoEstoque(trabalhoEncontrado):
                    print(f'Quantidade do trabalho ({trabalhoEncontrado.idTrabalho}) atualizada para {trabalhoEncontrado.quantidade}.')
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
            if textoEhIgual(trabalhoEstoque.nome, trabalhoProducao.tipoLicenca):
                novaQuantidade = trabalhoEstoque.quantidade - 1
                print(f'Quantidade de {trabalhoEstoque.nome} atualizada de {trabalhoEstoque.quantidade} para {novaQuantidade}.')
                trabalhoEstoque.quantidade = novaQuantidade
                if self.modificaTrabalhoEstoque(trabalhoEstoque):
                    print(f'Quantidade do trabalho ({trabalhoEstoque.nome}) atualizada para {novaQuantidade}.')

    def atualizaRecursosEstoqueTrabalhoComumProduzindo(self, trabalhoProducao: TrabalhoProducao):
        '''
            Método para atualizar a quantidade de recursos necessários para a produção de trabalhos do tipo "Comum".
            Args:
                trabalhoProducao (TrabalhoProducao): Objeto da classe TrabalhoProducao que contêm os atributos do trabalho comum produzido.
        '''
        trabalho: Trabalho = self.pegaTrabalhoPorId(id= trabalhoProducao.idTrabalho)
        if trabalho is None or trabalho.nome is None:
            return
        trabalhoRecurso: TrabalhoRecurso = self.defineTrabalhoRecurso(trabalho)
        for trabalhoEstoque in self.pegaTrabalhosEstoque():
            if textoEhIgual(trabalhoEstoque.nome, trabalhoRecurso.primario):
                trabalhoEstoque.setQuantidade(trabalhoEstoque.quantidade - trabalhoRecurso.pegaQuantidadePrimario)
                if self.modificaTrabalhoEstoque(trabalhoEstoque):
                    self.__loggerAplicacao.debug(f'Quantidade do trabalho ({trabalhoEstoque}) atualizada.')
                continue
            if textoEhIgual(trabalhoEstoque.nome, trabalhoRecurso.secundario):
                trabalhoEstoque.setQuantidade(trabalhoEstoque.quantidade - trabalhoRecurso.pegaQuantidadeSecundario)
                if self.modificaTrabalhoEstoque(trabalhoEstoque):
                    self.__loggerAplicacao.debug(f'Quantidade do trabalho ({trabalhoEstoque}) atualizada.')
                continue
            if textoEhIgual(trabalhoEstoque.nome, trabalhoRecurso.terciario):
                trabalhoEstoque.setQuantidade(trabalhoEstoque.quantidade - trabalhoRecurso.pegaQuantidadeTerciario)
                if self.modificaTrabalhoEstoque(trabalhoEstoque):
                    self.__loggerAplicacao.debug(f'Quantidade do trabalho ({trabalhoEstoque}) atualizada.')
                continue
            if textoEhIgual(trabalhoEstoque.nome, trabalhoProducao.tipoLicenca):
                trabalhoEstoque.setQuantidade(trabalhoEstoque.quantidade - 1)
                if self.modificaTrabalhoEstoque(trabalhoEstoque):
                    self.__loggerAplicacao.debug(f'Quantidade do trabalho ({trabalhoEstoque}) atualizada.')

    def trataMenuLicenca(self, trabalhoProducaoEncontrado: TrabalhoProducao) -> TrabalhoProducao:
        print(f"Buscando: {trabalhoProducaoEncontrado.tipoLicenca}")
        textoReconhecido: str = self.__imagem.retornaTextoLicencaReconhecida()
        if variavelExiste(variavel= textoReconhecido):
            print(f'Licença reconhecida: {textoReconhecido}')
            if texto1PertenceTexto2(texto1= 'Licença de Artesanato', texto2= textoReconhecido):
                primeiraBusca: bool = True
                listaCiclo: list[str] = []
                while not texto1PertenceTexto2(texto1= textoReconhecido, texto2= trabalhoProducaoEncontrado.tipoLicenca):
                    primeiraBusca = False
                    listaCiclo.append(textoReconhecido)
                    clickEspecifico(cliques= 1, teclaEspecifica= "right")
                    textoReconhecido: str = self.__imagem.retornaTextoLicencaReconhecida()
                    if variavelExiste(variavel= textoReconhecido):
                        print(f'Licença reconhecida: {textoReconhecido}.')
                        if textoEhIgual(texto1= textoReconhecido, texto2= 'nenhumitem'):
                            if textoEhIgual(texto1= trabalhoProducaoEncontrado.tipoLicenca, texto2= CHAVE_LICENCA_NOVATO):
                                if textoEhIgual(texto1= listaCiclo[-1], texto2= 'nenhumitem'):
                                    continue
                                self.__loggerTrabalhoProducaoDao.warning(f'Licença ({trabalhoProducaoEncontrado.tipoLicenca}) não encontrado')
                                self.__personagemEmUso.alternaEstado
                                self.modificaPersonagem()
                                clickEspecifico(cliques= 3, teclaEspecifica= 'f1')
                                clickContinuo(cliques= 10, teclaEspecifica= 'up')
                                clickEspecifico(cliques= 1, teclaEspecifica= 'left')
                                self.__confirmacao = False
                                return trabalhoProducaoEncontrado
                            self.__loggerTrabalhoProducaoDao.warning(f'Licença ({trabalhoProducaoEncontrado.tipoLicenca}) não encontrado')
                            self.__loggerTrabalhoProducaoDao.info(f'Licença ({trabalhoProducaoEncontrado.tipoLicenca}) modificado para ({CHAVE_LICENCA_NOVATO})')
                            trabalhoProducaoEncontrado.tipoLicenca = CHAVE_LICENCA_NOVATO
                            continue
                        if len(listaCiclo) > 15:
                            self.__loggerTrabalhoProducaoDao.warning(f'Licença ({trabalhoProducaoEncontrado.tipoLicenca}) não encontrado')
                            self.__loggerTrabalhoProducaoDao.info(f'Licença ({trabalhoProducaoEncontrado.tipoLicenca}) modificado para ({CHAVE_LICENCA_NOVATO})')
                            trabalhoProducaoEncontrado.tipoLicenca = CHAVE_LICENCA_NOVATO
                        continue
                    erro: int = self.verificaErro()
                    if ehErroOutraConexao(erro= erro):
                        self.__unicaConexao = False
                    self.__loggerTrabalhoProducaoDao.error(f'Erro ({erro}) encontrado ao buscar licença necessária')
                    self.__confirmacao = False
                    return trabalhoProducaoEncontrado
                trabalhoProducaoEncontrado.estado = CODIGO_PRODUZINDO
                clickEspecifico(cliques= 1, teclaEspecifica= "f1") if primeiraBusca else clickEspecifico(cliques= 1, teclaEspecifica= "f2")
                return trabalhoProducaoEncontrado
            self.__loggerTrabalhoProducaoDao.warning(f'Licença ({trabalhoProducaoEncontrado.tipoLicenca}) não encontrado')
            self.__personagemEmUso.alternaEstado
            self.modificaPersonagem()
            clickEspecifico(cliques= 3, teclaEspecifica= 'f1')
            clickContinuo(cliques= 10, teclaEspecifica= 'up')
            clickEspecifico(cliques= 1, teclaEspecifica= 'left')
            self.__confirmacao = False
            return trabalhoProducaoEncontrado
        self.__loggerTrabalhoProducaoDao.warning(f'Licença ({trabalhoProducaoEncontrado.tipoLicenca}) não encontrado')
        self.__confirmacao = False
        return trabalhoProducaoEncontrado
    
    def trataMenuTrabalhosAtuais(self, trabalho: TrabalhoProducao) -> None:
        self.verificaNovamente = True
        self.removeTrabalhoProducaoEstoque(trabalhoProducao= trabalho)
        if trabalho.ehRecorrente:
            self.clonaTrabalhoProducaoEncontrado(trabalhoProducaoEncontrado= trabalho)
            clickContinuo(cliques= 12, teclaEspecifica= 'up')
            return
        self.modificaTrabalhoProducao(trabalho= trabalho)
        clickContinuo(cliques= 12, teclaEspecifica= 'up')

    def trataMenuTrabalhoEspecifico(self, primeiraBusca: bool) -> None:
        if primeiraBusca:
            print(f'Entra menu licença.')
            clickEspecifico(cliques= 1, teclaEspecifica= 'up')
            clickEspecifico(cliques= 1, teclaEspecifica= 'enter')
            return
        clickEspecifico(cliques= 1, teclaEspecifica= 'f2')

    def iniciaProcessoDeProducao(self, dicionarioTrabalho: dict) -> dict:
        primeiraBusca: bool = True
        trabalhoProducaoEncontrado: TrabalhoProducao = dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO]
        while True:
            self.trataErrosProcessoDeProducao(trabalho= trabalhoProducaoEncontrado)
            if not self.__confirmacao or self.verificaNovamente:
                break
            menu: int = self.retornaMenu()
            if ehMenuTrabalhosAtuais(menu= menu): 
                self.trataMenuTrabalhosAtuais(trabalho= trabalhoProducaoEncontrado)
                return dicionarioTrabalho
            if ehMenuTrabalhoEspecifico(menu= menu):
                self.trataMenuTrabalhoEspecifico(primeiraBusca= primeiraBusca)
                primeiraBusca = False
                continue
            if ehMenuLicenca(menu= menu):
                dicionarioTrabalho[CHAVE_TRABALHO_PRODUCAO_ENCONTRADO]= self.trataMenuLicenca(trabalhoProducaoEncontrado)
                continue
            if ehMenuEscolhaEquipamento(menu= menu) or ehMenuAtributosEquipamento(menu= menu):
                clickEspecifico(cliques= 1, teclaEspecifica= 'f2')
                continue
            if ehMenuInicial(menu= menu) or ehMenuJogar(menu= menu):
                self.__confirmacao = False
        return dicionarioTrabalho

    def trataErrosProcessoDeProducao(self, trabalho: TrabalhoProducao) -> None:
        print(f'Tratando possíveis erros...')
        tentativas: int = 1
        erro: int = self.verificaErro()
        while erroEncontrado(erro= erro):
            if ehErroRecursosInsuficiente(erro= erro):
                self.__loggerTrabalhoProducaoDao.warning(f'Não possue recursos necessários ({trabalho})')
                self.verificaNovamente = True
                self.removeTrabalhoProducao(trabalho= trabalho)
                erro = self.verificaErro()
                continue
            if ehErroEspacoProducaoInsuficiente(erro= erro) or ehErroOutraConexao(erro= erro) or ehErroConectando(erro= erro) or ehErroRestauraConexao(erro= erro):
                self.__confirmacao = False
                if ehErroOutraConexao(erro= erro):
                    self.__unicaConexao = False
                    erro = self.verificaErro()
                    continue
                if ehErroConectando(erro= erro):
                    if tentativas > 10:
                        clickEspecifico(cliques= 1, teclaEspecifica= 'enter')
                        tentativas = 0
                    tentativas+=1
            erro = self.verificaErro()

    def retornaListaPossiveisTrabalhos(self, nomeTrabalhoReconhecido: str) -> list[TrabalhoProducao]:
        listaPossiveisTrabalhos: list[TrabalhoProducao] = []
        trabalhos: list[Trabalho] = self.pegaTrabalhosBanco()
        for trabalho in trabalhos:
            if texto1PertenceTexto2(nomeTrabalhoReconhecido[1:-1], trabalho.nomeProducao):
                trabalhoEncontrado: TrabalhoProducao = TrabalhoProducao()
                trabalhoEncontrado.dicionarioParaObjeto(trabalho.__dict__)
                trabalhoEncontrado.id = str(uuid.uuid4())
                trabalhoEncontrado.idTrabalho = trabalho.id
                trabalhoEncontrado.recorrencia = False
                trabalhoEncontrado.tipoLicenca = CHAVE_LICENCA_NOVATO
                trabalhoEncontrado.estado = CODIGO_CONCLUIDO
                listaPossiveisTrabalhos.append(trabalhoEncontrado)
        return listaPossiveisTrabalhos

    def retornaTrabalhoProducaoConcluido(self, nomeTrabalhoReconhecido: str) -> TrabalhoProducao | None:
        listaPossiveisTrabalhosProducao: list[TrabalhoProducao] = self.retornaListaPossiveisTrabalhos(nomeTrabalhoReconhecido= nomeTrabalhoReconhecido)
        if ehVazia(listaPossiveisTrabalhosProducao):
            self.__loggerTrabalhoProducaoDao.warning(f'Falha ao criar lista de possíveis trabalhos concluídos ({nomeTrabalhoReconhecido})...')
            return None
        trabalhosProducao: list[TrabalhoProducao] = self.pegaTrabalhosProducaoParaProduzirProduzindo()
        if trabalhosProducao is None:
            return listaPossiveisTrabalhosProducao[0]
        for possivelTrabalhoProducao in listaPossiveisTrabalhosProducao:
            for trabalhoProduzirProduzindo in trabalhosProducao:
                condicoes = trabalhoProduzirProduzindo.ehProduzindo and textoEhIgual(trabalhoProduzirProduzindo.nome, possivelTrabalhoProducao.nome)
                if condicoes:
                    return trabalhoProduzirProduzindo
        else:
            for trabalhoProducao in listaPossiveisTrabalhosProducao:
                self.__loggerTrabalhoProducaoDao.warning(f'Possível trabalho concluído ({trabalhoProducao.nome}) não encontrado na lista produzindo...')
            return listaPossiveisTrabalhosProducao[0]
    
    def existeEspacoProducao(self) -> bool:
        espacoProducao: int = self.__personagemEmUso.espacoProducao
        trabalhosProducao: list[TrabalhoProducao] = self.pegaTrabalhosProducao()
        for trabalho in trabalhosProducao:
            if trabalho.ehProduzindo:
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
            if self.existeEspacoProducao():
                dicionarioTrabalho[CHAVE_POSICAO] = -1
                self.verificaProfissaoNecessaria(dicionarioTrabalho= dicionarioTrabalho, profissao= profissaoNecessaria)
                continue
            return True

    def verificaProfissaoNecessaria(self, dicionarioTrabalho: dict, profissao: Profissao):
        while self.__confirmacao:
            self.verificaNovamente: bool = False
            self.vaiParaMenuProduzir()
            if not self.__confirmacao or not self.__unicaConexao or not self.existeEspacoProducao(): break
            if self.listaProfissoesFoiModificada(): self.verificaEspacoProducao()
            posicao: int= self.retornaPosicaoProfissaoNecessaria(profissaoNecessaria= profissao)
            if posicao == 0: break
            entraProfissaoEspecifica(posicao)
            self.__loggerAplicacao.debug(menssagem= f'Verificando profissão: {profissao.nome}')
            dicionarioTrabalho[CHAVE_PROFISSAO] = profissao.nome
            dicionarioTrabalho = self.veficaTrabalhosProducaoListaDesejos(dicionarioTrabalho)
            if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho):
                dicionarioTrabalho = self.iniciaProcessoDeProducao(dicionarioTrabalho)
            elif ehMenuTrabalhosDisponiveis(self.retornaMenu()):
                saiProfissaoVerificada(dicionarioTrabalho)
            if self.__confirmacao:
                if self.__unicaConexao and self.__espacoBolsa:
                    if self.__imagem.retornaEstadoTrabalho() == CODIGO_CONCLUIDO:
                        nomeTrabalhoReconhecido: str = self.reconheceRecuperaTrabalhoConcluido()
                        if variavelExiste(variavel= nomeTrabalhoReconhecido):
                            trabalhoProducaoConcluido: TrabalhoProducao = self.retornaTrabalhoProducaoConcluido(nomeTrabalhoReconhecido= nomeTrabalhoReconhecido)
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
        listaDeListasTrabalhosProducao: list[list[TrabalhoProducao]] = self.retornaListaDeListasTrabalhosProducao(nomeProfissao= dicionarioTrabalho[CHAVE_PROFISSAO])
        for listaTrabalhosProducao in listaDeListasTrabalhosProducao:
            dicionarioTrabalho[CHAVE_LISTA_TRABALHOS_PRODUCAO_PRIORIZADA]= listaTrabalhosProducao
            for trabalhoProducaoPriorizado in listaTrabalhosProducao:
                if trabalhoProducaoPriorizado.ehEspecial or trabalhoProducaoPriorizado.ehRaro:
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
                if trabalhoProducaoPriorizado.ehMelhorado or trabalhoProducaoPriorizado.ehComum:
                    dicionarioTrabalho: dict = self.defineDicionarioTrabalhoComumMelhorado(dicionarioTrabalho= dicionarioTrabalho)
                    if chaveDicionarioTrabalhoDesejadoExiste(dicionarioTrabalho) or not self.__confirmacao:
                        return dicionarioTrabalho
                    if listaDeListasTrabalhosProducao.index(listaTrabalhosProducao) + 1 >= len(listaDeListasTrabalhosProducao):
                        vaiParaMenuTrabalhoEmProducao()
                        break
                    vaiParaOTopoDaListaDeTrabalhosComunsEMelhorados(dicionarioTrabalho)
                    dicionarioTrabalho[CHAVE_POSICAO] = -1
                    break
        return dicionarioTrabalho

    def retornaListaDeListasTrabalhosProducao(self, nomeProfissao: str) -> list[list[TrabalhoProducao]]:
        '''
            Função para definir as listas de trabalhos a serem verificados, separados por raridade.
            Returns:
                listaDeListaTrabalhos (list[list[TrabalhoProducao]]): Lista de raridades que contêm uma lista de objetos do tipo TrabalhoProducao
            Args:
                nomeProfissao (str): Nome da profissão à ser verificada no momento
        '''
        listaDeListaTrabalhos: list[list[TrabalhoProducao]] = []
        raridades: list[str]= LISTA_RARIDADES
        raridades.reverse()
        for raridade in raridades:
            listaTrabalhosProducao: list[TrabalhoProducao] = self.retornaListaTrabalhosProducaoRaridadeEspecifica(nomeProfissao= nomeProfissao, raridade= raridade)
            if ehVazia(listaTrabalhosProducao):
                continue
            listaDeListaTrabalhos.append(listaTrabalhosProducao)
        return listaDeListaTrabalhos

    def retiraPersonagemJaVerificadoListaAtivo(self):
        '''
            Esta função é responsável por redefinir a lista de personagens ativos, verificando a lista de personagens já verificados
        '''        
        self.defineListaPersonagensAtivos()
        novaListaPersonagensAtivos: list[Personagem] = []
        if not ehVazia(self.__listaPersonagemAtivo):
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


    def vaiParaMenuJogar(self):
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

    def entraPersonagemAtivo(self) -> bool:
        self.__personagemEmUso = None
        for x in range(5):
            codigoMenu: int = self.retornaMenu()
            if ehMenuDesconhecido(menu= codigoMenu) or ehMenuProduzir(menu= codigoMenu) or ehMenuTrabalhosDisponiveis(menu= codigoMenu) or ehMenuTrabalhosAtuais(menu= codigoMenu): 
                clickMouseEsquerdo(clicks= 1, xTela= 2, yTela= 35)
                continue
            if ehMenuJogar(menu= codigoMenu):
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
                personagemReconhecido: str = self.__imagem.retornaTextoNomePersonagemReconhecido(posicao= 1)
                while variavelExiste(variavel= personagemReconhecido) and contadorPersonagem < 13:
                    self.confirmaNomePersonagem(personagemReconhecido= personagemReconhecido)
                    if self.__personagemEmUso is None:
                        clickEspecifico(cliques= 1, teclaEspecifica= 'right')
                        personagemReconhecido = self.__imagem.retornaTextoNomePersonagemReconhecido(posicao= 1)
                        contadorPersonagem += 1
                        continue
                    clickEspecifico(cliques= 1, teclaEspecifica= 'f2')
                    sleep(1)
                    print(f'Personagem ({self.__personagemEmUso.nome}) encontrado.')
                    tentativas: int = 1
                    erro: int = self.verificaErro()
                    while erroEncontrado(erro= erro):
                        if ehErroOutraConexao(erro= erro):
                            self.__unicaConexao = False
                            contadorPersonagem = 14
                            return False
                        if ehErroConectando(erro= erro):
                            if tentativas > 10:
                                clickEspecifico(cliques= 2, teclaEspecifica= 'enter')
                                tentativas = 0
                            tentativas += 1
                        erro = self.verificaErro()
                        continue
                    print(f'Login efetuado com sucesso!')
                    return True
                print(f'Personagem não encontrado!')
                if ehMenuEscolhaPersonagem(menu= self.retornaMenu()):
                    clickEspecifico(cliques= 1, teclaEspecifica= 'f1')
                    return False
            if ehMenuInicial(menu= codigoMenu): self.deslogaPersonagem(menu= codigoMenu)
            if ehMenuNoticias(menu= codigoMenu) or ehMenuEscolhaPersonagem(menu= codigoMenu): clickEspecifico(cliques= 1, teclaEspecifica= 'f1')
        return False

    def retornaProfissoesPriorizadas(self) -> list[Profissao]:
        profissoesPriorizadas: list[Profissao] = []
        profissoes: list[Profissao] = self.pegaProfissoes()
        for profissao in profissoes:
            if profissao.prioridade:
                self.__loggerProfissaoDao.debug(menssagem= f'Profissão priorizada encontrada: ({profissao.nome})')
                profissoesPriorizadas.append(profissao)
        return profissoesPriorizadas
    
    def pegaTrabalhosPorProfissaoRaridadeNivel(self, trabalho: Trabalho) -> list[Trabalho]:
        trabalhosProfissaoRaridadeNivelExpecifico: list[Trabalho] = self.__trabalhoDao.pegaTrabalhosPorProfissaoRaridadeNivel(trabalho)
        if trabalhosProfissaoRaridadeNivelExpecifico is None:
            self.__loggerTrabalhoDao.error(f'Erro ao buscar trabalhos específicos no banco: {self.__trabalhoDao.pegaErro}')
            return []
        for trabalho in trabalhosProfissaoRaridadeNivelExpecifico:
            self.__loggerTrabalhoDao.debug(menssagem= f'{trabalho.nome} encontrado!')
        return trabalhosProfissaoRaridadeNivelExpecifico
    
    def retornaListaIdsRecursosNecessarios(self, trabalho: Trabalho) -> list[str]:
        idsTrabalhos = self.__trabalhoDao.retornaListaIdsRecursosNecessarios(trabalho)
        if idsTrabalhos is None:
            self.__loggerTrabalhoDao.error(f'Erro ao buscar ids de recursos necessários ({trabalho.profissao}, {trabalho.nivel}): {self.__trabalhoDao.pegaErro}')
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
        trabalhosProduzindo = self.__trabalhoProducaoDao.pegaTrabalhosParaProduzirPorProfissaoRaridade(personagem= personagem, trabalho= trabalho)
        if trabalhosProduzindo is None:
            self.__loggerTrabalhoProducaoDao.error(f'Erro ao buscar trabalhos produzindo por profissão e raridade ({trabalho.profissao}, {trabalho.raridade}): {self.__trabalhoProducaoDao.pegaErro}')
            return []
        return trabalhosProduzindo

    def verificaRecursosNecessarios(self, trabalho: Trabalho) -> bool:
        trabalhoBuscado: Trabalho= Trabalho()
        trabalhoBuscado.nivel = trabalho.nivel
        trabalhoBuscado.profissao = trabalho.profissao
        trabalhoBuscado.raridade = trabalho.raridade
        if trabalhoBuscado.ehComum:
            quantidadeRecursosContingencia: int = 0
            for trabalhoParaProduzir in self.pegaTrabalhosParaProduzirPorProfissaoRaridade(trabalhoBuscado):
                quantidadeRecursosContingencia += trabalhoParaProduzir.pegaQuantidadeRecursosNecessarios() + 2
            quantidadeRecursosContingencia += trabalhoBuscado.pegaQuantidadeRecursosNecessarios() + 2
            trabalhoBuscado.nivel = 1 if trabalhoBuscado.nivel < 16 else 8
            idsRecursosNecessarios: list[str] = self.retornaListaIdsRecursosNecessarios(trabalhoBuscado)
            if len(idsRecursosNecessarios) < 3:
                return False
            dicionariosRecursosNecessarios: list[dict] = self.retornaListaDicionariosRecursosNecessarios(idsRecursosNecessarios)
            for dicionario in dicionariosRecursosNecessarios:
                if self.pegaQuantidadeTrabalhoEstoque(idTrabalho= dicionario[CHAVE_ID_TRABALHO]) < quantidadeRecursosContingencia:
                    return False
            return True
        return False
    
    def defineTrabalhoProducaoRecursosProfissaoPriorizada(self, trabalho: Trabalho):
        '''
            Função para definir trabalho para produção de recursos de acordo com o nível e profissão da profissão priorizada atual
            Args:
                trabalho (Trabalho): Objeto da classe Trabalho que contêm os atributos da profissão priorizada necessários para definição do seu trabalho para produção de recursos respectivo.
        '''
        nivel: int = 3 if trabalho.nivel < 16 else 10
        trabalho.raridade = CHAVE_RARIDADE_RARO
        trabalho.nivel = nivel
        trabalhoProducaoRecursosEncontrado: Trabalho= self.defineTrabalhoProducaoRecurso(trabalho= trabalho)
        if trabalhoProducaoRecursosEncontrado is None:
            self.__loggerTrabalhoProducaoDao.warning(f'Trabalho para produção de recursos (nível {nivel}, profissão {trabalho.profissao}, raridade {trabalho.raridade}) não encontrado!')
            return
        self.__loggerTrabalhoProducaoDao.debug(f'Trabalho para produção de recusos ({trabalhoProducaoRecursosEncontrado.nome}) encontrado!')
        trabalhosProducaoEncontrados: list[TrabalhoProducao] = self.pegaTrabalhosProducaoPorIdTrabalho(id= trabalhoProducaoRecursosEncontrado.id)
        if ehVazia(lista= trabalhosProducaoEncontrados):
            self.__loggerTrabalhoProducaoDao.debug(f'{trabalhoProducaoRecursosEncontrado.nome} não encontrado na lista para produção.')
        for trabalhoEncontrado in trabalhosProducaoEncontrados:
            if trabalhoEncontrado.ehParaProduzir:
                self.__loggerTrabalhoProducaoDao.debug(f'{trabalhoEncontrado.nome} já existe na lista para produção.')
                return
        trabalhoProducao: TrabalhoProducao= self.defineTrabalhoProducaoRecursosEspecfico(trabalhoProducaoRecursosEncontrado)
        self.insereTrabalhoProducao(trabalho= trabalhoProducao)

    def defineTrabalhoProducaoRecursosEspecfico(self, trabalhoEncontrado: Trabalho) -> TrabalhoProducao:
        '''
            Função para definir um objeto da classe TrabalhoProducao com atributos do trabalho para produção de recursos encontrado
            Args:
                trabalhoEncontrado (Trabalho): Objeto da classe Trabalho com atributos do trabalho para produção de recursos encontrado.
            Returns:
                trabalhoProducao (TrabalhoProducao): Objeto da classe TrabalhoProducao com atributos do trabalho para produção de recursos encontrado.
        '''
        trabalhoProducao: TrabalhoProducao = TrabalhoProducao()
        trabalhoProducao.idTrabalho = trabalhoEncontrado.id
        trabalhoProducao.recorrencia = True
        trabalhoProducao.tipoLicenca = CHAVE_LICENCA_APRENDIZ
        trabalhoProducao.estado = CODIGO_PARA_PRODUZIR
        return trabalhoProducao

    def defineTrabalhoProducaoRecurso(self, trabalho: Trabalho) -> Trabalho | None:
        '''
            Função para encontrado no banco um trabalho de produção de recursos de profissão, nível e raridade específica
            Args:
                trabalho (Trabalho): Objeto da classe Trabalho que contêm os atributos necessários para a busca (profissao, nivel, raridade)
            Returns:
                trabalhoEncontrado (Trabalho): Objeto da classe Trabalho com atributos do trabalho para produção de recursos encontrado.
        '''
        trabalhosProducaoRecursosEncontrados: list[Trabalho] = self.pegaTrabalhosPorProfissaoRaridadeNivel(trabalho= trabalho)
        trabalhoEncontrado: Trabalho = None
        for trabalho in trabalhosProducaoRecursosEncontrados:
            if trabalhoEhProducaoRecursos(trabalho= trabalho):
                trabalhoEncontrado= trabalho
                break
        return trabalhoEncontrado

    def defineTrabalhoComumProfissaoPriorizada(self):
        profissoesPriorizadas: list[Profissao] = self.retornaProfissoesPriorizadas()
        if ehVazia(profissoesPriorizadas):
            self.__loggerProfissaoDao.warning(f'Nem uma profissão priorizada encontrada!')
            return
        for profissaoPriorizada in profissoesPriorizadas:
            self.__loggerProfissaoDao.debug(menssagem= f'Verificando profissão priorizada: {profissaoPriorizada.nome}')
            nivelProfissao: int = profissaoPriorizada.pegaNivel()
            trabalhoBuscado: Trabalho = self.defineTrabalhoComumBuscado(profissaoPriorizada, nivelProfissao)
            trabalhosComunsProfissaoNivelExpecifico: list[Trabalho] = self.pegaTrabalhosPorProfissaoRaridadeNivel(trabalhoBuscado)
            if ehVazia(trabalhosComunsProfissaoNivelExpecifico):
                self.__loggerProfissaoDao.warning(f'Nem um trabalho nível ({trabalhoBuscado.nivel}), raridade (comum) e profissão ({trabalhoBuscado.profissao}) foi encontrado!')
                continue
            while True:
                trabalhosQuantidade: list[TrabalhoEstoque]= self.defineListaTrabalhosQuantidade(trabalhosComunsProfissaoNivelExpecifico)
                trabalhosQuantidade= self.atualizaListaTrabalhosQuantidadeEstoque(trabalhosQuantidade)
                trabalhosQuantidade, quantidadeTotalTrabalhoProducao= self.atualizaListaTrabalhosQuantidadeTrabalhosProducao(trabalhosQuantidade)
                trabalhosQuantidade= sorted(trabalhosQuantidade, key=lambda trabalho: trabalho.quantidade)
                quantidadeTrabalhosEmProducaoEhMaiorIgualAoTamanhoListaTrabalhosComuns = quantidadeTotalTrabalhoProducao >= len(trabalhosComunsProfissaoNivelExpecifico)
                if quantidadeTrabalhosEmProducaoEhMaiorIgualAoTamanhoListaTrabalhosComuns:
                    self.__loggerProfissaoDao.debug(menssagem= f'Existem ({quantidadeTotalTrabalhoProducao}) ou mais trabalhos sendo produzidos!')
                    break
                trabalhoComum: TrabalhoProducao = self.defineTrabalhoProducaoComum(trabalhosQuantidade)
                if nivelProfissao == 1 or nivelProfissao == 8:
                    self.__loggerProfissaoDao.warning(f'Nível de produção de ({profissaoPriorizada.nome}) é 1 ou 8')
                    trabalhoComum.tipoLicenca = CHAVE_LICENCA_APRENDIZ
                    self.insereTrabalhoProducao(trabalhoComum)
                    continue
                existeRecursosNecessarios = self.verificaRecursosNecessarios(trabalho= trabalhoBuscado)
                if existeRecursosNecessarios:
                    self.insereTrabalhoProducao(trabalhoComum)
                    continue
                self.__loggerProfissaoDao.debug(f'Recursos necessários insuficientes para produzir {trabalhosComunsProfissaoNivelExpecifico[0].nome}')
                self.defineTrabalhoProducaoRecursosProfissaoPriorizada(trabalho= trabalhoBuscado)
                break

    def defineTrabalhoComumBuscado(self, profissaoPriorizada: Profissao, nivelProfissao: int) -> Trabalho:
        trabalhoBuscado = Trabalho()
        trabalhoBuscado.profissao = profissaoPriorizada.nome
        trabalhoBuscado.nivel = trabalhoBuscado.pegaNivel(nivelProfissao)
        trabalhoBuscado.raridade = CHAVE_RARIDADE_COMUM
        return trabalhoBuscado

    def defineTrabalhoProducaoComum(self, trabalhosQuantidade: list[TrabalhoEstoque]) -> TrabalhoProducao:
        trabalhoComum = TrabalhoProducao()
        trabalhoComum.idTrabalho = trabalhosQuantidade[0].idTrabalho
        trabalhoComum.estado = CODIGO_PARA_PRODUZIR
        trabalhoComum.recorrencia = False
        trabalhoComum.tipoLicenca = CHAVE_LICENCA_NOVATO
        return trabalhoComum
    
    def pegaQuantidadeTrabalhoProducaoProduzirProduzindo(self, idTrabalho: str, personagem: Personagem = None) -> int:
        personagem = self.__personagemEmUso if personagem is None else personagem
        quantidade = self.__trabalhoProducaoDao.pegaQuantidadeTrabalhoProducaoProduzirProduzindo(personagem= personagem, idTrabalho= idTrabalho)
        if quantidade is None:
            self.__loggerTrabalhoProducaoDao.error(f'Erro ao buscar quantidade trabalho para produção por id ({idTrabalho}): {self.__trabalhoProducaoDao.pegaErro}')
            return 0
        return quantidade

    def atualizaListaTrabalhosQuantidadeTrabalhosProducao(self, trabalhosQuantidade: list[TrabalhoEstoque]):
        quantidadeTotalTrabalhoProducao: int= 0
        for trabalhoQuantidade in trabalhosQuantidade:
            quantidade = self.pegaQuantidadeTrabalhoProducaoProduzirProduzindo(trabalhoQuantidade.idTrabalho)
            trabalhoQuantidade.quantidade += quantidade
            quantidadeTotalTrabalhoProducao += quantidade
        return trabalhosQuantidade, quantidadeTotalTrabalhoProducao
    
    def pegaQuantidadeTrabalhoEstoque(self, idTrabalho: str, personagem: Personagem = None) -> int:
        personagem = self.__personagemEmUso if personagem is None else personagem
        quantidade = self.__estoqueDao.pegaQuantidadeTrabalho(personagem= personagem, idTrabalho= idTrabalho)
        if quantidade is None:
            self.__loggerEstoqueDao.error(f'Erro ao buscar quantidade ({idTrabalho}) no estoque: {self.__estoqueDao.pegaErro}')
            return 0
        return quantidade

    def atualizaListaTrabalhosQuantidadeEstoque(self, trabalhosQuantidade: list[TrabalhoEstoque]) -> list[TrabalhoEstoque]:
        for trabalhoQuantidade in trabalhosQuantidade:
            quantidade: int= self.pegaQuantidadeTrabalhoEstoque(idTrabalho= trabalhoQuantidade.idTrabalho)
            trabalhoQuantidade.quantidade += quantidade
            self.__loggerEstoqueDao.debug(menssagem= f'Quantidade de ({trabalhoQuantidade.idTrabalho}) encontrada: ({trabalhoQuantidade.quantidade})')
        return trabalhosQuantidade

    def defineListaTrabalhosQuantidade(self, trabalhosComunsProfissaoNivelExpecifico: list[Trabalho]) -> list[TrabalhoEstoque]:
        trabalhosQuantidade: list[TrabalhoEstoque] = []
        for trabalhoComum in trabalhosComunsProfissaoNivelExpecifico:
            trabalhoQuantidade = TrabalhoEstoque()
            trabalhoQuantidade.idTrabalho = trabalhoComum.id
            trabalhoQuantidade.quantidade = 0
            trabalhosQuantidade.append(trabalhoQuantidade)
        return trabalhosQuantidade
    
    def listaPersonagemJaVerificadoEPersonagemAnteriorEAtualMesmoEmail(self) -> bool:
        '''
            Função para verificar se o email do último personagem que foi verificado é igual ao email do próximo personagem na lista de ativos
            Returns:
                bool: Verdadeiro caso o último email verificado seja igual ao próximo email a ser verificado
        '''
        if ehVazia(self.__listaPersonagemJaVerificado) or ehVazia(self.__listaPersonagemAtivo):
            return False
        emailAnterior: str= self.__listaPersonagemJaVerificado[-1].email
        emailProximo: str= self.__listaPersonagemAtivo[0].email
        emailDoUltimoPersonagemEhIgualAoEmailPrimeiroPersonagemDaListaDeAtivos = textoEhIgual(texto1= emailAnterior, texto2= emailProximo)
        resultado: str= 'Igual' if emailDoUltimoPersonagemEhIgualAoEmailPrimeiroPersonagemDaListaDeAtivos else 'Diferente'
        self.__loggerAplicacao.debug(menssagem= f'Resultado: {resultado}. Email personagem anterior | próximo: ({emailAnterior}) | ({emailProximo})')
        if emailDoUltimoPersonagemEhIgualAoEmailPrimeiroPersonagemDaListaDeAtivos:
            return self.entraPersonagemAtivo()
        return False
    
    def listaPersonagensAtivosEstaVazia(self) -> bool:
        if ehVazia(self.__listaPersonagemAtivo):
            self.__listaPersonagemJaVerificado.clear()
            return True
        return False
    
    def personagemEmUsoExiste(self) -> bool:
        if self.__personagemEmUso is None: return False
        self.modificaAtributoUso()
        self.__loggerAplicacao.debug(f'Personagem ({self.__personagemEmUso.id.ljust(36)} | {self.__personagemEmUso.nome}) ESTÁ EM USO.')
        self.inicializaChavesPersonagem()
        print('Inicia busca...')
        if self.vaiParaMenuProduzir():
            self.defineTrabalhoComumProfissaoPriorizada()
            trabalhosProducao: list[TrabalhoProducao]= self.pegaTrabalhosProducaoParaProduzirProduzindo()
            if trabalhosProducao is None: return True
            if ehVazia(trabalhosProducao):
                print(f'Lista de trabalhos desejados vazia.')
                self.__personagemEmUso.alternaEstado
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
            self.verificaAlteracaoTrabalhos()
            self.verificaAlteracaoProducao()
            self.verificaAlteracaoPersonagens()
            self.verificaAlteracaoProfissoes()
            self.verificaAlteracaoEstoque()
            self.verificaAlteracaoVendas()
            self.retiraPersonagemJaVerificadoListaAtivo()
            if self.listaPersonagensAtivosEstaVazia(): continue
            self.definePersonagemEmUso()
            if self.personagemEmUsoExiste(): continue
            self.retiraPersonagemJaVerificadoListaAtivo()
            if self.listaPersonagensAtivosEstaVazia(): continue
            if self.listaPersonagemJaVerificadoEPersonagemAnteriorEAtualMesmoEmail(): continue
            if self.configuraEntraPersonagem(): self.entraPersonagemAtivo()

    def insereTrabalho(self, trabalho: Trabalho, modificaServidor: bool = True) -> bool:
        if self.__trabalhoDao.insereTrabalho(trabalho, modificaServidor):
            self.__loggerTrabalhoDao.info(f'({trabalho.id.ljust(36)} | {trabalho}) inserido no banco com sucesso!')
            return True
        self.__loggerTrabalhoDao.error(f'Erro ao inserir ({trabalho.id.ljust(36)} | {trabalho}) no banco: {self.__trabalhoDao.pegaErro}')
        return False

    def removeTrabalho(self, trabalho: Trabalho, modificaServidor: bool = True) -> bool:
        if self.__trabalhoDao.removeTrabalho(trabalho= trabalho, modificaServidor= modificaServidor):
            self.__loggerTrabalhoDao.info(f'({trabalho.id.ljust(36)} | {trabalho}) removido do banco com sucesso!')
            return True
        self.__loggerTrabalhoDao.error(f'Erro ao remover ({trabalho.id.ljust(36)} | {trabalho}) do banco: {self.__trabalhoDao.pegaErro}')
        return False

    def verificaAlteracaoTrabalhos(self):
        # self.__loggerTrabalhoDao.debug(f'Verificando alterações na lista de trabalhos...')
        if self.__repositorioTrabalho.estaPronto:
            trabalhos: list[dict]= self.__repositorioTrabalho.pegaDadosModificados()
            for trabalho in trabalhos:
                if len(trabalho) == 1:
                    trabalhoEncontrado = self.pegaTrabalhoPorId(id= trabalho[CHAVE_ID])
                    if trabalhoEncontrado is None:
                        continue
                    self.removeTrabalho(trabalho= trabalhoEncontrado, modificaServidor= False)
                    continue
                trabalhoEncontrado = self.pegaTrabalhoPorId(id= trabalho[CHAVE_ID])
                if trabalhoEncontrado is None:
                    continue
                if trabalhoEncontrado.id == trabalho[CHAVE_ID]:
                    trabalhoEncontrado.dicionarioParaObjeto(trabalho)
                    self.modificaTrabalho(trabalho= trabalhoEncontrado, modificaServidor= False)
                    continue
                trabalhoEncontrado.dicionarioParaObjeto(trabalho)
                self.insereTrabalho(trabalho= trabalhoEncontrado, modificaServidor= False)
            self.__repositorioTrabalho.limpaLista
            
    def verificaAlteracaoPersonagens(self):
        # self.__loggerProfissaoDao.debug(f'Verificando alterações na lista de personagens...')
        if self.__repositorioPersonagem.estaPronto:
            personagens: list[dict]= self.__repositorioPersonagem.pegaDadosModificados()
            for personagem in personagens:
                if len(personagem) == 1:
                    personagemEncontrado: Personagem= self.pegaPersonagemPorId(id= personagem[CHAVE_ID])
                    if personagemEncontrado is None:
                        continue
                    self.removePersonagem(personagem= personagemEncontrado, modificaServidor= False)
                    continue
                if self.__repositorioUsuario.verificaIdPersonagem(id= personagem[CHAVE_ID]):
                    personagemEncontrado: Personagem= self.pegaPersonagemPorId(id= personagem[CHAVE_ID])
                    if personagemEncontrado is None:
                        continue
                    if personagemEncontrado.id == personagem[CHAVE_ID]:
                        personagemEncontrado.dicionarioParaObjeto(personagem)
                        self.modificaPersonagem(personagem= personagemEncontrado, modificaServidor= False)
                        continue
                    personagemEncontrado.dicionarioParaObjeto(personagem)
                    self.inserePersonagem(personagem= personagemEncontrado, modificaServidor= False)
            self.__repositorioPersonagem.limpaLista
    
    def verificaAlteracaoProfissoes(self):
        # self.__loggerRepositorioProducao.debug(f'Verificando alterações na lista de trabalhos de produção...')
        if self.__repositorioProfissao.estaPronto:
            dicionariosProfissoes: list[dict]= self.__repositorioProfissao.pegaDadosModificados()
            for dicionarioProfissao in dicionariosProfissoes:
                personagem: Personagem= Personagem()
                personagem.id= dicionarioProfissao[CHAVE_ID_PERSONAGEM]
                if dicionarioProfissao[CHAVE_TRABALHOS] is None:
                    self.removeProfissoesPorIdPersonagem(personagem= personagem)
                    continue
                if self.__repositorioUsuario.verificaIdPersonagem(id= personagem.id):
                    dicionario: dict= dicionarioProfissao[CHAVE_TRABALHOS]
                    profissaoEncontrada: Profissao= self.pegaProfissaoPorId(id= dicionario[CHAVE_ID], personagem= personagem)
                    if profissaoEncontrada is None:
                        continue
                    if profissaoEncontrada.experiencia is None:
                        profissaoEncontrada.idPersonagem= personagem.id
                        self.removeProfissao(profissao= profissaoEncontrada, personagem= personagem, modificaServidor= False)
                        continue
                    if profissaoEncontrada.id == dicionario[CHAVE_ID]:
                        profissaoEncontrada.dicionarioParaObjeto(dicionario)
                        self.modificaProfissao(profissao= profissaoEncontrada, personagem= personagem, modificaServidor= False)
                        continue
                    profissaoEncontrada.nome= self.pegaNomeProfissaoPorId(id= profissaoEncontrada.id)
                    self.insereProfissao(profissao= profissaoEncontrada, personagem= personagem, modificaServidor= False)
            self.__repositorioProfissao.limpaLista
    
    def verificaAlteracaoEstoque(self):
        # self.__loggerRepositorioEstoque.debug(f'Verificando alterações na lista de trabalhos de produção...')
        if self.__repositorioEstoque.estaPronto:
            dicionariosEstoque: list[dict]= self.__repositorioEstoque.pegaDadosModificados()
            for dicionario in dicionariosEstoque:
                personagem: Personagem= Personagem()
                personagem.id= dicionario[CHAVE_ID_PERSONAGEM]
                if dicionario[CHAVE_TRABALHOS] is None:
                    self.removeEstoquePorIdPersonagem(personagem= personagem)
                    continue
                if self.__repositorioUsuario.verificaIdPersonagem(id= personagem.id):
                    dicionarioTrabalho: dict = dicionario[CHAVE_TRABALHOS]
                    trabalhoEncontrado: TrabalhoEstoque= self.pegaTrabalhoEstoquePorId(id= dicionarioTrabalho[CHAVE_ID])
                    if trabalhoEncontrado is None:
                        continue
                    if trabalhoEncontrado.idTrabalho is None:
                        self.removeTrabalhoEstoque(trabalho= trabalhoEncontrado, personagem= personagem, modificaServidor= False)
                        continue
                    if trabalhoEncontrado.id == dicionarioTrabalho[CHAVE_ID]:
                        trabalhoEncontrado.dicionarioParaObjeto(dicionarioTrabalho)
                        self.modificaTrabalhoEstoque(trabalho= trabalhoEncontrado, personagem= personagem, modificaServidor= False)
                        continue
                    trabalhoEncontrado.dicionarioParaObjeto(dicionarioTrabalho)
                    self.insereTrabalhoEstoque(trabalho= trabalhoEncontrado, personagem= personagem, modificaServidor= False)
            self.__repositorioEstoque.limpaLista
    
    def verificaAlteracaoProducao(self):
        # self.__loggerRepositorioProducao.debug(f'Verificando alterações na lista de trabalhos de produção...')
        if self.__repositorioProducao.estaPronto:
            dicionariosProducoes: list[dict]= self.__repositorioProducao.pegaDadosModificados()
            for dicionarioProducao in dicionariosProducoes:
                personagem: Personagem= Personagem()
                personagem.id= dicionarioProducao[CHAVE_ID_PERSONAGEM]
                if dicionarioProducao[CHAVE_TRABALHOS] is None:
                    self.removeProducoesPorIdPersonagem(personagem= personagem)
                    continue
                if self.__repositorioUsuario.verificaIdPersonagem(id= personagem.id):
                    dicionarioTrabalho: dict= dicionarioProducao[CHAVE_TRABALHOS]
                    trabalhoEncontrado: TrabalhoProducao= self.pegaTrabalhoProducaoPorId(id= dicionarioTrabalho[CHAVE_ID])
                    if trabalhoEncontrado is None:
                        continue
                    if trabalhoEncontrado.idTrabalho is None:
                        self.removeTrabalhoProducao(trabalho= trabalhoEncontrado, personagem= personagem, modificaServidor= False)
                        continue
                    if trabalhoEncontrado.id == dicionarioTrabalho[CHAVE_ID]:
                        trabalhoEncontrado.dicionarioParaObjeto(dicionarioTrabalho)
                        self.modificaTrabalhoProducao(trabalho= trabalhoEncontrado, personagem= personagem, modificaServidor= False)
                        continue
                    trabalhoEncontrado.dicionarioParaObjeto(dicionarioTrabalho)
                    self.insereTrabalhoProducao(trabalho= trabalhoEncontrado, personagem= personagem, modificaServidor= False)
            self.__repositorioProducao.limpaLista
    
    def verificaAlteracaoVendas(self):
        # self.__loggerRepositorioVendas.debug(f'Verificando alterações na lista de trabalhos de produção...')
        if self.__repositorioVendas.estaPronto:
            dicionariosVendas: list[dict]= self.__repositorioVendas.pegaDadosModificados()
            for dicionario in dicionariosVendas:
                personagem: Personagem= Personagem()
                personagem.id= dicionario[CHAVE_ID_PERSONAGEM]
                if dicionario[CHAVE_TRABALHOS] is None:
                    self.removeVendasPorIdPersonagem(personagem= personagem)
                    continue
                if self.__repositorioUsuario.verificaIdPersonagem(id= personagem.id):
                    dicionarioTrabalho: dict= dicionario[CHAVE_TRABALHOS]
                    trabalhoEncontrado: TrabalhoVendido= self.pegaTrabalhoVendidoPorId(id= dicionarioTrabalho[CHAVE_ID])
                    if trabalhoEncontrado is None:
                        continue
                    if trabalhoEncontrado.idTrabalho is None:
                        self.removeTrabalhoVendido(trabalho= trabalhoEncontrado, personagem= personagem, modificaServidor= False)
                        continue
                    if trabalhoEncontrado.id == dicionarioTrabalho[CHAVE_ID]:
                        trabalhoEncontrado.dicionarioParaObjeto(dicionarioTrabalho)
                        self.modificaTrabalhoVendido(trabalho= trabalhoEncontrado, personagem= personagem, modificaServidor= False)
                        continue
                    trabalhoEncontrado.dicionarioParaObjeto(dicionarioTrabalho)
                    self.insereTrabalhoVendido(trabalho= trabalhoEncontrado, personagem= personagem, modificaServidor= False)
            self.__repositorioVendas.limpaLista
    
    def modificaPersonagem(self, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        if self.__personagemDao.modificaPersonagem(personagem= personagem, modificaServidor= modificaServidor):
            self.__loggerPersonagemDao.info(f'({personagem}) modificado no banco com sucesso!')
            return True
        self.__loggerPersonagemDao.error(f'Erro ao modificar ({personagem}) no banco: {self.__personagemDao.pegaErro}')
        return False

    def inserePersonagem(self, personagem: Personagem, modificaServidor: bool = True) -> bool:
        if self.__personagemDao.inserePersonagem(personagem= personagem, modificaServidor= modificaServidor):
            self.__loggerPersonagemDao.info(f'({personagem}) inserido no banco com sucesso!')
            return True
        self.__loggerPersonagemDao.error(f'Erro ao inserir ({personagem}) no banco: {self.__personagemDao.pegaErro}')
        return False
        
    def removeTrabalhoEstoque(self, trabalho: TrabalhoEstoque, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        if self.__estoqueDao.removeTrabalhoEstoque(personagem= personagem, trabalhoEstoque= trabalho, modificaServidor= modificaServidor):
            self.__loggerEstoqueDao.info(f'({personagem.id.ljust(36)} | {trabalho}) removido do banco com sucesso!')
            return True
        self.__loggerEstoqueDao.error(f'Erro ao remover ({personagem.id.ljust(36)} | {trabalho}) do banco: {self.__estoqueDao.pegaErro}')
        return False

    def modificaTrabalhoEstoque(self, trabalho: TrabalhoEstoque, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        if self.__estoqueDao.modificaTrabalhoEstoque(personagem= personagem, trabalho= trabalho, modificaServidor= modificaServidor):
            self.__loggerEstoqueDao.info(f'({personagem.id.ljust(36)} | {trabalho}) modificado no banco com sucesso!')
            return True
        self.__loggerEstoqueDao.error(f'Erro ao modificar ({personagem.id.ljust(36)} | {trabalho}) no banco: {self.__estoqueDao.pegaErro}')
        return False
        
    def insereTrabalhoEstoque(self, trabalho: TrabalhoEstoque, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        if self.__estoqueDao.insereTrabalhoEstoque(personagem= personagem, trabalho= trabalho, modificaServidor= modificaServidor):
            self.__loggerEstoqueDao.info(f'({personagem.id.ljust(36)} | {trabalho}) inserido no banco com sucesso!')
            return True
        self.__loggerEstoqueDao.error(f'Erro ao inserir ({personagem.id.ljust(36)} | {trabalho}) no banco: {self.__estoqueDao.pegaErro}')
        return False
    
    def removePersonagem(self, personagem: Personagem, modificaServidor: bool = True) -> bool:
        if self.__personagemDao.removePersonagem(personagem= personagem, modificaServidor= modificaServidor):
            self.__loggerPersonagemDao.info(f'({personagem}) removido no banco com sucesso!')
            return True
        self.__loggerPersonagemDao.error(f'Erro ao remover ({personagem}) do banco: {self.__personagemDao.pegaErro}')
        return False
        
    def insereProfissao(self, profissao: Profissao, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        if self.__profissaoDao.insereProfissao(personagem= personagem, profissao= profissao, modificaServidor= modificaServidor):
            profissao.idPersonagem= personagem.id
            self.__loggerProfissaoDao.info(f'({profissao}) inserido no banco com sucesso!')
            return True
        self.__loggerProfissaoDao.error(f'Erro ao inserir ({profissao}) no banco: {self.__profissaoDao.pegaErro}')
        return False
    
    def pegaNomeProfissaoPorId(self, id: str) -> str:
        nomeProfissao: str= self.__profissaoDao.pegaNomeProfissaoPorId(id= id)
        if nomeProfissao is None:
            self.__loggerProfissaoDao.error(f'Erro ao buscar o nome da profissão ({id}) no servidor: {self.__profissaoDao.pegaErro}')
            return None
        self.__loggerProfissaoDao.info(f'Profissão ({nomeProfissao}) foi encontrado!')
        return nomeProfissao

    def pegaPersonagemPorId(self, id: str) -> Personagem | None:
        personagemEncontrado: Personagem= self.__personagemDao.pegaPersonagemPorId(id)
        if personagemEncontrado is None:
            self.__loggerPersonagemDao.error(f'Erro ao buscar personagem por id ({id}): {self.__personagemDao.pegaErro}')
            return None
        return personagemEncontrado
    
    def pegaProfissaoPorId(self, id: str, personagem: Personagem= None) -> Profissao | None:
        '''
            Função que busca uma profissão específica do personagem atual no banco de dados local
            Args:
                id (str): String que contêm o "id" da profissão a ser buscada
                personagem (Personagem): Objeto da classe Personagem que contêm o "id" do personagem atual
            Returns:
                profissaoEncontrada (Profissao): Objeto da classe Profisssao que contêm os dados encontrados
        '''
        personagem= self.__personagemEmUso if personagem is None else personagem
        profissaoEncontrada: Profissao= self.__profissaoDao.pegaProfissaoPorId(personagem= personagem, id= id)
        if profissaoEncontrada is None:
            self.__loggerProfissaoDao.error(f'Erro ao buscar por id ({id}): {self.__profissaoDao.pegaErro}')
            return None
        return profissaoEncontrada

    def pegaTrabalhoEstoquePorId(self, id: str) -> TrabalhoEstoque | None:
        trabalhoEstoque: TrabalhoEstoque = self.__estoqueDao.pegaTrabalhoEstoquePorId(id= id)
        if trabalhoEstoque is None:
            self.__loggerEstoqueDao.error(f'Erro ao buscar no trabalho no estoque por id ({id}): {self.__estoqueDao.pegaErro}')
            return None
        return trabalhoEstoque

    def pegaTrabalhoEstoquePorIdTrabalho(self, id: str) -> TrabalhoEstoque | None:
        trabalhoEstoque: TrabalhoEstoque = self.__estoqueDao.pegaTrabalhoEstoquePorIdTrabalho(id)
        if trabalhoEstoque is None:
            self.__loggerEstoqueDao.error(f'Erro ao buscar no trabalho no estoque por idTrabalho ({id}): {self.__estoqueDao.pegaErro}')
            return None
        return trabalhoEstoque
        
    def sincronizaListaTrabalhos(self):
        limpaTela()
        self.__loggerTrabalhoDao.debug(menssagem= f'Sincronizando trabalhos...')
        if self.__trabalhoDao.sincronizaTrabalhos():
            self.__loggerTrabalhoDao.debug(menssagem= 'Sincronização concluída com sucesso!')
            return
        self.__loggerTrabalhoDao.error(menssagem= f'Sincronização falhou: {self.__trabalhoDao.pegaErro}')

    def pegaPersonagens(self) -> list[Personagem]:
        try:
            personagensBanco: list[Personagem] = self.__personagemDao.pegaPersonagens()
            if personagensBanco is None:                  
                self.__loggerPersonagemDao.error(f'Erro ao buscar personagens no banco: {self.__personagemDao.pegaErro}')
                return []
            return personagensBanco
        except Exception as e:
            self.__loggerPersonagemDao.error(menssagem= f'Erro ao instânciar um objeto PersonagemDaoSqlite: {e}')
        return []

    def sincronizaListaPersonagens(self):
        limpaTela()
        self.__loggerPersonagemDao.debug(menssagem= f'Sincronizando personagens...')
        if self.__personagemDao.sinconizaPersonagens():
            self.__loggerPersonagemDao.debug(menssagem= 'Sincronização concluída com sucesso!')
            return
        self.__loggerPersonagemDao.error(menssagem= f'Sincronização falhou: {self.__personagemDao.pegaErro}')                

    def removeProfissao(self, profissao: Profissao, personagem: Personagem = None, modificaServidor: bool = True) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        if self.__profissaoDao.removeProfissao(personagem= personagem, profissao= profissao, modificaServidor= modificaServidor):
            self.__loggerProfissaoDao.info(f'({profissao}) removido do banco com sucesso!')
            return True
        self.__loggerProfissaoDao.error(f'Erro ao remover ({profissao}) do banco: {self.__profissaoDao.pegaErro}')
        return False

    def removeProfissoesPorIdPersonagem(self, personagem: Personagem = None) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        if self.__profissaoDao.removeProfissoesPorIdPersonagem(personagem= personagem):
            self.__loggerProfissaoDao.info(f'Profissões de ({personagem.id}) removidas do banco com sucesso!')
            return True
        self.__loggerProfissaoDao.error(f'Erro ao remover profissões de ({personagem.id}) do banco: {self.__profissaoDao.pegaErro}')
        return False

    def removeProducoesPorIdPersonagem(self, personagem: Personagem = None) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        if self.__trabalhoProducaoDao.removeProducoesPorIdPersonagem(personagem= personagem):
            self.__loggerTrabalhoProducaoDao.info(f'Produções de ({personagem.id}) removidas do banco com sucesso!')
            return True
        self.__loggerTrabalhoProducaoDao.error(f'Erro ao remover produções de ({personagem.id}) do banco: {self.__trabalhoProducaoDao.pegaErro}')
        return False

    def removeEstoquePorIdPersonagem(self, personagem: Personagem = None) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        if self.__estoqueDao.removeEstoquePorIdPersonagem(personagem= personagem):
            self.__loggerEstoqueDao.info(f'Estoque de ({personagem.id}) removidas do banco com sucesso!')
            return True
        self.__loggerEstoqueDao.error(f'Erro ao remover estoque de ({personagem.id}) do banco: {self.__estoqueDao.pegaErro}')
        return False

    def removeVendasPorIdPersonagem(self, personagem: Personagem = None) -> bool:
        personagem = self.__personagemEmUso if personagem is None else personagem
        if self.__vendasDao.removeEstoquePorIdPersonagem(personagem= personagem):
            self.__loggerVendaDao.info(f'Vendas de ({personagem.id}) removidas do banco com sucesso!')
            return True
        self.__loggerVendaDao.error(f'Erro ao remover vendas de ({personagem.id}) do banco: {self.__vendasDao.pegaErro}')
        return False

    def sincronizaListaProfissoes(self):
        limpaTela()
        self.__loggerProfissaoDao.debug(menssagem= f'Sincronizando profissões...')
        personagens: list[Personagem] = self.pegaPersonagens()
        for personagem in personagens:
            self.__loggerProfissaoDao.debug(menssagem= f'Personagem: {personagem.nome}')
            if self.__profissaoDao.sincronizaProfissoesPorId(personagem= personagem):
                self.__loggerProfissaoDao.debug(menssagem= f'Sincronização concluída com sucesso!')
                continue
            self.__loggerProfissaoDao.error(menssagem= f'Erro ao sincronizar profissões: {self.__profissaoDao.pegaErro}')
    
    def pegaTrabalhoProducaoPorId(self, id:  str) -> TrabalhoProducao:
        trabalhoProducaoEncontrado = self.__trabalhoProducaoDao.pegaTrabalhoProducaoPorId(id= id)
        if trabalhoProducaoEncontrado is None:
            self.__loggerTrabalhoProducaoDao.error(f'Erro ao buscar trabalho para produção por id ({id}) no banco: {self.__trabalhoProducaoDao.pegaErro}')
            return None
        return trabalhoProducaoEncontrado
    
    def pegaTrabalhoVendidoPorId(self, id:  str) -> TrabalhoProducao | None:
        trabalhoVendidoEncontrado: TrabalhoVendido= self.__vendasDao.pegaTrabalhoVendidoPorId(idBuscado= id)
        if trabalhoVendidoEncontrado is None:
            self.__loggerVendaDao.error(f'Erro ao buscar trabalho vendido por id ({id}) no banco: {self.__vendasDao.pegaErro}')
            return None
        return trabalhoVendidoEncontrado
    
    def pegaTrabalhosProducaoPorIdTrabalho(self, id:  str, personagem: Personagem = None) -> list[TrabalhoProducao]:
        '''
            Função para bucar no banco de dados uma lista de objetos da classe TrabalhoProducao onde o atributo (idTrabalho) é igual ao parâmetro recebido.
            Args:
                id (str): String que contêm o "id" buscado.
                personagem (Personagem): Objeto da classe Personagem que contêm o "id" do personagem buscado. É None por padrão.
            Returns:
                trabalhosEncontrados (list[TrabalhoProducao]): Lista de objetos da classe TrabalhoProducao encontrados no banco. Está vazia caso algum erro seja encontrado.
        '''
        personagem: Personagem = self.__personagemEmUso if personagem is None else personagem
        trabalhosEncontrados: list[TrabalhoProducao] = self.__trabalhoProducaoDao.pegaTrabalhosProducaoPorIdTrabalho(personagem= personagem, id= id)
        if trabalhosEncontrados is None:
            self.__loggerTrabalhoProducaoDao.error(f'Erro ao buscar trabalhos para produção por id ({id}) no banco: {self.__trabalhoProducaoDao.pegaErro}')
            return []
        return trabalhosEncontrados

    def sincronizaTrabalhosProducao(self):
        limpaTela()
        self.__loggerTrabalhoProducaoDao.debug(menssagem= f'Sincronizando trabalhos para produção...')
        personagens: list[Personagem] = self.pegaPersonagens()
        for personagem in personagens:
            self.__loggerTrabalhoProducaoDao.debug(menssagem= f'Personagem: {personagem.nome}')
            if self.__trabalhoProducaoDao.sincronizaTrabalhosProducao(personagem= personagem):
                self.__loggerTrabalhoProducaoDao.debug(menssagem= 'Sincronização concluída com sucesso!')
                continue
            self.__loggerTrabalhoProducaoDao.error(menssagem= f'Sincronização falhou: {self.__trabalhoProducaoDao.pegaErro}')
            
    def sincronizaTrabalhosVendidos(self):
        limpaTela()
        self.__loggerVendaDao.debug(menssagem= f'Sincronizando trabalhos vendidos...')
        personagens: list[Personagem] = self.pegaPersonagens()
        for personagem in personagens:
            self.__loggerVendaDao.debug(menssagem= f'Personagem: {personagem.nome}')
            if self.__vendasDao.sincronizaTrabalhosVendidos(personagem= personagem):
                self.__loggerVendaDao.debug(menssagem= 'Sincronização concluída com sucesso!')
                continue
            self.__loggerVendaDao.error(menssagem= f'Sincronização falhou: {self.__trabalhoProducaoDao.pegaErro}')
            
    def sincronizaTrabalhosEstoque(self):
        limpaTela()
        self.__loggerEstoqueDao.debug(menssagem= f'Sincronizando trabalhos no estoque...')
        personagens: list[Personagem] = self.pegaPersonagens()
        for personagem in personagens:
            self.__loggerEstoqueDao.debug(menssagem= f'Personagem: {personagem.nome}')
            if self.__estoqueDao.sincronizaTrabalhosEstoque(personagem= personagem):
                self.__loggerEstoqueDao.debug(menssagem= 'Sincronização concluída com sucesso!')
                continue
            self.__loggerEstoqueDao.error(menssagem= f'Sincronização falhou: {self.__estoqueDao.pegaErro}')

    def pegaPersonagensServidor(self) -> list[Personagem]:
        repositorioPersonagem: RepositorioPersonagem = RepositorioPersonagem()
        personagens: list[Personagem] = repositorioPersonagem.pegaTodosPersonagens()
        if personagens is None:
            self.__loggerRepositorioPersonagem.error(f'Erro ao buscar personagens no servidor: {repositorioPersonagem.pegaErro}')
            return []
        return personagens

    def pegaTrabalhosBanco(self) -> list[Trabalho]:
        '''
            Método para recuperar uma lista de objetos da classe Trabalho no banco de dados local.
            Returns:
                trabalhos (list[Trabalho]): Lista de objetos da classe Trabalho recuperados no banco de dados.
        '''
        trabalhos: list[Trabalho]= self.__trabalhoDao.pegaTrabalhos()
        if trabalhos is None:
            self.__loggerTrabalhoDao.error(f'Erro ao buscar trabalhos no banco: {self.__trabalhoDao.pegaErro}')
            return []
        return trabalhos
    
    def pegaTrabalhoPorNome(self, nomeTrabalho: str) -> Trabalho | None:
        trabalhoEncontrado = self.__trabalhoDao.pegaTrabalhoPorNome(nomeTrabalho)
        if trabalhoEncontrado is None:
            self.__loggerTrabalhoDao.error(f'Erro ao buscar por nome ({nomeTrabalho}) no banco: {self.__trabalhoDao.pegaErro}')
            return None
        if trabalhoEncontrado.nome is None:
            self.__loggerTrabalhoDao.warning(f'({nomeTrabalho}) não encontrado no banco!')
            return None
        return trabalhoEncontrado

    def preparaPersonagem(self):
        try:
            self.abreStreans()
            self.sincronizaListas()
            clickAtalhoEspecifico('alt', 'tab')
            clickAtalhoEspecifico('win', 'left')
            self.iniciaProcessoBusca()
        except ConnectionError as e:
            self.__loggerAplicacao.error(e)
            self.abreStreans()
            self.iniciaProcessoBusca()
        except Exception as e:
            self.__loggerAplicacao.error(e)
            if input(f'Tentar novamente? (S/N) \n').lower() == 's':
                self.iniciaProcessoBusca()

    def abreStreans(self):
        '''
            Método para iniciar streans
        '''
        self.abreStreamEstoque()
        self.abreStreamTrabalhos()
        self.abreStreamPersonagens()
        self.abreStreamProducao()
        self.abreStreamProfissoes()
        self.abreStreamVendas()
        while not self.__repositorioEstoque.streamPronta or not self.__repositorioTrabalho.streamPronta or not self.__repositorioPersonagem.streamPronta or not self.__repositorioPersonagem.streamPronta or not self.__repositorioProducao.streamPronta or not self.__repositorioProfissao.streamPronta or not self.__repositorioVendas.streamPronta:
            limpaTela()
            self.mostraResultadoStreamEstoque()
            self.mostraResultadoStreamTrabalhos()
            self.mostraResultadoStreamPersonagens()
            self.mostraResultadoStreamProducao()
            self.mostraResultadoStreamProfissoes()
            self.mostraResultadoStreamVendas()
            sleep(1.5)

    def mostraResultadoStreamEstoque(self):
        if self.__repositorioEstoque.streamPronta:
            print(f'✅ Repositório estoque')
            return
        print(f'❌ Repositório estoque')

    def mostraResultadoStreamTrabalhos(self):
        if self.__repositorioTrabalho.streamPronta:
            print(f'✅ Repositório trabalhos')
            return
        print(f'❌ Repositório trabalhos')

    def mostraResultadoStreamPersonagens(self):
        if self.__repositorioPersonagem.streamPronta:
            print(f'✅ Repositório personagens')
            return
        print(f'❌ Repositório personagens')

    def mostraResultadoStreamProducao(self):
        if self.__repositorioProducao.streamPronta:
            print(f'✅ Repositório produções')
            return
        print(f'❌ Repositório produções')

    def mostraResultadoStreamProfissoes(self):
        if self.__repositorioProfissao.streamPronta:
            print(f'✅ Repositório profissões')
            return
        print(f'❌ Repositório profissões')

    def mostraResultadoStreamVendas(self):
        if self.__repositorioEstoque.streamPronta:
            print(f'✅ Repositório vendas')
            return
        print(f'❌ Repositório vendas')

    def sincronizaListas(self) -> None:
        sincroniza = input(f'Sincronizar listas? (S/N) ')
        if sincroniza is not None and sincroniza.lower() == 's':
            self.sincronizaListaTrabalhos()
            self.sincronizaListaPersonagens()
            self.sincronizaListaProfissoes()
            self.sincronizaTrabalhosProducao()
            self.sincronizaTrabalhosVendidos()
            self.sincronizaTrabalhosEstoque()

    def abreStreamPersonagens(self) -> bool:
        if self.__repositorioPersonagem.abreStream:
            self.__loggerRepositorioPersonagem.info(f'Stream repositório personagem iniciada!')
            return True
        self.__loggerRepositorioPersonagem.error(f'Erro ao iniciar stream repositório personagem: {self.__repositorioPersonagem.pegaErro}')
        return False
    
    def abreStreamProducao(self) -> bool:
        if self.__repositorioProducao.abreStream:
            self.__loggerRepositorioProducao.info(f'Stream repositório produção iniciada!')
            return True
        self.__loggerRepositorioProducao.error(f'Erro ao iniciar stream repositório produções: {self.__repositorioProducao.pegaErro}')
        return False

    def abreStreamTrabalhos(self) -> bool:
        if self.__repositorioTrabalho.abreStream:
            self.__loggerRepositorioTrabalho.info(f'Stream repositório trabalhos iniciada!')
            return True
        self.__loggerRepositorioTrabalho.error(f'Erro ao iniciar stream repositório trabalhos: {self.__repositorioTrabalho.pegaErro}')
        return False

    def abreStreamProfissoes(self) -> bool:
        if self.__repositorioProfissao.abreStream:
            self.__loggerRepositorioProfissao.info(f'Stream repositório profissões iniciada!')
            return True
        self.__loggerRepositorioProfissao.error(f'Erro ao iniciar stream repositório profissões: {self.__repositorioProfissao.pegaErro}')
        return False

    def abreStreamEstoque(self) -> bool:
        if self.__repositorioEstoque.abreStream:
            self.__loggerRepositorioEstoque.info(f'Stream repositório estoque iniciada!')
            return True
        self.__loggerRepositorioEstoque.error(f'Erro ao iniciar stream repositório estoques: {self.__repositorioEstoque.pegaErro}')
        return False

    def abreStreamVendas(self) -> bool:
        if self.__repositorioVendas.abreStream:
            self.__loggerRepositorioVendas.info(f'Stream repositório estoque iniciada!')
            return True
        self.__loggerRepositorioVendas.error(f'Erro ao iniciar stream repositório vendas: {self.__repositorioVendas.pegaErro}')
        return False

    def modificaTrabalho(self, trabalho: Trabalho, modificaServidor: bool = True) -> bool:
        if self.__trabalhoDao.modificaTrabalho(trabalho, modificaServidor):
            self.__loggerTrabalhoDao.info(f'({trabalho.id.ljust(36)} | {trabalho}) modificado no banco com sucesso!')
            return True
        self.__loggerTrabalhoDao.error(f'Erro ao modificar ({trabalho.id.ljust(36)} | {trabalho}) no banco: {self.__trabalhoDao.pegaErro}')
        return False

if __name__=='__main__':
    try:
        Aplicacao().preparaPersonagem()
    except Exception as e:
        print(f'Erro ao iniciar aplicação: {e}')