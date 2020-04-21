#mkdir output

for domain in apply 12many boolean carcdrcons roshambo reverse seasons repeat integers-4 integers-3 integers-2 integers-1 integers-plus integers-plustimes 12many 12many-plus obama ifelse magnetism-simple dominance-2 dominance-3 dominance-4 dominance-5 even-odd exists singular-plural Y Ystar abn anbn anbncn dyck D4 object-track brown-cow Z triangle-group-333 square-group property-exception property-generalization property-nogeneralization D4 type-raising mam-3 same-different saffran boston monoid magma semigroup  linkedlist-reverse fold unfold unfold-nocons map associate parens unfold-generate-abn unfold-generate-an unfold-generate-anbn unfold-generate-anbncn deductive deductive-particular G Seasons12ManyObama
do
	
#     nice -n 19 pypy run.py --search-basis=SK             domains/$domain.churiso > output/$domain-SK.txt                 2> output/$domain-SK.log &
#     nice -n 19 pypy run.py --search-basis=SKI            domains/$domain.churiso > output/$domain-SKI.txt                2> output/$domain-SKI.log &
#     nice -n 19 pypy run.py --search-basis=BCKW           domains/$domain.churiso > output/$domain-BCKW.txt               2> output/$domain-BCKW.log &
#     nice -n 19 pypy run.py --search-basis=IBCKW          domains/$domain.churiso > output/$domain-IBCKW.txt              2> output/$domain-IBCKW.log &
#     nice -n 19 pypy run.py --search-basis=SKCskBskWskIsk domains/$domain.churiso > output/$domain-SKCskBskWskIsk.txt     2> output/$domain-SKCskBskWskIsk.log &

    nice -n 19 pypy run.py --search-basis=SK             domains/$domain.churiso > output/$domain-SK.txt                 2> output/$domain-SK.log &
    nice -n 19 pypy run.py --search-basis=SKIsk          domains/$domain.churiso > output/$domain-SKIsk.txt              2> output/$domain-SKIsk.log &
    nice -n 19 pypy run.py --search-basis=KBskCskWsk     domains/$domain.churiso > output/$domain-KBskCskWsk.txt         2> output/$domain-KBskCskWsk.log &
    nice -n 19 pypy run.py --search-basis=SKCskBskWskIsk domains/$domain.churiso > output/$domain-SKCskBskWskIsk.txt     2> output/$domain-SKCskBskWskIsk.log &

done
