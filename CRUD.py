import logging
from uuid import uuid4
from utilitarios import limpaTela, variavelExiste, tamanhoIgualZero, textoEhIgual
from constantes import LISTA_PROFISSOES, LISTA_RARIDADES, LISTA_LICENCAS, CODIGO_PARA_PRODUZIR, CODIGO_QUANTIDADE_MINIMA_TRABALHO_RARO_EM_ESTOQUE, CHAVE_LICENCA_NOVATO, CHAVE_LICENCA_INICIANTE, CHAVE_RARIDADE_MELHORADO

from dao.trabalhoProducaoDaoSqlite import TrabalhoProducaoDaoSqlite

from db.db import MeuBanco

from modelos.trabalho import Trabalho
from modelos.trabalhoProducao import TrabalhoProducao
from modelos.personagem import Personagem
from modelos.trabalhoEstoque import TrabalhoEstoque
from modelos.trabalhoVendido import TrabalhoVendido
from modelos.profissao import Profissao

from main import Aplicacao

class CRUD:
    def __init__(self):
        logging.basicConfig(level = logging.INFO, filename = 'logs/aplicacao.log', encoding='utf-8', format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt = '%d/%m/%Y %I:%M:%S %p')
        self.__personagemEmUso = None
        self.__aplicacao = Aplicacao()
        self.__loggerTrabalhoProducaoDao = logging.getLogger('trabalhoProducaoDao')
        self.menu()
    
    def insereNovoTrabalho(self):
        while True:
            limpaTela()
            trabalhoBuscado = Trabalho()
            print(f'{"ÍNDICE".ljust(6)} - {"PROFISSÃO".ljust(22)}')
            for profissao in LISTA_PROFISSOES:
                print(f'{str(LISTA_PROFISSOES.index(profissao) + 1).ljust(6)} - {profissao}')
            print(f'{"0".ljust(6)} - {"Voltar".ljust(9)}')
            opcaoProfissao = input(f'Opção de profissao: ')
            if int(opcaoProfissao) == 0:
                break
            trabalhoBuscado.profissao = LISTA_PROFISSOES[int(opcaoProfissao) - 1]
            limpaTela()
            print(f'{"ÍNDICE".ljust(6)} - {"RARIDADE".ljust(9)}')
            for raridade in LISTA_RARIDADES:
                print(f'{str(LISTA_RARIDADES.index(raridade) + 1).ljust(6)} - {raridade}')
            print(f'{"0".ljust(6)} - {"Voltar".ljust(9)}')
            opcaoRaridade = input(f'Opção raridade: ')
            if int(opcaoRaridade) == 0:
                continue
            trabalhoBuscado.raridade = LISTA_RARIDADES[int(opcaoRaridade) - 1]
            while True:
                limpaTela()
                trabalhos = self.__aplicacao.pegaTrabalhosPorProfissaoRaridade(trabalhoBuscado)
                if tamanhoIgualZero(trabalhos):
                    print('Lista de trabalhos está vazia!')
                else:
                    print(f'{"NOME".ljust(44)} | {"PROFISSÃO".ljust(22)} | {"RARIDADE".ljust(9)} | {"NÍVEL".ljust(5)} | TRABALHOS NECESSÁRIOS')
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
                self.__aplicacao.insereTrabalho(novoTrabalho)
                continue

    def modificaTrabalho(self):
        while True:
            limpaTela()
            trabalhoBuscado = Trabalho()
            print(f'{"ÍNDICE".ljust(6)} - {"PROFISSÃO".ljust(22)}')
            for profissao in LISTA_PROFISSOES:
                print(f'{str(LISTA_PROFISSOES.index(profissao) + 1).ljust(6)} - {profissao}')
            print(f'{"0".ljust(6)} - Voltar')
            opcaoProfissao = input(f'Opção de profissao: ')
            if int(opcaoProfissao) == 0:
                break
            trabalhoBuscado.profissao = LISTA_PROFISSOES[int(opcaoProfissao) - 1]
            limpaTela()
            print(f'{"ÍNDICE".ljust(6)} - {"RARIDADE".ljust(9)}')
            for raridade in LISTA_RARIDADES:
                print(f'{str(LISTA_RARIDADES.index(raridade) + 1).ljust(6)} - {raridade}')
            print(f'{"0".ljust(6)} - Voltar')
            opcaoRaridade = input(f'Opção raridade: ')
            if int(opcaoRaridade) == 0:
                continue
            trabalhoBuscado.raridade = LISTA_RARIDADES[int(opcaoRaridade) - 1]
            while True:
                limpaTela()
                trabalhos = self.__aplicacao.pegaTrabalhosPorProfissaoRaridade(trabalhoBuscado)
                if tamanhoIgualZero(trabalhos):
                    print('Lista de trabalhos está vazia!')
                else:
                    print(f"{'ÍNDICE'.ljust(6)} - {'NOME'.ljust(44)} | {'PROFISSÃO'.ljust(22)} | {'RARIDADE'.ljust(9)} | {'NÍVEL'.ljust(5)} | TRABALHOS NECESSÁRIOS")
                    for trabalho in trabalhos:
                        print(f'{str(trabalhos.index(trabalho) + 1).ljust(6)} - {trabalho} | {trabalho.trabalhoNecessario}')
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
                trabalhoEscolhido.experiencia = int(novaExperiencia)
                trabalhoEscolhido.nivel = int(novoNivel)
                trabalhoEscolhido.profissao = novaProfissao
                trabalhoEscolhido.raridade = novaRaridade
                trabalhoEscolhido.trabalhoNecessario = novoTrabalhoNecessario
                self.__aplicacao.modificaTrabalho(trabalhoEscolhido)

    def removeTrabalho(self):
        while True:
            limpaTela()
            trabalhoBuscado = Trabalho()
            print(f'{"ÍNDICE".ljust(6)} - {"PROFISSÃO".ljust(22)}')
            for profissao in LISTA_PROFISSOES:
                print(f'{str(LISTA_PROFISSOES.index(profissao) + 1).ljust(6)} - {profissao}')
            print(f'{"0".ljust(6)} - Voltar')
            opcaoProfissao = input(f'Opção de profissao: ')
            if int(opcaoProfissao) == 0:
                break
            trabalhoBuscado.profissao = LISTA_PROFISSOES[int(opcaoProfissao) - 1]
            limpaTela()
            print(f'{"ÍNDICE".ljust(6)} - {"RARIDADE".ljust(9)}')
            for raridade in LISTA_RARIDADES:
                print(f'{str(LISTA_RARIDADES.index(raridade) + 1).ljust(6)} - {raridade}')
            print(f'{"0".ljust(6)} - Voltar')
            opcaoRaridade = input(f'Opção raridade: ')
            if int(opcaoRaridade) == 0:
                continue
            trabalhoBuscado.raridade = LISTA_RARIDADES[int(opcaoRaridade) - 1]
            while True:
                limpaTela()
                trabalhos = self.__aplicacao.pegaTrabalhosPorProfissaoRaridade(trabalhoBuscado)
                print(f"{'ÍNDICE'.ljust(6)} - {'NOME'.ljust(44)} | {'PROFISSÃO'.ljust(22)} | {'RARIDADE'.ljust(9)} | {'NÍVEL'.ljust(5)} | TRABALHOS NECESSÁRIOS")
                if tamanhoIgualZero(trabalhos):
                    print('Lista de trabalhos está vazia!')
                else:
                    for trabalho in trabalhos:
                        print(f'{str(trabalhos.index(trabalho) + 1).ljust(6)} - {trabalho} | {trabalho.trabalhoNecessario}')
                print(f'{"0".ljust(6)} - Voltar')
                opcaoTrabalho = input(f'Opção trabalho: ')    
                if int(opcaoTrabalho) == 0:
                    break
                trabalhoEscolhido = trabalhos[int(opcaoTrabalho) - 1]
                self.__aplicacao.removeTrabalho(trabalhoEscolhido)
        
    def inserePersonagem(self):
        while True:
            limpaTela()
            print(f"{'ID'.ljust(36)} | {'NOME'.ljust(17)} | {'ESPAÇO'.ljust(6)} | {'ESTADO'.ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO")
            personagens = self.__aplicacao.pegaPersonagens()
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
            self.__aplicacao.inserePersonagem(novoPersonagem)

    def modificaPersonagem(self):
        while True:
            limpaTela()
            personagens = self.__aplicacao.pegaPersonagens()
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
            self.__aplicacao.modificaPersonagem(personagem)
    
    def removePersonagem(self):
        while True:
            limpaTela()
            personagens = self.__aplicacao.pegaPersonagens()
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
            self.__aplicacao.removePersonagem(personagem)

    def mostraListaTrabalhosProducao(self):
        limpaTela()
        trabalhos = self.__aplicacao.pegaTrabalhosProducao()
        if tamanhoIgualZero(trabalhos):
            print('Lista de trabalhos em produção está vazia!')
        else:
            print(f"{'ÍNDICE'.ljust(6)} - {'NOME'.ljust(44)} | {'PROFISSÃO'.ljust(22)} | {'NÍVEL'.ljust(5)} | {'ESTADO'.ljust(10)} | {'LICENÇA'.ljust(34)} | RECORRÊNCIA")
            for trabalhoProducao in trabalhos:
                estado = 'Produzir' if trabalhoProducao.estado == 0 else 'Produzindo' if trabalhoProducao.estado == 1 else 'Feito'
                recorrencia = 'Recorrente' if trabalhoProducao.recorrencia else 'Único'
                print(f'{str(trabalhos.index(trabalhoProducao) + 1).ljust(6)} - {trabalhoProducao.nome.ljust(44)} | {trabalhoProducao.profissao.ljust(22)} | {str(trabalhoProducao.nivel).ljust(5)} | {estado.ljust(10)} | {trabalhoProducao.tipo_licenca.ljust(34)} | {recorrencia}')
        return trabalhos
    
    def mostraListaTrabalhosPorProfissaoRaridade(self, trabalhoBuscado):
        limpaTela()
        trabalhos = self.__aplicacao.pegaTrabalhosPorProfissaoRaridade(trabalhoBuscado)
        if tamanhoIgualZero(trabalhos):
            print(f'Nem um trabalho encontrado!')
        else:
            print(f"{'ÍNDICE'.ljust(6)} - {'NOME'.ljust(40)} | {('PROFISSÃO').ljust(20)} | NÍVEL")
            for trabalho in trabalhos:
                print(f'{str(trabalhos.index(trabalho) + 1).ljust(6)} - {trabalho}')
        return trabalhos
    
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
    
    def defineInsereProfissao(self) -> bool:
        opcao: str = input(f'Inserir nova profissão? (S/N) ')
        return True if opcao.lower() == 's' else False

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
                            self.__aplicacao.insereTrabalhoProducao(novoTrabalhoProducao)
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
                    trabalhoProducaoSelecionado = self.defineTrabalhoProducaoSelecionado(trabalhos)
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
                            self.__aplicacao.modificaTrabalhoProducao(trabalhoProducaoSelecionado)
                            continue
                        break
                    break
                continue
            break
    
    def removeTrabalhoProducao(self):
        while True:
            personagens = self.mostraListaPersonagens()
            if variavelExiste(personagens) and self.definePersonagemEscolhido(personagens):
                while True: 
                    trabalhosProducao = self.mostraListaTrabalhosProducao()
                    trabalhoRemovido = self.defineTrabalhoProducaoSelecionado(trabalhosProducao)
                    if trabalhoRemovido is None:
                        break
                    self.__aplicacao.removeTrabalhoProducao(trabalhoRemovido)
                continue
            break

    def removeProfissao(self):
        while True:
            limpaTela()
            personagens = self.__aplicacao.pegaPersonagens()
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
                self.__aplicacao.personagemEmUso(personagens[int(opcaoPersonagem) - 1])
                profissoes = self.__aplicacao.pegaProfissoes()
                if tamanhoIgualZero(profissoes):
                    self.__aplicacao.insereListaProfissoes()
                    continue
                print(f"{'ÍNDICE'.ljust(6)} - {'ID'.ljust(40)} | {'ID PERSONAGEM'.ljust(40)} | {'NOME'.ljust(22)} | {'EXP'.ljust(6)} | PRIORIDADE")
                for profissao in profissoes:
                    print(f'{str(profissoes.index(profissao) + 1).ljust(6)} - {profissao}')
                print(f'{"0".ljust(6)} - Voltar')
                opcaoProfissao = input(f'Opção: ')
                if int(opcaoProfissao) == 0:
                    break
                profissaoRemovida = profissoes[int(opcaoProfissao)-1]
                self.__aplicacao.removeProfissao(profissaoRemovida)

    def insereProfissao(self):
        while True:
            personagens = self.mostraListaPersonagens()
            if variavelExiste(personagens) and self.definePersonagemEscolhido(personagens):
                while True:
                    profissoes = self.__aplicacao.pegaProfissoes()
                    if tamanhoIgualZero(profissoes):
                        self.__aplicacao.insereListaProfissoes()
                        continue
                    print(f"{'ÍNDICE'.ljust(6)} - {'ID'.ljust(40)} | {'ID PERSONAGEM'.ljust(40)} | {'NOME'.ljust(22)} | {'EXP'.ljust(6)} | PRIORIDADE")
                    for profissao in profissoes:
                        print(f'{str(profissoes.index(profissao) + 1).ljust(6)} - {profissao}')
                    insereProfissao = self.defineInsereProfissao()
                    if variavelExiste(profissoes) and insereProfissao:
                        self.mostraListaProfissoes()
                        nomeProfissao = self.defineProfissaoSelecionada()
                        experiencia = self.defineExperiencia()
                        profissao: Profissao = Profissao()
                        profissao.nome = nomeProfissao
                        profissao.setExperiencia(experiencia= experiencia)
                        self.__aplicacao.insereProfissao(profissao= profissao)
                        continue
                    break
                continue
            break

    def modificaProfissao(self):
        while True:
            limpaTela()
            personagens = self.__aplicacao.pegaPersonagens()
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
                self.__aplicacao.personagemEmUso(personagens[int(opcaoPersonagem) - 1])
                profissoes = self.__aplicacao.pegaProfissoes()
                if tamanhoIgualZero(profissoes):
                    self.__aplicacao.insereListaProfissoes()
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
                self.__aplicacao.modificaProfissao(profissaoModificado)

    def pegaTodosTrabalhosProducao(self):
        limpaTela()
        trabalhosProducao = self.__aplicacao.pegaTodosTrabalhosProducao()
        # print(f'{'NOME'.ljust(113)} | {'DATA'.ljust(10)} | {'ID TRABALHO'.ljust(36)} | {'VALOR'.ljust(5)} | UND')
        if tamanhoIgualZero(trabalhosProducao):
            print('Lista de trabalhos em produção está vazia!')
        else:
            for trabalhoProducao in trabalhosProducao:
                print(trabalhoProducao)
        input(f'Clique para continuar...')

    def insereTrabalhoEstoque(self):
        while True:
            personagens = self.mostraListaPersonagens()
            if variavelExiste(personagens) and self.definePersonagemEscolhido(personagens):
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
                                trabalhos = self.__aplicacao.pegaTrabalhosPorProfissaoRaridade(trabalhoBuscado)
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
                                    self.__aplicacao.insereTrabalhoEstoque(trabalhoEstoque)
                                    continue
                                break
                            break
                        break
                    break
                continue
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

    def defineProfissaoSelecionada(self) -> str | None:
        opcaoProfissao: str = input('Opçao profissão: ')
        return None if int(opcaoProfissao) == 0 else LISTA_PROFISSOES[int(opcaoProfissao) - 1]

    def defineExperiencia(self) -> int:
        experiencia: str = input('Experiência: ')
        return 0 if experiencia is None else 0 if tamanhoIgualZero(experiencia) else int(experiencia)

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
            if variavelExiste(personagens) and self.definePersonagemEscolhido(personagens):
                while True:
                    estoque = self.mostraListaTrabalhosEstoque()
                    if variavelExiste(estoque):
                        trabalhoEstoque = self.defineTrabalhoEstoqueSelecionado(estoque)
                        if variavelExiste(trabalhoEstoque):
                            trabalhoEstoque = self.defineTrabalhoEstoqueModificado(trabalhoEstoque)
                            self.__aplicacao.modificaTrabalhoEstoque(trabalhoEstoque)
                            continue
                        break
                    break
                continue
            break

    def defineTrabalhoEstoqueModificado(self, trabalhoEstoque):
        quantidade = input(f'Quantidade trabalho: ')
        quantidade = trabalhoEstoque.quantidade if tamanhoIgualZero(quantidade) else quantidade
        trabalhoEstoque.setQuantidade(quantidade)
        return trabalhoEstoque
    
    def removeTrabalhoEstoque(self):
        while True:
            personagens = self.mostraListaPersonagens()
            if variavelExiste(personagens) and self.definePersonagemEscolhido(personagens):
                while True:
                    estoque = self.mostraListaTrabalhosEstoque()
                    if variavelExiste(estoque):
                        trabalhoEstoque = self.defineTrabalhoEstoqueSelecionado(estoque)
                        if variavelExiste(trabalhoEstoque):
                            self.__aplicacao.removeTrabalhoEstoque(trabalhoEstoque)
                            continue
                        break
                    break
                continue
            break

    def defineTrabalhoEstoqueSelecionado(self, estoque):
        opcaoTrabalho = input(f'Opção trabalho: ')
        if int(opcaoTrabalho) == 0:
            return None
        trabalhoEstoque = estoque[int(opcaoTrabalho) - 1]
        return trabalhoEstoque
    
    def mostraListaTrabalhosEstoque(self):
        limpaTela()
        estoque = self.__aplicacao.pegaTrabalhosEstoque()
        if tamanhoIgualZero(estoque):
            print(f'Estoque está vazio!')
        else:
            print(f'{"ÍNDICE".ljust(6)} - {"NOME".ljust(40)} | {"PROFISSÃO".ljust(25)} | {"QNT".ljust(3)} | {"NÍVEL".ljust(5)} | {"RARIDADE".ljust(10)} | ID TRABALHO')
            for trabalhoEstoque in estoque:
                print(f'{str(estoque.index(trabalhoEstoque) + 1).ljust(6)} - {trabalhoEstoque.nome.ljust(40)} | {trabalhoEstoque.profissao.ljust(25)} | {str(trabalhoEstoque.quantidade).ljust(3)} | {str(trabalhoEstoque.nivel).ljust(5)} | {trabalhoEstoque.raridade.ljust(10)} | {trabalhoEstoque.trabalhoId}')
        print(f'{"0".ljust(6)} - Voltar')
        return estoque

    def mostraListaPersonagens(self):
        limpaTela()
        personagens = self.__aplicacao.pegaPersonagens()
        if tamanhoIgualZero(personagens):
            print('Lista de personagens está vazia!')
        else:
            print(f"{'ÍNDICE'.ljust(6)} - {'ID'.ljust(36)} | {'NOME'.ljust(17)} | {'ESPAÇO'.ljust(6)} | {'ESTADO'.ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO")
            for personagem in personagens:
                print(f'{str(personagens.index(personagem) + 1).ljust(6)} - {personagem}')
        print(f'{"0".ljust(6)} - Voltar')
        return personagens
    
    def definePersonagemEscolhido(self, personagens) -> bool:
        opcaoPersonagem = input(f'Opção: ')
        if int(opcaoPersonagem) == 0:
            return False
        self.__personagemEmUso = personagens[int(opcaoPersonagem) - 1]
        self.__aplicacao.personagemEmUso(personagens[int(opcaoPersonagem) - 1])
        return True
    
    def mostraListaVendas(self):
        limpaTela()
        print(f'{"ÍNDICE".ljust(6)} - {"ID".ljust(36)} | {"NOME".ljust(36)} | {"DATA".ljust(10)} | {"VALOR".ljust(5)} | UND')
        vendas = self.__aplicacao.pegaTrabalhosVendidos()
        if tamanhoIgualZero(vendas):
            print('Lista de vendas está vazia!')
        else:
            for trabalho in vendas:
                print(f'{str(vendas.index(trabalho) + 1).ljust(6)} - {trabalho}')
        return vendas
    
    def mostraListaTrabalhos(self):
        limpaTela()
        trabalhos = self.__aplicacao.pegaTrabalhosBanco()
        if tamanhoIgualZero(trabalhos):
            print('Lista de trabalhos está vazia!')
        else:
            print(f'{"ÍNDICE".ljust(6)} - {"NOME".ljust(44)} | {"PROFISSÃO".ljust(22)} | {"RARIDADE".ljust(9)} | NÍVEL')
            for trabalho in trabalhos:
                print(f'{str(trabalhos.index(trabalho) + 1).ljust(6)} - {trabalho}')
        return trabalhos

    def insereTrabalhoVendido(self):
        while True:
            personagens = self.mostraListaPersonagens()
            if variavelExiste(personagens) and self.definePersonagemEscolhido(personagens):
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
                                    trabalhoSelecionado = self.defineTrabalhoVendidoSelecionado(trabalhos)
                                    if variavelExiste(trabalhoSelecionado):
                                        novoTrabalhoVendido = self.defineNovoTrabalhoVendido(trabalhoSelecionado)
                                        if variavelExiste(novoTrabalhoVendido):
                                            self.__aplicacao.insereTrabalhoVendido(novoTrabalhoVendido)
                                            continue
                                        break
                                    break
                                break
                            break
                        break
                    break
                continue
            break

    def mostraTrabalhosPorProfissaoRaridade(self, trabalhoBuscado):
        limpaTela()
        trabalhos = self.__aplicacao.pegaTrabalhosPorProfissaoRaridade(trabalhoBuscado)
        if tamanhoIgualZero(trabalhos):
            print('Lista de trabalhos está vazia!')
        else:
            print(f'{"ÍNDICE".ljust(6)} - {"NOME".ljust(44)} | {"PROFISSÃO".ljust(22)} | {"RARIDADE".ljust(9)} | NÍVEL')
            for trabalho in trabalhos:
                print(f'{str(trabalhos.index(trabalho) + 1).ljust(6)} - {trabalho} | {trabalho.trabalhoNecessario}')
        return trabalhos

    def defineNovoTrabalhoVendido(self, trabalho: TrabalhoVendido) -> TrabalhoVendido:
        descricao = input(f'Descrição da venda: ')
        data = input(f'Data da venda: ')
        quantidade = input(f'Quantidade trabalho vendido: ')
        valor = input(f'Valor do trabalho vendido: ')
        trabalho.descricao = descricao
        trabalho.dataVenda = data
        trabalho.setQuantidade(quantidade)
        trabalho.setValor(valor)
        return trabalho

    def defineVendaEscolhida(self, vendas: list[TrabalhoVendido]) -> TrabalhoVendido:
        opcaoTrabalho = input(f'Opção trabalho: ')    
        if int(opcaoTrabalho) == 0:
            return None
        return vendas[int(opcaoTrabalho) - 1]
    
    def modificaTrabalhoVendido(self):
        while True:
            personagens = self.mostraListaPersonagens()
            if variavelExiste(personagens) and self.definePersonagemEscolhido(personagens):
                while True:
                    vendas = self.mostraListaVendas()
                    if variavelExiste(vendas):
                        print(f'{"0".ljust(6)} - Voltar')
                        trabalhoVendidoModificado = self.defineVendaEscolhida(vendas)
                        if variavelExiste(trabalhoVendidoModificado):
                            trabalhoVendidoModificado = self.defineTrabalhoVendidoModificado(trabalhoVendidoModificado)
                            self.__aplicacao.modificaTrabalhoVendido(trabalhoVendidoModificado)
                            continue
                        break
                    break
                continue
            break

    def removeTrabalhoVendido(self):
        while True:
            personagens = self.mostraListaPersonagens()
            if variavelExiste(personagens) and self.definePersonagemEscolhido(personagens):
                while True:
                    vendas = self.mostraListaVendas()
                    if variavelExiste(vendas):
                        print(f'{"0".ljust(6)} - Voltar')
                        trabalhoVendidoSelecionado = self.defineVendaEscolhida(vendas)
                        if variavelExiste(trabalhoVendidoSelecionado):
                            self.__aplicacao.removeTrabalhoVendido(trabalhoVendidoSelecionado)
                            continue
                        break
                    break
                continue
            break

    def defineTrabalhoVendidoModificado(self, trabalho: TrabalhoVendido):
        limpaTela()
        descricao = input(f'Descrição do trabalho: ')
        data = input(f'Data da venda: ')
        quantidade = input(f'Quantidade vendida: ')
        valor = input(f'Valor da venda: ')
        trabalho.descricao = trabalho.descricao if tamanhoIgualZero(descricao) else descricao
        trabalho.dataVenda = trabalho.dataVenda if tamanhoIgualZero(data) else data
        trabalho.quantidade = trabalho.quantidade if tamanhoIgualZero(quantidade) else quantidade
        trabalho.valor = trabalho.valor if tamanhoIgualZero(valor) else valor
        return trabalho

    def defineTrabalhoProducaoSelecionado(self, trabalhos: list[TrabalhoProducao]) -> TrabalhoProducao | None:
        trabalhoProducao = TrabalhoProducao()
        print(f'{"0".ljust(6)} - Voltar')
        opcaoTrabalho = input(f'Opção trabalho: ')    
        if int(opcaoTrabalho) == 0:
            return None
        trabalho: TrabalhoProducao = trabalhos[int(opcaoTrabalho) - 1]
        trabalhoProducao.id = trabalho.id
        trabalhoProducao.idTrabalho = trabalho.idTrabalho
        trabalhoProducao.tipo_licenca = trabalho.tipo_licenca
        trabalhoProducao.recorrencia = trabalho.recorrencia
        trabalhoProducao.estado = trabalho.estado
        return trabalhoProducao

    def defineTrabalhoVendidoSelecionado(self, trabalhos: list[Trabalho]) -> TrabalhoVendido | None:
        trabalhoVendido = TrabalhoVendido()
        print(f'{"0".ljust(6)} - Voltar')
        opcaoTrabalho = input(f'Opção trabalho: ')    
        if int(opcaoTrabalho) == 0:
            return None
        trabalho = trabalhos[int(opcaoTrabalho) - 1]
        trabalhoVendido.idTrabalho = trabalho.id
        return trabalhoVendido

    def sincronizaDados(self):
        # self.sincronizaListaTrabalhos()
        self.__aplicacao.sincronizaListaPersonagens()
        self.__aplicacao.sincronizaListaProfissoes()
        self.__aplicacao.sincronizaTrabalhosProducao()
        # self.__aplicacao.sincronizaTrabalhosVendidos()
    
    def verificaTrabalhoRaroMaisVendido(self):
        vendas = self.__aplicacao.pegaTrabalhosRarosVendidos()
        for trabalhoVendido in vendas:
            quantidadeTrabalhoRaroEmEstoque = self.__aplicacao.pegaQuantidadeTrabalhoEstoque(trabalhoVendido.trabalhoId)
            print(f'Quantidade de ({trabalhoVendido.nome}) no estoque: {quantidadeTrabalhoRaroEmEstoque}')
            # quantidadeTrabalhoRaroNecessario = CODIGO_QUANTIDADE_MINIMA_TRABALHO_RARO_EM_ESTOQUE - quantidadeTrabalhoEmEstoque
            quantidadeTrabalhoRaroNecessario = 2 - quantidadeTrabalhoRaroEmEstoque
            if quantidadeTrabalhoRaroNecessario > 0:
                trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
                quantidadeTrabalhoRaroEmProducao = trabalhoProducaoDao.pegaQuantidadeTrabalhoProducaoProduzindo(trabalhoVendido.trabalhoId)
                if variavelExiste(quantidadeTrabalhoRaroEmProducao):
                    quantidadeTrabalhoRaroNecessario -= quantidadeTrabalhoRaroEmProducao
                    print(f'Quantidade de ({trabalhoVendido.nome}) em produção: {quantidadeTrabalhoRaroEmProducao}')
                    if quantidadeTrabalhoRaroNecessario > 0:
                        trabalhoMelhoradoNecessario = trabalhoVendido.trabalhoNecessario
                        if variavelExiste(trabalhoMelhoradoNecessario):
                            print(f'Trabalho melhorado necessário: ({trabalhoMelhoradoNecessario})')
                            profissao = self.__aplicacao.retornaProfissaoTrabalhoProducaoConcluido(trabalhoVendido)
                            if variavelExiste(profissao):
                                print(f'Profissão: ({profissao})')
                                xpMaximo = profissao.pegaExperienciaMaximaPorNivel()
                                licencaProducaoIdeal = CHAVE_LICENCA_NOVATO if xpMaximo >= 830000 else CHAVE_LICENCA_INICIANTE
                                print(f'Licença de produção ideal: ({licencaProducaoIdeal})')
                                trabalhoMelhoradoBuscado = Trabalho()
                                trabalhoMelhoradoBuscado.nome = trabalhoVendido.trabalhoNecessario
                                trabalhoMelhoradoBuscado.raridade = CHAVE_RARIDADE_MELHORADO
                                trabalhoMelhoradoBuscado.profissao = trabalhoVendido.profissao
                                trabalhoMelhoradoEncontrado = self.__aplicacao.pegaTrabalhoPorNomeProfissaoRaridade(trabalhoMelhoradoBuscado)
                                if variavelExiste(trabalhoMelhoradoEncontrado):
                                    quantidadeTrabalhoMelhoradoEmEstoque = self.__aplicacao.pegaQuantidadeTrabalhoEstoque(trabalhoMelhoradoEncontrado.id)
                                    quantidadeTrabalhoMelhoradoNecessario = quantidadeTrabalhoRaroNecessario - quantidadeTrabalhoMelhoradoEmEstoque
                                    print(f'Quantidade de ({trabalhoMelhoradoEncontrado.nome}) no estoque: {quantidadeTrabalhoMelhoradoEmEstoque}')
                                    trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
                                    quantidadeTrabalhoMelhoradoEmProducao = trabalhoProducaoDao.pegaQuantidadeTrabalhoProducaoProduzindo(trabalhoMelhoradoEncontrado.id)
                                    if variavelExiste(quantidadeTrabalhoMelhoradoEmProducao):
                                        quantidadeTrabalhoMelhoradoNecessario -= quantidadeTrabalhoMelhoradoEmProducao
                                        if quantidadeTrabalhoMelhoradoNecessario < quantidadeTrabalhoRaroNecessario and quantidadeTrabalhoMelhoradoNecessario >= 0:
                                            quantidadeAdicionada = quantidadeTrabalhoMelhoradoNecessario
                                            if quantidadeTrabalhoMelhoradoNecessario == 0:
                                                quantidadeAdicionada = quantidadeTrabalhoRaroNecessario
                                            while quantidadeAdicionada > 0:
                                                self.__loggerTrabalhoProducaoDao.info(f'({trabalhoVendido.nome}) adicionado com sucesso!')
                                                quantidadeAdicionada -= 1
                                                pass
                                            return 
                                        continue                                                       
                                    self.__loggerTrabalhoProducaoDao.error(f'Erro ao buscar quantidade: {trabalhoProducaoDao.pegaErro()}')
                                    continue
                            continue
                        print(f'({trabalhoVendido.nome}) não possue trabalho necesssário!')
                    continue
                self.__loggerTrabalhoProducaoDao.error(f'Erro ao buscar quantidade: {trabalhoProducaoDao.pegaErro()}')
            continue
        input('Clique para continuar...')
        
    def iniciaStreans(self):
        self.__aplicacao.abreStreamTrabalhos()
        self.__aplicacao.abreStreamPersonagens()
        
    def testeFuncao(self):
        self.__aplicacao.abreStreamPersonagens()
        
    def menu(self):
        while True:
            self.__aplicacao.verificaAlteracaoListaTrabalhos()
            self.__aplicacao.verificaAlteracaoPersonagem()
            limpaTela()
            print(f'MENU')
            print(f'{"1".ljust(2)} - Insere trabalho')
            print(f'{"2".ljust(2)} - Modifica trabalho')
            print(f'{"3".ljust(2)} - Remove trabalho')
            print(f'{"4".ljust(2)} - Insere personagem')
            print(f'{"5".ljust(2)} - Modifica personagem')
            print(f'{"6".ljust(2)} - Remove personagem')
            print(f'{"7".ljust(2)} - Insere trabalho produção')
            print(f'{"8".ljust(2)} - Modifica trabalho produção')
            print(f'{"9".ljust(2)} - Remove trabalho produção')
            print(f'{"10".ljust(2)} - Insere profissao')
            print(f'{"11".ljust(2)} - Modifica profissao')
            print(f'{"12".ljust(2)} - Remove profissao')
            print(f'{"13".ljust(2)} - Insere trabalho no estoque')
            print(f'{"14".ljust(2)} - Modifica trabalho no estoque')
            print(f'{"15".ljust(2)} - Remove trabalho no estoque')
            print(f'{"16".ljust(2)} - Insere trabalho vendido')
            print(f'{"17".ljust(2)} - Modifica trabalho vendido')
            print(f'{"18".ljust(2)} - Remove trabalho vendido')
            print(f'{"20".ljust(2)} - Pega todos trabalhos producao')
            print(f'{"21".ljust(2)} - Sincroniza dados')
            print(f'{"22".ljust(2)} - Inicia streans')
            print(f'{"24".ljust(2)} - Teste de funções')
            print(f'{"0".ljust(2)} - Sair')
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
                    self.insereProfissao()
                    continue
                if int(opcaoMenu) == 11:
                    self.modificaProfissao()
                    continue
                if int(opcaoMenu) == 12:
                    self.removeProfissao()
                    continue
                if int(opcaoMenu) == 13:
                    self.insereTrabalhoEstoque()
                    continue
                if int(opcaoMenu) == 14:
                    self.modificaTrabalhoEstoque()
                    continue
                if int(opcaoMenu) == 15:
                    self.removeTrabalhoEstoque()
                    continue
                if int(opcaoMenu) == 16:
                    self.insereTrabalhoVendido()
                    continue
                if int(opcaoMenu) == 17:
                    self.modificaTrabalhoVendido()
                    continue
                if int(opcaoMenu) == 18:
                    self.removeTrabalhoVendido()
                    continue
                if int(opcaoMenu) == 20:
                    self.pegaTodosTrabalhosProducao()
                    continue
                if int(opcaoMenu) == 21:
                    self.sincronizaDados()
                    continue
                if int(opcaoMenu) == 22:
                    self.iniciaStreans()
                    continue
                if int(opcaoMenu) == 24:
                    self.testeFuncao()
                    continue
            except Exception as erro:
                print(f'Opção inválida! Erro: {erro}')
                input(f'Clique para continuar...')

if __name__=='__main__':
    CRUD()