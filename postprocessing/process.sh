
# This script gets some outputs and adds a column for the total description plus running time, sorts, removes comments
# use like: bash postprocessing/process.sh boolean
## NOTE: This CANNOT be used when you have ~= constraints, since it will pick out ones with finite runtime; you must use process-tilde!

# need to find the script directory since that's where addColumn.py lives
scriptDir=$(dirname -- "$(readlink -f -- "$BASH_SOURCE")")

cat ./output/$1-SK.txt ./output/$1-*.txt | grep --binary-files=text --perl --invert-match "^#" | python3 $scriptDir/addColumn.py | sort -k5 -g -z -r
