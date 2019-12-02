import settings
from sintagma import Sintagma


# revisa e corrige tags que precisem de tratamentos especiais
def tagFilhosCoord(filhos):
    # classe_base = filhos[0].classe
    filhos_iguais = True
    wordLevel = True
    tag_comp = ''
    for filho in filhos:
        if filho.classe in settings.listSkipTags:
            continue
        if tag_comp == '':
            tag_comp = filho.classe
        if len(filho.filhos) > 0:
            wordLevel = False
        if filho.classe != tag_comp:
            filhos_iguais = False

    tag_comp = tag_comp if filhos_iguais else 'UCP'
    if wordLevel:
        tag_comp += '_WL'

    return tag_comp


def corrigeTagCoord(arvore):
    # pro futuro: colocar function tags no UCP.
    nova_classe = tagFilhosCoord(arvore.filhos)
    if '_WL' in nova_classe:
        tag_prov = nova_classe.split('_')[0]
        nova_classe = settings.dictSintagma[tag_prov]
        # arvore.absorveFilhos()
        arvore.absorveFilhosSingleLine()

    arvore.classe = nova_classe
    arvore.atualizaClasseFilhos()


def corrigeTagKomp(arvore):
    comparativo = arvore.filhos[0].valor
    if len(arvore.filhos) > 1 and len(arvore.filhos[1].filhos) > 0:
        tag = 'SBAR'
        arvore.filhos[1].classe = 'S'
    else:
        tag = 'PP'
    arvore.valor = comparativo
    arvore.classe = tag
    arvore.removeFilho(arvore.filhos[0])
    arvore.atualizaClasseFilhos()


def corrigeTagEc(arvore, filho, i):
    irmao_direita = arvore.filhos[i + 1]
    novo_filho = Sintagma('NP', [], arvore.classe, '{0}{1}'.format(
        filho.valor, irmao_direita.valor))
    arvore.filhos.insert(i, novo_filho)
    # filho.classe = settings.tagRemover
    arvore.removeFilho(filho)
    # irmao_direita.classe = settings.tagRemover
    arvore.removeFilho(irmao_direita)


def corrigePercentTag(arvore, filho, i):
    irmao_esquerda = arvore.filhos[i - 1]
    novo_filho = Sintagma('NP', [], arvore.classe, '{0} {1}'.format(
        irmao_esquerda.valor, filho.valor))
    arvore.filhos.insert(i, novo_filho)
    # filho.classe = settings.tagRemover
    arvore.removeFilho(filho)
    # irmao_esquerda.classe = settings.tagRemover
    arvore.removeFilho(irmao_esquerda)


def corrigeTagAdj(arvore, filho, i):
    if filho.classe == '>A':
        # irmao_direita = arvore.filhos[i + 1]
        irmao_direita = filhoValido(arvore.filhos, i, '>')
        if irmao_direita.classe == 'ADVP' or irmao_direita.classe == 'RB':
            filho.classe = 'ADVP'
        if irmao_direita.classe == 'ADJP' or irmao_direita.classe == 'JJ':
            filho.classe = 'ADJP'
    if filho.classe == 'A<':
        irmao_esquerda = filhoValido(arvore.filhos, i, '<')
        # irmao_esquerda = arvore.filhos[i - 1]
        if irmao_esquerda.classe == 'ADVP' or irmao_esquerda.classe == 'RB':
            filho.classe = 'ADVP'
        if irmao_esquerda.classe == 'ADJP' or irmao_esquerda.classe == 'JJ':
            filho.classe = 'ADJP'


def filhoValido(filhos, i, dir):
    if dir == '>':
        indices = range(1 + 1, len(filhos))
    else:
        indices = reversed(range(i - 1))
    for j in indices:
        if filhos[j].classe not in settings.listSkipTags:
            return filhos[j]


def verificaFlat(classe_pai):
    return settings.tagFlat if classe_pai == settings.tagCoord else settings.tagConjCoord


def revisaTags(arvore):
    classe = arvore.classe

    # aqui em cima, ficam as verificações referentes ao nó individualmente, ou do nó com seus filhos

    # em caso de coordenação, pelo PTB o que importa é saber o tipo de sintagmas sendo
    # coordenados. se forem iguais, o sintagma pai tem o mesmo tipo que seus filhos.
    # C.C., recebe a tag UCP
    if classe == settings.tagCoord:
        corrigeTagCoord(arvore)

    # A comparação pro PTB, recebe a tag dependendo do tipo dos filhos. se o filho é folha,
    # ela será um PP. C.C., SBAR.
    if classe == settings.tagKomp:
        corrigeTagKomp(arvore)

    if len(arvore.filhos) > 0:
        for i in reversed(range(len(arvore.filhos))):
            # for i in range(len(arvore.filhos)):
            # aqui ficam as verificações dos nós com relação aos seus irmãos

            # como vários nós serão removidos, restrição para não travar o loop
            if i >= len(arvore.filhos) or i < 0:
                break
            # recursão
            filho = arvore.filhos[i]
            revisaTags(filho)

            if filho.classe == settings.tagHifem:
                corrigeTagEc(arvore, filho, i)

            if filho.classe == settings.percentTag:
                corrigePercentTag(arvore, filho, i)

            if filho.classe == '>A' or filho.classe == 'A<':
                corrigeTagAdj(arvore, filho, i)

            if filho.classe == settings.tagConjCoord:
                filho.classe = verificaFlat(classe)
            # if settings.removeTag == filho.classe:
            #     arvore.removeFilho(filho)
        # setRemoveTagsObj(arvore)
    else:
        return


# imprime a árvore no padrão PTB
def imprimeArvore(arvore, nivel):
    espaco_esquerda = ''.join(' ' for n in range(nivel))

    # raiz
    if arvore.classe == '':
        return '(\n{0})'.format(imprimeArvore(arvore.filhos[0], nivel + 1))

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
                string_filhos += imprimeArvore(filho, nivel + 1)

            if arvore.valor != '':
                string_retorno = '{0}({1} {2}\n{3}{0})\n'.format(espaco_esquerda, arvore.classe, arvore.valor,
                                                                 string_filhos)
            else:
                string_retorno = '{0}({1} \n{2}{0})\n'.format(
                    espaco_esquerda, arvore.classe, string_filhos)
    # terminal
    else:
        # tratamento para pontuações e nós sem marcação é o mesmo: remove tag, remove
        # parenteses, imprime so o conteudo
        if arvore.classe == settings.tagFlat:
            string_retorno = '{0}{1}\n'.format(espaco_esquerda, arvore.valor)
        elif arvore.classe == settings.tagPoint:
            # string_retorno = '{0}{1}\n'.format(espaco_esquerda, arvore.valor)
            string_retorno = ''
        else:
            string_retorno = '{0}({1} {2})\n'.format(
                espaco_esquerda, arvore.classe, arvore.valor)

    return string_retorno
