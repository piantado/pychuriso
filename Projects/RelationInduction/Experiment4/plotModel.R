#!/usr/bin/Rscript

#cat run-args-mini.txt | parallel --jobs 25 "nice -n 0 python pure-relations.py --search-basis='{}' --max-depth=5 --max-find=10000 | Rscript plotModel.R"

## TODO:
## When we compute the permuted samples, we should remove the samples that the model was given, probably? These are penalized in randomized samples but are not really penalized for the real sample since there is fitting. 

library(ggplot2)
library(plyr)
library(dplyr)


d <- read.table(file('stdin','r',blocking=TRUE),header=TRUE)
d$condition <- as.factor(d$condition)
d <- d[!(d$answer=="af"),]
d <- d[!(d$answer=="bf"),]
d <- d[!(d$answer=="cf"),]
d <- d[!(d$answer=="f"),]
d <- d[!(d$answer=="df"),]
d <- d[!(d$answer=="ef"),]
d <- d[!(d$answer==""),]
d$generalization <-gsub("f","",d$generalization) 
stopifnot(nrow(d)>0) #make sure there are more than zero lines 


# B <- "SKH" # which do we plot?
human = read.csv("human.csv", header=TRUE)
colnames(human) = c("x","answer","generalization","human.probability","condition","human.count")
human$generalization <- gsub(" ","",human$generalization)
human$answer <- gsub(" ","",human$answer) # shoot me, there were spaces
human$condition <- as.factor(human$condition)
human$generalization <- as.factor(human$generalization)
#View(human)
print(colnames(human)) 
#make the conditions match with their ID
human$conditionID[human$condition==0]<-"Successor1"
human$conditionID[human$condition==1]<-"Successor2"
human$conditionID[human$condition==2]<-"Constant1"
human$conditionID[human$condition==3]<-"Constant2"
human$conditionID[human$condition==4]<-"Identity1"
human$conditionID[human$condition==5]<-"Identity2"
human$conditionID[human$condition==6]<-"Symmetry1"
human$conditionID[human$condition==7]<-"Symmetry2"

#so if your proportions are e.g. [0.1, 0.6, 0.3], then you will have a binomial test of 0.1 -vs- 0.6+0.3=0.9
#and the next error bar will be 0.6 -vs- 0.1+0.3=0.4
#so it just that bar vs everything else

test <- function(x,n){
  print(x)
  binom.test(x, n, p=.5,alternative="two-sided")}
human <-human %>%
  group_by(condition,generalization)%>%
  mutate(sumofothers=sum(human.count)-human.count,
         t=human.count)%>%
  group_by(condition,generalization,answer)%>%
 mutate(conf_low=binom.test(c(t,(sumofothers)))$conf.int[1],
         conf_high=binom.test(c(t,(sumofothers)))$conf.int[2])
human$conf_high[is.na(human$human.probability)]=0


plt = ggplot(human,aes(answer,human.probability,fill=conditionID))+
  geom_bar(stat="identity")+
  geom_linerange(aes(x=answer,y=human.probability,fill=conditionID,ymin=conf_low,ymax=conf_high))+
  facet_grid(generalization ~ conditionID)+
  geom_rect(data = subset(human,((human$condition==0 & human$generalization=='b')|(human$condition==2 & human$generalization=='b')|(human$condition==4 & human$generalization=='b')|(human$condition==6 & human$generalization=='b')|(human$condition==1 & human$generalization=='c')|(human$condition==5 & human$generalization=='c')|(human$condition==7 & human$generalization=='c')|(human$condition==3 & human$generalization=='c')|(human$condition==3 & human$generalization=='d'))),aes(fill = conditionID),xmin = -Inf,xmax = Inf,
            ymin = -Inf,ymax = Inf,alpha = 0.1)+
  
  theme_bw()+
  xlab("Response")+
  ylab("Probability of Response")+
  guides(fill=FALSE)+
  scale_fill_manual(values = c("Successor1"="gray", "Successor2"="gray", "Constant1"="gray",  "Constant2"="gray",  "Identity1" ="gray",
                               "Identity2" ="gray", "Symmetry1"="gray",  "Symmetry2"="gray"))
  
plt
ggsave("human_results.pdf",plt)
View(human)

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
  
  colnames(d)<-c("condition", "nsolution", "basis", "generalization", "runtime", "length", "answer")
  d <- d[1:7]
 # print(colnames(d))
  if(nrow(d)==0) { next } # move on if empty
  d$condition <- as.factor(d$condition)
  d$generalization<-as.factor(d$generalization)
  d$answer<-as.factor(d$answer)
  d$runtime<-as.numeric(d$runtime)
  d$length <-as.numeric(d$length)
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
  
  
  
  # Merge together
  m <- merge(hp, ag, by=c("generalization", "condition", "answer"), all.x=TRUE, all.y=TRUE)
  m[is.na(m$human.probability),"human.probability"] <- 0 # fix the human zeros -- should not matter since these should have zero count
  m[is.na(m$model.probability),"model.probability"] <- 0 # fix the model zeros
  
  #make the conditions match with their ID
  m$conditionID[m$condition==0]<-"Successor1"
  m$conditionID[m$condition==1]<-"Successor2"
  m$conditionID[m$condition==2]<-"Constant1"
  m$conditionID[m$condition==3]<-"Constant2"
  m$conditionID[m$condition==4]<-"Identity1"
  m$conditionID[m$condition==5]<-"Identity2"
  m$conditionID[m$condition==6]<-"Symmetry1"
  m$conditionID[m$condition==7]<-"Symmetry2"
  m$model.probability[m$model.probability==0 & m$human.probability==0]<-NA
 # m<-m[(m$condition==0 & m$generalization=='b')|(m$condition==2 & m$generalization=='b')|(m$condition==4 & m$generalization=='b')|(m$condition==6 & m$generalization=='b')|(m$condition==1 & m$generalization=='c')|(m$condition==5 & m$generalization=='c')|(m$condition==7 & m$generalization=='c')|(m$condition==3 & m$generalization=='c')|(m$condition==3 & m$generalization=='d'),]
  
  # Let's make a plot with both since its easier to see
  plt <- ggplot(m, aes(x=answer, y=human.probability, fill=conditionID)) +
    geom_bar(stat="identity") + 
    facet_grid(generalization ~ conditionID)+
    geom_point(aes(x=answer,y=model.probability)) +
    geom_rect(data = subset(m,((m$condition==0 & m$generalization=='b')|(m$condition==2 & m$generalization=='b')|(m$condition==4 & m$generalization=='b')|(m$condition==6 & m$generalization=='b')|(m$condition==1 & m$generalization=='c')|(m$condition==5 & m$generalization=='c')|(m$condition==7 & m$generalization=='c')|(m$condition==3 & m$generalization=='c')|(m$condition==3 & m$generalization=='d'))),aes(fill = conditionID),xmin = -Inf,xmax = Inf,
              ymin = -Inf,ymax = Inf,alpha = 0.1)+
    ggtitle(d$basis[1])+
    xlab("Response")+
    ylab("Probability of Response")+
    guides(fill=FALSE)+
    theme_bw()+
    scale_fill_manual(values = c("Successor1"="gray", "Successor2"="gray", "Constant1"="gray",  "Constant2"="gray",  "Identity1" ="gray",
                                 "Identity2" ="gray", "Symmetry1"="gray",  "Symmetry2"="gray"))
  plt
 
  
 
  
  ggsave(paste("model-plots/",d$basis[1],"-", param,".pdf",sep=""), plt)
  D <- rbind(D, data.frame(basis=d$basis[1], 
                           cor=cor.test(m$human.probability, m$model.probability)$estimate,
                           mse=mean( (m$human.probability-m$model.probability)**2.0, na.rm=TRUE ),
                           ll=sum(m$human.count*log(m$model.probability*0.99 + 0.01/5.0), na.rm=TRUE),
                           param=param,
                           missing= sum(is.na(m$human.probability-m$model.probability))
  ))
 # print(str(D)) 
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
#print(str(D))
#print(str(P))
}
#print(colnames(P))
P$Data = "Random"
D$n = seq.int(nrow(D))
D$Data = "Human"
D <- D[,c(7, 1,2,3,4,5,6,8)]
#print(head(D))
final = rbind(P,D)
print(head(final[order(-final$cor),]))




write.csv(final,paste("model-stats/",final$basis[1], sep=""))

