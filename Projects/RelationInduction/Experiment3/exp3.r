data = read.csv("../Experiment3/AllConditions/data.csv")
library(ggplot2)
colnames(data) = c("WorkerID","Trial","TimeStamp","Condition","Argument1","Correct","ConditionID","Testarg1","Testarg2","Question","Response","ResponseImage","RT")

fail = data$WorkerID[data$RT<1000]
data=data[data$Argument1!=" Reason",]
data=data[!(data$Trial<8),]
data=data[!(data$WorkerID %in% fail),]
data=droplevels(data)
data$WorkerID=as.numeric(data$WorkerID)
write.csv(data,"exp3data.csv")


plt = ggplot(data,aes(x=Response,fill=ConditionID))+
  geom_histogram()+
  facet_grid(~Question~ConditionID)+
  xlab("Response to Test Question")+
  ggtitle("Distribution of Responses to Test Questions Across Conditions")
plt

ggsave("Exp3.pdf",plt,width=8,height=8)