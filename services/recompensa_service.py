from modelos.personagem import Personagem
from dao.personagemDaoSqlite import PersonagemDaoSqlite
from db.db import MeuBanco
from modelos.logger import MeuLogger
from visao.reconhecimento_texto import ReconhecimentoTexto
from visao.reconhecimento_tela import ReconhecimentoTela
from automacao.teclado import ManipulaTeclado
from automacao.mouse import ManipulaMouse
from utilitarios import ehMenuRecompensasDiarias, limpa_tela
from time import sleep

logger: MeuLogger = MeuLogger(nome='recompensa_service')
class RecompensaService():

	def __init__(self) -> None:
		banco_ref: MeuBanco = MeuBanco()
		banco_ref.pega_conexao()
		banco_ref.cria_tabelas()
		self.personagem_dao: PersonagemDaoSqlite = PersonagemDaoSqlite(banco_ref)
		self.personagens_verificados: list[Personagem] = []
		self.reconhecimento_texto: ReconhecimentoTexto = ReconhecimentoTexto()
		self.reconhecimento_tela: ReconhecimentoTela = ReconhecimentoTela()
		self.manipula_teclado: ManipulaTeclado = ManipulaTeclado()
		self.manipula_mouse: ManipulaMouse = ManipulaMouse()

	def buscar_personagem_disponivel(self) -> Personagem | None:
		personagens_ativos: list[Personagem] = self.personagem_dao.pegaPersonagens()
		emails_verificados = {p.email for p in self.personagens_verificados}

		personagens_disponiveis = [
			p for p in personagens_ativos
			if p.email not in emails_verificados
		]

		if not personagens_disponiveis:
			return None

		personagem = personagens_disponiveis[0]
		self.personagens_verificados.append(personagem)

		return personagem

	def inicia_coleta(self, personagem: Personagem):
		personagens_verificados: list[str] = []
		limpa_tela()

		logger.info(f'Iniciando coleta para:\n{personagem.nome} | {personagem.email}')

		nomes_reconhecidos: list[str] = self.reconhecimento_texto.reconhecer_nome_personagem(posicao=0)

		if len(nomes_reconhecidos) == 0:
			logger.warning('Não foi possível reconhecer o personagem atual.')
			return
		

		for nome_reconhecido in nomes_reconhecidos:
			if nome_reconhecido != str(personagem.nome).lower():
				# deslogar e logar personagem atual
				return
		
		if personagem.nome is None:
			return

		tentativas: int = 0
		max_tentativas: int = 12
		while tentativas < max_tentativas:
			tentativas += 1
			
			personagens_verificados.append(nomes_reconhecidos[0])

			self.reconhecimento_tela.reconhece_menu_atual()

			while not self.reconhecimento_tela.eh_menu_recompensas_diarias:
				if self.reconhecimento_tela.eh_menu_inicial:
					self.manipula_teclado.clica_tecla('f1')
					self.manipula_teclado.clica_tecla('enter', intervalo=1)
					self.manipula_teclado.clica_tecla('down')
					self.manipula_teclado.clica_tecla('enter')


				if self.reconhecimento_tela.eh_menu_loja_milagrosa:
					self.manipula_teclado.clica_tecla('down')
					self.manipula_teclado.clica_tecla('enter')

				if self.reconhecimento_tela.eh_menu_oferta_diaria:
					self.manipula_teclado.clica_tecla('f1')

				self.reconhecimento_tela.reconhece_menu_atual()
			
			for _ in range(2):
				logger.debug(f'Buscando botão "Pegar".')

				referencia: tuple | None = self.reconhecimento_tela.retorna_coordenadas_botao_pegar()
				if referencia is not None:
					self.manipula_mouse.clica(x=referencia[0], y=referencia[1])

					self.manipula_mouse.move_cursor_para()

					self.reconhecimento_tela.verifica_erro()
					
					sleep(0.5)
					if self.reconhecimento_tela.erro_encontrado:
						self.manipula_teclado.clica_tecla(tecla='f2')

				self.manipula_teclado.preciona_tecla(tecla='up', cliques=10)
				self.manipula_teclado.clica_tecla(tecla='left')

			self.manipula_teclado.clica_tecla(tecla='f1', cliques=2)

			self.manipula_teclado.desloga_conta()

			# Verificar se é menu inicial

			self.manipula_teclado.clica_tecla('enter')

			tentativas_login: int = 0
			max_tentativas_login: int = 10
			while tentativas_login < max_tentativas_login:
				self.reconhecimento_tela.verifica_erro()

				if not self.reconhecimento_tela.erro_encontrado:
					break

				if self.reconhecimento_tela.eh_erro_conectando:
					continue
				
				tentativas_login += 1

			self.manipula_teclado.clica_tecla('f2')
			self.manipula_teclado.preciona_tecla('left', 14)

			tentativas_login: int = 0
			max_tentativas_login: int = 12
			while tentativas_login <= max_tentativas_login:
				tentativas_login += 1
				nomes_reconhecidos: list[str] = self.reconhecimento_texto.reconhecer_nome_personagem(posicao=1)

				if len(nomes_reconhecidos) == 0:
					return

				for verificado in personagens_verificados:
					for reconhecido in nomes_reconhecidos:
						if reconhecido == verificado:
							self.manipula_teclado.clica_tecla('right')
							break
					else:
						continue
				
				break

			self.manipula_teclado.clica_tecla('enter')

			tentativas_login: int = 0
			max_tentativas_login: int = 10
			while tentativas_login < max_tentativas_login:
				self.reconhecimento_tela.verifica_erro()

				if not self.reconhecimento_tela.erro_encontrado:
					break

				if self.reconhecimento_tela.eh_erro_conectando:
					continue

				if self.reconhecimento_tela.eh_erro_novo_presente:
					self.manipula_teclado.clica_tecla('f2', intervalo=1)
					break
				
				tentativas_login += 1

