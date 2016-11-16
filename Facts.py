from reduction import app, ReductionException, reduce_combinator

class SimpleFact(object):
    def __init__(self, f, x, rhs):
        self.f = f
        self.x = x
        self.rhs = rhs

    def __repr__(self):
        return str(self)

    def check(self, solution):
        raise NotImplementedError

class EqualityFact(SimpleFact):
    def __str__(self):
        return "(%s %s) = %s" % (self.f, self.x, self.rhs)

    def check(self, solution):
        try:
           return app(solution[self.f], solution[self.x]) == solution[self.rhs]
        except ReductionException:
            return False

class InEqualityFact(SimpleFact):
    def __str__(self):
        return "(%s %s) != %s" % (self.f, self.x, self.rhs)

    def check(self, solution):
        try:
            return app(solution[self.f], solution[self.x]) != solution[self.rhs]
        except ReductionException:
            return False

class InFact(SimpleFact):
    def __init__(self, x, rhs):
        self.x = x
        self.rhs = rhs

    def __str__(self):
        return "%s in %s" % (self.x, set(self.rhs))

    def check(self, solution):
        try:
            xr = reduce_combinator(solution[self.x])
        except ReductionException:
            return False

        for r in self.rhs:
            try:
                if xr == reduce_combinator(solution[r]):
                    return True
            except ReductionException:
                pass

        return False


class PartialEqualityFact(SimpleFact):
    PARTIAL_LEN = 20

    def __str__(self):
        return "(%s %s) ~= %s" % (self.f, self.x, self.rhs)

    def check(self, solution):
        try:  # try this and store the value (partial computation) if we get an exception

            lhs = app(solution[self.f], solution[self.x])
        except ReductionException as r:
            lhs = r.value

        # and now compare the first PARTIAL_LEN characters to the rhs
        return lhs[:self.PARTIAL_LEN] == self.rhs




def compute_complexity(defines, facts):
    """ How many remaining searches through combinators do we need? (e..g ignoring pushes)
        Our search is O(compute_complexity(defines, facts))
     """

    defined = set(defines.keys())
    cplx = 0
    for f in facts:
        if f.f not in defined:
            cplx += 1
            defined.add(f.f)
        if f.x not in defined:
            cplx += 1
            defined.add(f.x)

        if f.op == '=': # we can only push equality constraints
            defined.add(f.rhs)

        elif f.rhs not in defined: # we can't have rhs undefined and non-equality
            return float("inf")

    return cplx