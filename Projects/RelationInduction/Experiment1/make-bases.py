#all the possible combinations of combinator bases

import itertools
c = "SKITBMWCE"
all = []
for l in range(0,len(c)+1):
    for v in itertools.combinations(list(c),l):
        all.append(''.join(v))
for t in all:
    print t
#print len(all)