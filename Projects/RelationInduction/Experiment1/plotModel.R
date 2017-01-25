library(ggplot2)
library(plyr)
library(dplyr)

# B <- "SKH" # which do we plot?
human = read.csv("human.csv", header=TRUE)
colnames(human) = c("answer","generalization","probability","condition")

#what does the human data look like?
human$generalization <- gsub(" ","",human$generalization)
humplt = ggplot(human, aes(answer, probability, fill=as.factor(condition)))+
  geom_bar(stat="identity")+
  facet_grid(~generalization~condition)
humplt

#put the human frame into the form of the model frame
hp <- human %>% arrange(generalization) %>% as.data.frame()
hp <- hp[,c(2,4,1,3)]

#initialize the correlations table
correlations = data.frame(Basis=character(),Correlation=double(),Kendall=double())

#inititalize the faceted correlations table
#faceted_cors = data.frame(Basis=character(), Condition = integer(), Generalization = character(),Correlation = double())
faceted_cors = NULL
#go through all the model outputs
for(f in list.files("model-outputs/", full.names=TRUE)) {
    if(!(file.info(f)$size==0)){
      
        d <- read.table(f, header=TRUE)
    
        # what if our probability was proportional to the runtime
        d$p <- 2**-(d$length-min(d$length)) ## TODO: Fix zero problems
    
        normalize <- function(x) { x/sum(x)} # fix normalization!
        
        ## add up prob over hypotheses (rows), then renormalize within generalization,condition
        ag <- d %>% 
          group_by(generalization, condition, answer) %>% 
          summarise(sump=sum(p)) %>% 
          group_by(generalization, condition) %>% 
          mutate(probability=normalize(sump)) %>% 
          as.data.frame()
        
        ag <- ag[!(ag$generalization=="cc"),]
        #clean up the name of the combinator basis
        name <- gsub("model-outputs//","",f)
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
            
            #what about faceted correlations? 
            #if a model prediction is overall kind of crappy because it missed a single condition, 
            #we still want to see how well it did!
            
            #rename ag probability before cbinding
            colnames(ag)[5] <- "modprobability"
            all <- cbind(hp, ag$modprobability)
            colnames(all)[5]="modprobability"
            
            #let's see the correlations for each condition (we could do by generalization also, but then we are dealing with very few points)
            cors <- ddply(na.omit(all), c("condition"), summarise, cor = round(cor(probability, modprobability), 2))
            cors$basis = name
            
            #put together the correlations by condition
            faceted_cors = rbind(faceted_cors,cors)
            
            #now let's compare the model to random
            
            #generate a bunch of randomizations of the human data
            
            
            
      }
        
  }
}

write.csv(correlations,"correlations.csv")
write.csv(faceted_cors,"condition_cors.csv")


#plot the overall correlations
correlations = read.csv("correlations.csv")
correlations$Fill = "Lower than .35"
correlations$Fill[correlations$Kendall>.35]="Higher than .35"

correlations =correlations[order(-correlations$Kendall),]
correlations = correlations[1:100,]
View(correlations)

plt = ggplot(correlations,aes(Basis,Kendall,fill=Fill))+
  geom_bar(stat="identity")+
  theme(axis.text.x = element_text(angle=60, hjust=1))
  
plt
#View(correlations)
ggsave("Correlations.pdf" ,plt,width=10)

#plot the correlations by condition
cond_correlations = read.csv("condition_cors.csv")
cond_correlations =cond_correlations[order(-cond_correlations$cor),]

for(i in 0:4){
 name = paste("cc_",i,sep="")
 m = max(cond_correlations$cor[cond_correlations$condition==i])*.8
 name = cond_correlations[which(cond_correlations$condition==i & cond_correlations$cor>m),]
}
#lists cc_0, cc_1, cc_2, cc_3, cc_4


plotdata <- function(x) {
  ggplot(data = x, aes(x=basis, y=cor)) + 
    geom_bar(stat="identity")+
    facet_grid(~condition)+
    theme(axis.text.x = element_text(angle=60, hjust=1))
  
}


conds = list(cc_0, cc_1, cc_2, cc_3, cc_4)
lapply(conds, plotdata)
plt = ggplot(cond_correlations,aes(basis,cor, fill=as.factor(condition)))+
  geom_bar(stat="identity")+
  facet_grid(~condition)+
  theme(axis.text.x = element_text(angle=60, hjust=1))

plt
ggsave("Correlation_by_Condition.pdf", plt, width=10, height=4)

#we need to test if our model is doing any better than random...
#let's scramble! (shuffles by condition and generalization)
scrambled <- na.omit(human) %>%
             group_by(condition,generalization) %>%
             mutate(probability=sample(probability))
              
#View(scrambled)

humplt = ggplot(scrambled, aes(answer, probability, fill=as.factor(condition)))+
  geom_bar(stat="identity")+
  facet_grid(~generalization~condition)
humplt
