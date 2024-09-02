from modelos.trabalhoRecurso import TrabalhoRecurso

class TestTrabalhoRecurso:
    def testDeveInstanciarNovoTrabalhoRecurso(self):
        self._trabalhoRecurso = TrabalhoRecurso('Arma de longo alcance', 32, 'Esfera do neófito', 'Varinha de aço', 'Cabeça do cajado de ônix', 19)
        print(self._trabalhoRecurso)