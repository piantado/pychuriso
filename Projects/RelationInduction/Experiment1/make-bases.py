#all the possible combinations of combinator bases

import itertools
import sys
if len(sys.argv)==1: # nothing specified
    c = "SKITBMWCE"
else:   
    c = sys.argv[1]

for l in range(0,len(c)+1):
    for v in itertools.combinations(list(c),l):
        b = ''.join(v)
        if len(b)>0:
            print b 
            
            