import os
import re

import corretor as cor
import settings
from sintagma import Sintagma


# def tradutor(tag, i, originalLines):
def tradutor(tag):
    if not settings.tabela:
        settings.tabela = {
            'S': 'S',  # Marcador de Sentença

            # # bracketing
            # '(': '-LRB-',
            # ')': '-RRB-',
            # '[': '-LSB-',
            # ']': '-RSB-',
            # '{': '-LCB-',
            # '}': '-RCB-',

            # Formas Oracionais
            # 3.1: A oração finita (fcl) contém um verbo de forma finita. A oração não finita (icl) contém um verbo de forma não finita, como particípio passado, infinitivo e gerúndio. Finalmente, na oração averbal, o verbo não está presente, mas normalmente estas orações são encabeçadas por uma conjunção subordinativa que indica a natureza oracional do período.
            'fcl': 'VP',  # Forma Oracional Finita -> usa verbos não no infinitivo -> sintagma verbal
            # Relativamente às orações não finitas e em particular àquelas que têm por predicador um verbo de forma participial, nem sempre a presença desta forma verbal implica a formação de oração.
            'icl': 'VP',  # Forma Oracional não finita
            'acl': 'ADVP',  # Forma Oracional averbal TODO

            # Sintagmas
            'np': 'NP',  # Sintagma nominais
            'adjp': 'ADJP',  # Sintagma adjectivais
            'advp': 'ADVP',  # Sintagma adverbiais
            'vp': 'VP',  # Sintagma verbais
            'pp': 'PP',  # Sintagma preposicionais
            # Sintagma evidenciador coordenação
            'cu': settings.tagCoord,
            # Sintagma sequências discursivas - começo de sentença
            'sq': 'S',

            # Classes de palavras
            'n': 'NN',  # substantivos
            'n-adj': 'NN',  # substantivos/adjectivos - pesquisar mostrou que são todos substantivos
            'adj': 'JJ',  # adjectivos
            'prop': 'NNP',  # nomes próprios
            'adv': 'RB',  # advérbios
            'num': 'CD',  # numeral
            'v-fin': 'VBP',  # verbos finitos
            'v-ger': 'VBG',  # verbos gerúndios
            'v-pcp': 'VBN',  # verbos particípios
            'v-inf': 'VB',  # verbos infinitivos
            'art': 'DT',  # artigos
            # pronomes determinativos - por PTB (POS guide), pronomes determinantes são DT
            'pron-det': 'DT',
            # pronomes independentes - pronomes relativos
            'pron-indp': 'PRP',
            # pronomes pessoais
            'pron-pers': 'PRP',
            'prp': 'IN',  # preposições
            'intj': 'UH',  # interjeições
            'conj-s': 'IN',  # conjunções subordinativa
            'conj-c': settings.tagConjCoord,  # conjunções coordenativa
            # 'conj-c': settings.tagFlat,  # conjunções coordenativa
            'ec': settings.tagHifem,  # prefixos - ativei o modo Elza e let it go
        }

    if tag == '':
        return tag

    # remove o travessão da tag
    # tag.replace('-', '')
    return settings.tabela[tag]


def tradutorFuncao(func_tag, form_tag):
    # form_tag = tradutor(form_tag)
    if not settings.tabelaFuncoes:
        settings.tabelaFuncoes = {
            # Enunciados - Todos Enunciados são considerados inicios de Sentenças -> S
            'UTT': 'S',  # enunciados -
            'STA': 'S',  # declarativo -
            'QUE': 'S',  # interrogativo
            'CMD': 'S',  # imperativo -
            'EXC': 'S',  # exclamativo -

            # Orações
            'SUBJ': tradutor(form_tag),
            # sujeito - marcador de sentenças. A tag de forma costuma dizer o tipo de sintagma.
            # obj. directo - similar a sujeito, a tag forma informa o tipo de sintagma.
            'ACC': tradutor(form_tag) if form_tag != settings.tagCu or form_tag != 'acl' else 'NP',
            # part. apassivante - ok, inglês não tem nenhuma particula de voz passiva. é obj+to be + verbo participio +
            'ACC-PASS': 'NP',
            # compl. seguindo o proprio BOSQUE, é um NP
            'DAT': 'NP',  # obj. ind. pronominal - sempre NP.
            'PIV': 'PP',  # obj. ind. preposicional
            # agente passiva - por def (https://www.normaculta.com.br/agente-da-passiva/), "é um termo preposicionado).
            # Logo, PP
            'PASS': 'PP',
            # adj. adverbiais do sujeito - adjunto adverbial sem ser PIV ou ADVL. Por definição de projeto (esse valor
            # só é requerido quando form é x, e na unica ocorrência, ele equivale a 'pp'
            'SA': 'PP',
            # adj. adverbiais do objecto - formTag informa o sintagma
            'OA': tradutor(form_tag),
            # adj. adverbiais  - a form_tag informa o sintagma. em caso de ACL, é advp.
            'ADVL': 'ADVP' if form_tag == 'acl' else tradutor(form_tag),
            # predicativos do sujeito - O Predicativo do Sujeito, representado pela etiqueta SC estabelece uma relação de
            # predicação com o sujeito por meio de verbos copulativos ou verbos que, não sendo copulativos, exibem um
            # comportamento semelhante em termos semânticos (Biblia). Logo, VP
            'SC': 'VP',
            # predicativos do objecto - a tag form costuma dizer o sintagma.
            'OC': 'NP' if form_tag == 'acl' else tradutor(form_tag),
            # predicativos verbo-nominais - podem ser icl, np, pp, adjp, cu, adj, pron-det. icl maioria.
            'PRED': 'VP',
            'VOC': 'NP',  # vocativo - todo vocativo do bosque é um NP
            'APP': 'NP',  # apostos normal - pode ser fcl, np, adjp, cu, advp. np maioria
            'N<PRED': 'NP',
            # apostos epit. predicativo - pode ser fcl, np, pp, cu. É bem distribuido, mas a priori, a maior parte é NP
            '>S': 'JJ',  # apostos da oração - se for >S, é sempre adj.
            'S<': 'NP',  # apostos da oração - se for S<, pode ser fcl ou np. Mais seguro ir no np
            'N<ARGS': 'PP',  # compl. nominais do sujeito
            'N<ARGO': 'PP',  # compl. nominais do objecto
            'N<ARG': 'PP',  # compl. nominais outros
            'P': 'VB',  # predicador - maior parte disparado é vp
            'FOC': 'RB',  # foco - maioria é advp
            # tópico - poucos casos. todos envolvem ou np, ou pronome.
            'TOP': 'NP',
            'X': settings.tagX,

            # Palavra
            'H': tradutor(form_tag),  # núcleo
            # 'MV': 'VBP',  # verbo principal - maioria v-fin
            # 'PMV': 'VBP',  # verbo principal - maioria são verbos finitos. Inflexões verbais do portugues muito diferentes da do inglês
            # verbo auxiliar (pra que por duas tags pramsm função? tnc). Maioria v-fin
            'AUX': 'VBP',
            # Por 11.1.1. Particípios com argumentos coordenados, com partilha de auxiliar, considerado VP
            'AUX<': 'VP',
            # 'PAUX': 'VBP',  # verbo auxiliar
            # 'PRT-AUX': 'IN',  # part. lig. verbal - MAIOR PARTE DISPARADA PRP
            # 'SUB': 'IN',  # subordinador - sempre conj-s
            # 'CO': 'CC',  # coordenador - CONJ-C maioria
            # elemento conjunto
            'CJT': settings.tagCJT,
            # 11.2. Coordenação de constituintes com funções diferentes
            'CJT&ACC': 'NP',
            'CJT&PRED': 'ADJP',
            'CJT&ADVL': 'PP',
            'CJT&PASS': 'PP',
            # 'PCJT': 'IN',  # elemento conjunto - p/ pcjt, maioria pp
            # # 'x': 'VB',  # Tomar no cu essa tag. TODO
            # 'COM': 'RB',  # compl. comparação - maioria adv

            # Adjuntos
            # Adjuntos adnominais - pela teoria X', ocorre uma dobra do XP origem. (Mioto, p 68)
            '>N': 'NP',
            # Adjuntos adnominais - pela teoria X', ocorre uma dobra do XP origem. (Mioto, p 68)
            'N<': 'NP',
            # Adjuntos adverbiais/adjectivais - PRECISA VERIFICAR O NUCLEO (irmão) TODO
            '>A': '>A',
            # Adjuntos adverbiais/adjectivais - PRECISA VERIFICAR O NUCLEO (irmão) TODO
            'A<': 'A<',
            '>P': 'PP',  # Adjuntos preposicionais - Adjunto de PP, pela X'
            'P<': 'PP',  # Adjuntos preposicionais - Adjunto de PP, pela X'
            # Comparativos - Comp. é o cap. 22 inteiro do bracketing guidelines. TODO
            'KOMP<': settings.tagKomp,
        }

    # func_tag.replace('-', '')
    return settings.tabelaFuncoes[func_tag]


def fatia_arvore(frase):
    frase_split = re.findall(
        '[\(\)]|[\wÀ-ú\,\.\'\"\!\*\,-\/\:\;\?\`\<\>\{\}\%\+\[\]\&\$\«\»]*', frase)
    frase_split = [c.strip() for c in frase_split]
    frase_split = [i for i in frase_split if i != '']
    return frase_split


def createTransFile(originalLines, dir):
    numero_tratado = ''
    tree_text = ''
    here = os.path.dirname(os.path.realpath(__file__))

    for i in range(len(originalLines)):
        line = originalLines[i]

        if line[0] == '#':
            numero = line[1:].split(' ')[0]
            if numero.isdigit():

                numero_tratado = settings.tratarNumero(numero)
                settings.sentenca_atual = numero_tratado
                file_name = 'Bosque_' + numero_tratado

                filepath = os.path.join(dir, file_name)
                # filepath = os.path.join(here, dir, file_name)

                finalFile = open(filepath, 'w', encoding='utf-8')

        elif line.strip() == '':
            if not finalFile.closed:
                tree_split = fatia_arvore(tree_text)
                tree_translate = translateTags(
                    tree_split) if numero_tratado not in settings.filesToIgnore else ''
                # tree_translate = translateTags(tree_split)

                finalFile.write(tree_translate)
                finalFile.close()
                tree_text = ''

        else:
            if finalFile.closed:
                continue
            tree_text += '' + line.strip()


def gera_tag_rels(func, form):
    if func not in settings.rel_func_tag:
        settings.rel_func_tag[func] = 1
    else:
        settings.rel_func_tag[func] += 1
    if form not in settings.rel_form_tag:
        settings.rel_form_tag[form] = 1
    else:
        settings.rel_form_tag[form] += 1
    par = '{0}:{1}'.format(func, form)
    if par not in settings.rel_func_form_tag:
        settings.rel_func_form_tag[par] = 1
    else:
        settings.rel_func_form_tag[par] += 1
    par = '{0}:{1}'.format(form, func)
    if par not in settings.rel_form_func_tag:
        settings.rel_form_func_tag[par] = 1
    else:
        settings.rel_form_func_tag[par] += 1


def gera_point_rel(point):
    if point not in settings.rel_point:
        settings.rel_point[point] = 1
    else:
        settings.rel_point[point] += 1


def removeHifens(tag):
    if tag[0] == '-':
        tag = tag[1:]
    if tag[-1] == '-':
        tag = tag[:-1]
    return tag


# reconstroi a estrutura da sentença classificada em árvores lógicas
def reconstroiArvore(frase_split, indice, arvore):
    i = 0

    while i < len(frase_split):
        item = frase_split[i]
        if item == '(':
            # começo da sentença
            if 'FRASE' in frase_split[i + 1]:
                frase_split.remove(frase_split[i + 2])
                frase_split.remove(frase_split[i + 1])
                frase_split.insert(i + 1, 'S')

                classe = frase_split[i + 1]

            # caso padrão. cabeçalho do bosque tem muitos valores
            elif ':' in frase_split[i + 1]:
                split_temp = frase_split[i + 1].split(':')

                func = removeHifens(split_temp[0])
                form = removeHifens(split_temp[1])

                gera_tag_rels(func, form)

                if (form == settings.tagCu or form == settings.tag_acl) and func in settings.sentenceList:
                    # if form == settings.tag_acl and func in settings.sentenceList:
                    frase_split[i + 1] = 'S'
                elif form not in settings.posTagsProb:
                    frase_split[i + 1] = tradutor(form)
                else:
                    # TODO
                    if func == 'CJT' and form == 'x':
                        frase_split[i + 1] = tradutor('vp')
                    elif func == 'CJT' and form == 'acl':
                        frase_split[i + 1] = tradutor('S')
                    else:
                        frase_split[i + 1] = tradutorFuncao(func, form)
                classe = frase_split[i + 1]

            # pontuações. são SEMPRE um problema.
            elif re.match('\W', frase_split[i + 1]):
                classe = settings.tagPoint
            #
            # # se a árvore precisar ser corrigida no futuro.
            # if '_' in classe and not settings.tagProblematica:
            #     settings.tagProblematica = True

            nova_arvore = Sintagma(classe, [], arvore.classe, '')
            novo_indice, subarvore = reconstroiArvore(
                frase_split[i + 1:], i + 1, nova_arvore)
            i = novo_indice + 1
            arvore.filhos.append(subarvore)
        elif item == ')':

            palavra = frase_split[i - 1]
            classe = frase_split[0]

            if classe == 'CD' and ',' in palavra:
                palavra = palavra.replace(',', '.')

            # porcentagem é considerada uma palavra, logo, um nó. será necessário marcá-lo, para transformar o símbolo,
            # e o numero anterior, numa \textit{flat structure}
            if palavra == '%':
                classe = settings.percentTag

            if re.match('\W', palavra) and palavra == classe:
                gera_point_rel(palavra)
                if palavra in settings.dictBrackets:
                    palavra = settings.dictBrackets[palavra]
                classe = settings.tagPoint

            # se a árvore precisar ser corrigida no futuro.
            if '_' in classe and not settings.tagProblematica:
                settings.tagProblematica = True

            if len(arvore.filhos):
                subarvore = Sintagma(classe, arvore.filhos,
                                     arvore.classe_pai, '')
            else:
                subarvore = Sintagma(classe, [], arvore.classe_pai, palavra)
            return i + indice, subarvore
        else:
            i += 1
    return i, arvore


def translateTags(tree_split):
    raiz = Sintagma('', [], '', '')
    i, arvore = reconstroiArvore(tree_split, 0, raiz)
    if settings.tagProblematica:
        cor.revisaTags(arvore)
        settings.tagProblematica = False
    tree_text = cor.imprimeArvore(arvore, 0)
    return tree_text
