pychuriso
=========

A python implementation of ChurIso. 
The name "ChurIso" comes from _**Chur**ch Encoding_, which corresponds to building a structure in a purely logical system that is _**Iso**morphic_ to another system. You can read more about Church Encoding [here](https://en.wikipedia.org/wiki/Church_encoding). For an overview of combinatory logic, you should start [here](https://en.wikipedia.org/wiki/Combinatory_logic). ChurIso finds the mapping (with the fastest running time) of symbols to combinators that are consistent with _base facts_. The following is an example of which representation ChurIso finds for base facts about the Seasons:
```
(succ) winter → spring              spring := (K (K K))
(succ spring) → summer              winter := (K (S (K K) (K (K K))))
(succ summer) → fall                fall := (K K)         
(succ fall) → winter                summer := K
                                    succ := ((S ((S S) S)) K)
```
The base facts can be encoded using S and K. The system that ChurIso finds is consistent with these base facts. In other words, reducing ```succ := ((S ((S S) S)) K)``` applied to ```spring := (K (K K))``` will yield the combinator structure of ```summer := K```!

combinators
-----------
A **combinator** is a higher-order function that uses only function application and earlier defined combinators to define a result from its arguments. You have already seen **S** and **K**. These are reduced as follows:
> (**K** x y) = x</br>
>(**S** x y z) = (x z (y z))</br>

Other combinators include:
>(**I** x) = x</br>
>(**B** x y z) = x (y z)</br>
>(**C** x y z = x z y</br>
>(**W** x y) = x y y</br>
>(**T** x y) = y x</br>
>(**M** x) = x x</br>

These combinators can be expressed in terms of **S** and **K**. See more about this below in the section on ```combinators.py```. Other combinators cannot be expressed in terms of **S** and **K**, but can be implemented in ChurIso.

>(**E** x y a b)  ```if x == y: return a  else: return b```</br>


the facts
----------
The base facts to be encoded are written in an input.txt file. Examples of these can be found in pychuriso/domains. Some examples of current domains are:
- boolean logic
- integers
- magnetism
- kinship
- Scheme ```cons```, ```cdr```, ```car```
- dominance relations
- propositional logic (e.g. brown cow)

There are **4** keywords that can be used in the input file.
>```unique```: each of the symbols following ```unique``` must be represented by distinct combinator structures.</br>
>```define```: allows you to explicitly set a combinator structure for a specified symbol.</br>
>```variable```: functions like "for all", where anything of the form specified will map to the same symbol.</br>
>```show```: indicates to print out the solution to a new problem, given the combinators mapped to the base facts.</br>


parsing the input
----------
pychuriso has a parser to handle the input.txt file. This uses regular expressions to return:
>```
    defines   = {}
    variables = []
    uniques   = []
    facts     = []
    shows     = dict()
```
> single statements are parsed using ```binarize()```

the basis
----------

reduction
----------

the search
-----------

run.py
-----------










requirements
============

pyparsing
docopt: [Docopt Explained]
(http://docopt.org/)
