#!/bin/bash

getTrainingBlock() {
  # shellcheck disable=SC2004
  case $1 in
  0) echo "$(($blockSize + 1))-$qntFiles" ;;
  9) echo "1-$(($1 * $blockSize))" ;;
  *) echo "1-$(($count * $blockSize)),$(((($count + 1) * $blockSize) + 1))-$qntFiles" ;;
  esac
}

# shellcheck disable=SC2164
cd "$HOME"/projeto-final-parsers/stanford-parser-full-2017-06-09
#mkdir $HOME/projeto-final-parsers/stanford-parser-full-2017-06-09/output/treinoCINTIL

qntFolds=10
dir="$HOME/projeto-final-parsers/cintil/separador-cintil/tree-trad"
# shellcheck disable=SC2012
qntFiles=$(ls -1 "$dir" | wc -l)
blockSize=$((qntFiles / qntFolds))
jarFile="stanford-parser.jar"
# jarFile="$HOME/projeto-final-parsers/stanford-parser-full-2017-06-09/stanford-parser.jar"
memAmmout="-mx4g"
nameParser="edu.stanford.nlp.parser.lexparser.LexicalizedParser"
#serializedGrammarFilename="$HOME/projeto-final-parsers/serialized-files/serialGrammarCINTIL"
#textGrammarFilename="$HOME/projeto-final-parsers/serialized-files/textGrammarCINTIL"
outputFormat='wordsAndTags,penn,typedDependencies'
mkdir -p $HOME/projeto-final-parsers/outputs/treinoCINTIL/treino
outputFilesDirectory="$HOME/projeto-final-parsers/outputs/treinoCINTIL/treino"
# outputFormatOptions=
# outputFilesExtension=

count=0

while (("$count" < "$qntFolds")); do

    testBlock="$((($count * $blockSize) + 1))-$(($(($count + 1)) * $blockSize))"

    trainingBlock=$(getTrainingBlock $count)

#  testBlock="$(getTrainingBlock $count)"
  #  # shellcheck disable=SC2004
#  trainingBlock=$((($count * $blockSize) + 1))-$(($(($count + 1)) * $blockSize))

  #  echo "$count $testBlock $trainingBlock"
  textGrammarFilename="$HOME/projeto-final-parsers/serialized-files/textGrammarCINTIL$(($count + 1))"
  serializedGrammarFilename="$HOME/projeto-final-parsers/serialized-files/serialGrammarCINTIL$(($count + 1))"
  trainFilesPath="$HOME/projeto-final-parsers/cintil/separador-cintil/tree-trad $trainingBlock"
  testFilePath="$HOME/projeto-final-parsers/cintil/separador-cintil/tree-trad $testBlock"
  mkdir -p "$HOME"/projeto-final-parsers/outputs/treinoCINTIL
  # shellcheck disable=SC2004
  trainResultFile="$HOME/projeto-final-parsers/outputs/treinoCINTIL/treino$(($count + 1)).txt"
  testResultFile="$HOME/projeto-final-parsers/outputs/treinoCINTIL/teste$(($count + 1)).txt"
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

  fullTrainingCmd="java -cp $jarFile $memAmmout $nameParser -train $trainFilesPath -test $testFilePath -saveToSerializedFile $serializedGrammarFilename -saveToTextFile $textGrammarFilename -writeOutputFiles -outputFormat $outputFormat -outputFormatOptions $outputFormatOptions -outputFilesDirectory $outputFilesDirectory > $trainResultFile"

  trainingCmd="java -cp $jarFile $memAmmout $nameParser -train $trainFilesPath -saveToSerializedFile $serializedGrammarFilename > $trainResultFile"
  testingCmd="java -cp $jarFile $memAmmout $nameParser -writeOutputFiles -outputFilesDirectory $outputFilesDirectory -loadFromSerializedFile $serializedGrammarFilename -testTreebank $testFilePath > $testResultFile"
  printf $"%d\n\n%s\n\n%s\n\n%s\n\n\n" "$(($count + 1))" "$fullTrainingCmd" "$trainingCmd" "$testingCmd"
  #  $trainingCmd | tee $trainResultFile

  count=$(($count + 1))
done
