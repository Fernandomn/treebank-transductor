import os
import sys

import settings
import translator
import folds_generator as fg

# Referencias:
# https://www.linguateca.pt/floresta/BibliaFlorestal/anexo1.html
# https://www.linguateca.pt/floresta/BibliaFlorestal/anexo4.html
# https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
# https://www.clips.uantwerpen.be/pages/mbsp-tags
# https://ciberduvidas.iscte-iul.pt/consultorio/perguntas/a-definicao-de-oracao-nao-finita/17097
# https://educacao.uol.com.br/disciplinas/portugues/nocoes-de-morfossintaxe-nomes-e-pronomes.htm
# https://www.todamateria.com.br/passive-voice/
# https://www.infoescola.com/portugues/funcoes-do-se/
# https://www.linguateca.pt/floresta/BibliaFlorestal/sec09.html
# https://catalog.ldc.upenn.edu/LDC99T42
# https://ciberduvidas.iscte-iul.pt/consultorio/perguntas/as-formas-finitas-e-nao-finitas-dos-verbos/32776

# Erro nos arquivos (CF):
# 498: Possuia uma tag P.vp -> converti pra P:vp
# 593: tem um PRP 'tipo' mal formatado. O prp não estava numa folha.
# 922: tinha um espaço em N>ARGS :pp, que tava zoando o rolê
# 1031: um artigo não fechado, que nem no 593
# 1183: palavra "tiro" não fechada. Como em 593
# 3013: Artigo não fechado. "o mais bonito". como em 593
# 3159: Artigo não fechado. Descobrir porque tem tantos artigos abertos.


#####################################

dir_relatorios = 'relatorios'
here = os.path.dirname(os.path.realpath(__file__))


def print_occ_list(rel, rel_name):
    # here = os.path.dirname(os.path.realpath(__file__))
    file_name = '{0}-{1}.csv'.format(rel_name, settings.portugues)

    filepath = os.path.join(here, dir_relatorios, file_name)

    if not os.path.exists(os.path.join(here, dir_relatorios)):
        os.mkdir(os.path.join(here, dir_relatorios))

    occ_file = open(filepath, 'w', encoding='utf-8')
    list_keys = rel.keys()
    for key in sorted(list_keys):
        occ_file.write("{0}, {1}\n".format(key, rel[key]))

    occ_file.close()


def imprimeRelatorios():
    rel_list = [settings.rel_point, settings.rel_form_tag, settings.rel_func_tag, settings.rel_func_form_tag,
                settings.rel_form_func_tag, settings.rel_inner_pos_conj_tag]
    rel_names = ["rel_point", "rel_form_tag", "rel_func_tag", "rel_func_form_tag", "rel_form_func_tag",
                 "rel_inner_pos_conj_tag"]
    for i in range(len(rel_list)):
        print_occ_list(rel_list[i], rel_names[i])
        
    if len(settings.filesToIgnoreBR) == 0:
        fg.createTenFold()


def setFilesToIgnore():
    settings.filesToIgnore = settings.filesToIgnoreBR if settings.portugues == 'br' else settings.filesToIgnorePT


def getOriginalLines():
    # NOTA: dentro do arquivo, a indicação está invertida: Aponta o CP como sendo
    # centemFolha, e viceversa. ignorar.
    # here = os.path.dirname(os.path.realpath(__file__))

    # CENTEMPublico (portugues de portugual)
    file_pt = "Bosque_CP_8.0.PennTreebank.txt"
    # CENTEMFolha (portugues brasileiro)
    file_br = "Bosque_CF_8.0.PennTreebank.txt"

    file_name = file_pt if settings.portugues == 'pt' else file_br

    # dir_name = '{0}-trad'.format(base_dir)
    file_path = os.path.join(here, file_name)

    originalFile = open(file_path, 'r', encoding='utf-8')

    return originalFile.readlines()


def createDestinyDir():
    dirBrasil = 'bosque_br'
    dirPortugal = 'bosque_pt'
    dir_name = dirPortugal if settings.portugues == 'pt' else dirBrasil

    # here = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(here, dir_name)

    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    # os.chdir(diretorio)
    return dir_path


def main():
    settings.init()

    # portugues = 'br'

    try:
        lingua = sys.argv[sys.argv.index('-l') + 1]
        if lingua == 'pt' or lingua == 'br':
            settings.portugues = lingua
            print('Língua definida:' + lingua)
        else:
            print('Erro: lingua não esperada')
            return 1
    except:
        settings.portugues = 'br'

    imprime_rel = True
    setFilesToIgnore()

    endereco = "~/stanford-parser/BOSQUE/"

    originalLines = getOriginalLines()

    dir = createDestinyDir()

    translator.createTransFile(originalLines, dir)

    if imprime_rel:
        imprimeRelatorios()


if __name__ == '__main__':
    main()
