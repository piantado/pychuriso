library(ggplot2)
data = read.csv("../Experiment1/PR4/data.csv")
View(data)
colnames(data) = c("WorkerID","Trial","TimeStamp","Condition","Argument1","Argument2","Correct","ConditionID","Testarg1","Testarg2","Question","Response","ResponseImage","RT")
data=data[-c(1:90),]
fail = data$WorkerID[data$RT<1000]
data=data[data$Argument1!=" Reason",]


data=data[!(data$WorkerID %in% fail),]

data=droplevels(data)
data$WorkerID=as.numeric(data$WorkerID)
write.csv(data,"exp1data.csv")


plt =ggplot(data, aes(x=Response)) +
  geom_bar(aes(y = ..density..,group=Question,fill = ConditionID)) +
  facet_grid(~Question~ConditionID) +
  ggtitle("Distribution of Responses to Test Questions Across Conditions")+
  ylab("Proportion of Responses")


plt
ggsave("Exp1.pdf",plt,width=8,height=7)


plt = ggplot(data,aes(Question,RT))+
  stat_summary(fun.y=mean,geom="point")+
  facet_wrap(~ConditionID)
plt



listy = list()
data <- read.csv("exp1data.csv",header=TRUE)
for(val in c(0,1,2,3,4)){
  t = table(data$Response[data$Condition==val],data$Question[data$Condition==val])
  tp = prop.table(t,2)
  frame = as.data.frame(tp)
  frame$cond = val
  t = as.data.frame(t)
  frame = cbind(frame,t$Freq)
  listy[[val+1]] = frame
 
}
humanframe = do.call(rbind,listy)
colnames(humanframe) <- c("Response","Question","Proportion","Condition","Frequency")
View(humanframe)

write.csv(humanframe,"human.csv")