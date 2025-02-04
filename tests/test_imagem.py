from imagem import ManipulaImagem
from constantes import CHAVE_LICENCA_APRENDIZ, CHAVE_LICENCA_NOVATO, CHAVE_LICENCA_INICIANTE, CHAVE_LICENCA_MESTRE, STRING_VERSAO_JOGO_DESATUALIZADA, STRING_FALHA_CONECTAR_SERVIDOR, STRING_JOGO_ESTA_MANUTENCAO, STRING_DESEJA_SAIR_WARSPEAR_ONLINE, STRING_TEM_CERTEZA_DESEJA_CONCLUIR_PRODUCAO, STRING_BOLSA_CHEIA, STRING_USUARIO_SENHA_INVALIDA, STRING_VOCE_PRECISA_MAIS, STRING_CONECTANDO, STRING_SELECIONE_ITEM_INICIAR_PEDIDO, STRING_PRECISA_LICENCA_INICIAR_PEDIDO
from utilitarios import limpaRuidoTexto

class TestImagem:
    __imagem = ManipulaImagem()

    def testDeveRetornarStringLicencaDeNovato(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeLicencaDeNovato.png')
        esperado = CHAVE_LICENCA_NOVATO
        recebido = self.__imagem.reconheceLicenca(imagemTeste)
        assert recebido == esperado

    def testDeveRetornarStringLicencaDeIniciante(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeLicencaDeIniciante.png')
        esperado = CHAVE_LICENCA_INICIANTE
        recebido = self.__imagem.reconheceLicenca(imagemTeste)
        assert recebido == esperado

    def testDeveRetornarStringLicencaDeMestre(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeLicencaDeMestre.png')
        esperado = CHAVE_LICENCA_MESTRE
        recebido = self.__imagem.reconheceLicenca(imagemTeste)
        assert recebido == esperado

    def testDeveRetornarStringLicencaDeAprendiz(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeLicencaDeAprendiz.png')
        esperado = CHAVE_LICENCA_APRENDIZ
        recebido = self.__imagem.reconheceLicenca(imagemTeste)
        assert recebido == esperado

    def testDeveRetornarStringLincencaNenhumItem(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeNenhumaLicencaDeProducao.png')
        esperado = 'Nenhum item'
        recebido = self.__imagem.reconheceLicenca(imagemTeste)
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
    
    def testDeveRetornaTrueQuandoMenuPrincipal(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuInicial.png')
        esperado = True
        recebido = self.__imagem.verificaMenuReferenciaInicial(imagemTeste)
        assert esperado == recebido

    def testDeveRetornarStringMenuNoticias(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuNoticias.png')
        esperado = 'noticias'
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringPersonagens(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuEscolhaPersonagem.png')
        esperado = 'personagens'
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringArtesanato(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuTrabalhoProducao.png')
        esperado = 'artesanato'
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringPedidosAtivos(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuTrabalhoProducao.png')
        esperado = 'pedidosativos'
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringProfissoes(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuProfissoes.png')
        esperado = 'profissoes'
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringVoltar(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuTrabalhosDisponiveis.png')
        esperado = 'voltar'
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringFechar(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuProfissoes.png')
        esperado = 'fechar'
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringOfertaDiaria(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuOfertaDiaria.png')
        esperado = 'ofertadiaria'
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringRecompensasDiarias(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuRecompensasDiarias.png')
        esperado = 'recompensasdiarias'
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringLojaMilagrosa(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeMenuLojaMilagrosa.png')
        esperado = 'milagrosa'
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste)
        assert esperado in recebido

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
        esperado = STRING_FALHA_CONECTAR_SERVIDOR
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste)
        assert limpaRuidoTexto(esperado) in recebido

    def testDeveRetornarStringErroJogoEmManutencao(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeErroJogoEmManutencao.png')
        esperado = STRING_JOGO_ESTA_MANUTENCAO
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste)
        assert esperado in recebido

    def testDeveRetornarStringErroErroVersaoJogoDesatualizada(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeErroVersaoJogoDesatualizada.png')
        esperado = STRING_VERSAO_JOGO_DESATUALIZADA
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste)
        assert limpaRuidoTexto(esperado) in recebido

    def testDeveRetornarStringErroSairDoJogo(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeErroSairDoJogo.png')
        esperado = STRING_DESEJA_SAIR_WARSPEAR_ONLINE
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste)
        assert limpaRuidoTexto(esperado) in recebido

    def testDeveRetornarStringErroTrabalhoNaoConcluido(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeErroTrabalhoNaoConcluido.png')
        esperado = STRING_TEM_CERTEZA_DESEJA_CONCLUIR_PRODUCAO
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste)
        assert limpaRuidoTexto(esperado) in recebido

    def testDeveRetornarStringErroBolsaCheia(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeErroBolsaCheia.png')
        esperado = STRING_BOLSA_CHEIA
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste)
        assert limpaRuidoTexto(esperado) in recebido

    def testDeveRetornarStringErroUsuarioOuSenhaInvalida(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeErroUsuarioOuSenhaInvalida.png')
        esperado = STRING_USUARIO_SENHA_INVALIDA
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste)
        assert limpaRuidoTexto(esperado) in recebido

    def testDeveRetornarStringErroMoedasMilagrosasInsuficientes(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeErroMoedasMilagrosasInsuficientes.png')
        esperado = STRING_VOCE_PRECISA_MAIS
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste)
        assert limpaRuidoTexto(esperado) in recebido

    def testDeveRetornarStringErroConectando(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeErroConectando.png')
        esperado = STRING_CONECTANDO
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste)
        assert limpaRuidoTexto(esperado) in recebido

    def testDeveRetornarStringErroSelecionarItemNecessario(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeErroSelecionarItemNecessario.png')
        esperado = STRING_SELECIONE_ITEM_INICIAR_PEDIDO
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste)
        assert limpaRuidoTexto(esperado) in recebido

    def testDeveRetornarStringErroLicencaDeProducaoNecessaria(self):
        imagemTeste = self.__imagem.abreImagem('tests/imagemTeste/testeErroLicencaDeProducaoNecessaria.png')
        esperado = STRING_PRECISA_LICENCA_INICIAR_PEDIDO
        recebido = self.__imagem.reconheceTextoMenu(imagemTeste)
        assert limpaRuidoTexto(esperado) in recebido

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