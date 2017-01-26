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
                
                #write out the ag files so we don't have to recompute
                write.csv(ag,paste("ag/output",name))
            
            
        }   
      }
        
  


write.csv(correlations,"correlations.csv")
write.csv(faceted_cors,"condition_cors.csv")


#plot the overall correlations
correlations = read.csv("correlations.csv")
correlations$Legend = "Lower than .4"
correlations$Legend[correlations$Kendall>.4]="Higher than .4"

correlations =correlations[order(-correlations$Kendall),]
correlations = correlations[1:100,]
#View(correlations)

plt = ggplot(correlations,aes(Basis,Kendall,fill=Legend))+
  geom_bar(stat="identity")+
  theme(axis.text.x = element_text(angle=60, hjust=1))
  
plt
ggsave("Correlations.pdf" ,plt,width=10)

#plot the correlations by condition
cond_correlations = read.csv("condition_cors.csv")
cond_correlations =cond_correlations[order(-cond_correlations$cor),]

#generate plots for each condition (plot only bases that do better than .7 of the mean correlation)
for(i in 0:4){
  print(i)
 #name = paste("cc_",i,sep="")
  m = max(cond_correlations$cor[cond_correlations$condition==i])*.7
  #d = cond_correlations[which(cond_correlations$condition==i & cond_correlations$cor>m),]
  print(cond_correlations[which(cond_correlations$condition==i & cond_correlations$cor>m),])
  plt = ggplot(data = cond_correlations[which(cond_correlations$condition==i & cond_correlations$cor>m),], aes(x=basis, y=cor)) + 
     geom_bar(stat="identity")+
     facet_grid(~condition)+
     theme(axis.text.x = element_text(angle=60, hjust=1))
  print(plt)
}
library(dplyr)
cc <- cond_correlations %>%
 
                    group_by(condition) %>%
                    arrange(condition,desc(cor)) %>%
                    top_n(n=10, wt=cor)


plt = ggplot(cc,aes(basis,cor, fill=as.factor(condition)))+
  geom_bar(stat="identity")+
  facet_grid(~condition, scales="free",space="free")+
  
  theme(axis.text.x = element_text(angle=60, hjust=1))

plt
ggsave("Correlation_by_Condition.pdf", plt, width=10, height=4)

maxes = list()
max_ks = list()

for (i in 0:100){
  #initialize the correlations table
  correlations = data.frame(Basis=character(),Correlation=double(),Kendall=double())
  faceted_cors = NULL
  #we need to test if our model is doing any better than random...
  #let's scramble! (shuffles by condition and generalization)
  scrambled <- human %>%
    group_by(condition,generalization) %>%
    mutate(probability=sample(probability))
  
  #now compare all the model bases to this scramble!
  for(f in list.files("ag/", full.names=TRUE)) {
   
      ag <- read.csv(f, header=TRUE)
      
      
      # what if our probability was proportional to the runtime
      
      
        #saving the correlations to a dataframe
        c = cor.test(scrambled$probability,ag$modprobability)
        k = cor.test(scrambled$probability,ag$modprobability,method="kendall")
        
        correlations <-rbind(correlations,data.frame(Basis=name,Correlation=c$estimate, Kendall=k$estimate))
        
        #what about faceted correlations? 
        #if a model prediction is overall kind of crappy because it missed a single condition, 
        #we still want to see how well it did!
        
        
        #let's see the correlations for each condition (we could do by generalization also, but then we are dealing with very few points)
        cors <- ddply(na.omit(all), c("condition"), summarise, cor = round(cor(probability, modprobability), 2))
        cors$basis = name
        
        #put together the correlations by condition
        faceted_cors = rbind(faceted_cors,cors)

  }
  
  m = max(correlations$Correlation)
  mk = max(correlations$Kendall)
  maxes<-append(maxes,m)
  max_ks <-append(max_ks,mk)
      
}

mc = read.csv("MaxCorrelations.csv")
plt = ggplot(mc, aes(x=m)) + geom_density()

mc$Better = FALSE
mc$Better[mc$m > max(correlations$Correlation)] = TRUE

num = length(mc$Better[mc$Better==TRUE]) #number of better than REAL human max correlation
denom = length(mc$Better[mc$Better==FALSE] )#number of worse than REAL human max correlation

num/length(mc$Better)
#0.0990099


mk = read.csv("MaximumKendalls.csv")
plt = ggplot(mk, aes(x=kk)) + geom_density()
plt
mk$Better = FALSE
mk$Better[mk$kk >= max(correlations$Kendall)] = TRUE

numk = length(mk$Better[mk$Better==TRUE]) #number of better than REAL human max correlation
denomk = length(mk$Better[mk$Better==FALSE] )#number of worse than REAL human max correlation

numk/length(mk$Better)
#.03960396
plt = ggplot(correlations, aes(x=Correlation)) + geom_density()
plt


plt = ggplot(correlations, aes(x=Kendall)) + geom_density()
plt

humplt = ggplot(scrambled, aes(answer, probability, fill=as.factor(condition)))+
  geom_bar(stat="identity")+
  facet_grid(~generalization~condition)
humplt
