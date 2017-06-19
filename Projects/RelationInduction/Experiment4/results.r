
library(ggplot2)
data = read.csv("data.csv")
data = tail(data,-13049) #where this experiment starts. needed to keep the same participants.db
colnames(data) = c("WorkerID","Trial","TimeStamp","Condition","Argument1","Correct","ConditionID","Testarg1","Testarg2","Question","Response","ResponseImage","RT")
trim <- function (x) gsub("^\\s+|\\s+$", "", x)
data = data[1:13]

data=data[data$Argument1!=" Reason",] #removes self-report
data=data[!(data$Trial<8),] #removes Demographics questions
data=droplevels(data)
data$WorkerID=as.numeric(data$WorkerID) #anonymizes WorkerID
data <- data[,-c(5,6,8,9,12)] #removes the images columns (messy)
data$Response <- trim(data$Response) #clean whitespace
data$Question <- trim(data$Question) #clean whitespace
write.csv(data,"exp4data.csv") #save cleaned data


plt = ggplot(data,aes(x=Response,fill=ConditionID))+
  geom_bar()+
  facet_grid(~Question~ConditionID)+
  xlab("Response to Test Question")+
  ggtitle("Distribution of Responses to Test Questions Across Conditions")
plt

ggsave("Exp4.pdf",plt,width=12,height=8)
