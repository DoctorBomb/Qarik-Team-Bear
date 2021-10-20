#!/bin/bash

## Convert to txt; Change directory if necessary
DIR='/home/kbari/Documents/Erdos/Original_Data/data1/'

pdf_miner () {
  for FILE in "$DIR"*; do 
    echo "Processing $(basename $FILE suffix)"
    pdf2txt.py $FILE > /home/kbari/Documents/Erdos/Text_Data/"$(basename $FILE suffix).txt"
  done
}


## Check
#for f in ~/Documents/Erdos/Text_Data/*.txt
#do
#  echo $(wc -c $f | awk '{print $1}')
#done



