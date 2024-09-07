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

    def testDeveRetornarStringWarspearOnline(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeMenuInicial.png')
        esperado = 'warspearonline'
        recebido = self.imagem.reconheceTextoMenu(imagemTeste, 26, 1, 150)
        assert esperado == recebido
    
    def testDeveRetornaTrueQuandoMenuPrincipal(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeMenuInicial.png')
        esperado = True
        recebido = self.imagem.verificaMenuReferenciaInicial(imagemTeste)
        assert esperado == recebido

    def testDeveRetornarStringMenuNoticias(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeMenuNoticias.png')
        esperado = 'noticias'
        recebido = self.imagem.reconheceTextoMenu(imagemTeste, 216, 197, 270)
        assert esperado == recebido

    def testDeveRetornarStringPersonagens(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeMenuEscolhaPersonagem.png')
        esperado = 'personagens'
        recebido = self.imagem.reconheceTextoMenu(imagemTeste, 216, 197, 270)
        assert esperado == recebido

    def testDeveRetornarStringArtesanato(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeMenuTrabalhoProducao.png')
        esperado = 'artesanato'
        recebido = self.imagem.reconheceTextoMenu(imagemTeste, 216, 197, 270)
        assert esperado == recebido

    def testDeveRetornarStringPedidosAtivos(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeMenuTrabalhoProducao.png')
        esperado = 'pedidosativos'
        recebido = self.imagem.reconheceTextoMenu(imagemTeste, 266, 242, 150)
        assert esperado == recebido

    def testDeveRetornarStringProfissoes(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeMenuProfissoes.png')
        esperado = 'profissoes'
        recebido = self.imagem.reconheceTextoMenu(imagemTeste, 266, 242, 150)
        assert esperado == recebido

    def testDeveRetornarStringVoltar(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeMenuTrabalhosDisponiveis.png')
        esperado = 'voltar'
        recebido = self.imagem.reconheceTextoMenu(imagemTeste, 191, 612, 100)
        assert esperado == recebido

    def testDeveRetornarStringFechar(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeMenuProfissoes.png')
        esperado = 'fechar'
        recebido = self.imagem.reconheceTextoMenu(imagemTeste, 191, 612, 100)
        assert esperado == recebido

    def testDeveRetornarStringOfertaDiaria(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeMenuOfertaDiaria.png')
        esperado = 'ofertadiaria'
        recebido = self.imagem.reconheceTextoMenu(imagemTeste, 266, 269, 150)
        assert esperado == recebido

    def testDeveRetornarStringRecompensasDiarias(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeMenuRecompensasDiarias.png')
        esperado = 'recompensasdiarias'
        recebido = self.imagem.reconheceTextoMenu(imagemTeste, 180, 40, 300)
        assert esperado == recebido

    def testDeveRetornarStringLojaMilagrosa(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeMenuLojaMilagrosa.png')
        esperado = 'lojamilagrosa'
        recebido = self.imagem.reconheceTextoMenu(imagemTeste, 181, 75, 150)
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
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeEstadoTrabalhoParaProduzir.png')
        esperado = 0
        recebido = self.imagem.reconheceEstadoTrabalho(imagemTeste)
        assert esperado == recebido

    def testDeveRetornarCodigoProduzindoQuandoExistirPeloMenosUmTrabalhoSendoProduzido(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeEstadoTrabalhoProduzindo.png')
        esperado = 1
        recebido = self.imagem.reconheceEstadoTrabalho(imagemTeste)
        assert esperado == recebido

    def testDeveRetornarCodigoConcluidoQuandoExistirUmTrabalhoConcluido(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeEstadoTrabalhoConcluido.png')
        esperado = 2
        recebido = self.imagem.reconheceEstadoTrabalho(imagemTeste)
        assert esperado == recebido
    
    def testDeveRetornarNomeTrabalhoConcluidoReconhecido(self):
        imagemTeste  = self.imagem.abreImagem('tests/imagemTeste/testeEstadoTrabalhoConcluido.png')
        esperado = 'Criar esfera do aprendiz'
        recebido = self.imagem.reconheceNomeTrabalhoFrameProducao(imagemTeste)
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

    def testDeveRetornarNomePersonagemAxeQuandoPosicaoEhUm(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeNomePersonagemAxePosicaoUm.png')
        quandoEh = 1
        esperado = 'provisorioatecair'
        recebido = self.imagem.reconheceTextoNomePersonagem(imagemTeste, quandoEh)
        assert esperado == recebido

    def testDeveRetornarNomePersonagemAxeQuandoPosicaoEhZero(self):
        quandoEh = 0
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeNomePersonagemAxePosicaoZero.png')
        esperado = 'provisorioatecair'
        recebido = self.imagem.reconheceTextoNomePersonagem(imagemTeste, quandoEh)
        assert esperado == recebido

    def testDeveRetornarStringErroFalhaAoConectar(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeErroFalhaAoConectarAoServidor.png')
        esperado = 'Falha ao se conectar ao servidor'
        recebido = self.imagem.reconheceTextoErro(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringErroJogoEmManutencao(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeErroJogoEmManutencao.png')
        esperado = 'Estamos fazendo de tudo paraconcluíla o mais rápido possível'
        recebido = self.imagem.reconheceTextoErro(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringErroErroVersaoJogoDesatualizada(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeErroVersaoJogoDesatualizada.png')
        esperado = 'Versão do jogo desatualizada'
        recebido = self.imagem.reconheceTextoErro(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringErroSairDoJogo(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeErroSairDoJogo.png')
        esperado = 'Desgeja sair do Warspear Online'
        recebido = self.imagem.reconheceTextoErro(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringErroTrabalhoNaoConcluido(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeErroTrabalhoNaoConcluido.png')
        esperado = 'Tem certeza de que deseja concluir aprodução'
        recebido = self.imagem.reconheceTextoErro(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringErroBolsaCheia(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeErroBolsaCheia.png')
        esperado = 'Bolsa cheia'
        recebido = self.imagem.reconheceTextoErro(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringErroUsuarioOuSenhaInvalida(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeErroUsuarioOuSenhaInvalida.png')
        esperado = 'Nome de usuário ou senha inválida'
        recebido = self.imagem.reconheceTextoErro(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringErroMoedasMilagrosasInsuficientes(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeErroMoedasMilagrosasInsuficientes.png')
        esperado = 'Você precisa de mais'
        recebido = self.imagem.reconheceTextoErro(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringErroConectando(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeErroConectando.png')
        esperado = 'Conectando'
        recebido = self.imagem.reconheceTextoErro(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringErroSelecionarItemNecessario(self):
        imagemTeste = self.imagem.abreImagem('tests/imagemTeste/testeErroSelecionarItemNecessario.png')
        esperado = 'Selecione um item para iniciar umpedido de artesanato'
        recebido = self.imagem.reconheceTextoErro(imagemTeste)
        assert esperado in recebido