"""
    Pre-compute a database of shortest-inverses.
    Invertible combinators then allow us

"""

from pychuriso.combinators import all_combinators
from pychuriso.reduction import app, ReductionException

MAX_INVERSE_DEPTH = 7 # 10

for c in all_combinators(max_depth=18):

    rinv = None

    for cinv in all_combinators(max_depth=MAX_INVERSE_DEPTH):
        try:
            if app(c, app(cinv, 'x')) == 'x': # we have to have (c (cinv x)) = x, allowing  us to compose cinv and y to get something c will map to y
                rinv = cinv
                break
        except ReductionException:
            pass

    # NOTE: We cannot find the left inverse (c2 c)=theidentity because there are many such combinators that work for all

    if rinv is not None:
        print c, rinv