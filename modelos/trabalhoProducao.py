class TrabalhoProducao:
    def __init__(self, id, nome, nomeProducao, estado, experiencia, nivel, profissao, raridade, recorrencia, tipoLicenca, trabalhoId):
        self.id = id
        self.nome = nome
        self.nomeProducao = nomeProducao
        self.estado = estado
        self.experiencia = experiencia
        self.nivel = nivel
        self.profissao = profissao
        self.raridade = raridade
        self.recorrencia = recorrencia
        self.tipo_licenca = tipoLicenca
        self.trabalhoId = trabalhoId

    def pegaId(self):
        return self.id

    def pegaNome(self):
        return self.nome
    
    def pegaNomeProducao(self):
        return self.nomeProducao
    
    def pegaEstado(self):
        return self.estado
    
    def pegaExperiencia(self):
        return self.experiencia
    
    def pegaNivel(self):
        return self.nivel
    
    def pegaProfissao(self):
        return self.profissao
    
    def pegaRaridade(self):
        return self.raridade
    
    def pegaRecorrencia(self):
        return self.recorrencia
    
    def pegaLicenca(self):
        return self.tipo_licenca
    
    def pegaTrabalhoId(self):
        return self.trabalhoId
    
    def setId(self, id):
        self.id = id

    def setEstado(self, estado):
        self.estado = estado

    def setTrabalhoId(self, trabalhoId):
        self.trabalhoId = trabalhoId

    def setNomeProducao(self, nomeProducao):
        self.nomeProducao = nomeProducao

    def setRecorrencia(self, recorrencia):
        self.recorrencia = recorrencia

    def __str__(self) -> str:
        return f'{(self.nome).ljust(20)} | {(self.profissao).ljust(6)} | {self.nivel}'