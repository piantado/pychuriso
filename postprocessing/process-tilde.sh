# This script gets some outputs and adds a column for the total description plus running time, sorts, removes comments
# use like: bash postprocessing/process.sh boolean

# need to find the script directory since that's where addColumn.py lives
scriptDir=$(dirname -- "$(readlink -f -- "$BASH_SOURCE")")

cat ./output/$1-SK.txt ./output/$1-*.txt | grep --binary-files=text --perl --invert-match "^#" | python3 $scriptDir/addColumn.py | sort -k4 -g -z -r
