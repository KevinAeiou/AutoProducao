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
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeTrabalhoAnelDeJadeBrutaPosicaoZero.png')
        posicao = 0
        esperado = 'Anel de jade bruta'
        recebido = self.imagem.reconheceNomeConfirmacaoTrabalhoProducao(imagemTeste, posicao)
        assert recebido == esperado

    def testDeveRetornarStringAnelDeJadeBrutaQuandoPosicaoForUm(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeTrabalhoAnelDeJadeBrutaPosicaoUm.png')
        posicao = 1
        esperado = 'Anel de jade bruta'
        recebido = self.imagem.reconheceNomeConfirmacaoTrabalhoProducao(imagemTeste, posicao)
        assert recebido == esperado

    def testDeveRetornarStringAnelDeJadeBrutaQuandoYFor530EIdentificadorIgual1(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeTrabalhoAnelDeJadeBrutaY530Identificador1.png')
        y = 530
        identificador = 1
        esperado = 'Anel de jade bruta'
        recebido = self.imagem.reconheceNomeTrabalho(imagemTeste, y, identificador)
        assert recebido == esperado

    def testDeveRetornarStringErroLicencaDeProducaoNecessaria(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeErroLicencaDeProducaoNecessaria.png')
        esperado = 'Você precisa de uma licença defabricação para iniciar este pedido'
        recebido = self.imagem.reconheceTextoErro(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringWarspearQuandoXIgual26EYIgual1ELarguraIgual150(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeMenuInicial.png')
        x = 26
        y = 1
        largura = 150
        esperado = 'warspearonline'
        recebido = self.imagem.reconheceTextoMenu(imagemTeste, x, y, largura)
        assert esperado in recebido

    def testDeveRetornarTrueQuandoEhMenuInicial(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeMenuInicial.png')
        esperado = True
        recebido = self.imagem.verificaMenuReferenciaInicial(imagemTeste)
        assert esperado == recebido

    def testDeveRetornarStringSair(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeMenuPrincipal.png')
        esperado = 'sair'
        recebido = self.imagem.reconheceTextoSair(imagemTeste)
        assert esperado == recebido

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

    def testDeveRetornaTrueQuandoMenuPrincipal(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeMenuInicial.png')
        esperado = True
        recebido = self.imagem.verificaMenuReferenciaInicial(imagemTeste)
        assert esperado == recebido

    def testDeveRetornarStringWarspearOnline(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeMenuInicial.png')
        esperado = 'warspearonline'
        recebido = self.imagem.reconheceTextoMenu(imagemTeste, 26, 1, 150)
        assert esperado == recebido

    def testDeveRetornarStringNoticias(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeMenuNoticias.png')
        esperado = 'noticias'
        recebido = self.imagem.reconheceTextoMenu(imagemTeste, 216, 197, 270)
        assert esperado == recebido

    def testDeveRetornarStringPersonagens(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeMenuEscolhaPersonagem.png')
        esperado = 'personagens'
        recebido = self.imagem.reconheceTextoMenu(imagemTeste, 216, 197, 270)
        assert esperado == recebido

    def testDeveRetornarStringProducao(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeMenuProducao.png')
        esperado = 'producao'
        recebido = self.imagem.reconheceTextoMenu(imagemTeste, 216, 197, 270)
        assert esperado == recebido