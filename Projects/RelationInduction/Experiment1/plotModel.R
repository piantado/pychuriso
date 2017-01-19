library(ggplot2)
library(dplyr)

# B <- "SKH" # which do we plot?


for(f in list.files("model-outputs/", full.names=TRUE)) {
    View(file.info(f)$size)
    d <- read.table(f, header=TRUE)

    # what if our probability was proportional to the runtime
    d$p <- 2**-(d$length-min(d$length)) ## TODO: Fix zero problems

    normalize <- function(x) { x/sum(x)} # fix normalization!

    ## add up prob over hypotheses (rows), then renormalize within generalization,condition
    ag <- d %>% group_by(generalization, condition, answer) %>% summarise(sump=sum(p)) %>% group_by(generalization, condition) %>% mutate(probability=normalize(sump)) %>% as.data.frame()
    View(ag)
    name <- gsub("model-test//","",f)
    name <-gsub(".txt","",name)
    plt <- ggplot(ag, aes(x=answer, y=probability, fill=as.factor(condition))) +
            geom_bar(stat="identity") + 
            facet_grid(generalization ~ condition)+
            ggtitle(name)+
            xlab("Response")+
            ylab("Probability Under the Model")
            #ylim(0,1)
    plt     
    ggsave(paste("model-plots2/",d$basis[1],".pdf",sep=""), plt)
}




