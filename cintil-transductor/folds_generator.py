import os
import math

here = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(here, os.pardir))
# serial_path='serialized-files'
serial_path = os.path.join(parent_dir, 'serialized-files')
training_path = os.path.join(parent_dir, 'output', 'treinoCINTIL')
if not os.path.exists(serial_path):
    os.mkdir(serial_path)
if not os.path.exists(training_path):
    os.mkdir(training_path)

qntFolds = 10
dir = os.path.join(here, 'tree-trad')
qntFiles = len(os.listdir(dir))
blockSize = math.floor(qntFiles/qntFolds)

jarFile = "stanford-parser.jar"
memAmmout = "-mx4g"
nameParser = "edu.stanford.nlp.parser.lexparser.LexicalizedParser"
outputFormat = 'wordsAndTags,penn,typedDependencies'
encoding = 'uft-8'
nthreads = -1
outputFormatOptions = 'lexicalize'


def getTrainingBlock(fold_num):
    block_str = ''
    if fold_num == 0:
        block_str = '{0}-{1}'.format(blockSize+1, qntFiles)
    elif fold_num == 9:
        block_str = '{0}-{1}'.format(1, fold_num*blockSize)
    else:
        block_str = '{0}-{1},{2}-{3}'.format(
            1, fold_num*blockSize, ((fold_num+1)*blockSize)+1, qntFiles)
    return block_str


def createTenFold():
    count = 0
    trainingInputsFile = open(os.path.join(here, 'trainingInputs.txt'), 'w')

    while count < qntFolds:
        testBlock = '{0}-{1}'.format((count *
                                        blockSize)+1, (count+1)*blockSize)
        
        trainingBlock = getTrainingBlock(count)

        textGrammarFilename = "{0}/textGrammarCINTIL{1}".format(
            serial_path, count+1)
        serializedGrammarFilename = "{0}/serialGrammarCINTIL{1}".format(
            serial_path, count+1)

        trainFilesPath = '{0} {1}'.format(dir, trainingBlock)
        testFilePath = '{0} {1}'.format(dir, testBlock)

        trainResultFile = "{0}/treino{1}.txt".format(
            training_path, count+1)
        testResultFile = "{0}/teste{1}.txt".format(training_path, count+1)

        fullTrainingCmd = "java -cp {0} {1} {2} -train {3} -test {4} -saveToSerializedFile {5} -saveToTextFile {6} -writeOutputFiles -outputFormat {7} -outputFormatOptions {8} -outputFilesDirectory {9} > {10}".format(
            jarFile, memAmmout, nameParser, trainFilesPath, testFilePath, serializedGrammarFilename, textGrammarFilename, outputFormat, outputFormatOptions, training_path, trainResultFile)
        trainingCmd = "java -cp {0} {1} {2} -train {3} -saveToSerializedFile {4} > {5}".format(
            jarFile, memAmmout, nameParser, trainFilesPath, serializedGrammarFilename, trainResultFile)
        testingCmd = "java -cp {0} {1} {2} -writeOutputFiles -outputFilesDirectory {3} -loadFromSerializedFile {4} -testTreebank {5} > {6}".format(
            jarFile, memAmmout, nameParser, training_path, serializedGrammarFilename, testFilePath, testResultFile)

        training_srt = '{0}\n\n{1}\n\n{2}\n\n{3}\n\n\n'.format(count+1, fullTrainingCmd, trainingCmd, testingCmd)

        trainingInputsFile.write(training_srt)

        count += 1

    trainingInputsFile.close()
