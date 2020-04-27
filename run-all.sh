#mkdir output

for domain in apply 12many boolean carcdrcons roshambo reverse seasons repeat integers-4 integers-3 integers-2 integers-1 integers-plus integers-plustimes 12many 12many-plus obama ifelse magnetism-simple dominance-2 dominance-3 dominance-4 dominance-5 even-odd exists singular-plural Y Ystar abn anbn anbncn dyck D4 object-track brown-cow Z square-group property-exception property-generalization property-nogeneralization D4 type-raising mam-3 same-different boston monoid magma semigroup linkedlist-reverse fold unfold unfold-nocons map associate parens deductive deductive-particular G Seasons12ManyObama peano-plustimes.churiso triangle robinson
do
    for basis in SK SKI KBCW SKCBWI
    do
        stdbuf -oL nohup nice -n 19 pypy3 src/run.py --search-basis=$basis domains/$domain.churiso > output/$domain-$basis.txt 2> output/$domain-$basis.log &
    done    
done
