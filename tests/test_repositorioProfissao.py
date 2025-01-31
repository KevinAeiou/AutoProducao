from repositorio.repositorioProfissao import RepositorioProfissao
from repositorio.repositorioPersonagem import RepositorioPersonagem

class TestRepositorioProfisssao:
    _personagemTeste = RepositorioPersonagem().pegaTodosPersonagens()[0]
    _repositorioProfissao = RepositorioProfissao(_personagemTeste)