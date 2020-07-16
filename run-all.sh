#mkdir output

for domain in apply 12many boolean carcdrcons roshambo reverse seasons repeat integers-4 integers-3 integers-2 integers-1 integers-plus integers-plustimes 12many 12many-plus obama ifelse magnetism-simple dominance-2 dominance-3 dominance-4 dominance-5 even-odd exists singular-plural Y Ystar abn anbn anbncn dyck D4 brown-cow Z square-group property-exception property-generalization property-nogeneralization D4 type-raising mam-3 same-different boston monoid magma semigroup linkedlist-reverse fold unfold unfold-nocons map associate deductive deductive-particular G Seasons12ManyObama peano-plustimes triangle robinson
#for domain in roshambo
do
    for basis in KBCW SKCBWI
    do
        nohup nice -n 19 stdbuf -oL pypy3 src/run.py --search-basis=$basis domains/$domain.churiso > output/$domain-$basis.txt 2> output/$domain-$basis.log &
    done    
    
    # only use normal-form flag for SK, SKI; give a little higher priority
    nohup nice -n 15 stdbuf -oL pypy3 src/run.py --search-basis=SK  domains/$domain.churiso --normal-form > output/$domain-SK.txt 2> output/$domain-SK.log &
    nohup nice -n 15 stdbuf -oL pypy3 src/run.py --search-basis=SKI domains/$domain.churiso --normal-form > output/$domain-SKI.txt 2> output/$domain-SKI.log &
done
