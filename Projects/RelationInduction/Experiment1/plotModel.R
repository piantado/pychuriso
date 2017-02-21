#!/usr/bin/Rscript

#cat run-args-mini.txt | parallel --jobs 25 "nice -n 0 python pure-relations.py --search-basis='{}' --max-depth=5 --max-find=10000 | Rscript plotModel.R"

## TODO:
## When we compute the permuted samples, we should remove the samples that the model was given, probably? These are penalized in randomized samples but are not really penalized for the real sample since there is fitting. 

library(ggplot2)
library(plyr)
library(dplyr)

d <- read.table(file('stdin','r'), header=TRUE)

stopifnot(nrow(d)>0) #make sure there are more than zero lines 


# B <- "SKH" # which do we plot?
human = read.csv("human.csv", header=TRUE)
colnames(human) = c("x","answer","generalization","human.probability","condition","human.count")
human$generalization <- gsub(" ","",human$generalization)
human$answer <- gsub(" ","",human$answer) # shoot me, there were spaces
human$condition <- as.factor(human$condition)
human$generalization <- as.factor(human$generalization)

#put the human frame into the form of the model frame
hp <- human %>% arrange(generalization) %>% as.data.frame()
hp <- hp[,c(2,4,1,3,5,6)]
hp$x <- NULL

normalize <- function(x) { x/sum(x, na.rm=TRUE)} # fix normalization!
            
D <- NULL # summary table for the true data
P <- NULL # table of permuted versions

#take each file from stdin and process it, outputting into model-statistics/


#seem to do best with param = 1
for(param in c(0.1, 0.5, 0.75, 0.9, 1, 1.1, 1.25, 1.5, 2.0)) {

            #d <- read.table(f, header=TRUE)
            if(nrow(d)==0) { next } # move on if empty
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
            
            # Merge together
            m <- merge(hp, ag, by=c("generalization", "condition", "answer"), all.x=TRUE, all.y=TRUE)
            m[is.na(m$human.probability),"human.probability"] <- 0 # fix the human zeros -- should not matter since these should have zero count
            m[is.na(m$model.probability),"model.probability"] <- 0 # fix the model zeros
            
            # Let's make a plot with both since its easier to see
            plt <- ggplot(m, aes(x=answer, y=human.probability, fill=condition)) +
                    geom_bar(stat="identity") + 
                    facet_grid(generalization ~ condition)+
                    geom_point(aes(x=answer,y=model.probability)) +
                    ggtitle(d$basis[1])+
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
                                rcor=cor.test(m$human.probability, m$model.probability)$estimate,
                                rmse=mean( (m$human.probability-m$model.probability)**2.0, na.rm=TRUE ),
                                rll=sum(m$human.count*log(m$model.probability*0.99 + 0.01/5.0), na.rm=TRUE),
                                param=param,
                                rmissing= sum(is.na(m$human.probability-m$model.probability))
                                ))
            }
}
     
      colnames(P) <- c("x","basis","p_cor","p_mse","p_ll","param","missing")
      
      
      #merge together to have an output for 
      final = merge(P,D, by=c("basis", "param", "missing"), all.x=TRUE, all.y=TRUE)
      print(head(final[order(-final$ll),]))
      


write.csv(final,paste("model-statistics/",final$basis[1], sep=""))

