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
> Single statements are parsed using ```binarize()```and are transformed into an instance of ```SimpleFact```. A ```Simple Fact``` has a single application on the left-hand side (f x) and a single right-hand side outcome (e.g. = y).

reduction
----------
As we mentioned earlier, ```succ := ((S ((S S) S)) K)``` applied to ```spring := (K (K K))``` will yield the combinator structure of ```summer := K```. This reduction happens in ```reduction.py```, where strings are reduced to normal form. Here, the ```reduce_combinator``` code specifies how each combinator is handled. By the definition of the K combinator above, ```reduce_combinator``` will take a string ".Kxy" and return "x". Along the way, ```reduce_combinator``` keeps track of how many reduction steps have been taken via ```GLOBAL_REDUCE_COUNTER```. This is one measure of complexity. Note that the combinators **BCTMWE** have reduction routines that do _not_ rely on **S** and **K**. This is further discussed in the section below.

the basis
----------
The combinator basis that you use is up to you! While traditional SKI combinatory logic is available, pychuriso also supports other combinator bases (mentioned above). For the combinators that can be expressed in terms of S and K, there is an option to use an SK basis in their reduction (and therefore in computing their complexity). There is also the option to rely on a single-step reduction routine in ```reduce_combinator```. This flexibility allows you to choose how you want to measure complexity, and allows you to observe the effects of different combinator bases on generalization results. Use the command line argument ```--search-basis``` to denote the combinator basis you want to use (e.g. ```--search-basis SKIBC```).
As mentioned, **BCTMW** can be defined in terms of S and K  (thus penalizing length/complexity in that way). They can also be primitives themselves, with only one reduction step. The convention is that combinators you wish to define in terms of SK should be followed by "sk" (case sensitive). So SKIskBskCW will include I and B in terms of SK, but C and W as primitives themselves.

the search
-----------


run.py
-----------










requirements
============

pyparsing
docopt: [docopt explained]
(http://docopt.org/)
