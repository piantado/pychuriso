
import re
import sys

for line in sys.stdin:
    line = line.strip()
    
    m = re.search(r"([0-9]+)\s+([0-9]+)\s+([0-9]+)", line)
    if m:
        g = m.groups(None)
        print(line, int(g[1])+int(g[2]))
    else:
        print(line)
        
        
    
    

