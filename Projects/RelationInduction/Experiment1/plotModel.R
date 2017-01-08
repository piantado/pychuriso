library(ggplot2)
library(dplyr)

# B <- "SKH" # which do we plot?


for(f in list.files("model-outputs/", full.names=TRUE)) {
    d <- read.table(f, header=TRUE)

    # what if our probability was proportional to the runtime
    d$p <- 2**-(d$length-min(d$length)) ## TODO: Fix zero problems

    normalize <- function(x) { x/sum(x)} # fix normalization!

    ## add up prob over hypotheses (rows), then renormalize within generalization,condition
    ag <- d %>% group_by(generalization, condition, answer) %>% summarise(sump=sum(p)) %>% group_by(generalization, condition) %>% mutate(probability=normalize(sump)) %>% as.data.frame()


    plt <- ggplot(ag, aes(x=answer, y=probability)) +
            geom_point() + 
            facet_grid(generalization ~ condition)
            
    ggsave(paste(d$basis[1],".pdf",sep=""), plt)
}




