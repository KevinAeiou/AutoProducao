import logging
from uuid import uuid4
from time import sleep
from utilitarios import limpaTela, variavelExiste, tamanhoIgualZero
from constantes import CHAVE_PROFISSAO_ARMA_DE_LONGO_ALCANCE, CHAVE_PROFISSAO_ARMA_CORPO_A_CORPO, CHAVE_PROFISSAO_ARMADURA_DE_TECIDO, CHAVE_PROFISSAO_ARMADURA_LEVE, CHAVE_PROFISSAO_ARMADURA_PESADA, CHAVE_PROFISSAO_ANEIS, CHAVE_PROFISSAO_AMULETOS, CHAVE_PROFISSAO_CAPOTES, CHAVE_PROFISSAO_BRACELETES, CHAVE_LICENCA_NOVATO, CHAVE_LICENCA_APRENDIZ, CHAVE_LICENCA_MESTRE, CHAVE_LICENCA_INICIANTE, CODIGO_PARA_PRODUZIR

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

class CRUD:
    def __init__(self):
        logging.basicConfig(level = logging.INFO, filename = 'logs/aplicacao.log', encoding='utf-8', format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt = '%d/%m/%Y %I:%M:%S %p')
        self.__personagemEmUso = None
        self.__repositorioPersonagem = RepositorioPersonagem()
        self.__repositorioTrabalho = RepositorioTrabalho()
        self.__loggerTrabalhoDao = logging.getLogger('trabalhoDao')
        self.__loggerRepositorioPersonagem = logging.getLogger('repositorioPersonagem')
        self.__loggerPersonagemDao = logging.getLogger('personagemDao')
        self.__loggerTrabalhoProducaoDao = logging.getLogger('trabalhoProducaoDao')
        self.__loggerRepositorioTrabalho = logging.getLogger('repositorioTrabalho')
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
            trabalhoDao = TrabalhoDaoSqlite()
            trabalhos = trabalhoDao.pegaTrabalhos()
            if variavelExiste(trabalhos):
                if tamanhoIgualZero(trabalhos):
                    print('Lista de trabalhos está vazia!')
                else:
                    print(f'{"NOME".ljust(44)} | {"PROFISSÃO".ljust(22)} | {"RARIDADE".ljust(9)} | NÍVEL')
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
                        novoTrabalho = Trabalho()
                        novoTrabalho.nome = nome
                        novoTrabalho.nomeProducao = nomeProducao
                        novoTrabalho.experiencia = int(experiencia)
                        novoTrabalho.nivel = int(nivel)
                        novoTrabalho.profissao = profissao
                        novoTrabalho.raridade = raridade
                        novoTrabalho.trabalhoNecessario = trabalhoNecessario
                        trabalhoDao = TrabalhoDaoSqlite()
                        logger = logging.getLogger('trabalhoDao')
                        if trabalhoDao.insereTrabalho(novoTrabalho):
                            logger.info(f'({novoTrabalho}) inserido com sucesso!')
                            continue
                        logger.error(f'Erro ao inserir ({novoTrabalho}): {trabalhoDao.pegaErro()}')
                    except Exception as erro:
                        print(f'Opção inválida!')
                        input(f'Clique para continuar...')
                except Exception as erro:
                    print(f'Opção inválida!')
                    input(f'Clique para continuar...')
                continue
            print(f'Erro ao buscar trabalhos no banco: {trabalhoDao.pegaErro()}')
            break

    def modificaTrabalho(self):
        logger = logging.getLogger('trabalhoDao')
        while True:
            limpaTela()
            trabalhoDao = TrabalhoDaoSqlite()
            trabalhos = trabalhoDao.pegaTrabalhos()
            if variavelExiste(trabalhos):
                if tamanhoIgualZero(trabalhos):
                    print('Lista de trabalhos está vazia!')
                else:
                    print(f"{'ÍNDICE'.ljust(6)} - {'NOME'.ljust(44)} | {'PROFISSÃO'.ljust(22)} | {'RARIDADE'.ljust(9)} | NÍVEL")
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
                trabalhoEscolhido.nomeProducao = novoNomeProducao
                trabalhoEscolhido.setExperiencia(novaExperiencia)
                trabalhoEscolhido.setNivel(novoNivel)
                trabalhoEscolhido.profissao = novaProfissao
                trabalhoEscolhido.raridade = novaRaridade
                trabalhoEscolhido.trabalhoNecessario = novoTrabalhoNecessario
                trabalhoDao = TrabalhoDaoSqlite()
                if trabalhoDao.modificaTrabalhoPorId(trabalhoEscolhido):
                    logger.info(f'({trabalhoEscolhido}) modificado com sucesso!')
                    continue
                logger.error(f'Erro ao modificar ({trabalhoEscolhido}): {trabalhoDao.pegaErro()}')
                input(f'Clique para continuar...')
                continue
            logger.error(f'Erro ao buscar trabalhos no banco: {trabalhoDao.pegaErro()}')
            input(f'Clique para continuar...')
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
                print(f"{'0'.ljust(6)} - Voltar")
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

    def insereNovoTrabalhoProducao(self):
        logger = logging.getLogger('trabalhoProducaoDao')
        while True:
            limpaTela()
            print(f"{'ÍNDICE'.ljust(6)} | {'ID'.ljust(36)} | {'NOME'.ljust(17)} | {'ESPAÇO'.ljust(6)} | {'ESTADO'.ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO")
            personagemDao = PersonagemDaoSqlite()
            personagens = personagemDao.pegaPersonagens()
            if variavelExiste(personagens):
                if tamanhoIgualZero(personagens):
                    print('Lista de personagens está vazia!')
                else:
                    for personagem in personagens:
                        print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
                print(f"{'0'.ljust(6)} - Voltar")
                opcaoPersonagem = input(f'Opção:')
                if int(opcaoPersonagem) == 0:
                    break
                while True:
                    limpaTela()
                    personagem = personagens[int(opcaoPersonagem) - 1]
                    self.__personagemEmUso = personagem
                    trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
                    trabalhos = trabalhoProducaoDao.pegaTrabalhosProducao()
                    if variavelExiste(trabalhos):
                        if tamanhoIgualZero(trabalhos):
                            print('Lista de trabalhos em produção está vazia!')
                        else:
                            print(f"{'NOME'.ljust(44)} | {'PROFISSÃO'.ljust(22)} | {'NÍVEL'.ljust(5)} | {'ESTADO'.ljust(10)} | {'LICENÇA'.ljust(31)} | RECORRÊNCIA")
                            for trabalhoProducao in trabalhos:
                                print(trabalhoProducao)
                        opcaoTrabalho = input(f'Adicionar novo trabalho? (S/N) ')    
                        if (opcaoTrabalho).lower() == 'n':
                            break
                        limpaTela()
                        profissoes = [CHAVE_PROFISSAO_ARMA_DE_LONGO_ALCANCE, CHAVE_PROFISSAO_ARMA_CORPO_A_CORPO, CHAVE_PROFISSAO_ARMADURA_DE_TECIDO, CHAVE_PROFISSAO_ARMADURA_LEVE, CHAVE_PROFISSAO_ARMADURA_PESADA, CHAVE_PROFISSAO_ANEIS, CHAVE_PROFISSAO_AMULETOS, CHAVE_PROFISSAO_CAPOTES, CHAVE_PROFISSAO_BRACELETES]
                        print(f"{'ÍNDICE'.ljust(6)} - PROFISSÃO")
                        for profissao in profissoes:
                            print(f'{str(profissoes.index(profissao) + 1).ljust(6)} - {profissao}')
                        opcaoProfissao = input(f'Opção de profissao: ')
                        if int(opcaoProfissao) == 0:
                            continue
                        profissao = profissoes[int(opcaoProfissao) - 1]
                        trabalhosFiltrados = []
                        trabalhoDao = TrabalhoDaoSqlite()
                        trabalhos = trabalhoDao.pegaTrabalhos()
                        if variavelExiste(trabalhos):
                            for trabalho in trabalhos:
                                if trabalho.profissao == profissao:
                                    trabalhosFiltrados.append(trabalho)
                            print(f"{'INDICE'.ljust(6)} - {'NOME'.ljust(40)} | {('PROFISSÃO').ljust(20)} | NÍVEL")
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
                            novoTrabalhoProducao.id = str(uuid4())
                            novoTrabalhoProducao.idTrabalho = trabalho.id
                            novoTrabalhoProducao.recorrencia = recorrencia
                            novoTrabalhoProducao.tipo_licenca = licenca
                            novoTrabalhoProducao.estado = CODIGO_PARA_PRODUZIR
                            self.insereTrabalhoProducao(novoTrabalhoProducao)
                            continue
                        logger.error(f'Erro ao buscar trabalhos: {trabalhoDao.pegaErro()}')
                        input(f'Clique para continuar...')
                        break
                    logger.error(f'Erro ao buscar trabalhos em produção: {trabalhoProducaoDao.pegaErro()}')
                    input(f'Clique para continuar...')
                    break
                continue
            logger.error(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
            input(f'Clique para continuar...')
            break
    
    def modificaTrabalhoProducao(self):
        logger = logging.getLogger('trabalhoProducaoDao')
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
                print(f"{'0'.ljust(6)} - Voltar")
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
                            print(f'Lista de trabalhos em produção está vazia!')
                        else:
                            for trabalhoProducao in trabalhosProducao:
                                print(f'{str(trabalhosProducao.index(trabalhoProducao) + 1).ljust(6)} - {trabalhoProducao}')
                        print(f"{'0'.ljust(6)} - Voltar")
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
                            logger.info(f'({trabalhoEscolhido}) modificado com sucesso!')
                            continue
                        logger.error(f'Erro ao modificar ({trabalhoEscolhido}): {trabalhoProducaoDao.pegaErro()}')
                        input(f'Clique para continuar...')
                        continue
                    logger.error(f'Erro ao buscar trabalhos em produção: {trabalhoProducaoDao.pegaErro()}')
                    input(f'Clique para continuar...')
                    break
                continue
            logger.error(f'Erro ao buscar personagens: {personagemDao.pegaErro()}')
            input(f'Clique para continuar...')
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
                print(f"{'0'.ljust(6)} - Voltar")
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
                        print(f"{'0'.ljust(6)} - Voltar")
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
                print(f"{'0'.ljust(6)} - Voltar")
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
                        print(f"{'0'.ljust(6)} - Voltar")
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
                trabalhoEncontrado = trabalhoDao.pegaTrabalhoEspecificoPorId(trabalho)
                if trabalhoEncontrado is None:
                    self.__loggerRepositorioTrabalho.error(f'Erro ao buscar trabalho por id: {trabalhoDao.pegaErro()}')
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
        if self.__repositorioTrabalho.abreStream():
            self.__loggerRepositorioTrabalho.info(f'Stream repositório trabalhos iniciada com sucesso!')
        else:
            self.__loggerRepositorioTrabalho.error(f'Erro ao iniciar stream repositório trabalhos: {self.__repositorioTrabalho.pegaErro()}')
        # if self.__repositorioPersonagem.abreStream():
        #     self.__loggerRepositorioPersonagem.info(f'Stream repositório personagem iniciada com sucesso!')
        # else:
        #     self.__loggerRepositorioPersonagem.info(f'Erro ao inicar stream: {self.__repositorioPersonagem.pegaErro()}')
        while True:
            self.verificaAlteracaoListaTrabalhos()
            # self.verificaAlteracaoPersonagem()

    def verificaAlteracaoPersonagem(self):
        if self.__repositorioPersonagem.estaPronto:
            dicionarios = self.__repositorioPersonagem.pegaDadosModificados()
            for dicionario in dicionarios:
                personagemModificado = Personagem()
                personagemModificado.id = dicionario['id']
                if 'Lista_desejo' in dicionario:
                    trabalhoProducao = TrabalhoProducao()
                    if dicionario['Lista_desejo'] == None:
                        trabalhoProducao.id = dicionario['idTrabalhoProducao']
                        self.removeTrabalhoProducaoStream(personagemModificado, trabalhoProducao)
                        continue
                    trabalhoProducao.dicionarioParaObjeto(dicionario['Lista_desejo'])
                    trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagemModificado)
                    trabalhoProducaoEncontrado = trabalhoProducaoDao.pegaTrabalhoProducaoPorId(trabalhoProducao)
                    if trabalhoProducaoEncontrado == None:
                        self.__loggerTrabalhoProducaoDao.error(f'Erro ao buscar trabalho em produção por id: {trabalhoProducaoDao.pegaErro()}')
                        continue
                    if trabalhoProducaoEncontrado.nome == None:
                        self.insereTrabalhoProducaoStream(personagemModificado, trabalhoProducao)
                        continue
                    self.modificaTrabalhoProducaoStream(personagemModificado, trabalhoProducao)
                    continue
                if dicionario['novoPersonagem'] == None:
                    persoangemDao = PersonagemDaoSqlite()
                    personagemEncontrado = persoangemDao.pegaPersonagemEspecificoPorId(personagemModificado)
                    if personagemEncontrado == None:
                        self.__loggerPersonagemDao.error(f'Erro ao buscar personagem por id: {persoangemDao.pegaErro()}')
                        continue
                    if personagemEncontrado.nome == None:
                        self.__loggerPersonagemDao.info(f'({personagemModificado}) não encontrado no banco!')
                        continue
                    personagemEncontrado.dicionarioParaObjeto(dicionario)
                    self.modificaPersonagemStream(personagemEncontrado)
                    continue
                personagemModificado.dicionarioParaObjeto(dicionario['novoPersonagem'])
                self.inserePersonagemStream(personagemModificado)
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
            limpaTela()
            print(f'MENU')
            print(f'01 - Adiciona trabalho')
            print(f'02 - Modifica trabalho')
            print(f'03 - Remove trabalho')
            print(f'04 - Insere personagem')
            print(f'05 - Modifica personagem')
            print(f'06 - Remove personagem')
            print(f'07 - Adiciona trabalho produção')
            print(f'08 - Modifica trabalho produção')
            print(f'09 - Remove trabalho produção')
            print(f'10 - Modifica profissao')
            print(f'08 - Mostra vendas')
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
                # if int(opcaoMenu) == 8:
                #     self.mostraVendas()
                #     continue
                # if int(opcaoMenu) == 12:
                #     self.insereTrabalhoEstoque()
                #     continue
                # if int(opcaoMenu) == 13:
                #     self.modificaTrabalhoEstoque()
                #     continue
                # if int(opcaoMenu) == 14:
                #     self.removeTrabalhoEstoque()
                #     continue
                # if int(opcaoMenu) == 15:
                #     self.pegaTodosTrabalhosEstoque()
                #     continue
                # if int(opcaoMenu) == 16:
                #     # insere trabalho vendido
                #     self.insereTrabalhoVendido()
                #     continue
                # if int(opcaoMenu) == 17:
                #     # modifica trabalho vendido
                #     self.modificaTrabalhoVendido()
                #     continue
                # if int(opcaoMenu) == 18:
                #     # remove trabalho vendido
                #     self.removeTrabalhoVendido()
                #     continue
                # if int(opcaoMenu) == 19:
                #     # pega todos trabalhos vendidos
                #     self.pegaTodosTrabalhosVendidos()
                #     continue
                if int(opcaoMenu) == 20:
                    self.pegaTodosTrabalhosProducao()
                    continue
                if int(opcaoMenu) == 21:
                    self.sincronizaDados()
                    continue
                # if int(opcaoMenu) == 22:
                #     # pega todos trabalhos vendidos
                #     self.pegaTodasProfissoes()
                #     continue
                # if int(opcaoMenu) == 23:
                #     # pega todos trabalhos vendidos
                #     self.redefineListaDeProfissoes()
                #     continue
                if int(opcaoMenu) == 24:
                    # pega todos trabalhos vendidos
                    self.testeFuncao()
                    continue
            except Exception as erro:
                print(f'Opção inválida! Erro: {erro}')
                input(f'Clique para continuar...')

if __name__=='__main__':
    CRUD()