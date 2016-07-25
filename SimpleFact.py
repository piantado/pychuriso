from reduce import apply, ReductionException

PARTIAL_LEN = 20 # In ~= comparison, how many chars do we compare?

class SimpleFact(object):
    """
    A simple fact has a single application on the LHS (f x) and a single rhs outcome
    """
    def __init__(self, f, x, op, rhs):
        self.f = f
        self.x = x
        self.op = op
        self.rhs = rhs

    def __str__(self):
        return "(%s %s)%s%s" % (self.f, self.x, self.op, self.rhs)

    def __repr__(self):
        return str(self)

    def check(self, solution):
        """ Return true if the solution satisfies this fact """
        if self.op == '=':
            try:
                return apply(solution[self.f], solution[self.x]) == solution[self.rhs]
            except ReductionException:
                return False
        elif self.op == '!=':
            try:
                return apply(solution[self.f], solution[self.x]) != solution[self.rhs]
            except ReductionException:
                return False
        elif self.op == "~=": # partial evaluation, allowing non-halting computation
            try: # try this and store the value (partial computation) if we get an exception
                lhs = apply(solution[self.f], solution[self.x])
            except ReductionException as r:
                lhs = r.value

            # and now compare the first PARTIAL_LEN characters to the rhs
            return lhs[:PARTIAL_LEN] == self.rhs

        else:
            assert False, "Bad op type: " + self.op




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