results = NULL
for(f in list.files("model-stats/", full.names=TRUE)) {
  f = read.csv(f, header=TRUE)
  results=rbind(results,f)
}

library(ggplot2)
plt = ggplot(results, aes(x=cor)) + 
  geom_density()+
  ggtitle("Distribution of Correlations to Random Data")+
  xlab("Correlation")+
  ylab("Density")+
  theme_bw()+
  facet_wrap(~Data)+
  theme(legend.position="none")

plt


hum <- na.omit(results[results$Data=="Human",])
rand <- results[results$Data=="Random",]
#droplevels(hum$Data)
#droplevels(rand$Data)
best <- hum[hum$cor==max(hum$cor),]
best_ll <- hum[hum$ll==max(hum$ll),]
View(hum[hum$basis=="SKI",])
print(best)
plt = ggplot(rand,aes(x=cor))+
  geom_density()+
  geom_vline(data = hum, aes(xintercept = max(hum$cor),color="red"),linetype="dashed")+
  theme_bw()+
  theme(legend.position="none")
plt
ggsave("cor.pdf",plt)
plt = ggplot(rand,aes(x=ll))+
  geom_density()+
  geom_vline(data = hum, aes(xintercept = max(hum$ll),color="red"),linetype="dashed")+
  theme_bw()+
  theme(legend.position="none")
plt
ggsave("ll.pdf",plt)

