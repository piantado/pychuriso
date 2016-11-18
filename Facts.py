from reduction import app, ReductionException, reduce_combinator
import collections
from combinators import substitute
from misc import flatten


class Fact(object):
    # store a constraint, e.g. lhs=rhs, where = vs !=, etc. determined by subclassing
    def __init__(self, lhs, rhs):
        # A constraint that (f x) = y (perhaps with other equality constraints)
        # where f, x, y are all single symbols

        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        return str(self)

    def can_push(self, defined): # only can push Equality
        return False

    def check(self, solution):
        raise NotImplementedError

    def dependents(self):
        # What symbols are we dependent on?
        return set(flatten(self.lhs)) | set(flatten(self.rhs))

class EqualityFact(Fact):
    def __str__(self):
        return "Fact<%s = %s>" % (self.lhs, self.rhs)

    def can_push(self, defined):
        return isinstance(self.rhs, str) and \
               self.rhs not in defined and \
               set(flatten(self.lhs)).issubset(set(defined))

    def check(self, solution):
        try:
            return reduce_combinator(substitute(self.lhs, solution)) == reduce_combinator(substitute(self.rhs, solution))
        except ReductionException:
            return False

class InEqualityFact(Fact):
    def __str__(self):
        return "Fact<%s != %s>" % (self.lhs, self.rhs)

    def check(self, solution):
        try:
            return reduce_combinator(substitute(self.lhs, solution)) != reduce_combinator(substitute(self.rhs, solution))
        except ReductionException:
            return False


class Disjunction(Fact):
    def __init__(self, disjuncts):
        self.disjuncts = disjuncts

    def add(self, x):
        self.disjuncts.append(x)

    def __str__(self):
        return "Disjunction<%s>" % tuple(self.disjuncts)

    def dependents(self):
        deps = set()
        for d in self.disjuncts:
            deps.update(d.dependents())
        return list(deps)

    def check(self, solution):
        for d in self.disjuncts:
            try:
                if d.check(solution):
                    return True
            except ReductionException:
                pass
        return False

class PartialEqualityFact(Fact):
    PARTIAL_LEN = 20

    def __str__(self):
        return "Fact<%s ~= %s>" % (self.lhs, self.rhs)

    def check(self, solution):
        try:  # try this and store the value (partial computation) if we get an exception
            lhs = reduce_combinator(substitute(self.lhs, solution))
        except ReductionException as r:
            lhs = r.value

        try:  # try this and store the value (partial computation) if we get an exception
            rhs = reduce_combinator(substitute(self.rhs, solution))
        except ReductionException as r:
            rhs = r.value

        # and now compare the first PARTIAL_LEN characters to the y
        return lhs[:self.PARTIAL_LEN] == rhs[:self.PARTIAL_LEN]




def compute_complexity(defines, facts):
    """ How many remaining searches through combinators do we need?
        Our search is O(compute_complexity(defines, facts))
     """

    defined = set(defines.keys())
    cplx = 0
    for f in facts:
        print f, f.dependents()
        if isinstance(f, EqualityFact) and f.can_push(defines):
            defined.add(f.rhs) # can push
        else:
            # we face O(dependents) search
            openset = set(f.dependents()) - defined
            cplx += len(openset)
            defined.update(openset)

    return cplx