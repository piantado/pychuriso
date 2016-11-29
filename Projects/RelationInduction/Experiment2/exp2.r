data = read.csv("../Experiment2/AllConditions/data.csv")
library(ggplot2)

colnames(data) = c("WorkerID","Trial","TimeStamp","Condition","Argument1","Argument2","Correct","ConditionID","Testarg1","Testarg2","Question","Response","ResponseImage","RT")
fail = data$WorkerID[data$RT<1000]
data=data[data$Argument1!=" Reason",]
data=data[data$ConditionID %in% c(" Successor"," ApplytoSelfSame", " ApplytoSelfNew", " ReturnApply"," Not"," Constant"," Symmetry", " ReturnSame"),]
data=data[data$Trial>=8 & data$Trial<=22,]
data=data[!(data$WorkerID %in% fail),]
library(scales)
data=droplevels(data)
plt = ggplot(data,aes(x=Response,fill=ConditionID))+
  geom_histogram()+
  facet_grid(~Question~ConditionID)+
  xlab("Response to Test Question")+
  ggtitle("Distribution of Responses to Test Questions Across Conditions")
plt


plt =ggplot(data, aes(x=Response)) +
  geom_bar(aes(y = ..density..,group=Question,fill = ConditionID)) +
  facet_grid(~Question~ConditionID) +
  ggtitle("Distribution of Responses to Test Questions Across Conditions")+
  ylab("Proportion of Responses")
  #opts(legend.position = "top") +
  #scale_y_continuous(labels = percent_format())
  
plt



ggsave("Exp2.pdf",plt,width=13,height=10)
