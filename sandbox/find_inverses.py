"""
    Pre-compute a database of shortest-inverses.
    Invertible combinators then allow us

"""

from pychuriso.combinators import all_combinators
from pychuriso.reduction import app, ReductionException

MAX_INVERSE_DEPTH = 5 # 10
theidentity = '..SKK'

for c in all_combinators(max_depth=18):

    rinv = None

    for c2 in all_combinators(max_depth=MAX_INVERSE_DEPTH):
        try:
            if app(c, c2) == theidentity:
                rinv = c2
                break
        except ReductionException:
            pass

    # NOTE: We cannot find the left inverse (c2 c)=theidentity because there are many such combinators that work for all

    if rinv is not None:
        print c, rinv