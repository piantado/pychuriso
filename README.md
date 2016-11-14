pychuriso
=========

A python implementation of ChurIso. 
The name "ChurIso" comes from _**Chur**ch Encoding_, which corresponds to building a structure in a purely logical system that is _**Iso**morphic_ to another system. You can read more about Church Encoding [here](https://en.wikipedia.org/wiki/Church_encoding). ChurIso finds the mapping (with the fastest running time) of symbols to combinators that are consistent with _base facts_. The following is an example of which representation ChurIso finds for base facts about the Seasons:
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
A **combinator** is a higher-order function that uses only function application and earlier defined combinators to define a result from its arguments. You have already seen *S* and *K*. These are reduced as follows:
> (**K**x y) → x</br>
>(**S**x y z) → (x z (y z))</br>

Other combinators include:
>(**I**x) → x
>C
>B
>W
>T
>E

requirements
============

pyparsing
docopt: [Docopt Explained]
(http://docopt.org/)
