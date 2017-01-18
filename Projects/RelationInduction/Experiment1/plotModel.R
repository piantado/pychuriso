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
    View(ag)
   
    plt <- ggplot(ag, aes(x=answer, y=probability, fill=as.factor(condition))) +
            geom_bar(stat="identity") + 
            facet_grid(generalization ~ condition)+
            ggtitle(f)
            #ylim(0,1)
    plt     
    ggsave(paste("model_plots/",d$basis[1],".pdf",sep=""), plt)
}




