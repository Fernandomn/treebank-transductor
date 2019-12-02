import os
import math

here = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(here, os.pardir))
# serial_path='serialized-files'
serial_path = os.path.join(parent_dir, 'serialized-files')
training_path = os.path.join(parent_dir, 'output', 'treinoBOSQUE')
if not os.path.exists(serial_path):
    os.mkdir(serial_path)
if not os.path.exists(training_path):
    os.mkdir(training_path)


qntFolds = 10
dirBr = os.path.join(here, 'bosque_br')
dirPt = os.path.join(here, 'bosque_pt')
qntFilesBr = len(os.listdir(dirBr))
qntFilesPt = len(os.listdir(dirPt))
blockSizeBr = math.floor(qntFilesBr/qntFolds)
blockSizePt = math.floor(qntFilesPt/qntFolds)

jarFile = "stanford-parser.jar"
memAmmout = "-mx4g"
nameParser = "edu.stanford.nlp.parser.lexparser.LexicalizedParser"
outputFormat = 'wordsAndTags,penn,typedDependencies'
encoding = 'uft-8'
nthreads = -1
outputFormatOptions = 'lexicalize'


def getTrainingBlockBr(fold_num):
    block_str = ''
    if fold_num == 0:
        block_str = '{0}-{1}'.format(blockSizeBr+1, qntFilesBr)
    elif fold_num == 9:
        block_str = '{0}-{1}'.format(1, fold_num*blockSizeBr)
    else:
        block_str = '{0}-{1},{2}-{3}'.format(
            1, fold_num*blockSizeBr, ((fold_num+1)*blockSizeBr)+1, qntFilesBr)
    return block_str


def getTrainingBlockPt(fold_num):
    block_str = ''
    if fold_num == 0:
        block_str = '{0}-{1}'.format(blockSizePt+1, qntFilesPt)
    elif fold_num == 9:
        block_str = '{0}-{1}'.format(1, fold_num*blockSizePt)
    else:
        block_str = '{0}-{1},{2}-{3}'.format(
            1, fold_num*blockSizePt, ((fold_num+1)*blockSizePt)+1, qntFilesPt)
    return block_str


def createTenFold():
    count = 0
    trainingInputsFile = open(os.path.join(here, 'trainingInputs.txt'), 'w')

    while count < qntFolds:
        testBlockBr = '{0}-{1}'.format((count *
                                        blockSizeBr)+1, (count+1)*blockSizeBr)
        testBlockPt = '{0}-{1}'.format((count *
                                        blockSizePt)+1, (count+1)*blockSizePt)
        trainingBlockBr = getTrainingBlockBr(count)
        trainingBlockPt = getTrainingBlockPt(count)

        textGrammarFilename = "{0}/textGrammarBOSQUE{1}".format(
            serial_path, count+1)
        serializedGrammarFilename = "{0}/serialGrammarBOSQUE{1}".format(
            serial_path, count+1)

        trainFilesPathBr = '{0} {1}'.format(dirBr, trainingBlockBr)
        testFilePathBr = '{0} {1}'.format(dirBr, testBlockBr)

        trainFilesPathPt = '{0} {1}'.format(dirPt, trainingBlockPt)
        testFilePathPt = '{0} {1}'.format(dirPt, testBlockPt)

        trainResultFileBr = "{0}/treinoBr{1}.txt".format(
            training_path, count+1)
        testResultFileBr = "{0}/testeBr{1}.txt".format(training_path, count+1)

        trainResultFilePt = "{0}/treinoPt{1}.txt".format(
            training_path, count+1)
        testResultFilePt = "{0}/testePt{1}.txt".format(training_path, count+1)

        fullTrainingCmdBr = "java -cp {0} {1} {2} -train {3} -test {4} -saveToSerializedFile {5} -saveToTextFile {6} -writeOutputFiles -outputFormat {7} -outputFormatOptions {8} -outputFilesDirectory {9} > {10}".format(
            jarFile, memAmmout, nameParser, trainFilesPathBr, testFilePathBr, serializedGrammarFilename, textGrammarFilename, outputFormat, outputFormatOptions, training_path, trainResultFileBr)
        trainingCmdBr = "java -cp {0} {1} {2} -train {3} -saveToSerializedFile {4} > {5}".format(
            jarFile, memAmmout, nameParser, trainFilesPathBr, serializedGrammarFilename, trainResultFileBr)
        testingCmdBr = "java -cp {0} {1} {2} -writeOutputFiles -outputFilesDirectory {3} -loadFromSerializedFile {4} -testTreebank {5} > {6}".format(
            jarFile, memAmmout, nameParser, training_path, serializedGrammarFilename, testFilePathBr, testResultFileBr)

        fullTrainingCmdPt = "java -cp {0} {1} {2} -train {3} -test {4} -saveToSerializedFile {5} -saveToTextFile {6} -writeOutputFiles -outputFormat {7} -outputFormatOptions {8} -outputFilesDirectory {9} > {10}".format(
            jarFile, memAmmout, nameParser, trainFilesPathPt, testFilePathPt, serializedGrammarFilename, textGrammarFilename, outputFormat, outputFormatOptions, training_path, trainResultFilePt)
        trainingCmdPt = "java -cp {0} {1} {2} -train {3} -saveToSerializedFile {4} > {5}".format(
            jarFile, memAmmout, nameParser, trainFilesPathPt, serializedGrammarFilename, trainResultFilePt)
        testingCmdPt = "java -cp {0} {1} {2} -writeOutputFiles -outputFilesDirectory {3} -loadFromSerializedFile {4} -testTreebank {5} > {6}".format(
            jarFile, memAmmout, nameParser, training_path, serializedGrammarFilename, testFilePathPt, testResultFilePt)

        training_srt = '{0}\nBR\n{1}\n\n{2}\n\n{3}\n\nPT\n{4}\n\n{5}\n\n{6}\n\n\n'.format(
            count+1, fullTrainingCmdBr, trainingCmdBr, testingCmdBr, fullTrainingCmdPt, trainingCmdPt, testingCmdPt)

        trainingInputsFile.write(training_srt)

        count += 1

    trainingInputsFile.close()
