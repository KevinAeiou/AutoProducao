from modelos.personagem import Personagem
from dao.personagemDaoSqlite import PersonagemDaoSqlite
from db.db import MeuBanco
from modelos.logger import MeuLogger
from visao.reconhecimento_texto import ReconhecimentoTexto
from utilitarios import ehMenuRecompensasDiarias

logger: MeuLogger = MeuLogger(nome='recompensa_service')
class RecompensaService():

	def __init__(self) -> None:
		banco_ref: MeuBanco = MeuBanco()
		banco_ref.pega_conexao()
		banco_ref.cria_tabelas()
		self.personagem_dao: PersonagemDaoSqlite = PersonagemDaoSqlite(banco_ref)
		self.personagens_verificados: list[Personagem] = []
		self.reconhecimento_texto: ReconhecimentoTexto = ReconhecimentoTexto()

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
		logger.info(f'Iniciando coleta para {personagem.email}')

		nome_personagem: str | None = self.reconhecimento_texto.reconhecer_nome_personagem()

		if not nome_personagem:
			logger.warning('Não foi possível reconhecer o personagem atual.')
			return
		
		logger.debug(f'NOME_RECONHECIDO: {nome_personagem}')
		
		
		pass