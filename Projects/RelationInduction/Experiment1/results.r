results = NULL
for(f in list.files("model-statistics/", full.names=TRUE)) {
  f = read.csv(f, header=TRUE)
  results=rbind(results,f)
}
print(results[results$cor == max(results$cor),])
