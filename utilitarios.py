from unidecode import unidecode
from constantes import *

def textoEhIgual(texto1, texto2):
    return limpaRuidoTexto(texto1) == limpaRuidoTexto(texto2)

def texto1PertenceTexto2(texto1, texto2):
    return limpaRuidoTexto(texto1) in limpaRuidoTexto(texto2)

def tamanhoIgualZero(lista):
    return len(lista) == 0

def variavelExiste(variavel):
    return variavel != None

def limpaRuidoTexto(texto):
    return unidecode(texto).replace(' ','').replace('-','').lower()

def retiraDigitos(texto):
    listaDigitos = ['0','1','2','3','4','5','6','7','8','9']
    for digito in listaDigitos:
        texto = texto.replace(digito,'')
    return texto

def erroEncontrado(erro):
    return erro != 0

def existePixelPretoSuficiente(contadorPixelPreto):
    return contadorPixelPreto > 250 and contadorPixelPreto < 3000

def ehMenuInicial(menu):
    return menu == MENU_INICIAL

def ehMenuProduzir(menu):
    return menu == MENU_PRODUZIR

def ehErroOutraConexao(erro):
    return erro == CODIGO_ERRO_OUTRA_CONEXAO

def chaveConfirmacaoEhVerdadeira(dicionario):
    return dicionario[CHAVE_CONFIRMACAO]

def trabalhoEhParaProduzir(trabalhoProducao):
    return trabalhoProducao.pegaEstado() == CODIGO_PARA_PRODUZIR

def trabalhoEhProduzindo(trabalhoProducao):
    return trabalhoProducao.pegaEstado() == CODIGO_PRODUZINDO

def trabalhoEhProducaoRecursos(trabalhoProducao):
    listaProducaoRecurso = [
        'melhorarlicençacomum',
        'licençadeproduçãodoaprendiz',
        'grandecoleçãoderecursoscomuns',
        'grandecoleçãoderecursosavançados',
        'coletaemmassaderecursosavançados',
        'melhoriadaessênciacomum',
        'melhoriadasubstânciacomum',
        'melhoriadocatalizadorcomum',
        'melhoriadaessênciacomposta',
        'melhoriadasubtânciacomposta',
        'melhoriadocatalizadoramplificado',
        'criaresferadoaprendiz','produzindoavarinhademadeira','produzindocabeçadocajadodejade',
        'produzindocabeçadecajadodeônix','criaresferadoneófito','produzindoavarinhadeaço',
        'extraçãodelascas','manipulaçãodelascas','fazermódoaprendiz',
        'preparandolascasdequartzo','manipulaçãodeminériodecobre','fazermódoprincipiante',
        'adquirirtesouradoaprendiz','produzindofioresistente','fazendotecidodelinho',
        'fazendotecidodecetim','comprartesouradoprincipiante','produzindofiogrosso',
        'adquirirfacadoaprendiz','recebendoescamasdaserpente','concluindocouroresistente',
        'adquirirfacadoprincipiante','recebendoescamasdolagarto','curtindocourogrosso',
        'adquirirmarretãodoaprendiz','forjandoplacasdecobre','fazendoplacasdebronze',
        'adquirirmarretãodoprincipiante','forjandoplacasdeferro','fazendoanéisdeaço',
        'adquirirmoldedoaprendiz','extraçãodepepitasdecobre','recebendogemadassombras',
        'adquirirmoldedoprincipiante','extraçãodepepitasdeprata','recebendogemadaluz',
        'adquirirpinçadoaprendiz','extraçãodejadebruta','recebendoenergiainicial',
        'adquirirpinçasdoprincipiante','extraçãodeônixextraordinária','recebendoéterinicial',
        'adquirirfuradordoaprendiz','produzindotecidodelicado','extraçãodesubstânciainstável',
        'adquirirfuradordoprincipiante','produzindotecidodenso','extraçãodesubstânciaestável',
        'recebendofibradebronze','recebendoprata','recebendoinsígniadeestudante',
        'recebendofibradeplatina','recebendoâmbar','recebendodistintivodeaprendiz']
    for recurso in listaProducaoRecurso:
        if textoEhIgual(recurso, trabalhoProducao.pegaNomeProducao()):
            return True
    return False

def trabalhoEhColecaoRecursosAvancados(dicionarioTrabalho):
    return textoEhIgual(dicionarioTrabalho.pegaNome(), 'grandecoleçãoderecursosavançados') or textoEhIgual(dicionarioTrabalho.pegaNome(), 'coletaemmassaderecursosavançados')

def trabalhoEhColecaoRecursosComuns(trabalhoProducao):
    return textoEhIgual(trabalhoProducao.pegaNome(), 'grandecoleçãoderecursoscomuns')

def trabalhoEhMelhoriaCatalisadorComposto(trabalhoProducao):
    return textoEhIgual(trabalhoProducao.pegaNome(), 'melhoriadocatalizadoramplificado')

def trabalhoEhMelhoriaCatalisadorComum(trabalhoProducao):
    return textoEhIgual(trabalhoProducao.pegaNome(), 'melhoriadocatalizadorcomum')

def trabalhoEhMelhoriaSubstanciaComposta(trabalhoProducao):
    return textoEhIgual(trabalhoProducao.pegaNome(), 'melhoriadasubstânciacomposta')

def trabalhoEhMelhoriaSubstanciaComum(trabalhoProducao):
    return textoEhIgual(trabalhoProducao.pegaNome(), 'melhoriadasubstânciacomum')

def trabalhoEhMelhoriaEssenciaComposta(trabalhoProducao):
    return textoEhIgual(trabalhoProducao.pegaNome(), 'melhoriadaessênciacomposta')

def trabalhoEhProducaoLicenca(trabalhoProducao):
    return textoEhIgual(trabalhoProducao.pegaNome(),'melhorarlicençacomum') or textoEhIgual(trabalhoProducao.pegaNome(),'licençadeproduçãodoaprendiz')

def trabalhoEhMelhoriaEssenciaComum(dicionarioTrabalho):
    return textoEhIgual(dicionarioTrabalho.pegaNome(), 'melhoriadaessênciacomum')

def retornaListaDicionarioProfissaoRecursos(nivelProduzTrabalhoComum):
    listaDicionarioProfissaoRecursos = []
    if nivelProduzTrabalhoComum == 1:
        listaDicionarioProfissaoRecursos=[
                {'braceletes':['Fibra de Bronze','Prata','Pin de Estudante']},
                {'capotes':['Furador do aprendiz','Tecido delicado','Substância instável']},
                {'amuletos':['Pinça do aprendiz','Jade bruta','Energia inicial']},
                {'aneis':['Molde do aprendiz','Pepita de cobre','Pedra de sombras']},
                {'armadurapesada':['Marretão do aprendiz','Placas de cobre','Anéis de bronze']},
                {'armaduraleve':['Faca do aprendiz','Escamas da serpente','Couro resistente']},
                {'armaduradetecido':['Tesoura do aprendiz','Fio grosseiro','Tecido de linho']},
                {'armacorpoacorpo':['Lascas','Minério de cobre','Mó do aprendiz']},
                {'armadelongoalcance':['Esfera do aprendiz','Varinha de madeira','Cabeça do cajado de jade']}]
    elif nivelProduzTrabalhoComum == 8:    
        listaDicionarioProfissaoRecursos=[
                {'braceletes':['Fibra de Platina','Âmbarito','Pino do Aprendiz']},
                {'capotes':['Furador do principiante','Tecido espesso','Substância estável']},
                {'amuletos':['Pinça do principiante','Ônix extraordinária','Éter inicial']},
                {'aneis':['Molde do principiante','Pepita de prata','Pedra da luz']},
                {'armadurapesada':['Marretão do principiante','Placas de ferro','Anéis de aço']},
                {'armaduraleve':['Faca do principiante','Escamas do lagarto','Couro grosso']},
                {'armaduradetecido':['Tesoura do principiante','Fio grosso','Tecido de cetim']},
                {'armacorpoacorpo':['Lascas de quartzo','Minério de ferro','Mó do principiante']},
                {'armadelongoalcance':['Esfera do neófito','Varinha de aço','Cabeça do cajado de ônix']}]
    return listaDicionarioProfissaoRecursos

def retornaChaveTipoRecurso(trabalhoEstoque):
    listaDicionarioProfissaoRecursos = retornaListaDicionarioProfissaoRecursos(trabalhoEstoque.pegaNivel())
    chaveProfissao = limpaRuidoTexto(trabalhoEstoque.pegaProfissao())
    for dicionarioProfissaoRecursos in listaDicionarioProfissaoRecursos:
        if chaveProfissao in dicionarioProfissaoRecursos:
            for x in range(len(dicionarioProfissaoRecursos[chaveProfissao])):
                if textoEhIgual(dicionarioProfissaoRecursos[chaveProfissao][x], trabalhoEstoque.pegaNome()):
                    if x == 0 and trabalhoEstoque.pegaNivel() == 1:
                        return CHAVE_RCP
                    elif x == 0 and trabalhoEstoque.pegaNivel() == 8:
                        return CHAVE_RAP
                    elif x == 1 and trabalhoEstoque.pegaNivel() == 1:
                        return CHAVE_RCS
                    elif x == 1 and trabalhoEstoque.pegaNivel() == 8:
                        return CHAVE_RAS
                    elif x == 2 and trabalhoEstoque.pegaNivel() == 1:
                        return CHAVE_RCT
                    elif x == 2 and trabalhoEstoque.pegaNivel() == 8:
                        return CHAVE_RAT
                    break
    return None

def existeEspacoProducao(dicionarioPersonagemAtributos):
    espacoProducao = dicionarioPersonagemAtributos[CHAVE_PERSONAGEM_EM_USO][CHAVE_ESPACO_PRODUCAO]
    for trabalhoProducao in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS_PRODUCAO]:
        if trabalhoProducao[CHAVE_ESTADO] == CODIGO_PRODUZINDO:
            espacoProducao -= 1
            if espacoProducao <= 0:
                print(f'{espacoProducao} espaços de produção - FALSO.')
                return False
    print(f'{espacoProducao} espaços de produção - VERDADEIRO.')
    return True

def retornaListaTrabalhosParaProduzirProduzindo(dicionarioPersonagemAtributos):
    listaTrabalhosParaProduzirProduzindo = []
    for trabalhoProducao in dicionarioPersonagemAtributos[CHAVE_LISTA_TRABALHOS_PRODUCAO]:
        if trabalhoEhParaProduzir(trabalhoProducao) or trabalhoEhProduzindo(trabalhoProducao):
            listaTrabalhosParaProduzirProduzindo.append(trabalhoProducao)
    return listaTrabalhosParaProduzirProduzindo