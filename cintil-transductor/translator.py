import settings
import treebuilder as tb
from sintagma import Sintagma
import re


def tradutor(tag):
    if not settings.posDict:
        settings.posDict = {
            "A": "JJ",  # Adjetivo
            "A'": "ADJP",  # Sintagma Adjectival
            # "ADJ": "JJ",  # Adjectivos
            "ADV": "RB",  # Advérbios
            "ADV'": "ADVP",  # Sintagma Adverbial
            "ADVP": "ADVP",  # Sintagma Adverbial
            "AP": "ADJP",  # Sintagma Adjectival
            # Artigo # Artigo [REVISAR] (TODO) nota: unico caso em que essa tag aparece está errado.
            "ART": "DT",
            "ART'": "NP",  # sintagma de artigo - não ocorre no handbook
            # # o artigo 'Primeiros passos na aquisição da sintaxe:' chama NP de DT. talvez ajude. mas acho que é melhor corrigir essa árvore.
            "C": settings.CTag,  # Complemento (TODO) objeto
            "C'": settings.CPBarTag,  # "SBAR" Sintagma Objetal  - nao ocorre no handbook
            "CP": settings.CPTag,  # "SBAR"  Sintagma Objetal (TODO) v
            "CARD": "CD",  # Cardinais
            "CARD'": "NP",  # Sintagmas Cardinais
            # "CJ": "CC",  # Conjunções - Essa tag aparece apenas em manuais. não ocorre no CINTIL em momento algum.
            # Clíticos [explicar] https://ciberduvidas.iscte-iul.pt/consultorio/perguntas/clitico/15150
            "CL": "PRP",
            # "CN": "NNS",  # Nomes comuns
            "CONJ": settings.conjTag,  # Conjunções
            "CONJ'": settings.conjBarTag,  # sintagma Conjuntivo
            "CONJP": settings.conjPTag,  # sintagma Conjuntivo
            "D": "DT",  # Artigo
            "D1": "DT",  # Quantificadores - nao ocorre no handbook, só no site
            "D2": "JJ",  # Quantificadores - nao ocorre no handbook, só no site
            # "DA": "DT",  # Artigos Definidos
            "DEM": "DT",
            # # Demonstrativos -> Para o PTB, this, that, these, those são, também, artigos. logo, DEM -> DT.
            # "DFR": "QP",  # Denominadores de Fracções
            # "DGT": "CD",  # Numerais Árabes
            # "DGTR": "CD",  # Numerais Romanos
            # "DM": "UH",  # Marcadores Discursivos nota: não aparece em nenhum caso
            # "EADR": "NN",  # Endereços Electrónicos
            # "EOE": settings.eofTag,  # Fim de Enumeração
            # "EXC": "UH",  # Exclamação
            # "GER": "VBG",  # Gerúndios
            # "GERAUX": "VBG",  # Gerúndio "ter"/"haver" em tempos compostos
            # "IA    ": "DT",  # Artigos Indefinidos
            # "IND": "PRP",  # Indefinidos
            # "INF": "VB",  # Infinitivo
            # "INFAUX": "VB",  # Infinitivo "ter"/"haver" em tempos compostos
            # "INT": "WP",  # Interrogativos
            "ITJ": "UH",  # Interjecções
            "ITJ'": "INTJ",  # Interjecções (TODO)
            # "LTR": "NN",  # Letras
            # "MGT": "NN",  # Unidade de Medida
            # "MTH": "NNP",  # Meses (TODO) v
            "N": "NNS",  # Substantivo
            "N'": "NP",  # Sintagmas Nominais
            "NP": "NP",  # Sintagmas Nominais
            "ORD": "CD",  # Ordinais
            "P": "IN",  # Preposição
            "P'": "PP",  # Sintagmas Preposicionais - não ocorre no handbook
            # "PADR": "NN",  # Parte de Endereço
            "PERCENT": "NN",
            # Sintagma percentual (TODO) nota: pode ser substituido por um termo so 'por cento'
            "PERCENT'": "NP",
            # # simbolo percentual nota: pode ser pronome + substantivo tbm ('por cento') # nota2: PTB considera o % como NN (single noum)
            # Sintagma percentual (TODO) nota: ptb considera como NP
            "PERCENTP": "NP",
            # "PNM": "NP",  # Parte de Nome (TODO) v
            "PNT": settings.pointTag,  # Pontuação
            "POSS": "PP$",  # Possessivos v
            # Possessivos (TODO) nota: não existe um sintagma pronominal. o jeito é manter o NP msm
            "POSS'": "NP",
            # "POSSP": "NP",  # Possessivos (TODO) nota: não ocorre
            "PP": "PP",  # Sintagmas Preposicionais
            # "PPA": "VBN",  # Particípios passados que não formam tempos compostos
            # "PPT": "VBN",  # Particípios passados em tempos compostos
            # "PREP": "IN",  # Preposições
            "PRS": "PRP",  # Pronomes Pessoais
            "QNT": "PRP",  # Quantificadores
            "QNT'": "NP",  # Quantificadores
            "REL": "PRP",  # Pronomes Relativos
            "S": "S",  # Sentença
            # "STT": "NN",  # Títulos Sociais
            # "SYB": "SYM",  # Símbolos
            # "TERMN": "SYM",  # Terminações Opcionais
            # "UM    ": "CD",  # "um" ou "uma"
            # "UNIT": "NN",  # Unidade de Medida Abreviada
            "V'": "VP",  # Sintagma Verbal
            "V": "VB",  # Verbos (sem ser PPA, PPT, INF ou GER)
            # "VAUX": "VB",  # Formas Finitas de "ter" ou "haver" em tempos compostos
            "VP": "VP",  # Sintagma Verbal
            # "WD": "NNP"  # Dias da Semana
        }
    return settings.posDict[tag]


def classeProblematica(classe):
    return '_' in classe[-1]


def extraiPnt(index, inicio, treeText):
    final = inicio + treeText[inicio:].index(')')
    inicio = inicio + treeText[inicio:].index(' ')

    pntWord = treeText[inicio + 1:final].strip()
    if pntWord == '"' or pntWord == "'":
        # se é a primeira ocorrência
        if settings.isFirstQuoteMark:
            pntWord = "``"
        else:  # se é a última
            pntWord = "''"
        settings.isFirstQuoteMark = not settings.isFirstQuoteMark

    if not pntWord in settings.pointList:  # verificar necessidade de adicionar simbolos singulares, além dos pares
        settings.pointList.append(pntWord)

    return treeText[:index] + pntWord + treeText[final + 1:]


def appendRefLists(treeText, inicio, final, classe):
    if classe == settings.conjTag or classe == 'CONJ':
        palavra = treeText[inicio: inicio +
                           treeText[inicio:].index(')')].split()[1].lower()
        if palavra not in settings.conjList:
            settings.conjList.append(palavra)
    if classe == 'CL':
        palavra = treeText[inicio: inicio +
                           treeText[inicio:].index(')')].split()[1].lower()
        if palavra not in settings.clitList:
            settings.clitList.append(palavra)
    # ------------------------

    if classe in settings.tagOcc:
        settings.tagOcc[classe] += 1
    else:
        settings.tagOcc[classe] = 1

    if classe == settings.CTag:
        word = treeText[final:].split(')')[0].strip().lower()
        if word in settings.CWordDict:
            settings.CWordDict[word] += 1
        else:
            settings.CWordDict[word] = 1
    # ------------------------


def fatia_arvore(frase):
    frase_split = re.findall('[\(\)]|[\wÀ-ú\,\.\'\"\!\*\,-\/\:\;\?\`]*', frase)
    frase_split = [c.strip() for c in frase_split]
    frase_split = [i for i in frase_split if i != '']
    return frase_split


def traduzirTags(tree_text):
    settings.isFirstQuoteMark = True
    rever_arvore = False

    for index in reversed(range(len(tree_text))):
        caractere = tree_text[index]

        if caractere == '(':
            inicio = index + 1
            final = inicio + tree_text[inicio:].index(' ')
            classe = tree_text[inicio:final]

            if classe == settings.pointTag:
                tree_text = extraiPnt(index, inicio, tree_text)
            else:
                classe_traduzida = tradutor(classe)
                if classe_traduzida == 'NNS':
                    palavra = tree_text[final:final +
                                        tree_text[final:].index(')')].strip()
                    if palavra in settings.pointList:
                        # classe_traduzida = settings.pointTag
                        tree_text = extraiPnt(index, inicio, tree_text)
                tree_text = tree_text[:inicio] + \
                    classe_traduzida + tree_text[final:]
                if not rever_arvore and classeProblematica(classe_traduzida):
                    rever_arvore = True

            appendRefLists(tree_text, inicio, final, classe)

    raiz = Sintagma('', [], '', '')
    text_split = fatia_arvore(tree_text)
    i, arvore = tb.reconstroiArvoreObj(text_split, 0, raiz)
    if rever_arvore:
        tb.revisaTagsObj(arvore)
    tree_text = tb.imprimeArvoreObj(arvore, 0)

    return tree_text
