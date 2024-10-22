import logging
from uuid import uuid4
from utilitarios import limpaTela, variavelExiste, tamanhoIgualZero
from constantes import CHAVE_PROFISSAO_ARMA_DE_LONGO_ALCANCE, CHAVE_PROFISSAO_ARMA_CORPO_A_CORPO, CHAVE_PROFISSAO_ARMADURA_DE_TECIDO, CHAVE_PROFISSAO_ARMADURA_LEVE, CHAVE_PROFISSAO_ARMADURA_PESADA, CHAVE_PROFISSAO_ANEIS, CHAVE_PROFISSAO_AMULETOS, CHAVE_PROFISSAO_CAPOTES, CHAVE_PROFISSAO_BRACELETES, CHAVE_LICENCA_NOVATO, CHAVE_LICENCA_APRENDIZ, CHAVE_LICENCA_MESTRE, CHAVE_LICENCA_INICIANTE, CODIGO_PARA_PRODUZIR

from dao.trabalhoDaoSqlite import TrabalhoDaoSqlite
from dao.personagemDaoSqlite import PersonagemDaoSqlite
from dao.trabalhoProducaoDaoSqlite import TrabalhoProducaoDaoSqlite
from dao.estoqueDaoSqlite import EstoqueDaoSqlite
from dao.vendaDaoSqlite import VendaDaoSqlite

from repositorio.repositorioTrabalho import RepositorioTrabalho

from modelos.trabalho import Trabalho
from modelos.trabalhoProducao import TrabalhoProducao
from modelos.personagem import Personagem

class CRUD:
    def __init__(self):
        logging.basicConfig(level = logging.INFO, filename = 'logs/aplicacao.log', encoding='utf-8', format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt = '%d/%m/%Y %I:%M:%S %p')
        self.__personagemEmUso = None
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
            print(f'{('ÍNDICE').ljust(6)} - {('NOME').ljust(44)} | {('PROFISSÃO').ljust(22)} | {('RARIDADE').ljust(9)} | NÍVEL')
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
            print(f'{('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
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
                    print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
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
                    print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
                    for personagem in personagens:
                        print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
                print(f'{'0'.ljust(6)} | Voltar')
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
            print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
            personagemDao = PersonagemDaoSqlite()
            personagens = personagemDao.pegaPersonagens()
            if variavelExiste(personagens):
                if tamanhoIgualZero(personagens):
                    print('Lista de personagens está vazia!')
                else:
                    for personagem in personagens:
                        print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
                print(f'{'0'.ljust(6)} | Voltar')
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
                            print(f'{('NOME').ljust(44)} | {('PROFISSÃO').ljust(22)} | {('NÍVEL').ljust(5)} | {('ESTADO').ljust(10)} | {('LICENÇA').ljust(31)} | RECORRÊNCIA')
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
                        if variavelExiste(trabalhos):
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
                            novoTrabalhoProducao.id = str(uuid4())
                            novoTrabalhoProducao.trabalhoId = trabalho.id
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
                    print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
                    for personagem in personagens:
                        print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
                print(f'{'0'.ljust(6)} | Voltar')
                opcaoPersonagem = input(f'Opção: ')
                if int(opcaoPersonagem) == 0:
                    break
                personagem = personagens[int(opcaoPersonagem) - 1]
                while True:
                    limpaTela()
                    trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(personagem)
                    trabalhosProducao = trabalhoProducaoDao.pegaTrabalhosProducao()
                    if variavelExiste(trabalhosProducao):
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
                    print(f'{('ÍNDICE').ljust(6)} | {('ID').ljust(36)} | {('NOME').ljust(17)} | {('ESPAÇO').ljust(6)} | {('ESTADO').ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO')
                    for personagem in personagens:
                        print(f'{str(personagens.index(personagem) + 1).ljust(6)} | {personagem}')
                print(f'{'0'.ljust(6)} | Voltar')
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
                            print(f'{('ÍNDICE').ljust(6)} - {('NOME').ljust(40)} | {('PROFISSÃO').ljust(21)} | {('NÍVEL').ljust(5)} | {('ESTADO').ljust(10)} | LICENÇA')
                            for trabalhoProducao in trabalhosProducao:
                                print(f'{str(trabalhosProducao.index(trabalhoProducao) + 1).ljust(6)} - {trabalhoProducao}')
                        print(f'{'0'.ljust(6)} | Voltar')
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
        repositorioTrabalho = RepositorioTrabalho()        
        trabalhosServidor = repositorioTrabalho.pegaTodosTrabalhos()
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
        print(f'Erro ao buscar trabalhos no servidor: {repositorioTrabalho.pegaErro()}')

    def sincronizaDados(self):
        self.sincronizaListaTrabalhos()
        self.sincronizaListaPersonagens()
        self.sincronizaListaProfissoes()
        self.sincronizaTrabalhosProducao()
        self.sincronizaTrabalhosVendidos()
    
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
            print(f'11 - Modifica profissao')
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
                # if int(opcaoMenu) == 4:
                #     self.modificaProfissao()
                #     continue
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
                # if int(opcaoMenu) == 20:
                #     # pega todos trabalhos produção
                #     self.pegaTodosTrabalhosProducao()
                #     continue
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
                # if int(opcaoMenu) == 24:
                #     # pega todos trabalhos vendidos
                #     self.testeFuncao()
                #     continue
            except Exception as erro:
                print(f'Opção inválida! Erro: {erro}')
                input(f'Clique para continuar...')

if __name__=='__main__':
    CRUD()