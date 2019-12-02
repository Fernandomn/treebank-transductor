def init():
    global tabela
    global tabelaFuncoes
    global tagPoint
    global tagRemover
    global tagHifem
    global tagCoord
    global tagConjCoord
    global percentTag
    global tag_x
    global tagX
    global tag_acl
    global posTagsProb
    global wordLevelTags
    global tagProblematica
    global tagCu
    global tagCJT
    global tagFlat
    global rel_point
    global rel_func_tag
    global rel_form_tag
    global rel_func_form_tag
    global rel_form_func_tag
    global rel_inner_pos_conj_tag
    global portugues
    global tagKomp
    global dictBrackets
    global dictSintagma
    global listSkipTags
    global filesToIgnore
    global filesToIgnoreBR
    global filesToIgnorePT
    global sentenceList
    global sentenca_atual

    # caso seja necessário
    listaKompBr = ['0004', '0070', '0119', '0274', '0344', '0459', '0666', '0675', '0689', '0719', '0795', '0810',
                   '0878', '0878', '1205', '1239', '1426', '1528', '1594', '1606', '1669', '1670', '1779', '2017',
                   '2030', '2470', '2475', '2680', '2804', '2809', '2810', '3223', '3329', '3337', '3410', '3491',
                   '3493', '3493', '3557', '3591', '3592', '3650', '3668', '3920', '3940', '3992']

    listPercBr = ['0002', '0004', '0092', '0282', '0294', '0360', '0362', '0408', '0429', '0430', '0468', '0469',
                  '0471', '0564', '0567', '0569', '0570', '0670', '0861', '0862', '0887', '1043', '1062', '1063',
                  '1064', '1073', '1082', '1148', '1149', '1153', '1197', '1211', '1284', '1330', '1349', '1409',
                  '1420', '1465', '1472', '1517', '1519', '1535', '1545', '1573', '1574', '1577', '1607', '1611',
                  '1621', '1656', '1657', '1723', '1731', '1754', '1755', '1756', '1757', '1758', '1759', '1773',
                  '1775', '1839', '1847', '1848', '1951', '1969', '2020', '2021', '2022', '2029', '2030', '2031',
                  '2082', '2083', '2084', '2086', '2118', '2164', '2175', '2176', '2178', '2209', '2287', '2290',
                  '2291', '2293', '2302', '2324', '2400', '2469', '2583', '2585', '2588', '2589', '2607', '2627',
                  '2678', '2710', '2713', '2725', '2860', '2863', '2979', '2980', '2982', '2990', '2991', '2993',
                  '3056', '3142', '3180', '3198', '3239', '3240', '3242', '3306', '3313', '3314', '3327', '3328',
                  '3329', '3346', '3347', '3540', '3541', '3561', '3564', '3566', '3578', '3616', '3617', '3618',
                  '3635', '3636', '3704', '3719', '3720', '3742', '3753', '3855', '3856', '3871', '3928', '3929',
                  '4079', '4159', '4161', '4162', '4163']

    filesToIgnoreBR = listPercBr  # usar para testar
    # filesToIgnoreBR = [] #usar para treinar

    filesToIgnorePT = []
    sentenca_atual = ''  # apenas para auxiliar debug
    tagProblematica = False
    tagRemover = '_TOREMOVE_'
    tagHifem = '_EC_'
    tagCu = 'cu'
    tagCoord = '_CU_'
    tagCJT = '_CJT_'
    tagConjCoord = 'CC'
    percentTag = '_PERC_'
    tag_acl = 'acl'
    tag_x = 'x'
    tagX = '_X_'
    tagFlat = '_FLAT_'
    tagPoint = 'PNT'
    tagKomp = '_KOMP_'
    posTagsProb = [tag_x, tag_acl]
    wordLevelTags = [tagFlat]
    listSkipTags = [tagFlat, tagPoint, tagConjCoord]
    tabela = {}
    tabelaFuncoes = {}
    rel_point = {}
    rel_form_tag = {}
    rel_func_tag = {}
    rel_func_form_tag = {}
    rel_form_func_tag = {}
    rel_inner_pos_conj_tag = {}
    dictBrackets = {
        '(': '-LRB-',
        ')': '-RRB-',
        '[': '-LSB-',
        ']': '-RSB-',
        '{': '-LCB-',
        '}': '-RCB-',
        '«': "``",
        '»': "''"
    }
    dictSintagma = {
        'NN': 'NP',
        'VBP': 'VP',  # verbos finitos - Verbo "normal". conferir inflexão da 3ª pessoa do inglês
        'VBG': 'VP',  # verbos gerúndios
        'VBN': 'VP',  # verbos particípios
        'VB': 'VP',
        'JJ': 'ADJP',  # Sintagma adjectivais
        'RB': 'ADVP',  # Sintagma adverbiais
        'IN': 'PP',  # não deve se aplicar
    }

    sentenceList = ['UTT', 'STA', 'QUE', 'CMD', 'EXC']


# Verifica se o o nó aliado é uma folha ou não


def ehFolha(linha, inicio):
    for i in range(inicio, len(linha)):
        if linha[i] == ')':
            return True
        elif linha[i] == '(' or linha[i] == '\n':
            return False
        else:
            continue


# trata o numero para fazer o nome do arquivo bonitinho
def tratarNumero(numero):
    if numero.isdigit():
        stringNumero = str(numero)
        tamString = len(stringNumero)
        if tamString == 1:
            return '000' + stringNumero
        elif tamString == 2:
            return '00' + stringNumero
        elif tamString == 3:
            return '0' + stringNumero
        elif tamString >= 4:
            return stringNumero
    else:
        return '0000'
