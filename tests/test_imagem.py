from imagem import ManipulaImagem

class TestImagem:
    imagem = ManipulaImagem()

    def testDeveRetornarStringLicencaDeProducaoDoIniciante(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeLicencaDeProducaoDoIniciante.png')
        esperado = 'Licença de produção do iniciante'
        recebido = self.imagem.reconheceTextoLicenca(imagemTeste)
        assert recebido == esperado

    def testDeveRetornarStringLicencaDeProducaoDoPrincipiante(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeLicencaDeProducaoDoPrincipiante.png')
        esperado = 'Licença de produção do principiante'
        recebido = self.imagem.reconheceTextoLicenca(imagemTeste)
        assert recebido == esperado

    def testDeveRetornarStringLicencaDeProducaoDoMestre(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeLicencaDeProducaoDoMestre.png')
        esperado = 'Licença de produção do mestre'
        recebido = self.imagem.reconheceTextoLicenca(imagemTeste)
        assert recebido == esperado

    def testDeveRetornarStringLicencaDeProducaoDoAprendiz(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeLicencaDeProducaoDoAprendiz.png')
        esperado = 'Licença de produção do aprendiz'
        recebido = self.imagem.reconheceTextoLicenca(imagemTeste)
        assert recebido == esperado

    def testDeveRetornarStringLincencaNenhumItem(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeNenhumaLicencaDeProducao.png')
        esperado = 'Nenhum item'
        recebido = self.imagem.reconheceTextoLicenca(imagemTeste)
        assert esperado == recebido

    def testDeveRetornarStringAnelDeJadeBrutaQuandoPosicaoForZero(self):
        imagemTeste = self.imagem.abreImagem('')
        posicao = 0
        esperado = 'Anel de jade bruta'
        recebido = self.imagem.reconheceNomeConfirmacaoTrabalhoProducao(imagemTeste, posicao)
        assert recebido == esperado

    def testDeveRetornarStringAnelDeJadeBrutaQuandoPosicaoForUm(self):
        posicao = 1
        esperado = 'Anel de jade bruta'
        recebido = self.imagem.reconheceNomeConfirmacaoTrabalhoProducao(posicao)
        assert recebido == esperado

    def testDeveRetornarStringAnelDeJadeBrutaQuandoYFor530EIdentificadorIgual1(self):
        y = 530
        identificador = 1
        esperado = 'Anel de jade bruta'
        recebido = self.imagem.retornaNomeTrabalhoReconhecido(y, identificador)
        assert recebido == esperado

    def testDeveRetornarStringErroLicencaDeProducaoNecessaria(self):
        esperado = 'Você precisa de uma licença defabricação para iniciar este pedido'
        recebido = self.imagem.retornaErroReconhecido()
        assert esperado in recebido

    def testDeveRetornarStringWarspearQuandoXIgual26EYIgual1ELarguraIgual150(self):
        x = 26
        y = 1
        largura = 150
        esperado = 'warspearonline'
        recebido = self.imagem.retornaTextoMenuReconhecido(x, y, largura)
        assert esperado in recebido

    def testDeveRetornarStringWarspearQuandoXIgual26EYIgual1ELarguraIgual150(self):
        x = 26
        y = 1
        largura = 150
        esperado = 'warspearonline'
        recebido = self.imagem.retornaTextoMenuReconhecido(x, y, largura)
        assert esperado in recebido

    def testDeveRetornarTrueQuandoEhMenuInicial(self):
        esperado = True
        recebido = self.imagem.verificaMenuReferencia()
        assert esperado == recebido

    def testDeveRetornarStringSair(self):
        esperado = 'sair'
        recebido = self.imagem.retornaTextoSair()

    def testDeveRetornarTrueQuandoExistePixelCorreioRecebido(self):
        esperado = True
        recebido = self.imagem.existePixelCorrespondencia()

    def testDeveRetornarTrueQuandoExisteCorrespondencia(self):
        esperado = True
        recebido = self.imagem.existeCorrespondencia()
        assert esperado == recebido

    def testDeveRetornarFalseQuandoNaoExisteCorrespondencia(self):
        esperado = False
        recebido = self.imagem.existeCorrespondencia()
        assert esperado == recebido

    def testDeveRetornarTextoCorrespondenciaQuandoLoteVendido(self):
        esperado = 'Lote vendido'
        recebido = self.imagem.retornaTextoCorrespondenciaReconhecido(self.imagem.retornaAtualizacaoTela())
        assert esperado in recebido

    def testDeveRetornarValorDoLoteVendido(self):
        esperado = 1
        recebido = self.imagem.retornaValorDoTrabalhoVendido(self.imagem.retornaAtualizacaoTela())
        assert esperado == recebido

    def testDeveRetornarCodigoParaProduzirQuandoNaoExistirNemUmTrabalhoSendoProduzido(self):
        esperado = 0
        recebido = self.imagem.retornaEstadoTrabalho()
        assert esperado == recebido

    def testDeveRetornarCodigoProduzindoQuandoExistirPeloMenosUmTrabalhoSendoProduzido(self):
        esperado = 1
        recebido = self.imagem.retornaEstadoTrabalho()
        assert esperado == recebido

    def testDeveRetornarCodigoConcluidoQuandoExistirUmTrabalhoConcluido(self):
        esperado = 2
        recebido = self.imagem.retornaEstadoTrabalho()
        assert esperado == recebido
    
    def testDeveMostrarImagem(self):
        self.imagem.mostraImagem(0, self.imagem.retornaAtualizacaoTela()[311:311+43, 233:486], None)
        assert '' == ''
    
    def testDeveRetornarNomeTrabalhoConcluidoReconhecido(self):
        esperado = 'Adquirir molde do aprendiz'
        recebido = self.imagem.retornaNomeTrabalhoConcluidoReconhecido()
        assert esperado == recebido

    def testDeveRetornarNomePersonagemPallakuraQuandoPosicaoEhUm(self):
        quandoEh = 1
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeNomePersonagemPallakuraPosicaoUm.png')
        esperado = 'pallakura'
        recebido = self.imagem.reconheceTextoNomePersonagem(imagemTeste, quandoEh)
        assert esperado == recebido

    def testDeveRetornarNomePersonagemPallakuraQuandoPosicaoEhZero(self):
        quandoEh = 0
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeNomePersonagemPallakuraPosicaoZero.png')
        esperado = 'pallakura'
        recebido = self.imagem.reconheceTextoNomePersonagem(imagemTeste, quandoEh)
        assert esperado == recebido

    def testDeveRetornarStringErroFalhaAoConectar(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeErroFalhaAoConectarAoServidor.png')
        esperado = 'Falha ao se conectar ao servidor'
        recebido = self.imagem.reconheceTextoErro(imagemTeste)
        assert esperado == recebido