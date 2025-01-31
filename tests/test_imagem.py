from imagem import ManipulaImagem
from constantes import CHAVE_LICENCA_APRENDIZ, CHAVE_LICENCA_NOVATO, CHAVE_LICENCA_INICIANTE, CHAVE_LICENCA_MESTRE

class TestImagem:
    __imagem = ManipulaImagem()

    def testDeveRetornarStringLicencaDeNovato(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeLicencaDeNovato.png')
        esperado = CHAVE_LICENCA_NOVATO
        recebido = self.__imagem.reconheceTextoLicenca(imagemTeste)
        assert recebido == esperado

    def testDeveRetornarStringLicencaDeIniciante(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeLicencaDeIniciante.png')
        esperado = CHAVE_LICENCA_INICIANTE
        recebido = self.__imagem.reconheceTextoLicenca(imagemTeste)
        assert recebido == esperado

    def testDeveRetornarStringLicencaDeMestre(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeLicencaDeMestre.png')
        esperado = CHAVE_LICENCA_MESTRE
        recebido = self.__imagem.reconheceTextoLicenca(imagemTeste)
        assert recebido == esperado

    def testDeveRetornarStringLicencaDeAprendiz(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeLicencaDeAprendiz.png')
        esperado = CHAVE_LICENCA_APRENDIZ
        recebido = self.__imagem.reconheceTextoLicenca(imagemTeste)
        assert recebido == esperado

    def testDeveRetornarStringLincencaNenhumItem(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeNenhumaLicencaDeProducao.png')
        esperado = 'Nenhum item'
        recebido = self.__imagem.reconheceTextoLicenca(imagemTeste)
        assert esperado == recebido

    def testDeveRetornarStringAnelDeJadeBrutaQuandoPosicaoForZero(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeTrabalhoAnelDeJadeBrutaPosicaoZero.png')
        posicao = 0
        esperado = 'Anel de jade bruta'
        recebido = self.__imagem.reconheceNomeConfirmacaoTrabalhoProducao(imagemTeste, posicao)
        assert recebido == esperado

    def testDeveRetornarStringAnelDeJadeBrutaQuandoPosicaoForUm(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeTrabalhoAnelDeJadeBrutaPosicaoUm.png')
        posicao = 1
        esperado = 'Anel de jade bruta'
        recebido = self.__imagem.reconheceNomeConfirmacaoTrabalhoProducao(imagemTeste, posicao)
        assert recebido == esperado

    def testDeveRetornarStringAnelDeJadeBrutaQuandoYFor530EIdentificadorIgual1(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeTrabalhoAnelDeJadeBrutaY530Identificador1.png')
        y = 530
        identificador = 1
        esperado = 'Anel de jade bruta'
        recebido = self.__imagem.reconheceNomeTrabalho(imagemTeste, y, identificador)
        assert recebido == esperado

    def testDeveRetornarStringErroLicencaDeProducaoNecessaria(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeErroLicencaDeProducaoNecessaria.png')
        esperado = 'Você precisa de uma licença defabricação para iniciar este pedido'
        recebido = self.__imagem.reconheceTextoErro(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringWarspearOnline(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuInicial.png')
        esperado = 'warspearonline'
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste, 26, 1, 150)
        assert esperado == recebido
    
    def testDeveRetornaTrueQuandoMenuPrincipal(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuInicial.png')
        esperado = True
        recebido = self.__imagem.verificaMenuReferenciaInicial(imagemTeste)
        assert esperado == recebido

    def testDeveRetornarStringMenuNoticias(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuNoticias.png')
        esperado = 'noticias'
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste, 216, 197, 270)
        assert esperado == recebido

    def testDeveRetornarStringPersonagens(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuEscolhaPersonagem.png')
        esperado = 'personagens'
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste, 216, 197, 270)
        assert esperado == recebido

    def testDeveRetornarStringArtesanato(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuTrabalhoProducao.png')
        esperado = 'artesanato'
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste, 216, 197, 270)
        assert esperado == recebido

    def testDeveRetornarStringPedidosAtivos(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuTrabalhoProducao.png')
        esperado = 'pedidosativos'
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste, 266, 242, 150)
        assert esperado == recebido

    def testDeveRetornarStringProfissoes(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuProfissoes.png')
        esperado = 'profissoes'
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste, 266, 242, 150)
        assert esperado == recebido

    def testDeveRetornarStringVoltar(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuTrabalhosDisponiveis.png')
        esperado = 'voltar'
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste, 191, 612, 100)
        assert esperado == recebido

    def testDeveRetornarStringFechar(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuProfissoes.png')
        esperado = 'fechar'
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste, 191, 612, 100)
        assert esperado == recebido

    def testDeveRetornarStringOfertaDiaria(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuOfertaDiaria.png')
        esperado = 'ofertadiaria'
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste, 266, 269, 150)
        assert esperado == recebido

    def testDeveRetornarStringRecompensasDiarias(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuRecompensasDiarias.png')
        esperado = 'recompensasdiarias'
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste, 180, 40, 300)
        assert esperado == recebido

    def testDeveRetornarStringLojaMilagrosa(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuLojaMilagrosa.png')
        esperado = 'lojamilagrosa'
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste, 181, 75, 150)
        assert esperado == recebido

    def testDeveRetornarStringSair(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuPrincipal.png')
        esperado = 'sair'
        recebido = self.__imagem.reconheceTextoSair(imagemTeste)
        assert esperado == recebido

    def testDeveRetornarTrueQuandoExistePixelCorreioRecebido(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuInicialComCorrespondencia.png')
        esperado = True
        recebido = self.__imagem.verificaPixelCorrespondencia(imagemTeste)
        assert esperado == recebido

    def testDeveRetornarFalseQuandoNaoExistirPixelCorreioRecebido(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuInicial.png')
        esperado = False
        recebido = self.__imagem.verificaPixelCorrespondencia(imagemTeste)
        assert esperado == recebido


    def testDeveRetornarTrueQuandoExisteCorrespondencia(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuCorrespondenciaComCorrespondencia.png')
        esperado = True
        recebido = self.__imagem.quantidadePixelBrancoEhMaiorQueZero(imagemTeste)
        assert esperado == recebido

    def testDeveRetornarFalseQuandoNaoExisteCorrespondencia(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuCorrespondenciaSemCorrespondencia.png')
        esperado = False
        recebido = self.__imagem.quantidadePixelBrancoEhMaiorQueZero(imagemTeste)
        assert esperado == recebido

    def testDeveRetornarTextoCorrespondenciaQuandoLoteVendido(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeTrabalhoProducaoVendido.png')
        esperado = 'Item vendido'
        recebido = self.__imagem.reconheceTextoCorrespondencia(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarCodigoParaProduzirQuandoNaoExistirNemUmTrabalhoSendoProduzido(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeEstadoTrabalhoParaProduzir.png')
        esperado = 0
        recebido = self.__imagem.reconheceEstadoTrabalho(imagemTeste)
        assert esperado == recebido

    def testDeveRetornarCodigoProduzindoQuandoExistirPeloMenosUmTrabalhoSendoProduzido(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeEstadoTrabalhoProduzindo.png')
        esperado = 1
        recebido = self.__imagem.reconheceEstadoTrabalho(imagemTeste)
        assert esperado == recebido

    def testDeveRetornarCodigoConcluidoQuandoExistirUmTrabalhoConcluido(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeEstadoTrabalhoConcluido.png')
        esperado = 2
        recebido = self.__imagem.reconheceEstadoTrabalho(imagemTeste)
        assert esperado == recebido
    
    def testDeveRetornarNomeTrabalhoConcluidoReconhecido(self):
        imagemTeste  = self.__imagem.abreImagem('tests/imagemTeste/testeEstadoTrabalhoConcluido.png')
        esperado = 'Criar esfera do aprendiz'
        recebido = self.__imagem.reconheceNomeTrabalhoFrameProducao(imagemTeste)
        assert esperado == recebido

    def testDeveRetornarNomePersonagemPallakuraQuandoPosicaoEhUm(self):
        quandoEh = 1
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeNomePersonagemPallakuraPosicaoUm.png')
        esperado = 'pallakura'
        recebido = self.__imagem.reconheceTextoNomePersonagem(imagemTeste, quandoEh)
        assert esperado == recebido

    def testDeveRetornarNomePersonagemPallakuraQuandoPosicaoEhZero(self):
        quandoEh = 0
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeNomePersonagemPallakuraPosicaoZero.png')
        esperado = 'pallakura'
        recebido = self.__imagem.reconheceTextoNomePersonagem(imagemTeste, quandoEh)
        assert esperado == recebido

    def testDeveRetornarNomePersonagemAxeQuandoPosicaoEhUm(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeNomePersonagemAxePosicaoUm.png')
        quandoEh = 1
        esperado = 'provisorioatecair'
        recebido = self.__imagem.reconheceTextoNomePersonagem(imagemTeste, quandoEh)
        assert esperado == recebido

    def testDeveRetornarNomePersonagemAxeQuandoPosicaoEhZero(self):
        quandoEh = 0
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeNomePersonagemAxePosicaoZero.png')
        esperado = 'provisorioatecair'
        recebido = self.__imagem.reconheceTextoNomePersonagem(imagemTeste, quandoEh)
        assert esperado == recebido

    def testDeveRetornarStringErroFalhaAoConectar(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeErroFalhaAoConectarAoServidor.png')
        esperado = 'Falha ao se conectar ao servidor'
        recebido = self.__imagem.reconheceTextoErro(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringErroJogoEmManutencao(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeErroJogoEmManutencao.png')
        esperado = 'Estamos fazendo de tudo paraconcluíla o mais rápido possível'
        recebido = self.__imagem.reconheceTextoErro(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringErroErroVersaoJogoDesatualizada(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeErroVersaoJogoDesatualizada.png')
        esperado = 'Versão do jogo desatualizada'
        recebido = self.__imagem.reconheceTextoErro(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringErroSairDoJogo(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeErroSairDoJogo.png')
        esperado = 'Desgeja sair do Warspear Online'
        recebido = self.__imagem.reconheceTextoErro(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringErroTrabalhoNaoConcluido(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeErroTrabalhoNaoConcluido.png')
        esperado = 'Tem certeza de que deseja concluir aprodução'
        recebido = self.__imagem.reconheceTextoErro(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringErroBolsaCheia(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeErroBolsaCheia.png')
        esperado = 'Bolsa cheia'
        recebido = self.__imagem.reconheceTextoErro(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringErroUsuarioOuSenhaInvalida(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeErroUsuarioOuSenhaInvalida.png')
        esperado = 'Nome de usuário ou senha inválida'
        recebido = self.__imagem.reconheceTextoErro(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringErroMoedasMilagrosasInsuficientes(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeErroMoedasMilagrosasInsuficientes.png')
        esperado = 'Você precisa de mais'
        recebido = self.__imagem.reconheceTextoErro(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringErroConectando(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeErroConectando.png')
        esperado = 'Conectando'
        recebido = self.__imagem.reconheceTextoErro(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringErroSelecionarItemNecessario(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeErroSelecionarItemNecessario.png')
        esperado = 'Selecione um item para iniciar umpedido de artesanato'
        recebido = self.__imagem.reconheceTextoErro(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringSapatosAltosDaLuzImQuandoTrabalhoProducaoEhConcluido(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeReconheceNomeTrabalhoProducaoConcluido.png')
        esperado = 'Sapatos altos da Luz Impura'
        recebido = self.__imagem.reconheceNomeTrabalhoFrameProducao(imagemTeste)
        assert recebido in esperado

    def testDeveRetornarPosicao414_243QuandoMetodoRetornaReferenciaEhChamado(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuRecompensasDiarias.png')
        esperado = [414.0, 243.5]
        recebido = self.__imagem.retornaReferencia(imagemTeste)
        assert esperado == recebido

    def testDeveRetornarPosicaoValidaQuandoMetodoRetornaReferenciaEhChamado(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuRecompensasDiarias2.png')
        esperado = [414.5, 212.0]
        recebido = self.__imagem.retornaReferencia(imagemTeste)
        assert esperado == recebido