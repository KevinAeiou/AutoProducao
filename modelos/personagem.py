class Personagem:
    def __init__(self, id, nome, email, senha, espacoProducao, estado, uso):
        self._id = id
        self._nome = nome
        self._email = email
        self._senha = senha
        self._espacoProducao = espacoProducao
        self._estado = estado
        self._uso = uso

    def __str__(self) -> str:
        return f'{(self._nome).ljust(20)} | {self._email}'
    
    def pegaId(selft):
        return selft._id

    def pegaNome(self):
        return self._nome
    
    def pegaEmail(self):
        return self._email
    
    def pegaSenha(self):
        return self._senha
    
    def pegaEspacoProducao(self):
        return self._espacoProducao
    
    def pegaEstado(self):
        return self._estado
    
    def pegaUso(self):
        return self._uso