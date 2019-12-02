#!/bin/bash

getTrainingBlockBr() {
  # shellcheck disable=SC2004
  case $1 in
  0) echo "$(($blockSizeBr + 1))-$qntFilesBr" ;;
  9) echo "1-$(($1 * $blockSizeBr))" ;;
  *) echo "1-$(($count * $blockSizeBr)),$(((($count + 1) * $blockSizeBr) + 1))-$qntFilesBr" ;;
  esac
}

getTrainingBlockPt() {
  # shellcheck disable=SC2004
  case $1 in
  0) echo "$(($blockSizePt + 1))-$qntFilesPt" ;;
  9) echo "1-$(($1 * $blockSizePt))" ;;
  *) echo "1-$(($count * $blockSizePt)),$(((($count + 1) * $blockSizePt) + 1))-$qntFilesPt" ;;
  esac
}

# shellcheck disable=SC2164
cd "$HOME"/projeto-final-parsers/stanford-parser-full-2017-06-09

qntFolds=10

dirBr="$HOME/projeto-final-parsers/BOSQUE/bosque_br_limpo_traduzido"
dirPt="$HOME/projeto-final-parsers/BOSQUE/bosque_pt_limpo_traduzido"

# shellcheck disable=SC2012
qntFilesBr=$(ls -1 "$dirBr" | wc -l)
qntFilesPt=$(ls -1 "$dirPt" | wc -l)
count=0

blockSizeBr=$((qntFilesBr / qntFolds))
blockSizePt=$((qntFilesPt / qntFolds))

jarFile="stanford-parser.jar"

memAmmout="-mx4g"
nameParser="edu.stanford.nlp.parser.lexparser.LexicalizedParser"

outputFormat='wordsAndTags,penn,typedDependencies'
mkdir -p $HOME/projeto-final-parsers/outputs/treinoBOSQUE/treino
outputFilesDirectory="$HOME/projeto-final-parsers/outputs/treinoBOSQUE/treino"

while (("$count" < "$qntFolds")); do

  testBlockBr=$((($count * $blockSizeBr) + 1))-$(($(($count + 1)) * $blockSizeBr))
  testBlockPt=$((($count * $blockSizePt) + 1))-$(($(($count + 1)) * $blockSizePt))
  #  # shellcheck disable=SC2004
  trainingBlockBr="$(getTrainingBlockBr $count)"
  trainingBlockPt="$(getTrainingBlockPt $count)"

  # testBlockBr="$(getTrainingBlockBr $count)"
  #  testBlockPt="$(getTrainingBlockPt $count)"
  #  #  # shellcheck disable=SC2004
  #  trainingBlockBr=$((($count * $blockSizeBr) + 1))-$(($(($count + 1)) * $blockSizeBr))
  #  trainingBlockPt=$((($count * $blockSizePt) + 1))-$(($(($count + 1)) * $blockSizePt))

  textGrammarFilename="$HOME/projeto-final-parsers/serialized-files/textGrammarBOSQUE$(($count + 1))"
  serializedGrammarFilename="$HOME/projeto-final-parsers/serialized-files/serialGrammarBOSQUE$(($count + 1))"

  trainFilesPathBr="$HOME/projeto-final-parsers/BOSQUE/bosque_br_limpo_traduzido $trainingBlockBr"
  testFilePathBr="$HOME/projeto-final-parsers/BOSQUE/bosque_br_limpo_traduzido $testBlockBr"

  trainFilesPathPt="$HOME/projeto-final-parsers/BOSQUE/bosque_pt_limpo_traduzido $trainingBlockPt"
  testFilePathPt="$HOME/projeto-final-parsers/BOSQUE/bosque_pt_limpo_traduzido $testBlockPt"
  mkdir -p "$HOME"/projeto-final-parsers/outputs/treinoBOSQUE
  # shellcheck disable=SC2004

  trainResultFileBr="$HOME/projeto-final-parsers/outputs/treinoBOSQUE/treinoBr$(($count + 1)).txt"
  testResultFileBr="$HOME/projeto-final-parsers/outputs/treinoBOSQUE/testeBr$(($count + 1)).txt"

  trainResultFilePt="$HOME/projeto-final-parsers/outputs/treinoBOSQUE/treinoPt$(($count + 1)).txt"
  testResultFilePt="$HOME/projeto-final-parsers/outputs/treinoBOSQUE/testept$(($count + 1)).txt"

  outputFormatOptions='lexicalize'
  encoding='uft-8'
  nthreads=-1

  #  trainingCmd="java -cp $jarFile $memAmmout $nameParser
  #  -train $trainFilesPath
  #  -testTreebank $testFilePath
  #  -saveToSerializedFile $serializedGrammarFilename
  #  -saveToTextFile $textGrammarFilename
  #  -encoding $encoding
  #  -writeOutputFiles
  #  -outputFormat $outputFormat
  #  -outputFormatOptions $outputFormatOptions
  #  -outputFilesDirectory $outputFilesDirectory
  #   > $trainResultFile
  #  "
  # -nthreads $nthreads

  fullTrainingCmdBr="java -cp $jarFile $memAmmout $nameParser -train $trainFilesPathBr -test $testFilePathBr -saveToSerializedFile $serializedGrammarFilename -saveToTextFile $textGrammarFilename -writeOutputFiles -outputFormat $outputFormat -outputFormatOptions $outputFormatOptions -outputFilesDirectory $outputFilesDirectory > $trainResultFileBr"
  trainingCmdBr="java -cp $jarFile $memAmmout $nameParser -train $trainFilesPathBr -saveToSerializedFile $serializedGrammarFilename > $trainResultFileBr"
  testingCmdBr="java -cp $jarFile $memAmmout $nameParser -writeOutputFiles -outputFilesDirectory $outputFilesDirectory -loadFromSerializedFile $serializedGrammarFilename -testTreebank $testFilePathBr > $testResultFileBr"

  fullTrainingCmdPt="java -cp $jarFile $memAmmout $nameParser -train $trainFilesPathPt -test $testFilePathPt -saveToSerializedFile $serializedGrammarFilename -saveToTextFile $textGrammarFilename -writeOutputFiles -outputFormat $outputFormat -outputFormatOptions $outputFormatOptions -outputFilesDirectory $outputFilesDirectory > $trainResultFilePt"
  trainingCmdPt="java -cp $jarFile $memAmmout $nameParser -train $trainFilesPathPt -saveToSerializedFile $serializedGrammarFilename > $trainResultFilePt"
  testingCmdPt="java -cp $jarFile $memAmmout $nameParser -writeOutputFiles -outputFilesDirectory $outputFilesDirectory -loadFromSerializedFile $serializedGrammarFilename -testTreebank $testFilePathPt > $testResultFilePt"

  printf $"%d\n\nBr\n%s\n\n%s\n\n%s\n\nPt\n%s\n\n%s\n\n%s\n\n\n" "$(($count + 1))" "$fullTrainingCmdBr" "$trainingCmdBr" "$testingCmdBr" "$fullTrainingCmdPt" "$trainingCmdPt" "$testingCmdPt"

  count=$(($count + 1))
done
