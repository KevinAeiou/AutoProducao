import logging
from uuid import uuid4
from time import sleep
from utilitarios import limpaTela, variavelExiste, tamanhoIgualZero
from constantes import LISTA_PROFISSOES, LISTA_RARIDADES, LISTA_LICENCAS, CODIGO_PARA_PRODUZIR, CHAVE_LISTA_TRABALHOS_PRODUCAO, CHAVE_LISTA_ESTOQUE

from dao.trabalhoDaoSqlite import TrabalhoDaoSqlite
from dao.personagemDaoSqlite import PersonagemDaoSqlite
from dao.trabalhoProducaoDaoSqlite import TrabalhoProducaoDaoSqlite
from dao.estoqueDaoSqlite import EstoqueDaoSqlite
from dao.vendaDaoSqlite import VendaDaoSqlite
from dao.profissaoDaoSqlite import ProfissaoDaoSqlite

from repositorio.repositorioTrabalho import RepositorioTrabalho
from repositorio.repositorioPersonagem import RepositorioPersonagem

from modelos.trabalho import Trabalho
from modelos.trabalhoProducao import TrabalhoProducao
from modelos.personagem import Personagem
from modelos.trabalhoEstoque import TrabalhoEstoque
from modelos.trabalhoVendido import TrabalhoVendido

from main import Aplicacao

class CRUD:
    def __init__(self):
        logging.basicConfig(level = logging.INFO, filename = 'logs/aplicacao.log', encoding='utf-8', format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt = '%d/%m/%Y %I:%M:%S %p')
        self.__personagemEmUso = None
        self.__aplicacao = Aplicacao()
        self.__repositorioPersonagem = RepositorioPersonagem()
        self.__repositorioTrabalho = RepositorioTrabalho()
        self.__loggerTrabalhoDao = logging.getLogger('trabalhoDao')
        self.__loggerPersonagemDao = logging.getLogger('personagemDao')
        self.__loggerEstoqueDao = logging.getLogger('estoqueDao')
        self.__loggerTrabalhoProducaoDao = logging.getLogger('trabalhoProducaoDao')
        self.__loggerVendaDao = logging.getLogger('vendaDao')
        self.__loggerRepositorioPersonagem = logging.getLogger('repositorioPersonagem')
        self.__loggerRepositorioTrabalho = logging.getLogger('repositorioTrabalho')
        if self.__repositorioPersonagem.abreStream():
            self.__loggerRepositorioPersonagem.info(f'Stream repositório personagem iniciada com sucesso!')
        else:
            self.__loggerRepositorioPersonagem.info(f'Erro ao inicar stream: {self.__repositorioPersonagem.pegaErro()}')
        if self.__repositorioTrabalho.abreStream():
            self.__loggerRepositorioTrabalho.info(f'Stream repositório trabalhos iniciada com sucesso!')
        else:
            self.__loggerRepositorioTrabalho.error(f'Erro ao iniciar stream repositório trabalhos: {self.__repositorioTrabalho.pegaErro()}')
        self.menu()
    
    def insereTrabalhoProducao(self, trabalhoProducao):
        if variavelExiste(trabalhoProducao):
            logger = logging.getLogger('trabalhoProducaoDao')
            trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
            if trabalhoProducaoDao.insereTrabalhoProducao(trabalhoProducao):
                logger.info(f'({trabalhoProducao}) inserido com sucesso!')
                return True
            logger.error(f'Erro ao inserir ({trabalhoProducao}): {trabalhoProducaoDao.pegaErro()}')
            return False
    
    def insereNovoTrabalho(self):
        while True:
            limpaTela()
            trabalhoBuscado = Trabalho()
            for profissao in LISTA_PROFISSOES:
                print(f'{LISTA_PROFISSOES.index(profissao) + 1} - {profissao}')
            opcaoProfissao = input(f'Opção de profissao: ')
            if int(opcaoProfissao) == 0:
                break
            trabalhoBuscado.profissao = LISTA_PROFISSOES[int(opcaoProfissao) - 1]
            limpaTela()
            for raridade in LISTA_RARIDADES:
                print(f'{LISTA_RARIDADES.index(raridade) + 1} - {raridade}')
            opcaoRaridade = input(f'Opção raridade: ')
            if int(opcaoRaridade) == 0:
                continue
            trabalhoBuscado.raridade = LISTA_RARIDADES[int(opcaoRaridade) - 1]
            while True:
                limpaTela()
                trabalhoDao = TrabalhoDaoSqlite()
                trabalhos = trabalhoDao.pegaTrabalhosPorProfissaoRaridade(trabalhoBuscado)
                if variavelExiste(trabalhos):
                    if tamanhoIgualZero(trabalhos):
                        print('Lista de trabalhos está vazia!')
                    else:
                        print(f'{"NOME".ljust(44)} | {"PROFISSÃO".ljust(22)} | {"RARIDADE".ljust(9)} | NÍVEL')
                        for trabalho in trabalhos:
                            print(f'{trabalho} | {trabalho.trabalhoNecessario}')
                    opcaoTrabalho = input(f'Adicionar novo trabalho? (S/N)')
                    if opcaoTrabalho.lower() == 'n':
                        break
                    limpaTela()
                    nome = input(f'Nome: ')
                    nomeProducao = input(f'Nome produção: ')
                    experiencia = input(f'Experiência: ')
                    nivel = input(f'Nível: ')
                    trabalhoNecessario = input(f'Trabalhos necessarios: ')
                    novoTrabalho = Trabalho()
                    novoTrabalho.nome = nome
                    novoTrabalho.nomeProducao = nomeProducao
                    novoTrabalho.experiencia = int(experiencia)
                    novoTrabalho.nivel = int(nivel)
                    novoTrabalho.profissao = trabalhoBuscado.profissao
                    novoTrabalho.raridade = trabalhoBuscado.raridade
                    novoTrabalho.trabalhoNecessario = trabalhoNecessario
                    trabalhoDao = TrabalhoDaoSqlite()
                    if trabalhoDao.insereTrabalho(novoTrabalho):
                        self.__loggerTrabalhoDao.info(f'({novoTrabalho}) inserido com sucesso!')
                        continue
                    self.__loggerTrabalhoDao.error(f'Erro ao inserir ({novoTrabalho}): {trabalhoDao.pegaErro()}')
                    continue
                self.__loggerTrabalhoDao.error(f'Erro ao buscar trabalhos no banco: {trabalhoDao.pegaErro()}')
                break

    def modificaTrabalho(self):
        while True:
            limpaTela()
            trabalhoBuscado = Trabalho()
            for profissao in LISTA_PROFISSOES:
                print(f'{LISTA_PROFISSOES.index(profissao) + 1} - {profissao}')
            print(f'{"0".ljust(6)} - Voltar')
            opcaoProfissao = input(f'Opção de profissao: ')
            if int(opcaoProfissao) == 0:
                break
            trabalhoBuscado.profissao = LISTA_PROFISSOES[int(opcaoProfissao) - 1]
            limpaTela()
            for raridade in LISTA_RARIDADES:
                print(f'{LISTA_RARIDADES.index(raridade) + 1} - {raridade}')
            print(f'{"0".ljust(6)} - Voltar')
            opcaoRaridade = input(f'Opção raridade: ')
            if int(opcaoRaridade) == 0:
                continue
            trabalhoBuscado.raridade = LISTA_RARIDADES[int(opcaoRaridade) - 1]
            while True:
                limpaTela()
                trabalhoDao = TrabalhoDaoSqlite()
                trabalhos = trabalhoDao.pegaTrabalhosPorProfissaoRaridade(trabalhoBuscado)
                if variavelExiste(trabalhos):
                    if tamanhoIgualZero(trabalhos):
                        print('Lista de trabalhos está vazia!')
                    else:
                        print(f"{'ÍNDICE'.ljust(6)} - {'NOME'.ljust(44)} | {'PROFISSÃO'.ljust(22)} | {'RARIDADE'.ljust(9)} | NÍVEL")
                        for trabalho in trabalhos:
                            print(f'{str(trabalhos.index(trabalho) + 1).ljust(6)} - {trabalho}')
                    print(f'{"0".ljust(6)} - Voltar')
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
                    trabalhoEscolhido.nomeProducao = novoNomeProducao
                    trabalhoEscolhido.setExperiencia(novaExperiencia)
                    trabalhoEscolhido.setNivel(novoNivel)
                    trabalhoEscolhido.profissao = novaProfissao
                    trabalhoEscolhido.raridade = novaRaridade
                    trabalhoEscolhido.trabalhoNecessario = novoTrabalhoNecessario
                    trabalhoDao = TrabalhoDaoSqlite()
                    if trabalhoDao.modificaTrabalhoPorId(trabalhoEscolhido):
                        self.__loggerTrabalhoDao.info(f'({trabalhoEscolhido}) modificado com sucesso!')
                        continue
                    self.__loggerTrabalhoDao.error(f'Erro ao modificar ({trabalhoEscolhido}): {trabalhoDao.pegaErro()}')
                    continue
                self.__loggerTrabalhoDao.error(f'Erro ao buscar trabalhos no banco: {trabalhoDao.pegaErro()}')
                break

    def removeTrabalho(self):
        logger = logging.getLogger('trabalhoDao')
        while True:
            limpaTela()
            print(f"{'ÍNDICE'.ljust(6)} - {'NOME'.ljust(44)} | {'PROFISSÃO'.ljust(22)} | {'RARIDADE'.ljust(9)} | NÍVEL")
            trabalhoDao = TrabalhoDaoSqlite()
            trabalhos = trabalhoDao.pegaTrabalhos()
            if variavelExiste(trabalhos):
                if tamanhoIgualZero(trabalhos):
                    print('Lista de trabalhos está vazia!')
                else:
                    for trabalho in trabalhos:
                        print(f'{str(trabalhos.index(trabalho) + 1).ljust(6)} - {trabalho}')
                opcaoTrabalho = input(f'Opção trabalho: ')    
                if int(opcaoTrabalho) == 0:
                    break
                trabalhoEscolhido = trabalhos[int(opcaoTrabalho) - 1]
                trabalhoDao = TrabalhoDaoSqlite()
                if trabalhoDao.removeTrabalho(trabalhoEscolhido):
                    logger.info(f'({trabalhoEscolhido}) removido com sucesso!')
                    continue
                logger.error(f'Erro ao remover ({trabalhoEscolhido}): {trabalhoDao.pegaErro()}')
                input(f'Clique para continuar...')
                continue
            logger.error(f'Erro ao buscar trabalhos: {trabalhoDao.pegaErro()}')
            input(f'Clique para continuar...')
            break
    
    def inserePersonagem(self):
        logger = logging.getLogger('personagemDao')
        while True:
            limpaTela()
            print(f"{'ID'.ljust(36)} | {'NOME'.ljust(17)} | {'ESPAÇO'.ljust(6)} | {'ESTADO'.ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO")
            personagemDao = PersonagemDaoSqlite()
            personagens = personagemDao.pegaPersonagens()
            if variavelExiste(personagens):
                if tamanhoIgualZero(personagens):
                    print('Lista de personagens está vazia!')
                else:
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
                novoPersonagem.email = email
                novoPersonagem.senha = senha
                personagemDao = PersonagemDaoSqlite()
                if personagemDao.inserePersonagem(novoPersonagem):
                    logger.info(f'({novoPersonagem}) inserido com sucesso!')
                    continue
                logger.error(f'Erro ao inserir ({novoPersonagem}): {personagemDao.pegaErro()}')
                input(f'Clique para continuar...')
                continue
            logger.error(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
            input(f'Clique para continuar...')
            break

    def modificaPersonagem(self):
        logger = logging.getLogger('personagemDao')
        while True:
            limpaTela()
            personagemDao = PersonagemDaoSqlite()
            personagens = personagemDao.pegaPersonagens()
            if variavelExiste(personagens):
                if tamanhoIgualZero(personagens):
                    print('Lista de personagens está vazia!')
                else:
                    print(f"{'ÍNDICE'.ljust(6)} - {'ID'.ljust(36)} | {'NOME'.ljust(17)} | {'ESPAÇO'.ljust(6)} | {'ESTADO'.ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO")
                    for personagem in personagens:
                        print(f'{str(personagens.index(personagem) + 1).ljust(6)} - {personagem}')
                opcaoPersonagem = input(f'Opção:')
                if int(opcaoPersonagem) == 0:
                    break
                limpaTela()
                personagem = personagens[int(opcaoPersonagem) - 1]
                novoNome = input(f'Novo nome: ')
                if tamanhoIgualZero(novoNome):
                    novoNome = personagem.nome
                novoEmail = input(f'Novo email: ')
                if tamanhoIgualZero(novoEmail):
                    novoEmail = personagem.email
                novasenha = input(f'Nova senha: ')
                if tamanhoIgualZero(novasenha):
                    novasenha = personagem.senha
                novoEspaco = input(f'Nova quantidade de produção: ')
                if tamanhoIgualZero(novoEspaco):
                    novoEspaco = personagem.espacoProducao
                novoEstado = input(f'Modificar estado? (S/N) ')
                if novoEstado.lower() == 's':
                    personagem.alternaEstado()
                novoUso = input(f'Modificar uso? (S/N) ')
                if novoUso.lower() == 's':
                    personagem.alternaUso()
                novoAutoProducao = input(f'Modificar autoProducao? (S/N) ')
                if novoAutoProducao.lower() == 's':
                    personagem.alternaAutoProducao()
                personagem.nome = novoNome
                personagem.email = novoEmail
                personagem.senha = novasenha
                personagem.setEspacoProducao(novoEspaco)
                personagemDao = PersonagemDaoSqlite()
                if personagemDao.modificaPersonagem(personagem):
                    logger.info(f'({personagem}) modificado com sucesso!')
                    continue
                logger.error(f'Erro ao modificar ({personagem}): {personagemDao.pegaErro()}')
                input(f'Clique para continuar...')
                continue
            logger.error(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
            input(f'Clique para continuar...')
            break
    
    def removePersonagem(self):
        logger = logging.getLogger('personagemDao')
        while True:
            limpaTela()
            personagemDao = PersonagemDaoSqlite()
            personagens = personagemDao.pegaPersonagens()
            if variavelExiste(personagens):
                if tamanhoIgualZero(personagens):
                    print('Lista de personagens está vazia!')
                else:
                    print(f"{'ÍNDICE'.ljust(6)} - {'ID'.ljust(36)} | {'NOME'.ljust(17)} | {'ESPAÇO'.ljust(6)} | {'ESTADO'.ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO")
                    for personagem in personagens:
                        print(f'{str(personagens.index(personagem) + 1).ljust(6)} - {personagem}')
                print(f'{"0".ljust(6)} - Voltar')
                opcaoPersonagem = input(f'Opção:')
                if int(opcaoPersonagem) == 0:
                    break
                personagem = personagens[int(opcaoPersonagem) - 1]
                personagemDao = PersonagemDaoSqlite()
                if personagemDao.removePersonagem(personagem):
                    logger.info(f'({personagem}) removido com sucesso!')
                    continue
                logger.error(f'Erro ao remover ({personagem}): {personagemDao.pegaErro()}')
                input(f'Clique para continuar...')
                continue
            logger.error(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
            input(f'Clique para continuar...')
            break

    def mostraListaTrabalhosProducao(self):
        limpaTela()
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
        trabalhos = trabalhoProducaoDao.pegaTrabalhosProducao()
        if variavelExiste(trabalhos):
            if tamanhoIgualZero(trabalhos):
                print('Lista de trabalhos em produção está vazia!')
            else:
                print(f"{'ÍNDICE'.ljust(6)} - {'NOME'.ljust(44)} | {'PROFISSÃO'.ljust(22)} | {'NÍVEL'.ljust(5)} | {'ESTADO'.ljust(10)} | {'LICENÇA'.ljust(34)} | RECORRÊNCIA")
                for trabalhoProducao in trabalhos:
                    print(f'{str(trabalhos.index(trabalhoProducao) + 1).ljust(6)} - {trabalhoProducao}')
            return trabalhos
        self.__loggerTrabalhoProducaoDao.error(f'Erro ao buscar trabalhos em produção: {trabalhoProducaoDao.pegaErro()}')
        return None
    
    def mostraListaTrabalhosPorProfissaoRaridade(self, trabalhoBuscado):
        limpaTela()
        trabalhoDao = TrabalhoDaoSqlite()
        trabalhos = trabalhoDao.pegaTrabalhosPorProfissaoRaridade(trabalhoBuscado)
        if variavelExiste(trabalhos):
            if tamanhoIgualZero(trabalhos):
                print(f'Nem um trabalho encontrado!')
            else:
                print(f"{'ÍNDICE'.ljust(6)} - {'NOME'.ljust(40)} | {('PROFISSÃO').ljust(20)} | NÍVEL")
                for trabalho in trabalhos:
                    print(f'{str(trabalhos.index(trabalho) + 1).ljust(6)} - {trabalho}')
            return trabalhos
        self.__loggerTrabalhoDao.error(f'Erro ao buscar trabalhos: {trabalhoDao.pegaErro()}')
        return None
    
    def defineNovoTrabalhoProducao(self, trabalhos):
        print(f'{"0".ljust(6)} - Voltar')
        opcaoTrabalho = input(f'Trabalhos escolhido: ')
        return None if int(opcaoTrabalho) == 0 else trabalhos[int(opcaoTrabalho) - 1]
    
    def defineLicencaSelecionada(self):
        opcaoLicenca = input(f'Licença escolhida: ')
        return None if int(opcaoLicenca) == 0 else LISTA_LICENCAS[int(opcaoLicenca) - 1]

    def defineRecorrenciaSelecionada(self):
        opcaoRecorrencia = input(f'Trabalho recorrente? (S/N)')
        return True if (opcaoRecorrencia).lower() == 's' else False
    
    def defineInsereNovoTrabalho(self):
        opcaoTrabalho = input(f'Adicionar novo trabalho? (S/N) ')
        return True if opcaoTrabalho.lower() == 's' else False

    def insereNovoTrabalhoProducao(self):
        while True:
            personagens = self.mostraListaPersonagens()
            if variavelExiste(personagens) and self.definePersonagemEscolhido(personagens):
                while True:
                    trabalhosProducao = self.mostraListaTrabalhosProducao()
                    insereNovoTrabalho = self.defineInsereNovoTrabalho()
                    if variavelExiste(trabalhosProducao) and insereNovoTrabalho:
                        trabalhoBuscado = self.defineTrabalhoBuscadoPorProfissaoRaridade()
                        trabalhosEncontrados = self.mostraListaTrabalhosPorProfissaoRaridade(trabalhoBuscado)
                        trabalhoSelecionado = self.defineNovoTrabalhoProducao(trabalhosEncontrados)
                        if variavelExiste(trabalhosEncontrados) and variavelExiste(trabalhoSelecionado):
                            novoTrabalhoProducao = self.defineNovoTrabalhoProducaoSelecionado(trabalhoSelecionado)
                            self.insereTrabalhoProducao(novoTrabalhoProducao)
                            continue
                        break
                    break
                continue
            break

    def defineNovoTrabalhoProducaoSelecionado(self, trabalhoSelecionado):
        self.mostraListaLicencas()
        licenca = self.defineLicencaSelecionada()
        recorrencia = self.defineRecorrenciaSelecionada()
        novoTrabalhoProducao = TrabalhoProducao()
        novoTrabalhoProducao.dicionarioParaObjeto(trabalhoSelecionado.__dict__)
        novoTrabalhoProducao.id = str(uuid4())
        novoTrabalhoProducao.idTrabalho = trabalhoSelecionado.id
        novoTrabalhoProducao.recorrencia = recorrencia
        novoTrabalhoProducao.tipo_licenca = licenca
        novoTrabalhoProducao.estado = CODIGO_PARA_PRODUZIR
        return novoTrabalhoProducao

    def defineTrabalhoBuscadoPorProfissaoRaridade(self):
        self.mostraListaProfissoes()
        profissaoSelecionada = self.defineProfissaoSelecionada()
        self.mostraListaRaridades()
        raridadeSelecionada = self.defineRaridadeSelecionada()
        trabalhoBuscado = Trabalho()
        trabalhoBuscado.raridade = raridadeSelecionada
        trabalhoBuscado.profissao = profissaoSelecionada
        return trabalhoBuscado

    def mostraListaLicencas(self):
        limpaTela()
        for licenca in LISTA_LICENCAS:
            print(f'{LISTA_LICENCAS.index(licenca) + 1} - {licenca}')
    
    def modificaTrabalhoProducao(self):
        while True:
            personagens = self.mostraListaPersonagens()
            if variavelExiste(personagens) and self.definePersonagemEscolhido(personagens):
                while True:
                    trabalhos = self.mostraListaTrabalhosProducao()
                    trabalhoProducaoSelecionado = self.defineTrabalhoSelecionado(trabalhos)
                    if variavelExiste(trabalhoProducaoSelecionado):
                        self.mostraListaLicencas()
                        novaLicenca = self.defineLicencaSelecionada()
                        if variavelExiste(novaLicenca):
                            trabalhoProducaoSelecionado.tipo_licenca = novaLicenca
                            novaRecorrencia = input(f'Alterna recorrencia? (S/N) ')
                            if novaRecorrencia.lower() == 's':
                                trabalhoProducaoSelecionado.alternaRecorrencia()
                            limpaTela()
                            novoEstado = input(f'Novo estado: (0 - PRODUZIR, 1 - PRODUZINDO, 2 - CONCLUÍDO) ')
                            if tamanhoIgualZero(novoEstado):
                                novoEstado = trabalhoProducaoSelecionado.estado 
                            else:
                                trabalhoProducaoSelecionado.estado = int(novoEstado)
                            trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
                            if trabalhoProducaoDao.modificaTrabalhoProducao(trabalhoProducaoSelecionado):
                                self.__loggerTrabalhoProducaoDao.info(f'({trabalhoProducaoSelecionado}) modificado com sucesso!')
                                continue
                            self.__loggerTrabalhoProducaoDao.error(f'Erro ao modificar ({trabalhoProducaoSelecionado}): {trabalhoProducaoDao.pegaErro()}')
                            continue
                        break
                    break
                continue
            break
    
    def removeTrabalhoProducao(self):
        logger = logging.getLogger('trabalhoProducaoDao')
        while True:
            limpaTela()
            personagemDao = PersonagemDaoSqlite()
            personagens = personagemDao.pegaPersonagens()
            if variavelExiste(personagens):
                if tamanhoIgualZero(personagens):
                    print('Lista de personagens está vazia!')
                else:
                    print(f"{'ÍNDICE'.ljust(6)} | {'ID'.ljust(36)} | {'NOME'.ljust(17)} | {'ESPAÇO'.ljust(6)} | {'ESTADO'.ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO")
                    for personagem in personagens:
                        print(f'{str(personagens.index(personagem) + 1).ljust(6)} - {personagem}')
                print(f'{"0".ljust(6)} - Voltar')
                opcaoPersonagem = input(f'Opção: ')
                if int(opcaoPersonagem) == 0:
                    break
                personagem = personagens[int(opcaoPersonagem) - 1]
                while True: 
                    limpaTela()
                    trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
                    trabalhosProducao = trabalhoProducaoDao.pegaTrabalhosProducao()
                    if variavelExiste(trabalhosProducao):
                        if tamanhoIgualZero(trabalhosProducao):
                            print('Lista de trabalhos em produção está vazia!')
                        else:
                            print(f"{'ÍNDICE'.ljust(6)} - {'NOME'.ljust(40)} | {'PROFISSÃO'.ljust(21)} | {'NÍVEL'.ljust(5)} | {'ESTADO'.ljust(10)} | LICENÇA")
                            for trabalhoProducao in trabalhosProducao:
                                print(f'{str(trabalhosProducao.index(trabalhoProducao) + 1).ljust(6)} - {trabalhoProducao}')
                        print(f'{"0".ljust(6)} - Voltar')
                        opcaoTrabalho = input(f'Opção trabalho: ')
                        if int(opcaoTrabalho) == 0:
                            break
                        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
                        trabalhoRemovido = trabalhosProducao[int(opcaoTrabalho) - 1]
                        if trabalhoProducaoDao.removeTrabalhoProducao(trabalhoRemovido):
                            logger.info(f'({trabalhoRemovido}) removido com sucesso!')
                            continue
                        logger.error(f'Erro ao remover ({trabalhoRemovido}): {trabalhoProducaoDao.pegaErro()}')
                        input(f'Clique para continuar...')
                        continue
                    print(f'Erro ao buscar trabalhos em produção: {trabalhoProducaoDao.pegaErro()}')
                    input(f'Clique para continuar...')
                    break
                continue
            print(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
            input(f'Clique para continuar...')
            break

    def sincronizaListaTrabalhos(self):
        loggerTrabalho = logging.getLogger('trabalhoDAO')
        loggerEstoque = logging.getLogger('estoqueDAO')
        loggerProducao = logging.getLogger('trabalhoProducaoDAO')
        loggerVenda = logging.getLogger('vendaDAO')
        self.__repositorioTrabalho = RepositorioTrabalho()        
        trabalhosServidor = self.__repositorioTrabalho.pegaTodosTrabalhos()
        if variavelExiste(trabalhosServidor):
            trabalhoDao = TrabalhoDaoSqlite()
            trabalhosBanco = trabalhoDao.pegaTrabalhos()
            if variavelExiste(trabalhosBanco):
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
                return
            print(f'Erro ao buscar trabalhos no banco: {trabalhoDao.pegaErro()}')
            return
        print(f'Erro ao buscar trabalhos no servidor: {self.__repositorioTrabalho.pegaErro()}')

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
    
    def modificaProfissao(self):
        logger = logging.getLogger('profissaoDao')
        while True:
            limpaTela()
            personagemDao = PersonagemDaoSqlite()
            personagens = personagemDao.pegaPersonagens()
            if variavelExiste(personagens):
                if tamanhoIgualZero(personagens):
                    print(f'Lista de personagens está vazia!')
                else:
                    print(f"{'ÍNDICE'.ljust(6)} - {'ID'.ljust(36)} | {'NOME'.ljust(17)} | {'ESPAÇO'.ljust(6)} | {'ESTADO'.ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO")
                    for personagem in personagens:
                        print(f'{str(personagens.index(personagem) + 1).ljust(6)} - {personagem}')
                print(f'{"0".ljust(6)} - Voltar')
                opcaoPersonagem = input(f'Opção:')
                if int(opcaoPersonagem) == 0:
                    break
                while True:
                    limpaTela()
                    profissaoDao = ProfissaoDaoSqlite(personagens[int(opcaoPersonagem) - 1])
                    profissoes = profissaoDao.pegaProfissoes()
                    if variavelExiste(profissoes):
                        if len(profissoes) == 0:
                            profissaoDao = ProfissaoDaoSqlite(personagens[int(opcaoPersonagem) - 1])
                            if profissaoDao.insereListaProfissoes():
                                logger.info(f'Profissões inseridas com sucesso!')
                            else:
                                logger.error(f'Erro ao inserir profissões: {profissaoDao.pegaErro()}')
                                input(f'Clique para continuar...')
                                break
                            continue
                        print(f"{'ÍNDICE'.ljust(6)} - {'ID'.ljust(40)} | {'ID PERSONAGEM'.ljust(40)} | {'NOME'.ljust(22)} | {'EXP'.ljust(6)} | PRIORIDADE")
                        for profissao in profissoes:
                            print(f'{str(profissoes.index(profissao) + 1).ljust(6)} - {profissao}')
                        print(f'{"0".ljust(6)} - Voltar')
                        opcaoProfissao = input(f'Opção: ')
                        if int(opcaoProfissao) == 0:
                            break
                        profissaoModificado = profissoes[int(opcaoProfissao)-1]
                        novoNome = input(f'Novo nome: ')
                        novaExperiencia = input(f'Nova experiência: ')
                        alternaPrioridade = input(f'Alternar prioridade? (S/N) ')
                        novoNome = profissaoModificado.nome if tamanhoIgualZero(novoNome) else novoNome
                        novaExperiencia = profissaoModificado.experiencia if tamanhoIgualZero(novaExperiencia) else novaExperiencia
                        profissaoModificado.nome = novoNome
                        profissaoModificado.setExperiencia(novaExperiencia)
                        if alternaPrioridade.lower() == 's':
                            profissaoModificado.alternaPrioridade()
                        profissaoDao = ProfissaoDaoSqlite(personagens[int(opcaoPersonagem)-1])
                        if profissaoDao.modificaProfissao(profissaoModificado):
                            logger.info(f'({profissaoModificado}) modificado com sucesso!')
                            continue
                        logger.error(f'Erro ao modificar ({profissaoModificado}): {profissaoDao.pegaErro()}')
                        input(f'Clique para continuar...')
                        continue
                    print(f'Erro ao buscar profissões: {profissaoDao.pegaErro()}')
                    input(f'Clique para continuar...')
                    break
                continue
            logger.error(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
            input(f'Clique para continuar...')
            break

    def pegaTodosTrabalhosProducao(self):
        limpaTela()
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite()
        trabalhosProducao = trabalhoProducaoDao.pegaTodosTrabalhosProducao()
        if variavelExiste(trabalhosProducao):
            # print(f'{'NOME'.ljust(113)} | {'DATA'.ljust(10)} | {'ID TRABALHO'.ljust(36)} | {'VALOR'.ljust(5)} | UND')
            if tamanhoIgualZero(trabalhosProducao):
                print('Lista de trabalhos em produção está vazia!')
            else:
                for trabalhoProducao in trabalhosProducao:
                    print(trabalhoProducao)
            input(f'Clique para continuar...')
            return
        self.__loggerTrabalhoProducaoDao.error(f'Erro ao buscar todos os trabalhos em produção: {trabalhoProducaoDao.pegaErro()}')
        input(f'Clique para continuar...')

    def insereTrabalhoEstoque(self):
        while True:
            personagens = self.mostraListaPersonagens()
            if variavelExiste(personagens):
                if self.definePersonagemEscolhido(personagens):
                    while True:
                        estoque = self.mostraListaTrabalhosEstoque()
                        if variavelExiste(estoque):
                            opcaoTrabalho = input(f'Inserir novo trabalho ao estoque? (S/N) ')
                            if opcaoTrabalho.lower() == 'n':
                                break
                            self.mostraListaProfissoes()
                            trabalhoBuscado = Trabalho()
                            profissaoSelecionada =  self.defineProfissaoSelecionada()
                            trabalhoBuscado.profissao = profissaoSelecionada
                            if variavelExiste(profissaoSelecionada):
                                self.mostraListaRaridades()
                                raridadeSelecionada = self.defineRaridadeSelecionada()
                                trabalhoBuscado.raridade = raridadeSelecionada
                                if variavelExiste(raridadeSelecionada):
                                    trabalhoDao = TrabalhoDaoSqlite()
                                    trabalhos = trabalhoDao.pegaTrabalhosPorProfissaoRaridade(trabalhoBuscado)
                                    if variavelExiste(trabalhos):
                                        if tamanhoIgualZero(trabalhos):
                                            print('Lista de trabalhos está vazia!')
                                        else:
                                            print(f'{"ÍNDICE".ljust(6)} - {"NOME".ljust(44)} | {"PROFISSÃO".ljust(22)} | {"RARIDADE".ljust(9)} | NÍVEL')
                                            for trabalho in trabalhos:
                                                print(f'{str(trabalhos.index(trabalho) + 1).ljust(6)} - {trabalho}')
                                        print(f'{"0".ljust(6)} - Voltar')
                                        trabalho = self.defineTrabalhoEstoqueSelecionado(trabalhos)
                                        if variavelExiste(trabalho):
                                            trabalhoEstoque = self.defineNovoTrabalhoEstoque(trabalho)
                                            self.concluiInsereTrabalhoEstoque(trabalhoEstoque)
                                            continue
                                        break
                                    break
                                break
                            break
                        break
                    continue
                break
            break

    def defineTrabalhoEstoqueSelecionado(self, trabalhos):
        opcaoTrabalho = input(f'Opção trabalho: ')    
        if int(opcaoTrabalho) == 0:
            return
        trabalho = trabalhos[int(opcaoTrabalho) - 1]
        return trabalho

    def defineNovoTrabalhoEstoque(self, trabalho):
        quantidadeTrabalho = input(f'Quantidade trabalho: ')
        trabalhoEstoque = TrabalhoEstoque()
        trabalhoEstoque.dicionarioParaObjeto(trabalho.__dict__)
        trabalhoEstoque.id = str(uuid4())
        trabalhoEstoque.trabalhoId = trabalho.id
        trabalhoEstoque.setQuantidade(quantidadeTrabalho)
        return trabalhoEstoque

    def concluiInsereTrabalhoEstoque(self, trabalhoEstoque):
        trabalhoEstoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
        if trabalhoEstoqueDao.insereTrabalhoEstoque(trabalhoEstoque):
            self.__loggerEstoqueDao.info(f'({trabalhoEstoque}) inserido com sucesso!')
            return
        self.__loggerEstoqueDao.error(f'Erro ao inserir ({trabalhoEstoque}): {trabalhoEstoqueDao.pegaErro()}')

    def defineProfissaoSelecionada(self):
        opcaoProfissao = input('Opçao profissão: ')
        if int(opcaoProfissao) == 0:
            return None
        return LISTA_PROFISSOES[int(opcaoProfissao) - 1]

    def defineRaridadeSelecionada(self):
        opcaoRaridade = input('Opçao raridade: ')
        if int(opcaoRaridade) == 0:
            return None
        return LISTA_RARIDADES[int(opcaoRaridade) - 1]

    def mostraListaProfissoes(self):
        limpaTela()
        print(f"{'ÍNDICE'.ljust(6)} - PROFISSÃO")
        for profissao in LISTA_PROFISSOES:
            print(f'{str(LISTA_PROFISSOES.index(profissao) + 1).ljust(6)} - {profissao}')
        print(f'{"0".ljust(6)} - Voltar')

    def mostraListaRaridades(self):
        limpaTela()
        print(f"{'ÍNDICE'.ljust(6)} - RARIDADE")
        for raridade in LISTA_RARIDADES:
            print(f'{str(LISTA_RARIDADES.index(raridade) + 1).ljust(6)} - {raridade}')
        print(f'{"0".ljust(6)} - Voltar')

    def modificaTrabalhoEstoque(self):
        while True:
            personagens = self.mostraListaPersonagens()
            if variavelExiste(personagens):
                if self.definePersonagemEscolhido(personagens):
                    while True:
                        estoque = self.mostraListaTrabalhosEstoque()
                        if variavelExiste(estoque):
                            trabalhoEstoque = self.defineTrabalhoEstoqueSelecionado(estoque)
                            if variavelExiste(trabalhoEstoque):
                                trabalhoEstoque = self.defineTrabalhoEstoqueModificado(trabalhoEstoque)
                                self.concluiModificaTrabalhoEstoque(trabalhoEstoque)
                                continue
                            break
                        break
                    continue
                break
            break

    def defineTrabalhoEstoqueModificado(self, trabalhoEstoque):
        quantidade = input(f'Quantidade trabalho: ')
        quantidade = trabalhoEstoque.quantidade if tamanhoIgualZero(quantidade) else quantidade
        trabalhoEstoque.setQuantidade(quantidade)
        return trabalhoEstoque

    def concluiModificaTrabalhoEstoque(self, trabalhoEstoque):
        estoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
        if estoqueDao.modificaTrabalhoEstoque(trabalhoEstoque):
            self.__loggerEstoqueDao.info(f'({trabalhoEstoque}) modificado com sucesso!')
            return
        self.__loggerEstoqueDao.error(f'Erro ao modificar ({trabalhoEstoque}): {estoqueDao.pegaErro()}')
    
    def removeTrabalhoEstoque(self):
        while True:
            personagens = self.mostraListaPersonagens()
            if variavelExiste(personagens):
                if self.definePersonagemEscolhido(personagens):
                    while True:
                        estoque = self.mostraListaTrabalhosEstoque()
                        if variavelExiste(estoque):
                            trabalhoEstoque = self.defineTrabalhoEstoqueSelecionado(estoque)
                            if variavelExiste(trabalhoEstoque):
                                self.concluiRemoveTrabalhoEstoque(trabalhoEstoque)
                                continue
                            break
                        break
                    continue
                break
            break

    def concluiRemoveTrabalhoEstoque(self, trabalhoEstoque):
        trabalhoEstoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
        if trabalhoEstoqueDao.removeTrabalhoEstoque(trabalhoEstoque):
            self.__loggerEstoqueDao.info(f'({trabalhoEstoque}) removido com sucesso!')
            return
        self.__loggerEstoqueDao.error(f'Erro ao remover ({trabalhoEstoque}): {trabalhoEstoqueDao.pegaErro()}')

    def defineTrabalhoEstoqueSelecionado(self, estoque):
        opcaoTrabalho = input(f'Opção trabalho: ')
        if int(opcaoTrabalho) == 0:
            return None
        trabalhoEstoque = estoque[int(opcaoTrabalho) - 1]
        return trabalhoEstoque
    
    def mostraListaTrabalhosEstoque(self):
        limpaTela()
        estoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
        estoque = estoqueDao.pegaEstoque()
        if variavelExiste(estoque):
            if tamanhoIgualZero(estoque):
                print(f'Estoque está vazio!')
            else:
                print(f'{"ÍNDICE".ljust(6)} - {"NOME".ljust(40)} | {"PROFISSÃO".ljust(25)} | {"QNT".ljust(3)} | {"NÍVEL".ljust(5)} | {"RARIDADE".ljust(10)} | ID TRABALHO')
                for trabalhoEstoque in estoque:
                    print(f'{str(estoque.index(trabalhoEstoque) + 1).ljust(6)} - {trabalhoEstoque}')
                print(f'{"0".ljust(6)} - Voltar')
            return estoque
        self.__loggerEstoqueDao.error(f'Erro ao buscar trabalhos no estoque: {estoqueDao.pegaErro()}')

    def mostraListaPersonagens(self):
        limpaTela()
        personagemDao = PersonagemDaoSqlite()
        personagens = personagemDao.pegaPersonagens()
        if variavelExiste(personagens):
            if tamanhoIgualZero(personagens):
                print('Lista de personagens está vazia!')
            else:
                print(f"{'ÍNDICE'.ljust(6)} - {'ID'.ljust(36)} | {'NOME'.ljust(17)} | {'ESPAÇO'.ljust(6)} | {'ESTADO'.ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO")
                for personagem in personagens:
                    print(f'{str(personagens.index(personagem) + 1).ljust(6)} - {personagem}')
            print(f'{"0".ljust(6)} - Voltar')
            return personagens
        self.__loggerPersonagemDao.error(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
        return None
    
    def definePersonagemEscolhido(self, personagens) -> bool:
        opcaoPersonagem = input(f'Opção: ')
        if int(opcaoPersonagem) == 0:
            return False
        self.__aplicacao.__personagemEmUso = personagens[int(opcaoPersonagem) - 1]
        self.__personagemEmUso = personagens[int(opcaoPersonagem) - 1]
        return True
    
    def mostraListaVendas(self):
        limpaTela()
        print(f'{"ÍNDICE".ljust(6)} - {"NOME".ljust(44)} | {"DATA".ljust(10)} | {"VALOR".ljust(5)} | UND')
        trabalhoVendidoDao = VendaDaoSqlite(self.__personagemEmUso)
        vendas = trabalhoVendidoDao.pegaVendas()
        if variavelExiste(vendas):
            if tamanhoIgualZero(vendas):
                print('Lista de vendas está vazia!')
            else:
                for trabalhoVendido in vendas:
                    print(f'{str(vendas.index(trabalhoVendido) + 1).ljust(6)} - {trabalhoVendido}')
            return vendas
        self.__loggerVendaDao.error(f'Erro ao buscar trabalhos vendidos: {trabalhoVendidoDao.pegaErro()}')
        return None
    
    def mostraListaTrabalhos(self):
        limpaTela()
        trabalhoDao = TrabalhoDaoSqlite()
        trabalhos = trabalhoDao.pegaTrabalhos()
        if variavelExiste(trabalhos):
            if tamanhoIgualZero(trabalhos):
                print('Lista de trabalhos está vazia!')
            else:
                print(f'{"ÍNDICE".ljust(6)} - {"NOME".ljust(44)} | {"PROFISSÃO".ljust(22)} | {"RARIDADE".ljust(9)} | NÍVEL')
                for trabalho in trabalhos:
                    print(f'{str(trabalhos.index(trabalho) + 1).ljust(6)} - {trabalho}')
            return trabalhos
        self.__loggerTrabalhoDao.error(f'Erro ao buscar trabalhos: {trabalhoDao.pegaErro()}')
        return None

    def insereTrabalhoVendido(self):
        while True:
            personagens = self.mostraListaPersonagens()
            if variavelExiste(personagens):
                if self.definePersonagemEscolhido(personagens):
                    while True:
                        vendas = self.mostraListaVendas()
                        if variavelExiste(vendas):
                            inserir = input(f'Inserir novo trabalho ao estoque: (S/N) ')
                            if inserir.lower() == 'n':
                                break
                            self.mostraListaProfissoes()
                            profissaoSelecionada = self.defineProfissaoSelecionada()
                            if variavelExiste(profissaoSelecionada):
                                self.mostraListaRaridades()
                                raridadeSelecionada = self.defineRaridadeSelecionada()
                                if variavelExiste(raridadeSelecionada):
                                    trabalhoBuscado = Trabalho()
                                    trabalhoBuscado.profissao = profissaoSelecionada
                                    trabalhoBuscado.raridade = raridadeSelecionada
                                    trabalhos = self.mostraTrabalhosPorProfissaoRaridade(trabalhoBuscado)
                                    if variavelExiste(trabalhos):
                                        trabalhoSelecionado = self.defineTrabalhoSelecionado(trabalhos)
                                        if variavelExiste(trabalhoSelecionado):
                                            novoTrabalhoVendido = self.defineNovoTrabalhoVendido(trabalhoSelecionado)
                                            if variavelExiste(novoTrabalhoVendido):
                                                self.concluiInsereTrabalhoVendido(novoTrabalhoVendido)
                                                continue
                                            break
                                        break
                                    break
                                break
                            break
                        break
                    continue
                break
            break

    def mostraTrabalhosPorProfissaoRaridade(self, trabalhoBuscado):
        limpaTela()
        trabalhoDao = TrabalhoDaoSqlite()
        trabalhos = trabalhoDao.pegaTrabalhosPorProfissaoRaridade(trabalhoBuscado)
        if variavelExiste(trabalhos):
            if tamanhoIgualZero(trabalhos):
                print('Lista de trabalhos está vazia!')
            else:
                print(f'{"ÍNDICE".ljust(6)} - {"NOME".ljust(44)} | {"PROFISSÃO".ljust(22)} | {"RARIDADE".ljust(9)} | NÍVEL')
                for trabalho in trabalhos:
                    print(f'{str(trabalhos.index(trabalho) + 1).ljust(6)} - {trabalho} | {trabalho.trabalhoNecessario}')
                return trabalhos
        self.__loggerTrabalhoDao.error(f'Erro ao buscar trabalhos por profissão e raridade: {trabalhoDao.pegaErro()}')
        return None

    def concluiInsereTrabalhoVendido(self, trabalhoVendido):
        trabalhoVendidoDao = VendaDaoSqlite(self.__personagemEmUso)
        if trabalhoVendidoDao.insereTrabalhoVendido(trabalhoVendido):
            self.__loggerVendaDao.info(f'({trabalhoVendido}) inserido com sucesso!')
            return
        self.__loggerVendaDao.error(f'Erro ao inserir ({trabalhoVendido}): {trabalhoVendidoDao.pegaErro()}')

    def defineNovoTrabalhoVendido(self, trabalho):
        descricao = input(f'Descrição da venda: ')
        data = input(f'Data da venda: ')
        quantidade = input(f'Quantidade trabalho vendido: ')
        valor = input(f'Valor do trabalho vendido: ')
        trabalhoVendido = TrabalhoVendido()
        trabalhoVendido.trabalhoId = trabalho.id
        trabalhoVendido.nomeProduto = descricao
        trabalhoVendido.dataVenda = data
        trabalhoVendido.setQuantidade(quantidade)
        trabalhoVendido.setValor(valor)
        return trabalhoVendido

    def defineVendaEscolhida(self, vendas) -> TrabalhoVendido:
        opcaoTrabalho = input(f'Opção trabalho: ')    
        if int(opcaoTrabalho) == 0:
            return None
        return vendas[int(opcaoTrabalho) - 1]
    
    def modificaTrabalhoVendido(self):
        while True:
            personagens = self.mostraListaPersonagens()
            if variavelExiste(personagens):
                if self.definePersonagemEscolhido(personagens):
                    while True:
                        vendas = self.mostraListaVendas()
                        if variavelExiste(vendas):
                            print(f'{"0".ljust(6)} - Voltar')
                            trabalhoVendidoModificado = self.defineVendaEscolhida(vendas)
                            if variavelExiste(trabalhoVendidoModificado):
                                trabalhoVendidoModificado = self.defineTrabalhoVendidoModificado(trabalhoVendidoModificado)
                                self.concluiModificaTrabalhoVendido(trabalhoVendidoModificado)
                                continue
                            break
                        break
                    continue
                break
            break

    def removeTrabalhoVendido(self):
        while True:
            personagens = self.mostraListaPersonagens()
            if variavelExiste(personagens):
                if self.definePersonagemEscolhido(personagens):
                    while True:
                        vendas = self.mostraListaVendas()
                        if variavelExiste(vendas):
                            print(f'{"0".ljust(6)} - Voltar')
                            trabalhoVendidoSelecionado = self.defineVendaEscolhida(vendas)
                            if variavelExiste(trabalhoVendidoSelecionado):
                                self.concluiRemoveTrabalhoVendido(trabalhoVendidoSelecionado)
                                continue
                            break
                        break
                    continue
                break
            break

    def concluiRemoveTrabalhoVendido(self, trabalhoVendidoSelecionado):
        trabalhoVendidoDao = VendaDaoSqlite(self.__personagemEmUso)
        if trabalhoVendidoDao.removeTrabalhoVendido(trabalhoVendidoSelecionado):
            self.__loggerVendaDao.info(f'({trabalhoVendidoSelecionado}) removido com sucesso!')
            return
        self.__loggerVendaDao.error(f'Erro ao remover ({trabalhoVendidoSelecionado}): {trabalhoVendidoDao.pegaErro()}')

    def concluiModificaTrabalhoVendido(self, trabalhoVendidoModificado):
        trabalhoVendidoDao = VendaDaoSqlite(self.__personagemEmUso)
        trabalhoVendidoModificado.nome = None
        trabalhoVendidoModificado.nivel = None
        trabalhoVendidoModificado.profissao = None
        trabalhoVendidoModificado.raridade = None
        trabalhoVendidoModificado.trabalhoNecessario = None
        if trabalhoVendidoDao.modificaTrabalhoVendido(trabalhoVendidoModificado):
            self.__loggerVendaDao.info(f'({trabalhoVendidoModificado}) modificado com sucesso!')
            return
        self.__loggerVendaDao.error(f'Erro ao modificar ({trabalhoVendidoModificado}): {trabalhoVendidoDao.pegaErro()}')

    def defineTrabalhoVendidoModificado(self, trabalhoVendidoModificado):
        limpaTela()
        descricao = input(f'Descrição do trabalho: ')
        if tamanhoIgualZero(descricao):
            descricao = trabalhoVendidoModificado.nomeProduto
        data = input(f'Data da venda: ')
        if tamanhoIgualZero(data):
            data = trabalhoVendidoModificado.dataVenda
        quantidade = input(f'Quantidade vendida: ')
        if tamanhoIgualZero(quantidade):
            quantidade = trabalhoVendidoModificado.quantidadeProduto
        valor = input(f'Valor da venda: ')
        if tamanhoIgualZero(valor):
            valor = trabalhoVendidoModificado.valorProduto
        trabalhoVendidoModificado.nomeProduto = descricao
        trabalhoVendidoModificado.dataVenda = data
        trabalhoVendidoModificado.setQuantidade(quantidade)
        trabalhoVendidoModificado.setValor(valor)
        return trabalhoVendidoModificado

    def defineTrabalhoSelecionado(self, trabalhos):
        print(f'{"0".ljust(6)} - Voltar')
        opcaoTrabalho = input(f'Opção trabalho: ')    
        if int(opcaoTrabalho) == 0:
            return None
        trabalho = trabalhos[int(opcaoTrabalho) - 1]
        return trabalho

    def sincronizaDados(self):
        self.sincronizaListaTrabalhos()
        self.sincronizaListaPersonagens()
        # self.sincronizaListaProfissoes()
        # self.sincronizaTrabalhosProducao()
        # self.sincronizaTrabalhosVendidos()

    def verificaAlteracaoListaTrabalhos(self):
        if self.__repositorioTrabalho.estaPronto:
            for trabalho in self.__repositorioTrabalho.pegaDadosModificados():
                trabalhoDao = TrabalhoDaoSqlite()
                if trabalho.nome is None:
                    trabalhoDao = TrabalhoDaoSqlite()
                    if trabalhoDao.removeTrabalho(trabalho, False):
                        self.__loggerTrabalhoDao.info(f'({trabalho}) removido com sucesso!')
                        continue
                    self.__loggerTrabalhoDao.error(f'Erro ao remover ({trabalho}): {trabalhoDao.pegaErro()}')
                    continue
                trabalhoEncontrado = trabalhoDao.pegaTrabalhoEspecificoPorId(trabalho.id)
                if trabalhoEncontrado is None:
                    self.__loggerRepositorioTrabalho.error(f'Erro ao buscar ({trabalho}) por id: {trabalhoDao.pegaErro()}')
                    continue
                if trabalhoEncontrado.nome is None:
                    trabalhoDao = TrabalhoDaoSqlite()
                    if trabalhoDao.insereTrabalho(trabalho, False):
                        self.__loggerTrabalhoDao.info(f'({trabalho}) inserido com sucesso!')
                        continue
                    self.__loggerTrabalhoDao.error(f'Erro ao inserir ({trabalho}): {trabalhoDao.pegaErro()}')
                    continue
                trabalhoDao = TrabalhoDaoSqlite()
                if trabalhoDao.modificaTrabalhoPorId(trabalho, False):
                    self.__loggerTrabalhoDao.info(f'({trabalho}) modificado com sucesso!')
                    continue
                self.__loggerTrabalhoDao.error(f'Erro ao modificar trabalho: {trabalhoDao.pegaErro()}')
            self.__repositorioTrabalho.limpaLista()

    def testeFuncao(self):
        # estoqueDao = EstoqueDaoSqlite()
        # if estoqueDao.removeColunasTabelaEstoque():
        #     self.__loggerEstoqueDao.info(f'Coluna da tabela removida')
        # else:
        #     self.__loggerEstoqueDao.error(f'Erro ao remover coluna da tabela: {estoqueDao.pegaErro()}')
        personagens = self.mostraListaPersonagens()
        if variavelExiste(personagens) and self.definePersonagemEscolhido(personagens):
            vendaDao = VendaDaoSqlite(self.__personagemEmUso)
            vendas = vendaDao.pegaTrabalhosRarosVendidos()
            if variavelExiste(vendas):
                for trabalhoVendido in vendas:
                    print(trabalhoVendido.id, trabalhoVendido.nome, trabalhoVendido.nivel, trabalhoVendido.quantidadeProduto)
                    estoqueDao = EstoqueDaoSqlite(self.__personagemEmUso)
                    quantidadeTrabalhoEmEstoque = estoqueDao.pegaQuantidadeTrabalho(trabalhoVendido)
                    if variavelExiste(quantidadeTrabalhoEmEstoque):
                        print(f'Quantidade de ({trabalhoVendido.nome}) no estoque: {quantidadeTrabalhoEmEstoque}')
                        continue
                    self.__loggerEstoqueDao.error(f'Erro ao buscar quantidade: {estoqueDao.pegaErro()}')
                    input('Clique para continuar...')
                input('Clique para continuar...')
                return
            self.__loggerVendaDao.error(f'Erro: {vendaDao.pegaErro()}')
        input('Clique para continuar...')

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
                        self.removeTrabalhoProducaoStream(personagemModificado, trabalhoProducao)
                        continue
                    trabalhoProducao.dicionarioParaObjeto(dicionario[CHAVE_LISTA_TRABALHOS_PRODUCAO])
                    trabalhoProducao.id = dicionario['idTrabalhoProducao']
                    trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagemModificado)
                    trabalhoProducaoEncontrado = trabalhoProducaoDao.pegaTrabalhoProducaoPorId(trabalhoProducao)
                    if trabalhoProducaoEncontrado == None:
                        self.__loggerTrabalhoProducaoDao.error(f'Erro ao buscar trabalho em produção por id: {trabalhoProducaoDao.pegaErro()}')
                        continue
                    if trabalhoProducaoEncontrado.id != trabalhoProducao.id:
                        self.insereTrabalhoProducaoStream(personagemModificado, trabalhoProducao)
                        continue
                    self.modificaTrabalhoProducaoStream(personagemModificado, trabalhoProducao)
                    continue
                if CHAVE_LISTA_ESTOQUE in dicionario:
                    trabalhoEstoque = TrabalhoEstoque()
                    if dicionario[CHAVE_LISTA_ESTOQUE] == None:
                        trabalhoEstoque.id = dicionario['idTrabalhoProducao']
                        trabalhoEstoqueDao = EstoqueDaoSqlite(personagemModificado)
                        trabalhoEstoqueEncontrado = trabalhoEstoqueDao.pegaTrabalhoEstoquePorId(trabalhoEstoque)
                        if variavelExiste(trabalhoEstoqueEncontrado):
                            if variavelExiste(trabalhoEstoqueEncontrado.nome):
                                # Remove trabalho do estoque
                                pass
                            continue
                        self.__loggerEstoqueDao.error(f'Erro ao buscar ({trabalhoEstoque.id}) por id: {trabalhoEstoqueDao.pegaErro()}')
                        continue
                    trabalhoEstoque.dicionarioParaObjeto(dicionario[CHAVE_LISTA_ESTOQUE])
                    trabalhoEstoqueDao = EstoqueDaoSqlite(personagemModificado)
                    trabalhoEstoqueEncontrado = trabalhoEstoqueDao.pegaTrabalhoEstoquePorId(trabalhoEstoque)
                    if variavelExiste(trabalhoEstoqueEncontrado):
                        if variavelExiste(trabalhoEstoqueEncontrado.nome):
                            # Modifica trabalho no estoque
                            continue
                        # Insere tarbalho no estoque
                        continue
                    self.__loggerEstoqueDao.error(f'Erro ao buscar ({trabalhoEstoque.id}) por id: {trabalhoEstoqueDao.pegaErro()}')
                    continue
                persoangemDao = PersonagemDaoSqlite()
                personagemEncontrado = persoangemDao.pegaPersonagemEspecificoPorId(personagemModificado)
                if variavelExiste(personagemEncontrado):
                    if variavelExiste(personagemEncontrado.nome):
                        personagemEncontrado.dicionarioParaObjeto(dicionario)
                        self.modificaPersonagemStream(personagemEncontrado)
                        continue
                    self.__loggerPersonagemDao.warning(f'({personagemModificado}) não encontrado no banco!')
                    if variavelExiste(dicionario['novoPersonagem']):
                        personagemModificado.dicionarioParaObjeto(dicionario['novoPersonagem'])
                        self.inserePersonagemStream(personagemModificado)
                    continue
                self.__loggerPersonagemDao.error(f'Erro ao buscar personagem por id: {persoangemDao.pegaErro()}')
                continue
            self.__repositorioPersonagem.limpaLista()

    def modificaPersonagemStream(self, personagemEncontrado):
        personagemDao = PersonagemDaoSqlite()
        if personagemDao.modificaPersonagem(personagemEncontrado, False):
            self.__loggerPersonagemDao.info(f'({personagemEncontrado}) modificado com sucesso!')
            return
        self.__loggerPersonagemDao.error(f'Erro ao modificar ({personagemEncontrado}): {personagemDao.pegaErro()}')

    def inserePersonagemStream(self, personagemModificado):
        personagemDao = PersonagemDaoSqlite()
        if personagemDao.inserePersonagem(personagemModificado, False):
            self.__loggerPersonagemDao.info(f'({personagemModificado}) inserido com sucesso!')
            return
        self.__loggerPersonagemDao.error(f'Erro ao inserir ({personagemModificado}): {personagemDao.pegaErro()}')

    def removeTrabalhoProducaoStream(self, personagemModificado, trabalhoProducao):
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagemModificado)
        if trabalhoProducaoDao.removeTrabalhoProducao(trabalhoProducao, False):
            self.__loggerTrabalhoProducaoDao.info(f'({trabalhoProducao}) removido com sucesso!')
            return
        self.__loggerTrabalhoProducaoDao.error(f'Erro ao remover ({trabalhoProducao}): {trabalhoProducaoDao.pegaErro()}')

    def insereTrabalhoProducaoStream(self, personagemModificado, trabalhoProducao):
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagemModificado)
        if trabalhoProducaoDao.insereTrabalhoProducao(trabalhoProducao, False):
            self.__loggerTrabalhoProducaoDao.info(f'({trabalhoProducao}) inserido com sucesso!')
            return
        self.__loggerTrabalhoProducaoDao.error(f'Erro ao inserir ({trabalhoProducao}): {trabalhoProducaoDao.pegaErro()}')

    def modificaTrabalhoProducaoStream(self, personagemModificado, trabalhoProducao):
        trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagemModificado)
        if trabalhoProducaoDao.modificaTrabalhoProducao(trabalhoProducao, False):
            self.__loggerTrabalhoProducaoDao.info(f'({trabalhoProducao}) modificado com sucesso!')
            return
        self.__loggerTrabalhoProducaoDao.error(f'Erro ao modificar ({trabalhoProducao}): {trabalhoProducaoDao.pegaErro()}')

    def menu(self):
        while True:
            self.verificaAlteracaoListaTrabalhos()
            self.verificaAlteracaoPersonagem()
            limpaTela()
            print(f'MENU')
            print(f'01 - Insere trabalho')
            print(f'02 - Modifica trabalho')
            print(f'03 - Remove trabalho')
            print(f'04 - Insere personagem')
            print(f'05 - Modifica personagem')
            print(f'06 - Remove personagem')
            print(f'07 - Insere trabalho produção')
            print(f'08 - Modifica trabalho produção')
            print(f'09 - Remove trabalho produção')
            print(f'10 - Modifica profissao')
            print(f'11 - Insere trabalho no estoque')
            print(f'12 - Modifica trabalho no estoque')
            print(f'13 - Remove trabalho no estoque')
            print(f'14 - Insere trabalho vendido')
            print(f'15 - Modifica trabalho vendido')
            print(f'16 - Remove trabalho vendido')
            print(f'20 - Pega todos trabalhos producao')
            print(f'21 - Sincroniza dados')
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
                    self.modificaTrabalho()
                    continue
                if int(opcaoMenu) == 3:
                    self.removeTrabalho()
                    continue
                if int(opcaoMenu) == 4:
                    self.inserePersonagem()
                    continue
                if int(opcaoMenu) == 5:
                    self.modificaPersonagem()
                    continue
                if int(opcaoMenu) == 6:
                    self.removePersonagem()
                    continue
                if int(opcaoMenu) == 7:
                    self.insereNovoTrabalhoProducao()
                    continue
                if int(opcaoMenu) == 8:
                    self.modificaTrabalhoProducao()
                    continue
                if int(opcaoMenu) == 9:
                    self.removeTrabalhoProducao()
                    continue
                if int(opcaoMenu) == 10:
                    self.modificaProfissao()
                    continue
                if int(opcaoMenu) == 11:
                    self.insereTrabalhoEstoque()
                    continue
                if int(opcaoMenu) == 12:
                    self.modificaTrabalhoEstoque()
                    continue
                if int(opcaoMenu) == 13:
                    self.removeTrabalhoEstoque()
                    continue
                if int(opcaoMenu) == 14:
                    self.insereTrabalhoVendido()
                    continue
                if int(opcaoMenu) == 15:
                    self.modificaTrabalhoVendido()
                    continue
                if int(opcaoMenu) == 16:
                    self.removeTrabalhoVendido()
                    continue
                if int(opcaoMenu) == 20:
                    self.pegaTodosTrabalhosProducao()
                    continue
                if int(opcaoMenu) == 21:
                    self.sincronizaDados()
                    continue
                if int(opcaoMenu) == 24:
                    self.testeFuncao()
                    continue
            except Exception as erro:
                print(f'Opção inválida! Erro: {erro}')
                input(f'Clique para continuar...')

if __name__=='__main__':
    CRUD()