import settings
import sintagma as s
import re


def reconstroiArvoreObj(frase_split, indice, arvore):
    i = 0

    while i < len(frase_split):
        item = frase_split[i]
        if item == '(':
            classe = frase_split[i + 1]
            nova_arvore = s.Sintagma(classe, [], arvore.classe, '')
            novo_indice, subarvore = reconstroiArvoreObj(
                frase_split[i + 1:], i + 1, nova_arvore)
            i = novo_indice + 1
            arvore.filhos.append(subarvore)
        elif item == ')':
            classe = frase_split[0]
            palavra = frase_split[i - 1]
            if len(arvore.filhos):
                subarvore = s.Sintagma(
                    classe, arvore.filhos, arvore.classe, '')
            else:
                subarvore = s.Sintagma(classe, [], arvore.classe_pai, palavra)
            return i + indice, subarvore
        elif item in settings.pointList:
            if frase_split[i - 1] == 'NNS':
                frase_split[i - 1] = settings.pointTag
                subarvore = s.Sintagma(
                    settings.pointTag, [], arvore.classe, item)

                arvore.filhos.append(subarvore)
            else:
                # point = item if not (item == '"' or item == "'") else item + item
                subarvore = s.Sintagma(
                    settings.pointTag, [], arvore.classe, item)
                arvore.filhos.append(subarvore)
            i += 1
        else:
            i += 1
    return i, arvore


def consertaTagProbObj(arvore):
    if arvore.classe == settings.conjBarTag and settings.conjPTag not in arvore.classe_pai:
        arvore.classe = settings.conjPTag
    for filho in arvore.filhos:
        arvore.valor += filho.valor + ' '
    arvore.valor = arvore.valor.strip()
    return arvore


def setRemoveTagsObj(arvore):
    if arvore.classe == settings.conjPTag:
        for filho in arvore.filhos:
            if filho.classe == settings.conjBarTag:
                filho.classe = settings.conjPTag
                arvore.classe = settings.removeTag

    if arvore.classe == settings.CPTag:
        for filho in arvore.filhos:
            if filho.classe == settings.CPBarTag:
                filho.classe = settings.CPTag
        arvore.classe = settings.removeTag


def revisaTagsObj(arvore):
    classe = arvore.classe

    if classe == settings.pointTag:
        return
    if classe in settings.tagsProblematicas:
        arvore = consertaTagProbObj(arvore)

    if len(arvore.filhos) > 0:
        for filho in arvore.filhos:
            revisaTagsObj(filho)
            if settings.removeTag == filho.classe:
                arvore.removeFilho(filho)
        setRemoveTagsObj(arvore)
    else:
        return


def imprimeArvoreObj(arvore, nivel):
    espaco_esquerda = ''.join(' ' for n in range(nivel))

    # raiz
    if arvore.classe == '':
        return '(\n{0})'.format(imprimeArvoreObj(arvore.filhos[0], nivel + 1))

    # nao-terminal
    if len(arvore.filhos) > 0:

        string_filhos = ''
        if arvore.classe in settings.wordLevelTags and arvore.valor != '':
            for filho in arvore.filhos:
                string_filhos += filho.valor + ' '

            string_retorno = '{0}{1}\n'.format(
                espaco_esquerda, string_filhos.strip())
            # string_retorno = '{0}({1} {2})\n'.format(espaco_esquerda, arvore.classe, string_filhos.strip())
        else:
            for filho in arvore.filhos:
                string_filhos += imprimeArvoreObj(filho, nivel + 1)

            string_retorno = '{0}({1} \n{2}{0})\n'.format(
                espaco_esquerda, arvore.classe, string_filhos)
    # terminal
    else:
        if arvore.classe == settings.pointTag:
            # string_retorno = '{0}{1}\n'.format(espaco_esquerda, arvore.valor)
            string_retorno = ''
        else:
            string_retorno = '{0}({1} {2})\n'.format(
                espaco_esquerda, arvore.classe, arvore.valor)

    return string_retorno
