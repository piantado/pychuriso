from reduction import app, ReductionException, reduce_combinator

class SimpleFact(object):
    def __init__(self, f, x, y):
        # A constraint that (f x) = y (perhaps with other equality constraints)
        # where f, x, y are all single symbols

        assert isinstance(f, str), "f must be a single symbol"
        self.f = f

        assert isinstance(x, str), "x must be a single symbol"
        self.x = x

        assert isinstance(y, str), "y must be a single symbol"
        self.y = y

    def __repr__(self):
        return str(self)

    def check(self, solution):
        raise NotImplementedError

    def dependents(self):
        # What symbols are we dependent on?
        return [self.f, self.x, self.y]

class EqualityFact(SimpleFact):
    def __str__(self):
        return "Fact<(%s %s) = %s>" % (self.f, self.x, self.y)

    def check(self, solution):
        try:
            return app(solution[self.f], solution[self.x]) == solution[self.y]
        except ReductionException:
            return False

class InEqualityFact(SimpleFact):
    def __str__(self):
        return "Fact<(%s %s) != %s>" % (self.f, self.x, self.y)

    def check(self, solution):
        # print ">>", self
        try:
            return app(solution[self.f], solution[self.x]) != solution[self.y]
        except ReductionException:
            return False

class InFact(SimpleFact):
    def __init__(self, x, y):

        assert isinstance(x, str), "x must be a single symbol"
        self.x = x

        self.y = y
        for yi in y:
            assert isinstance(yi, str), "yi must be a single symbol"

    def __str__(self):
        return "Fact<%s in %s>" % (self.x, set(self.y))

    def dependents(self):
        return [self.x] + self.y # y is not a list of dependent symbols

    def check(self, solution):
        try:
            xr = reduce_combinator(solution[self.x])
        except ReductionException:
            return False

        for r in self.y:
            try:
                if xr == reduce_combinator(solution[r]):
                    return True
            except ReductionException:
                pass

        return False


class PartialEqualityFact(SimpleFact):
    PARTIAL_LEN = 20

    def __str__(self):
        return "Fact<(%s %s) ~= %s>" % (self.f, self.x, self.y)

    def check(self, solution):
        try:  # try this and store the value (partial computation) if we get an exception

            lhs = app(solution[self.f], solution[self.x])
        except ReductionException as r:
            lhs = r.value

        # and now compare the first PARTIAL_LEN characters to the y
        return lhs[:self.PARTIAL_LEN] == self.y




def compute_complexity(defines, facts):
    """ How many remaining searches through combinators do we need?
        Our search is O(compute_complexity(defines, facts))
     """

    defined = set(defines.keys())
    cplx = 0
    for f in facts:
        if isinstance(f, EqualityFact) and f.f in defined and f.x in defined:
            defined.add(f.y) # can push
        else:
            # we face O(dependents) search
            openset = set(f.dependents()) - defined
            cplx += len(openset)
            defined.update(openset)

    return cplx