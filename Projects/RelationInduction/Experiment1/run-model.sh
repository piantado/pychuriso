for b in 'GSKH' 'GSKHI' 'GSKHIE' 'GBMWCESKHI' 'GSK' 'GSKI' 'GSKIE' 'GBMWC' 'GBMWCE' 'GTSKH' 'GTSKHI' 'GTSKHIE' 'GTBMWCESKHI' 'GTSK' 'GTSKI' 'GTSKIE' 'GTBMWC' 'GTBMWCE' 'SKH' 'SKHI' 'SKHIE' 'BMWCESKHI' 'SK' 'SKI' 'SKIE' 'BMWC' 'BMWCE' 'TSKH' 'TSKHI' 'TSKHIE' 'TBMWCESKHI' 'TSK' 'TSKI' 'TSKIE' 'TBMWC' 'TBMWCE' 
do 
    nohup pypy pure-relations.py --search-basis=$b > model-outputs/$b.txt 2>> err.txt &
done 
               
