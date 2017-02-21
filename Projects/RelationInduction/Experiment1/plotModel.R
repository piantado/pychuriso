## TODO:
## When we compute the permuted samples, we should remove the samples that the model was given, probably? These are penalized in randomized samples but are not really penalized for the real sample since there is fitting. 


library(ggplot2)
library(plyr)
library(dplyr)

# B <- "SKH" # which do we plot?
human = read.csv("human.csv", header=TRUE)
colnames(human) = c("x","answer","generalization","human.probability","condition","human.count")
human$generalization <- gsub(" ","",human$generalization)
human$answer <- gsub(" ","",human$answer) # shoot me, there were spaces
human$condition <- as.factor(human$condition)
human$generalization <- as.factor(human$generalization)

#what does the human data look like?
# humplt = ggplot(human, aes(answer, human.probability, fill=as.factor(condition)))+
#   geom_bar(stat="identity")+
#   facet_grid(~generalization~condition)
# humplt

#put the human frame into the form of the model frame
hp <- human %>% arrange(generalization) %>% as.data.frame()
hp <- hp[,c(2,4,1,3,5,6)]
hp$x <- NULL
#initialize the correlations table
correlations = data.frame(Basis=character(),Correlation=double(),Kendall=double())

normalize <- function(x) { x/sum(x, na.rm=TRUE)} # fix normalization!
            
D <- NULL # summary table for the true data
P <- NULL # table of permuted versions
# for(f in c("model-outputs/SKHIE.txt")){#list.files("model-outputs/", full.names=TRUE)) {
for(f in list.files("model-outputs/", full.names=TRUE)) {
for(param in c(0.01, 0.1, 1.0, 10.0, 20.0, 50.0, 100.0)) {

            d <- read.table(gzfile(f), header=TRUE)
            if(nrow(d)==0) { next } 
            d$condition <- as.factor(d$condition)
            
            # what if our probability was proportional to the runtime
#             d$p <- 2**-(1.0*(d$length-min(d$length, na.rm=TRUE))) ## TODO: Fix zero problems
            d$p <- 2**-(param*(d$runtime-min(d$runtime, na.rm=TRUE))) ## TODO: Fix zero problems

            ## add up prob over hypotheses (rows), then renormalize within generalization,condition
            ag <- d %>% 
              group_by(generalization, condition, answer) %>% 
              summarise(sump=sum(p, na.rm=TRUE)) %>% 
              group_by(generalization, condition) %>% 
              mutate(model.probability=normalize(sump)) %>% 
              as.data.frame()
            
            ag <- ag[!(ag$generalization=="cc"),]
            
            #clean up the name of the combinator basis
            name <- gsub("model-outputs//","",f)
            name <-gsub(".txt","",name)
            
            # Merge together
            m <- merge(hp, ag, by=c("generalization", "condition", "answer"), all.x=TRUE, all.y=TRUE)
            m[is.na(m$human.probability),"human.probability"] <- 0 # fix the human zeros -- should not matter since these should have zero count
            m[is.na(m$model.probability),"model.probability"] <- 0 # fix the model zeros
            
            # Let's make a plot with both since its easier to see
            plt <- ggplot(m, aes(x=answer, y=human.probability, fill=condition)) +
                    geom_bar(stat="identity") + 
                    facet_grid(generalization ~ condition)+
                    geom_point(aes(x=answer,y=model.probability)) +
                    ggtitle(name)+
                    xlab("Response")+
                    ylab("Probability Under the Model")
                    #ylim(0,1)
            plt     
            ggsave(paste("model-plots/",d$basis[1],"-", param,".pdf",sep=""), plt)
            

            D <- rbind(D, data.frame(basis=d$basis[1], 
                                     cor=cor.test(m$human.probability, m$model.probability)$estimate,
                                     mse=mean( (m$human.probability-m$model.probability)**2.0, na.rm=TRUE ),
                                     ll=sum(m$human.count*log(m$model.probability*0.99 + 0.01/5.0), na.rm=TRUE),
                                     param=param,
                                     missing= sum(is.na(m$human.probability-m$model.probability))
                                     ))
                           
            # since the data is all loaded, do the permuted version
            # we'll make a column "p" so we can pull out p=1, p=2, etc. to get the different permutations
            # of the entire dataset
            for(n in 1:300) {
                idx <- sample(1:nrow(m)) # shuffle prob and count the same (keeping them paired)
                m$human.probability <- m$human.probability[idx]
                m$human.count <- m$human.count[idx]
                
                # now save the permuted data in P
                P <- rbind(P, data.frame(n=n,  # what permutation are we on?
                                basis=d$basis[1], 
                                cor=cor.test(m$human.probability, m$model.probability)$estimate,
                                mse=mean( (m$human.probability-m$model.probability)**2.0, na.rm=TRUE ),
                                ll=sum(m$human.count*log(m$model.probability*0.99 + 0.01/5.0), na.rm=TRUE),
                                param=param,
                                missing= sum(is.na(m$human.probability-m$model.probability))
                                ))
            }
      }
      
      print(head(D[order(-D$ll),]))
      
}
  
## Now if we want we can process the permutations
## Compute the ll for each permutation (indexed by n)
maxes <- P %>% group_by(n) %>% summarise(ll=max(ll), cor=max(cor), mse=min(mse)) %>% as.data.frame()

# Now a histogram of maxes will show what we want
plt <- ggplot(maxes, aes(x=ll)) +
        geom_histogram() +
        geom_vline(xintercept=max(D$ll), col="red", size=2) # draw a line at the real max

# We could plot the others but we probably want to plot the cor of the max ll, not the max cor, right?
# In that case we need to change above where maxes is defined
