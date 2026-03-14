from uuid import uuid4
from utilitarios import limpa_tela, variavelExiste, eh_vazia
from utilitariosTexto import limpa_ruido_texto

from constantes import *

from dao.trabalhoProducaoDaoSqlite import TrabalhoProducaoDaoSqlite


from modelos.trabalho import Trabalho
from modelos.trabalhoProducao import TrabalhoProducao
from modelos.personagem import Personagem
from modelos.trabalhoEstoque import TrabalhoEstoque
from modelos.trabalhoVendido import TrabalhoVendido
from modelos.profissao import Profissao
from modelos.logger import MeuLogger
from modelos.profissao import ProfissaoBase

from repositorio.repositorioProfissao import RepositorioProfissao
from main import Aplicacao


class CRUD:
	def __init__(self):
		self.__loggerTrabalhoProducaoDao: MeuLogger = MeuLogger(
			nome="trabalhoProducaoDao"
		)
		self.__personagemEmUso = None
		self.__aplicacao: Aplicacao = Aplicacao()
		self.__profissoes: list[ProfissaoBase] = []
		self.__profissao_selecionada: ProfissaoBase | None = None
		self.__raridade_selecionada: str | None = None
		self.__trabalhos_profissao_raridade: list[Trabalho] = []

		self.__inicializa_atributos()
		self.menu()

	def __inicializa_atributos(self):
		self.atualiza_profissoes()

	def atualiza_profissoes(self):
		repositorio_profissao: RepositorioProfissao = RepositorioProfissao()
		profissoes: list[ProfissaoBase] | None = (
			repositorio_profissao.pega_todas_profissoes()
		)
		if profissoes is None:
			return

		self.__profissoes = profissoes

	def insere_novo_trabalho(self):
		while True:
			self.mostra_lista_profissoes()
			self.define_profissao_selecionada()
			if self.__profissao_selecionada is None:
				break

			self.mostra_lista_raridades()
			self.define_raridade_selecionada()
			if self.__raridade_selecionada is None:
				break

			trabalho_buscado = Trabalho()
			trabalho_buscado.profissao = self.__profissao_selecionada.id
			trabalho_buscado.raridade = self.__raridade_selecionada
			while True:
				self.__mostra_lista_trabalhos_por_profissao_raridade(trabalho_buscado)
				opcao_trabalho = input(f"Adicionar novo trabalho? (S/N)")
				if opcao_trabalho.lower() == "n":
					break

				novo_trabalho = self.__define_novo_trabalho(trabalho_buscado)
				# self.__aplicacao.insere_trabalho(novo_trabalho)

	def __define_novo_trabalho(self, trabalho_buscado: Trabalho) -> Trabalho:
		limpa_tela()

		nome = input(f"Nome: ")
		nome_producao = input(f"Nome produção: ")
		experiencia = input(f"Experiência: ")
		nivel = input(f"Nível: ")
		novo_trabalho = Trabalho()
		novo_trabalho.nome = nome
		novo_trabalho.nomeProducao = nome_producao
		novo_trabalho.experiencia = int(experiencia)
		novo_trabalho.nivel = int(nivel)
		novo_trabalho.profissao = trabalho_buscado.profissao
		novo_trabalho.raridade = trabalho_buscado.raridade
		if (
			trabalho_buscado.raridade == CHAVE_RARIDADE_MELHORADO
			or trabalho_buscado.raridade == CHAVE_RARIDADE_RARO
			or trabalho_buscado.raridade == CHAVE_RARIDADE_ESPECIAL
		):
			trabalhos_por_profissao_nivel_raridade = self.__aplicacao.define_trabalhos_por_profissao_nivel_raridade(novo_trabalho)
			for indice, trabalho in enumerate(trabalhos_por_profissao_nivel_raridade, start=1):
				print(f"{str(indice).ljust(3)} - {trabalho.nome}")
			print(f"{'0'.ljust(3)} - Pular")
			trabalho_selecionado = input(f"Opção: ")
			while int(trabalho_selecionado) != 0:
				trabalho_selecionado = input(f"Opção: ")
			# novo_trabalho.trabalhoNecessario = trabalho_necessario

		return novo_trabalho

	def __mostra_lista_trabalhos_por_profissao_raridade(
		self, trabalho_buscado: Trabalho, index: bool = False
	):
		self.__trabalhos_profissao_raridade = (
			self.__aplicacao.pega_trabalhos_por_profissao_raridade(trabalho_buscado)
		)

		self.__mostra_cabecalho(trabalho_buscado, index)

		for indice, trabalho in enumerate(self.__trabalhos_profissao_raridade, start=1):
			if index:
				print(
					f"{str(indice).ljust(3)} - {(trabalho.nome or '').ljust(44)} | {str(trabalho.nivel).ljust(5)} | {trabalho.trabalhoNecessario}"
				)
			else:
				print(
					f"{(trabalho.nome or '').ljust(44)} | {str(trabalho.nivel).ljust(5)} | {trabalho.trabalhoNecessario}"
				)

	def __mostra_cabecalho(self, trabalho_buscado, index):
		limpa_tela()

		print(
			f"{(trabalho_buscado.profissao or '').ljust(22).upper()} - {(trabalho_buscado.raridade or '').ljust(9).upper()}"
		)
		if eh_vazia(self.__trabalhos_profissao_raridade):
			return print("Lista de trabalhos está vazia!")

		if (
			trabalho_buscado.raridade == CHAVE_RARIDADE_MELHORADO
			or trabalho_buscado.raridade == CHAVE_RARIDADE_RARO
		):
			if index:
				return print(
					f"{'#'.ljust(3)} - {'NOME'.ljust(44)} | {'NÍVEL'.ljust(5)} | TRABALHOS NECESSÁRIOS"
				)

			return print(
				f"{'NOME'.ljust(44)} | {'NÍVEL'.ljust(5)} | TRABALHOS NECESSÁRIOS"
			)

		if index:
			return print(f"{'#'.ljust(3)} - {'NOME'.ljust(44)} | {'NÍVEL'.ljust(5)}")

		print(f"{'NOME'.ljust(44)} | {'NÍVEL'.ljust(5)}")

	def modifica_trabalho(self):
		while True:
			self.mostra_lista_profissoes()
			self.define_profissao_selecionada()
			if self.__profissao_selecionada is None:
				break

			self.mostra_lista_raridades()
			self.define_raridade_selecionada()
			if self.__raridade_selecionada is None:
				break

			trabalho_buscado = Trabalho()
			trabalho_buscado.profissao = self.__profissao_selecionada.id
			trabalho_buscado.raridade = self.__raridade_selecionada
			while True:
				self.__mostra_lista_trabalhos_por_profissao_raridade(
					trabalho_buscado, index=True
				)
				opcao_trabalho = input(f"Opção trabalho: ")
				if int(opcao_trabalho) == 0:
					break

				if self.__trabalhos_profissao_raridade is None:
					break

				trabalho_selecionado = self.__trabalhos_profissao_raridade[
					int(opcao_trabalho) - 1
				]
				novo_nome = input(f"Novo nome: ")
				novo_nome = (
					trabalho_selecionado.nome if eh_vazia(novo_nome) else novo_nome
				)

				novo_nome_producao = input(f"Novo nome de produção: ")
				novo_nome_producao = (
					trabalho_selecionado.nomeProducao
					if eh_vazia(novo_nome_producao)
					else novo_nome_producao
				)

				nova_experiencia = input(f"Nova experiência: ")
				nova_experiencia = (
					trabalho_selecionado.experiencia
					if eh_vazia(nova_experiencia)
					else nova_experiencia
				)

				novo_nivel = input(f"Novo nível: ")
				novo_nivel = (
					trabalho_selecionado.nivel if eh_vazia(novo_nivel) else novo_nivel
				)

				nova_profissao = input(f"Nova profissão: ")
				nova_profissao = (
					trabalho_selecionado.profissao
					if eh_vazia(nova_profissao)
					else nova_profissao
				)

				nova_raridade = input(f"Nova raridade: ")
				nova_raridade = (
					trabalho_selecionado.raridade
					if eh_vazia(nova_raridade)
					else nova_raridade
				)

				novo_trabalho_necessario = input(f"Novo trabalho necessário: ")
				novo_trabalho_necessario = (
					trabalho_selecionado.trabalhoNecessario
					if eh_vazia(novo_trabalho_necessario)
					else novo_trabalho_necessario
				)

				trabalho_selecionado.nome = novo_nome
				trabalho_selecionado.nomeProducao = novo_nome_producao
				trabalho_selecionado.experiencia = int(nova_experiencia)
				trabalho_selecionado.nivel = int(novo_nivel)
				trabalho_selecionado.profissao = nova_profissao
				trabalho_selecionado.raridade = nova_raridade
				trabalho_selecionado.trabalhoNecessario = novo_trabalho_necessario

				self.__aplicacao.modificaTrabalho(trabalho_selecionado)

	def new_method(self, trabalho_buscado):
		limpa_tela()
		trabalhos: list[Trabalho] = (
			self.__aplicacao.pega_trabalhos_por_profissao_raridade(trabalho_buscado)
		)
		print(
			f"{trabalho_buscado.profissao.ljust(22).upper()} - {trabalho_buscado.raridade.ljust(9).upper()}"
		)
		if eh_vazia(trabalhos):
			print("Lista de trabalhos está vazia!")

		else:
			if (
				trabalho_buscado.raridade == CHAVE_RARIDADE_MELHORADO
				or trabalho_buscado.raridade == CHAVE_RARIDADE_RARO
			):
				print(
					f"{'#'.ljust(3)} - {'NOME'.ljust(44)} | {'NÍVEL'.ljust(5)} | TRABALHOS NECESSÁRIOS"
				)
			else:
				print(f"{'#'.ljust(3)} - {'NOME'.ljust(44)} | {'NÍVEL'.ljust(5)}")
			for trabalho in trabalhos:
				print(
					f"{str(trabalhos.index(trabalho) + 1).ljust(3)} - {(trabalho.nome or '').ljust(44)} | {str(trabalho.nivel).ljust(5)} | {trabalho.trabalhoNecessario}"
				)

			print(f'{"0".ljust(3)} - Voltar')
		return trabalhos

	def removeTrabalho(self):
		while True:
			trabalhoBuscado = Trabalho()
			self.mostra_lista_profissoes()
			self.define_profissao_selecionada()
			if self.__profissao_selecionada is None:
				break

			trabalhoBuscado.profissao = self.__profissao_selecionada.id
			self.mostra_lista_raridades()
			self.define_raridade_selecionada()
			if self.__raridade_selecionada is None:
				break

			trabalhoBuscado.raridade = self.__raridade_selecionada
			while True:
				limpa_tela()
				trabalhos = self.__aplicacao.pega_trabalhos_por_profissao_raridade(
					trabalhoBuscado
				)
				print(
					f"{'ÍNDICE'.ljust(6)} - {'NOME'.ljust(44)} | {'PROFISSÃO'.ljust(22)} | {'RARIDADE'.ljust(9)} | {'NÍVEL'.ljust(5)} | TRABALHOS NECESSÁRIOS"
				)
				if eh_vazia(trabalhos):
					print("Lista de trabalhos está vazia!")
				else:
					for trabalho in trabalhos:
						print(
							f"{str(trabalhos.index(trabalho) + 1).ljust(6)} - {trabalho} | {trabalho.trabalhoNecessario}"
						)
				print(f'{"0".ljust(6)} - Voltar')
				opcaoTrabalho = input(f"Opção trabalho: ")
				if int(opcaoTrabalho) == 0:
					break
				trabalhoEscolhido = trabalhos[int(opcaoTrabalho) - 1]
				self.__aplicacao.removeTrabalho(trabalhoEscolhido)

	def inserePersonagem(self):
		while True:
			limpa_tela()
			print(
				f"{'ID'.ljust(36)} | {'NOME'.ljust(17)} | {'ESPAÇO'.ljust(6)} | {'ESTADO'.ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO"
			)
			personagens = self.__aplicacao.pegaPersonagens()
			if eh_vazia(personagens):
				print("Lista de personagens está vazia!")
			else:
				for personagem in personagens:
					print(personagem)
			opcaoPersonagem = input(f"Inserir novo personagem? (S/N) ")
			if opcaoPersonagem.lower() == "n":
				break
			nome = input(f"Nome: ")
			email = input(f"Email: ")
			senha = input(f"Senha: ")
			novoPersonagem = Personagem()
			novoPersonagem.nome = nome
			novoPersonagem.email = email
			novoPersonagem.senha = senha
			if self.__aplicacao.inserePersonagem(novoPersonagem):
				self.__aplicacao.insereListaProfissoes(personagem=novoPersonagem)
				continue
			input(f"Clique para continuar...")

	def modificaPersonagem(self):
		while True:
			limpa_tela()
			personagens = self.__aplicacao.pegaPersonagens()
			if eh_vazia(personagens):
				print("Lista de personagens está vazia!")
			else:
				print(
					f"{'ÍNDICE'.ljust(6)} - {'ID'.ljust(36)} | {'NOME'.ljust(17)} | {'ESPAÇO'.ljust(6)} | {'ESTADO'.ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO"
				)
				for personagem in personagens:
					print(
						f"{str(personagens.index(personagem) + 1).ljust(6)} - {personagem}"
					)
			opcaoPersonagem = input(f"Opção:")
			if int(opcaoPersonagem) == 0:
				break
			limpa_tela()
			personagem = personagens[int(opcaoPersonagem) - 1]
			novoNome = input(f"Novo nome: ")
			if eh_vazia(novoNome):
				novoNome = personagem.nome
			novoEmail = input(f"Novo email: ")
			if eh_vazia(novoEmail):
				novoEmail = personagem.email
			novasenha = input(f"Nova senha: ")
			if eh_vazia(novasenha):
				novasenha = personagem.senha
			novoEspaco = input(f"Nova quantidade de produção: ")
			if eh_vazia(novoEspaco):
				novoEspaco = personagem.espacoProducao
			novoEstado = input(f"Modificar estado? (S/N) ")
			if novoEstado.lower() == "s":
				personagem.alternaEstado
			novoUso = input(f"Modificar uso? (S/N) ")
			if novoUso.lower() == "s":
				personagem.alternaUso
			novoAutoProducao = input(f"Modificar autoProducao? (S/N) ")
			if novoAutoProducao.lower() == "s":
				personagem.alternaAutoProducao
			personagem.nome = novoNome
			personagem.email = novoEmail
			personagem.senha = novasenha
			personagem.setEspacoProducao(novoEspaco)
			if self.__aplicacao.modifica_personagem(personagem=personagem):
				continue
			input(f"Clique para continuar...")

	def removePersonagem(self):
		while True:
			limpa_tela()
			personagens = self.__aplicacao.pegaPersonagens()
			if eh_vazia(personagens):
				print("Lista de personagens está vazia!")
			else:
				print(
					f"{'ÍNDICE'.ljust(6)} - {'ID'.ljust(36)} | {'NOME'.ljust(17)} | {'ESPAÇO'.ljust(6)} | {'ESTADO'.ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO"
				)
				for personagem in personagens:
					print(
						f"{str(personagens.index(personagem) + 1).ljust(6)} - {personagem}"
					)
			print(f'{"0".ljust(6)} - Voltar')
			opcaoPersonagem = input(f"Opção:")
			if int(opcaoPersonagem) == 0:
				break
			personagem = personagens[int(opcaoPersonagem) - 1]
			if self.__aplicacao.removePersonagem(personagem=personagem):
				continue
			input(f"Clique para continuar...")

	def mostraListaTrabalhosProducao(self):
		limpa_tela()
		trabalhos = self.__aplicacao.pegaTrabalhosProducao()
		if eh_vazia(trabalhos):
			print("Lista de trabalhos em produção está vazia!")
		else:
			print(
				f"{'ÍNDICE'.ljust(6)} - {'NOME'.ljust(44)} | {'PROFISSÃO'.ljust(22)} | {'NÍVEL'.ljust(5)} | {'ESTADO'.ljust(10)} | {'LICENÇA'.ljust(34)} | RECORRÊNCIA"
			)
			for trabalhoProducao in trabalhos:
				estado = (
					"Produzir"
					if trabalhoProducao.estado == 0
					else "Produzindo" if trabalhoProducao.estado == 1 else "Feito"
				)
				recorrencia = "Recorrente" if trabalhoProducao.recorrencia else "Único"
				print(
					f"{str(trabalhos.index(trabalhoProducao) + 1).ljust(6)} - {trabalhoProducao.nome.ljust(44)} | {trabalhoProducao.profissao.ljust(22)} | {str(trabalhoProducao.nivel).ljust(5)} | {estado.ljust(10)} | {trabalhoProducao.tipoLicenca.ljust(34)} | {recorrencia}"
				)
		return trabalhos

	def mostraListaTrabalhosPorProfissaoRaridade(self, trabalhoBuscado):
		limpa_tela()
		trabalhos = self.__aplicacao.pega_trabalhos_por_profissao_raridade(
			trabalhoBuscado
		)
		if eh_vazia(trabalhos):
			print(f"Nem um trabalho encontrado!")
		else:
			print(
				f"{'ÍNDICE'.ljust(6)} - {'NOME'.ljust(40)} | {('PROFISSÃO').ljust(20)} | NÍVEL"
			)
			for trabalho in trabalhos:
				print(f"{str(trabalhos.index(trabalho) + 1).ljust(6)} - {trabalho}")
		return trabalhos

	def defineNovoTrabalhoProducao(self, trabalhos):
		print(f'{"0".ljust(6)} - Voltar')
		opcaoTrabalho = input(f"Trabalhos escolhido: ")
		return None if int(opcaoTrabalho) == 0 else trabalhos[int(opcaoTrabalho) - 1]

	def defineLicencaSelecionada(self):
		opcaoLicenca = input(f"Licença escolhida: ")
		return None if int(opcaoLicenca) == 0 else LISTA_LICENCAS[int(opcaoLicenca) - 1]

	def defineRecorrenciaSelecionada(self):
		opcaoRecorrencia = input(f"Trabalho recorrente? (S/N)")
		return True if (opcaoRecorrencia).lower() == "s" else False

	def defineInsereNovoTrabalho(self):
		opcaoTrabalho = input(f"Adicionar novo trabalho? (S/N) ")
		return True if opcaoTrabalho.lower() == "s" else False

	def defineInsereProfissao(self) -> bool:
		opcao: str = input(f"Inserir nova profissão? (S/N) ")
		return True if opcao.lower() == "s" else False

	def insereNovoTrabalhoProducao(self):
		while True:
			personagens = self.mostraListaPersonagens()
			if variavelExiste(personagens) and self.definePersonagemEscolhido(
				personagens
			):
				while True:
					trabalhosProducao = self.mostraListaTrabalhosProducao()
					insereNovoTrabalho = self.defineInsereNovoTrabalho()
					if variavelExiste(trabalhosProducao) and insereNovoTrabalho:
						trabalhoBuscado = (
							self.defineTrabalhoBuscadoPorProfissaoRaridade()
						)
						trabalhosEncontrados = (
							self.mostraListaTrabalhosPorProfissaoRaridade(
								trabalhoBuscado
							)
						)
						trabalhoSelecionado = self.defineNovoTrabalhoProducao(
							trabalhosEncontrados
						)
						if variavelExiste(trabalhosEncontrados) and variavelExiste(
							trabalhoSelecionado
						):
							novoTrabalhoProducao = (
								self.defineNovoTrabalhoProducaoSelecionado(
									trabalhoSelecionado
								)
							)
							if self.__aplicacao.insereTrabalhoProducao(
								trabalho=novoTrabalhoProducao
							):
								continue
							input("Clique para continuar...")
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
		novoTrabalhoProducao.tipoLicenca = licenca
		novoTrabalhoProducao.estado = CODIGO_PARA_PRODUZIR
		return novoTrabalhoProducao

	def defineTrabalhoBuscadoPorProfissaoRaridade(self) -> Trabalho | None:
		self.mostra_lista_profissoes()
		self.define_profissao_selecionada()
		if self.__profissao_selecionada is None:
			return

		self.mostra_lista_raridades()
		self.define_raridade_selecionada()
		if self.__raridade_selecionada is None:
			return

		trabalhoBuscado = Trabalho()
		trabalhoBuscado.raridade = self.__raridade_selecionada
		trabalhoBuscado.profissao = self.__profissao_selecionada.id
		return trabalhoBuscado

	def mostraListaLicencas(self):
		limpa_tela()
		for licenca in LISTA_LICENCAS:
			print(f"{LISTA_LICENCAS.index(licenca) + 1} - {licenca}")

	def modificaTrabalhoProducao(self):
		while True:
			personagens = self.mostraListaPersonagens()
			if variavelExiste(personagens) and self.definePersonagemEscolhido(
				personagens
			):
				while True:
					trabalhos = self.mostraListaTrabalhosProducao()
					trabalhoProducaoSelecionado = (
						self.defineTrabalhoProducaoSelecionado(trabalhos)
					)
					if variavelExiste(trabalhoProducaoSelecionado):
						self.mostraListaLicencas()
						novaLicenca = self.defineLicencaSelecionada()
						if variavelExiste(novaLicenca):
							trabalhoProducaoSelecionado.tipoLicenca = novaLicenca
							novaRecorrencia = input(f"Alterna recorrencia? (S/N) ")
							if novaRecorrencia.lower() == "s":
								trabalhoProducaoSelecionado.alternaRecorrencia
							limpa_tela()
							novoEstado = input(
								f"Novo estado: (0 - PRODUZIR, 1 - PRODUZINDO, 2 - CONCLUÍDO) "
							)
							if eh_vazia(novoEstado):
								novoEstado = trabalhoProducaoSelecionado.estado
							else:
								trabalhoProducaoSelecionado.estado = int(novoEstado)
							if self.__aplicacao.modifica_trabalho_producao(
								trabalho=trabalhoProducaoSelecionado
							):
								continue
							input("Clique para continuar...")
							continue
						break
					break
				continue
			break

	def removeTrabalhoProducao(self):
		while True:
			personagens = self.mostraListaPersonagens()
			if variavelExiste(personagens) and self.definePersonagemEscolhido(
				personagens
			):
				while True:
					trabalhosProducao = self.mostraListaTrabalhosProducao()
					trabalhoRemovido = self.defineTrabalhoProducaoSelecionado(
						trabalhosProducao
					)
					if trabalhoRemovido is None:
						break
					if self.__aplicacao.remove_trabalho_producao(
						trabalho=trabalhoRemovido
					):
						continue
					input("Clique para continuar...")
				continue
			break

	def removeProfissao(self):
		while True:
			limpa_tela()
			personagens = self.__aplicacao.pegaPersonagens()
			if eh_vazia(personagens):
				print(f"Lista de personagens está vazia!")
			else:
				print(
					f"{'ÍNDICE'.ljust(6)} - {'ID'.ljust(36)} | {'NOME'.ljust(17)} | {'ESPAÇO'.ljust(6)} | {'ESTADO'.ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO"
				)
				for personagem in personagens:
					print(
						f"{str(personagens.index(personagem) + 1).ljust(6)} - {personagem}"
					)
			print(f'{"0".ljust(6)} - Voltar')
			opcaoPersonagem = input(f"Opção:")
			if int(opcaoPersonagem) == 0:
				break
			while True:
				limpa_tela()
				self.__aplicacao.personagemEmUso(personagens[int(opcaoPersonagem) - 1])
				profissoes: list[Profissao] = self.__aplicacao.pegaProfissoes()
				if eh_vazia(profissoes):
					self.__aplicacao.insereListaProfissoes()
					continue
				print(
					f"{'ÍNDICE'.ljust(6)} - {'ID'.ljust(40)} | {'NOME'.ljust(22)} | {'EXP'.ljust(6)} | PRIORIDADE"
				)
				for profissao in profissoes:
					prioridade: str = (
						"Ativa" if profissao.prioridade == 1 else "Inativa"
					)
					print(
						f"{str(profissoes.index(profissao) + 1).ljust(6)} - {profissao.id.ljust(40)} | {profissao.nome.ljust(22)} | {str(profissao.experiencia).ljust(6)} | {prioridade}"
					)
				print(f'{"0".ljust(6)} - Voltar')
				opcaoProfissao = input(f"Opção: ")
				if int(opcaoProfissao) == 0:
					break
				profissaoRemovida = profissoes[int(opcaoProfissao) - 1]
				if self.__aplicacao.removeProfissao(profissao=profissaoRemovida):
					continue
				input(f"Clique para continuar...")

	def insereProfissao(self):
		while True:
			personagens = self.mostraListaPersonagens()
			if variavelExiste(personagens) and self.definePersonagemEscolhido(
				personagens
			):
				while True:
					profissoes = self.__aplicacao.pegaProfissoes()
					if eh_vazia(profissoes):
						self.__aplicacao.insereListaProfissoes()
						continue
					print(
						f"{'ÍNDICE'.ljust(6)} - {'ID'.ljust(40)} | {'ID PERSONAGEM'.ljust(40)} | {'NOME'.ljust(22)} | {'EXP'.ljust(6)} | PRIORIDADE"
					)
					for profissao in profissoes:
						print(
							f"{str(profissoes.index(profissao) + 1).ljust(6)} - {profissao}"
						)
					insereProfissao = self.defineInsereProfissao()
					if variavelExiste(profissoes) and insereProfissao:
						self.mostra_lista_profissoes()
						self.define_profissao_selecionada()
						if self.__profissao_selecionada is None:
							break

						experiencia = self.defineExperiencia()
						profissao: Profissao = Profissao()
						profissao.nome = self.__profissao_selecionada.nome
						profissao.setExperiencia(experiencia=experiencia)
						self.__aplicacao.insereProfissao(profissao=profissao)
						continue
					break
				continue
			break

	def modificaProfissao(self):
		while True:
			limpa_tela()
			personagens = self.__aplicacao.pegaPersonagens()
			if eh_vazia(personagens):
				print(f"Lista de personagens está vazia!")
			else:
				print(
					f"{'ÍNDICE'.ljust(6)} - {'ID'.ljust(36)} | {'NOME'.ljust(17)} | {'ESPAÇO'.ljust(6)} | {'ESTADO'.ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO"
				)
				for personagem in personagens:
					print(
						f"{str(personagens.index(personagem) + 1).ljust(6)} - {personagem}"
					)
			print(f'{"0".ljust(6)} - Voltar')
			opcaoPersonagem = input(f"Opção:")
			if int(opcaoPersonagem) == 0:
				break
			while True:
				limpa_tela()
				self.__aplicacao.personagemEmUso(personagens[int(opcaoPersonagem) - 1])
				profissoes = self.__aplicacao.pegaProfissoes()
				if eh_vazia(profissoes):
					self.__aplicacao.insereListaProfissoes()
					continue
				print(
					f"{'ÍNDICE'.ljust(6)} - {'ID'.ljust(40)} | {'ID PERSONAGEM'.ljust(40)} | {'NOME'.ljust(22)} | {'EXP'.ljust(6)} | PRIORIDADE"
				)
				for profissao in profissoes:
					print(
						f"{str(profissoes.index(profissao) + 1).ljust(6)} - {profissao}"
					)
				print(f'{"0".ljust(6)} - Voltar')
				opcaoProfissao = input(f"Opção: ")
				if int(opcaoProfissao) == 0:
					break
				profissaoModificado: Profissao = profissoes[int(opcaoProfissao) - 1]
				novoNome = input(f"Novo nome: ")
				novaExperiencia = input(f"Nova experiência: ")
				alternaPrioridade = input(f"Alternar prioridade? (S/N) ")
				novoNome = profissaoModificado.nome if eh_vazia(novoNome) else novoNome
				novaExperiencia = (
					profissaoModificado.experiencia
					if eh_vazia(novaExperiencia)
					else novaExperiencia
				)
				profissaoModificado.nome = novoNome
				profissaoModificado.setExperiencia(novaExperiencia)
				if alternaPrioridade.lower() == "s":
					profissaoModificado.alternaPrioridade
				if self.__aplicacao.modificaProfissao(profissao=profissaoModificado):
					continue
				input(f"Clique para continuar...")

	def pegaTodosTrabalhosProducao(self):
		limpa_tela()
		trabalhosProducao = self.__aplicacao.pegaTodosTrabalhosProducao()
		# print(f'{'NOME'.ljust(113)} | {'DATA'.ljust(10)} | {'ID TRABALHO'.ljust(36)} | {'VALOR'.ljust(5)} | UND')
		if eh_vazia(trabalhosProducao):
			print("Lista de trabalhos em produção está vazia!")
		else:
			for trabalhoProducao in trabalhosProducao:
				print(trabalhoProducao)
		input(f"Clique para continuar...")

	def insereTrabalhoEstoque(self):
		while True:
			personagens = self.mostraListaPersonagens()
			if variavelExiste(personagens) and self.definePersonagemEscolhido(
				personagens
			):
				while True:
					estoque = self.mostraListaTrabalhosEstoque()
					if variavelExiste(estoque):
						opcaoTrabalho = input(
							f"Inserir novo trabalho ao estoque? (S/N) "
						)
						if opcaoTrabalho.lower() == "n":
							break
						self.mostra_lista_profissoes()
						trabalhoBuscado = Trabalho()
						self.define_profissao_selecionada()
						if self.__profissao_selecionada is None:
							break

						trabalhoBuscado.profissao = self.__profissao_selecionada.id
						self.mostra_lista_raridades()
						self.define_raridade_selecionada()
						if self.__raridade_selecionada is None:
							break

						trabalhoBuscado.raridade = self.__raridade_selecionada
						trabalhos = (
							self.__aplicacao.pega_trabalhos_por_profissao_raridade(
								trabalhoBuscado
							)
						)
						if eh_vazia(trabalhos):
							print("Lista de trabalhos está vazia!")
						else:
							print(
								f'{"ÍNDICE".ljust(6)} - {"NOME".ljust(44)} | {"PROFISSÃO".ljust(22)} | {"RARIDADE".ljust(9)} | NÍVEL'
							)
							for trabalho in trabalhos:
								print(
									f"{str(trabalhos.index(trabalho) + 1).ljust(6)} - {trabalho}"
								)
						print(f'{"0".ljust(6)} - Voltar')
						trabalho = self.defineTrabalhoEstoqueSelecionado(trabalhos)
						if variavelExiste(trabalho):
							trabalhoEstoque = self.defineNovoTrabalhoEstoque(trabalho)
							if self.__aplicacao.insereTrabalhoEstoque(
								trabalho=trabalhoEstoque
							):
								continue
							input("Clique para continuar...")
							continue
						break
					break
				continue
			break

	def defineTrabalhoEstoqueSelecionado(self, trabalhos):
		opcaoTrabalho = input(f"Opção trabalho: ")
		if int(opcaoTrabalho) == 0:
			return
		trabalho = trabalhos[int(opcaoTrabalho) - 1]
		return trabalho

	def defineNovoTrabalhoEstoque(self, trabalho):
		quantidadeTrabalho = input(f"Quantidade trabalho: ")
		trabalhoEstoque = TrabalhoEstoque()
		trabalhoEstoque.dicionarioParaObjeto(trabalho.__dict__)
		trabalhoEstoque.id = str(uuid4())
		trabalhoEstoque.idTrabalho = trabalho.id
		trabalhoEstoque.setQuantidade(quantidadeTrabalho)
		return trabalhoEstoque

	def define_profissao_selecionada(self):
		opcao_selecionada: str = input("Opçao profissão: ")
		self.__profissao_selecionada = (
			None
			if int(opcao_selecionada) == 0
			else self.__profissoes[int(opcao_selecionada) - 1]
		)

	def defineExperiencia(self) -> int:
		experiencia: str = input("Experiência: ")
		return (
			0
			if experiencia is None
			else 0 if eh_vazia(experiencia) else int(experiencia)
		)

	def define_raridade_selecionada(self):
		opcao_selecionada = input("Opçao raridade: ")
		self.__raridade_selecionada = (
			None
			if int(opcao_selecionada) == 0
			else LISTA_RARIDADES[int(opcao_selecionada) - 1]
		)

	def mostra_lista_profissoes(self):
		limpa_tela()
		print(f'{"ÍNDICE".ljust(6)} - {"ID".ljust(40)} | {"DESCRIÇÃO".ljust(22)}')
		for profissao in self.__profissoes:
			print(
				f"{str(self.__profissoes.index(profissao) + 1).ljust(6)} - {profissao}"
			)
		print(f'{"0".ljust(6)} - Voltar')

	def mostra_lista_raridades(self):
		limpa_tela()
		print(f"{'ÍNDICE'.ljust(6)} - DESCRIÇÃO")
		for raridade in LISTA_RARIDADES:
			print(f"{str(LISTA_RARIDADES.index(raridade) + 1).ljust(6)} - {raridade}")
		print(f'{"0".ljust(6)} - Voltar')

	def modificaTrabalhoEstoque(self):
		while True:
			personagens = self.mostraListaPersonagens()
			if variavelExiste(personagens) and self.definePersonagemEscolhido(
				personagens
			):
				while True:
					estoque = self.mostraListaTrabalhosEstoque()
					if variavelExiste(estoque):
						trabalhoEstoque = self.defineTrabalhoEstoqueSelecionado(estoque)
						if variavelExiste(trabalhoEstoque):
							trabalhoEstoque = self.defineTrabalhoEstoqueModificado(
								trabalhoEstoque
							)
							if self.__aplicacao.modifica_trabalho_estoque(
								trabalhoEstoque
							):
								continue
							input("Clique para continuar...")
							continue
						break
					break
				continue
			break

	def defineTrabalhoEstoqueModificado(self, trabalhoEstoque):
		quantidade = input(f"Quantidade trabalho: ")
		quantidade = trabalhoEstoque.quantidade if ehVazia(quantidade) else quantidade
		trabalhoEstoque.setQuantidade(quantidade)
		return trabalhoEstoque

	def removeTrabalhoEstoque(self):
		while True:
			personagens = self.mostraListaPersonagens()
			if variavelExiste(personagens) and self.definePersonagemEscolhido(
				personagens
			):
				while True:
					estoque = self.mostraListaTrabalhosEstoque()
					if variavelExiste(estoque):
						trabalhoEstoque = self.defineTrabalhoEstoqueSelecionado(estoque)
						if variavelExiste(trabalhoEstoque):
							if self.__aplicacao.removeTrabalhoEstoque(
								trabalho=trabalhoEstoque
							):
								continue
							input("Cliue para continuar...")
							continue
						break
					break
				continue
			break

	def defineTrabalhoEstoqueSelecionado(self, estoque):
		opcaoTrabalho = input(f"Opção trabalho: ")
		if int(opcaoTrabalho) == 0:
			return None
		trabalhoEstoque = estoque[int(opcaoTrabalho) - 1]
		return trabalhoEstoque

	def mostraListaTrabalhosEstoque(self):
		limpa_tela()
		estoque = self.__aplicacao.recupera_trabalhos_estoque()
		if eh_vazia(estoque):
			print(f"Estoque está vazio!")
		else:
			print(
				f'{"ÍNDICE".ljust(6)} - {"NOME".ljust(40)} | {"PROFISSÃO".ljust(25)} | {"QNT".ljust(3)} | {"NÍVEL".ljust(5)} | {"RARIDADE".ljust(10)} | ID TRABALHO'
			)
			for trabalhoEstoque in estoque:
				print(
					f"{str(estoque.index(trabalhoEstoque) + 1).ljust(6)} - {trabalhoEstoque.nome.ljust(40)} | {trabalhoEstoque.profissao.ljust(25)} | {str(trabalhoEstoque.quantidade).ljust(3)} | {str(trabalhoEstoque.nivel).ljust(5)} | {trabalhoEstoque.raridade.ljust(10)} | {trabalhoEstoque.idTrabalho}"
				)
		print(f'{"0".ljust(6)} - Voltar')
		return estoque

	def mostraListaPersonagens(self):
		limpa_tela()
		personagens = self.__aplicacao.pegaPersonagens()
		if eh_vazia(personagens):
			print("Lista de personagens está vazia!")
		else:
			print(
				f"{'ÍNDICE'.ljust(6)} - {'ID'.ljust(36)} | {'NOME'.ljust(17)} | {'ESPAÇO'.ljust(6)} | {'ESTADO'.ljust(10)} | {'USO'.ljust(10)} | AUTOPRODUCAO"
			)
			for personagem in personagens:
				print(
					f"{str(personagens.index(personagem) + 1).ljust(6)} - {personagem}"
				)
		print(f'{"0".ljust(6)} - Voltar')
		return personagens

	def definePersonagemEscolhido(self, personagens) -> bool:
		opcaoPersonagem = input(f"Opção: ")
		if int(opcaoPersonagem) == 0:
			return False
		self.__personagemEmUso = personagens[int(opcaoPersonagem) - 1]
		self.__aplicacao.personagemEmUso(personagens[int(opcaoPersonagem) - 1])
		return True

	def mostraListaVendas(self):
		limpa_tela()
		print(
			f'{"ÍNDICE".ljust(6)} - {"ID".ljust(36)} | {"NOME".ljust(36)} | {"DATA".ljust(10)} | {"VALOR".ljust(5)} | UND'
		)
		vendas = self.__aplicacao.recupera_trabalhos_vendidos()
		if eh_vazia(vendas):
			print("Lista de vendas está vazia!")
		else:
			for trabalho in vendas:
				print(f"{str(vendas.index(trabalho) + 1).ljust(6)} - {trabalho}")
		return vendas

	def mostraListaTrabalhos(self):
		limpa_tela()
		trabalhos = self.__aplicacao.pegaTrabalhosBanco()
		if eh_vazia(trabalhos):
			print("Lista de trabalhos está vazia!")
		else:
			print(
				f'{"ÍNDICE".ljust(6)} - {"NOME".ljust(44)} | {"PROFISSÃO".ljust(22)} | {"RARIDADE".ljust(9)} | NÍVEL'
			)
			for trabalho in trabalhos:
				print(f"{str(trabalhos.index(trabalho) + 1).ljust(6)} - {trabalho}")
		return trabalhos

	def insereTrabalhoVendido(self):
		while True:
			personagens = self.mostraListaPersonagens()
			if variavelExiste(personagens) and self.definePersonagemEscolhido(
				personagens
			):
				while True:
					vendas = self.mostraListaVendas()
					if variavelExiste(vendas):
						inserir = input(f"Inserir novo trabalho ao estoque: (S/N) ")
						if inserir.lower() == "n":
							break
						self.mostra_lista_profissoes()
						self.define_profissao_selecionada()
						if self.__profissao_selecionada is None:
							break

						self.mostra_lista_raridades()
						self.define_raridade_selecionada()
						if self.__raridade_selecionada is None:
							break
						trabalhoBuscado = Trabalho()
						trabalhoBuscado.profissao = self.__profissao_selecionada.id
						trabalhoBuscado.raridade = self.__raridade_selecionada
						trabalhos = self.mostraTrabalhosPorProfissaoRaridade(
							trabalhoBuscado
						)
						if variavelExiste(trabalhos):
							trabalhoSelecionado = self.defineTrabalhoVendidoSelecionado(
								trabalhos
							)
							if variavelExiste(trabalhoSelecionado):
								novoTrabalhoVendido = self.defineNovoTrabalhoVendido(
									trabalhoSelecionado
								)
								if variavelExiste(novoTrabalhoVendido):
									if self.__aplicacao.insere_trabalho_vendido(
										trabalho=novoTrabalhoVendido
									):
										continue
									input("Clique para continuar...")
									continue
								break
							break
						break
					break
				continue
			break

	def mostraTrabalhosPorProfissaoRaridade(self, trabalhoBuscado):
		limpa_tela()
		trabalhos = self.__aplicacao.pega_trabalhos_por_profissao_raridade(
			trabalhoBuscado
		)
		if eh_vazia(trabalhos):
			print("Lista de trabalhos está vazia!")
		else:
			print(
				f'{"ÍNDICE".ljust(6)} - {"NOME".ljust(44)} | {"PROFISSÃO".ljust(22)} | {"RARIDADE".ljust(9)} | NÍVEL'
			)
			for trabalho in trabalhos:
				print(
					f"{str(trabalhos.index(trabalho) + 1).ljust(6)} - {trabalho} | {trabalho.trabalhoNecessario}"
				)
		return trabalhos

	def defineNovoTrabalhoVendido(self, trabalho: TrabalhoVendido) -> TrabalhoVendido:
		descricao = input(f"Descrição da venda: ")
		data = input(f"Data da venda: ")
		quantidade = input(f"Quantidade trabalho vendido: ")
		valor = input(f"Valor do trabalho vendido: ")
		trabalho.descricao = descricao
		trabalho.dataVenda = data
		trabalho.setQuantidade(quantidade)
		trabalho.setValor(valor)
		return trabalho

	def defineVendaEscolhida(self, vendas: list[TrabalhoVendido]) -> TrabalhoVendido:
		opcaoTrabalho = input(f"Opção trabalho: ")
		if int(opcaoTrabalho) == 0:
			return None
		return vendas[int(opcaoTrabalho) - 1]

	def modificaTrabalhoVendido(self):
		while True:
			personagens = self.mostraListaPersonagens()
			if variavelExiste(personagens) and self.definePersonagemEscolhido(
				personagens
			):
				while True:
					vendas = self.mostraListaVendas()
					if variavelExiste(vendas):
						print(f'{"0".ljust(6)} - Voltar')
						trabalhoVendidoModificado = self.defineVendaEscolhida(vendas)
						if variavelExiste(trabalhoVendidoModificado):
							trabalhoVendidoModificado = (
								self.defineTrabalhoVendidoModificado(
									trabalhoVendidoModificado
								)
							)
							if self.__aplicacao.modificaTrabalhoVendido(
								trabalho=trabalhoVendidoModificado
							):
								continue
							input("Clique para continuar...")
							continue
						break
					break
				continue
			break

	def removeTrabalhoVendido(self):
		while True:
			personagens = self.mostraListaPersonagens()
			if variavelExiste(personagens) and self.definePersonagemEscolhido(
				personagens
			):
				while True:
					vendas = self.mostraListaVendas()
					if variavelExiste(vendas):
						print(f'{"0".ljust(6)} - Voltar')
						trabalhoVendidoSelecionado = self.defineVendaEscolhida(vendas)
						if variavelExiste(trabalhoVendidoSelecionado):
							if self.__aplicacao.removeTrabalhoVendido(
								trabalho=trabalhoVendidoSelecionado
							):
								continue
							input("Clique para continuar...")
							continue
						break
					break
				continue
			break

	def defineTrabalhoVendidoModificado(self, trabalho: TrabalhoVendido):
		limpa_tela()
		descricao = input(f"Descrição do trabalho: ")
		data = input(f"Data da venda: ")
		quantidade = input(f"Quantidade vendida: ")
		valor = input(f"Valor da venda: ")
		trabalho.descricao = trabalho.descricao if eh_vazia(descricao) else descricao
		trabalho.dataVenda = trabalho.dataVenda if eh_vazia(data) else data
		trabalho.quantidade = (
			trabalho.quantidade if eh_vazia(quantidade) else quantidade
		)
		trabalho.valor = trabalho.valor if eh_vazia(valor) else valor
		return trabalho

	def defineTrabalhoProducaoSelecionado(
		self, trabalhos: list[TrabalhoProducao]
	) -> TrabalhoProducao | None:
		trabalhoProducao = TrabalhoProducao()
		print(f'{"0".ljust(6)} - Voltar')
		opcaoTrabalho = input(f"Opção trabalho: ")
		if int(opcaoTrabalho) == 0:
			return None
		trabalho: TrabalhoProducao = trabalhos[int(opcaoTrabalho) - 1]
		trabalhoProducao.id = trabalho.id
		trabalhoProducao.idTrabalho = trabalho.idTrabalho
		trabalhoProducao.tipoLicenca = trabalho.tipoLicenca
		trabalhoProducao.recorrencia = trabalho.recorrencia
		trabalhoProducao.estado = trabalho.estado
		return trabalhoProducao

	def defineTrabalhoVendidoSelecionado(
		self, trabalhos: list[Trabalho]
	) -> TrabalhoVendido | None:
		trabalhoVendido = TrabalhoVendido()
		print(f'{"0".ljust(6)} - Voltar')
		opcaoTrabalho = input(f"Opção trabalho: ")
		if int(opcaoTrabalho) == 0:
			return None
		trabalho = trabalhos[int(opcaoTrabalho) - 1]
		trabalhoVendido.idTrabalho = trabalho.id
		return trabalhoVendido

	def sincronizaDados(self):
		self.__aplicacao.sincronizaListaTrabalhos()
		self.__aplicacao.sincronizaListaPersonagens()
		self.__aplicacao.sincronizaListaProfissoes()
		self.__aplicacao.sincronizaTrabalhosEstoque()
		self.__aplicacao.sincronizaTrabalhosProducao()
		self.__aplicacao.sincronizaTrabalhosVendidos()

	def verificaTrabalhoRaroMaisVendido(self):
		vendas = self.__aplicacao.pegaTrabalhosRarosVendidos()
		for trabalhoVendido in vendas:
			quantidadeTrabalhoRaroEmEstoque = (
				self.__aplicacao.recupera_quantidade_trabalho_estoque(
					trabalhoVendido.trabalhoId
				)
			)
			print(
				f"Quantidade de ({trabalhoVendido.nome}) no estoque: {quantidadeTrabalhoRaroEmEstoque}"
			)
			# quantidadeTrabalhoRaroNecessario = CODIGO_QUANTIDADE_MINIMA_TRABALHO_RARO_EM_ESTOQUE - quantidadeTrabalhoEmEstoque
			quantidadeTrabalhoRaroNecessario = 2 - quantidadeTrabalhoRaroEmEstoque
			if quantidadeTrabalhoRaroNecessario > 0:
				trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(self.__personagemEmUso)
				quantidadeTrabalhoRaroEmProducao = (
					trabalhoProducaoDao.pegaQuantidadeTrabalhoProducaoProduzindo(
						trabalhoVendido.trabalhoId
					)
				)
				if variavelExiste(quantidadeTrabalhoRaroEmProducao):
					quantidadeTrabalhoRaroNecessario -= quantidadeTrabalhoRaroEmProducao
					print(
						f"Quantidade de ({trabalhoVendido.nome}) em produção: {quantidadeTrabalhoRaroEmProducao}"
					)
					if quantidadeTrabalhoRaroNecessario > 0:
						trabalhoMelhoradoNecessario = trabalhoVendido.trabalhoNecessario
						if variavelExiste(trabalhoMelhoradoNecessario):
							print(
								f"Trabalho melhorado necessário: ({trabalhoMelhoradoNecessario})"
							)
							profissao = self.__aplicacao.retornaProfissaoTrabalhoProducaoConcluido(
								trabalhoVendido
							)
							if variavelExiste(profissao):
								print(f"Profissão: ({profissao})")
								xpMaximo = profissao.pegaExperienciaMaximaPorNivel
								licencaProducaoIdeal = (
									CHAVE_LICENCA_NOVATO
									if xpMaximo >= 830000
									else CHAVE_LICENCA_INICIANTE
								)
								print(
									f"Licença de produção ideal: ({licencaProducaoIdeal})"
								)
								trabalhoMelhoradoBuscado = Trabalho()
								trabalhoMelhoradoBuscado.nome = (
									trabalhoVendido.trabalhoNecessario
								)
								trabalhoMelhoradoBuscado.raridade = (
									CHAVE_RARIDADE_MELHORADO
								)
								trabalhoMelhoradoBuscado.profissao = (
									trabalhoVendido.profissao
								)
								trabalhoMelhoradoEncontrado = self.__aplicacao.pegaTrabalhoPorNomeProfissaoRaridade(
									trabalhoMelhoradoBuscado
								)
								if variavelExiste(trabalhoMelhoradoEncontrado):
									quantidadeTrabalhoMelhoradoEmEstoque = self.__aplicacao.recupera_quantidade_trabalho_estoque(
										trabalhoMelhoradoEncontrado.id
									)
									quantidadeTrabalhoMelhoradoNecessario = (
										quantidadeTrabalhoRaroNecessario
										- quantidadeTrabalhoMelhoradoEmEstoque
									)
									print(
										f"Quantidade de ({trabalhoMelhoradoEncontrado.nome}) no estoque: {quantidadeTrabalhoMelhoradoEmEstoque}"
									)
									trabalhoProducaoDao = TrabalhoProducaoDaoSqlite(
										self.__personagemEmUso
									)
									quantidadeTrabalhoMelhoradoEmProducao = trabalhoProducaoDao.pegaQuantidadeTrabalhoProducaoProduzindo(
										trabalhoMelhoradoEncontrado.id
									)
									if variavelExiste(
										quantidadeTrabalhoMelhoradoEmProducao
									):
										quantidadeTrabalhoMelhoradoNecessario -= (
											quantidadeTrabalhoMelhoradoEmProducao
										)
										if (
											quantidadeTrabalhoMelhoradoNecessario
											< quantidadeTrabalhoRaroNecessario
											and quantidadeTrabalhoMelhoradoNecessario
											>= 0
										):
											quantidadeAdicionada = (
												quantidadeTrabalhoMelhoradoNecessario
											)
											if (
												quantidadeTrabalhoMelhoradoNecessario
												== 0
											):
												quantidadeAdicionada = (
													quantidadeTrabalhoRaroNecessario
												)
											while quantidadeAdicionada > 0:
												self.__loggerTrabalhoProducaoDao.info(
													f"({trabalhoVendido.nome}) adicionado com sucesso!"
												)
												quantidadeAdicionada -= 1
												pass
											return
										continue
									self.__loggerTrabalhoProducaoDao.error(
										f"Erro ao buscar quantidade: {trabalhoProducaoDao.pegaErro}"
									)
									continue
							continue
						print(
							f"({trabalhoVendido.nome}) não possue trabalho necesssário!"
						)
					continue
				self.__loggerTrabalhoProducaoDao.error(
					f"Erro ao buscar quantidade: {trabalhoProducaoDao.pegaErro}"
				)
			continue
		input("Clique para continuar...")

	def iniciaStreans(self):
		self.__aplicacao.abreStreans()

	def testeFuncao(self):
		from repositorio.repositorioTrabalho import RepositorioTrabalho
		from repositorio.repositorioProfissao import RepositorioProfissao

		repositorio_trabalho: RepositorioTrabalho = RepositorioTrabalho()
		trabalhos = repositorio_trabalho.pega_todos_trabalhos()

		repositorio_profissao: RepositorioProfissao = RepositorioProfissao()
		profissoes = repositorio_profissao.pega_todas_profissoes()
		if not profissoes:
			return

		if not trabalhos:
			return
		mapa_profissoes = {
			limpa_ruido_texto(profissao.nome): profissao.id
			for profissao in profissoes
			if profissao.nome
		}

		total = len(trabalhos)

		for indice, trabalho in enumerate(trabalhos, start=1):
			limpa_tela()
			porcentagem = (indice / total) * 100
			print(f"{indice} de {total} verificado. {porcentagem:.2f}%")
			if not trabalho.profissao:
				continue

			chave_trabalho = limpa_ruido_texto(trabalho.profissao)

			if chave_trabalho in mapa_profissoes:
				trabalho.profissao = mapa_profissoes[chave_trabalho]
				repositorio_trabalho.modificaTrabalho(trabalho)

	def testeStream(self):
		from repositorio.repositorioTrabalho import RepositorioTrabalho
		from repositorio.repositorioTrabalhoProducao import RepositorioTrabalhoProducao

		repositorioTrabalho: RepositorioTrabalho = RepositorioTrabalho()
		repositorioTrabalhoProducao: RepositorioTrabalhoProducao = (
			RepositorioTrabalhoProducao()
		)
		if not repositorioTrabalhoProducao.abreStream():
			print(repositorioTrabalhoProducao.pegaErro)
		if not repositorioTrabalho.abreStream():
			print(repositorioTrabalho.pegaErro)
		while True:
			if repositorioTrabalho.estaPronto:
				trabalhos: list[Trabalho] = repositorioTrabalho.pegaDadosModificados()
				print(
					f"{CHAVE_NOME.upper().ljust(44)} | {CHAVE_PROFISSAO.upper().ljust(22)} | {CHAVE_RARIDADE.upper().ljust(9)} | {CHAVE_NIVEL.upper().ljust(5)}"
				)
				for trabalho in trabalhos:
					print(trabalho)
				repositorioTrabalho.limpaLista
			if repositorioTrabalhoProducao.estaPronto:
				dicionariosTrabalhoProducao: list[dict] = (
					repositorioTrabalhoProducao.pegaDadosModificados()
				)
				for dicionarioTrabalho in dicionariosTrabalhoProducao:
					for atributo in dicionarioTrabalho:
						print(f"{atributo} | {dicionarioTrabalho[atributo]}")
				repositorioTrabalhoProducao.limpaLista

	def migraDadosNovoServidor(self):
		from pyrebase.pyrebase import Database
		from pyrebase.pyrebase import PyreResponse
		from repositorio.firebaseDatabase import FirebaseDatabase
		from modelos.usuario import Usuario

		logger = MeuLogger(nome="novoServidor")
		firebase: FirebaseDatabase = FirebaseDatabase()
		meuBanco: Database = firebase.pegaMeuBanco()
		referenciaUsuarios: PyreResponse = meuBanco.child(CHAVE_USUARIOS).get()
		for usuarioEncontrado in referenciaUsuarios.each():
			usuario: Usuario = Usuario()
			dicionarioUsuario: dict = usuarioEncontrado.val()
			usuario.dicionarioParaObjeto(dicionario=dicionarioUsuario)
			meuBanco.child(CHAVE_USUARIOS2).child(usuario.id).update(
				{CHAVE_ID: usuario.id, CHAVE_NOME: usuario.nome}
			)
			for idpersonagem in dicionarioUsuario[CHAVE_LISTA_PERSONAGEM]:
				meuBanco.child(CHAVE_USUARIOS2).child(usuario.id).child(
					CHAVE_PERSONAGENS
				).update({idpersonagem: True})
				dicionarioPersonagem: dict = dicionarioUsuario[CHAVE_LISTA_PERSONAGEM][
					idpersonagem
				]
				personagem: Personagem = Personagem()
				personagem.dicionarioParaObjeto(dicionario=dicionarioPersonagem)
				meuBanco.child(CHAVE_PERSONAGENS).child(personagem.id).update(
					{
						CHAVE_ID: personagem.id,
						CHAVE_NOME: personagem.nome,
						CHAVE_AUTO_PRODUCAO: personagem.autoProducao,
						CHAVE_EMAIL: personagem.email,
						CHAVE_ESPACO_PRODUCAO: personagem.espacoProducao,
						CHAVE_ESTADO: personagem.estado,
						CHAVE_SENHA: personagem.senha,
						CHAVE_USO: personagem.uso,
					}
				)
				dicionarioPersonagem: dict = dicionarioUsuario[CHAVE_LISTA_PERSONAGEM][
					idpersonagem
				]
				if CHAVE_LISTA_TRABALHOS_PRODUCAO in dicionarioPersonagem:
					for idTrabalhoProducao in dicionarioPersonagem[
						CHAVE_LISTA_TRABALHOS_PRODUCAO
					]:
						dicionarioTrabalhoProducao: dict = dicionarioPersonagem[
							CHAVE_LISTA_TRABALHOS_PRODUCAO
						][idTrabalhoProducao]
						if CHAVE_ID_TRABALHO in dicionarioTrabalhoProducao:
							meuBanco.child(CHAVE_PRODUCAO).child(idpersonagem).child(
								idTrabalhoProducao
							).update(
								{
									CHAVE_ESTADO: dicionarioTrabalhoProducao[
										CHAVE_ESTADO
									],
									CHAVE_ID: dicionarioTrabalhoProducao[CHAVE_ID],
									CHAVE_ID_TRABALHO: dicionarioTrabalhoProducao[
										CHAVE_ID_TRABALHO
									],
									CHAVE_RECORRENCIA: dicionarioTrabalhoProducao[
										CHAVE_RECORRENCIA
									],
									CHAVE_TIPO_LICENCA: dicionarioTrabalhoProducao[
										"tipo_licenca"
									],
								}
							)
							continue
						logger.error(
							mensagem=f"Erro ao inserir trabalho de produção: {idTrabalhoProducao} não possue atributo idTrabalho"
						)
				if CHAVE_LISTA_ESTOQUE in dicionarioPersonagem:
					for idTrabalhoEstoque in dicionarioPersonagem[CHAVE_LISTA_ESTOQUE]:
						dicionarioTrabalhoEstoque: dict = dicionarioPersonagem[
							CHAVE_LISTA_ESTOQUE
						][idTrabalhoEstoque]
						if CHAVE_TRABALHO_ID in dicionarioTrabalhoEstoque:
							meuBanco.child(CHAVE_ESTOQUE).child(idpersonagem).child(
								idTrabalhoEstoque
							).update(
								{
									CHAVE_ID: dicionarioTrabalhoEstoque[CHAVE_ID],
									CHAVE_ID_TRABALHO: dicionarioTrabalhoEstoque[
										CHAVE_TRABALHO_ID
									],
									CHAVE_QUANTIDADE: dicionarioTrabalhoEstoque[
										CHAVE_QUANTIDADE
									],
								}
							)
							continue
						logger.error(
							mensagem=f"Erro ao inserir trabalho de estoque: {idTrabalhoEstoque} não possue atributo trabalhoId"
						)
				if CHAVE_LISTA_VENDAS in dicionarioPersonagem:
					for idTrabalhoVendido in dicionarioPersonagem[CHAVE_LISTA_VENDAS]:
						dicionarioTrabalhoVendido: dict = dicionarioPersonagem[
							CHAVE_LISTA_VENDAS
						][idTrabalhoVendido]
						if CHAVE_ID_TRABALHO in dicionarioTrabalhoVendido:
							meuBanco.child(CHAVE_VENDAS).child(idpersonagem).child(
								idTrabalhoVendido
							).update(
								{
									CHAVE_ID: dicionarioTrabalhoVendido[CHAVE_ID],
									CHAVE_ID_TRABALHO: dicionarioTrabalhoVendido[
										CHAVE_ID_TRABALHO
									],
									CHAVE_DATA_VENDA: dicionarioTrabalhoVendido[
										CHAVE_DATA_VENDA
									],
									CHAVE_DESCRICAO: dicionarioTrabalhoVendido[
										CHAVE_DESCRICAO
									],
									CHAVE_QUANTIDADE: dicionarioTrabalhoVendido[
										CHAVE_QUANTIDADE
									],
									CHAVE_VALOR: dicionarioTrabalhoVendido[CHAVE_VALOR],
								}
							)
							continue
						logger.error(
							mensagem=f"Erro ao inserir trabalho de estoque: {idTrabalhoVendido} não possue atributo trabalhoId"
						)
		input("Clique para continuar...")

	def menu(self):
		while True:
			self.__aplicacao.verificaAlteracaoTrabalhos()
			self.__aplicacao.verificaAlteracaoProducao()
			self.__aplicacao.verificaAlteracaoPersonagens()
			self.__aplicacao.verificaAlteracaoProfissoes()
			self.__aplicacao.verificaAlteracaoEstoque()
			self.__aplicacao.verificaAlteracaoVendas()
			limpa_tela()
			print(f"MENU")
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
				opcaoMenu = input(f"Opção escolhida: ")
				if int(opcaoMenu) == 0:
					break
				if int(opcaoMenu) == 1:
					self.insere_novo_trabalho()
					continue
				if int(opcaoMenu) == 2:
					self.modifica_trabalho()
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
				print(f"Opção inválida! Erro: {erro}")
				input(f"Clique para continuar...")


if __name__ == "__main__":
	crud: CRUD = CRUD()
	crud.menu()
	# aplicacaoCRUD: AplicacaoCRUD= AplicacaoCRUD()
	# aplicacaoCRUD.mainloop()
