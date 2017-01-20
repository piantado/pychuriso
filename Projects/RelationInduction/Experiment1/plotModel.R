library(ggplot2)
library(dplyr)

# B <- "SKH" # which do we plot?
human = read.csv("human.csv")

#what does the human data look like?
human$generalization <- gsub(" ","",human$generalization)
humplt = ggplot(human, aes(answer, probability, fill=as.factor(condition)))+
  geom_bar(stat="identity")+
  facet_grid(~generalization~condition)
humplt

#put the human frame into the form of the model frame
hp <- human %>% arrange(generalization) %>% as.data.frame()

#initialize the correlations table
correlations = data.frame(Basis=character(),Correlation=double(),Kendall=double())


#go through all the model outputs
for(f in list.files("MetropolisResults/model-outputs/", full.names=TRUE)) {
    if(!(file.info(f)$size==0)){
      
        d <- read.table(f, header=TRUE)
    
        # what if our probability was proportional to the runtime
        d$p <- 2**-(d$length-min(d$length)) ## TODO: Fix zero problems
    
        normalize <- function(x) { x/sum(x)} # fix normalization!
    
        ## add up prob over hypotheses (rows), then renormalize within generalization,condition
        ag <- d %>% group_by(generalization, condition, answer) %>% summarise(sump=sum(p)) %>% group_by(generalization, condition) %>% mutate(probability=normalize(sump)) %>% as.data.frame()
        ag <- ag[!(ag$generalization=="cc"),]
        #clean up the name of the combinator basis
        name <- gsub("MetropolisResults/model-outputs//","",f)
        name <-gsub(".txt","",name)
        
        if(length(hp$probability)==length(ag$probability)){
            plt <- ggplot(ag, aes(x=answer, y=probability, fill=as.factor(condition))) +
                    geom_bar(stat="identity") + 
                    facet_grid(generalization ~ condition)+
                    ggtitle(name)+
                    xlab("Response")+
                    ylab("Probability Under the Model")
                    #ylim(0,1)
            plt     
            ggsave(paste("model-plots/",d$basis[1],".pdf",sep=""), plt)
            #saving the correlations to a dataframe
            c = cor.test(hp$probability,ag$probability)
            k = cor.test(hp$probability,ag$probability,method="kendall")
            
            correlations <-rbind(correlations,data.frame(Basis=name,Correlation=c$estimate, Kendall=k$estimate))
            View(correlations)
      }
        
  }
}

write.csv(correlations,"correlations.csv")
correlations = read.csv("correlations.csv")
correlations$Fill = "Lower than .35"
correlations$Fill[correlations$Kendall>.35]="Higher than .35"

correlations =correlations[order(-correlations$Kendall),]
correlations = correlations[1:50,]

plt = ggplot(correlations,aes(Basis,Kendall,fill=Fill))+
  geom_bar(stat="identity")+
  theme(axis.text.x = element_text(angle=60, hjust=1))
  
plt


