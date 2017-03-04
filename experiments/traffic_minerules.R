library(arules) # load lib + 
library(methods)
train <- read.csv("output/traffic_accidents_types.shortened.csv",header=TRUE, sep = ";", colClasses = "character",  na.strings="0.0", check.names=TRUE) # load csv + 
#train <- na.omit(train) # remove rows with missing data
train <- train[,-match(c("DbpediaURL"),names(train))]
train <- train[,-match(c("YagoPermanentlyLocatedEntity"),names(train))]
train <- train[,-match(c("YagoLegalActorGeo"),names(train))]
train <- train[,-match(c("YagoGeoEntity"),names(train))]

#drops <- c("Dbpedia_URL")
#train<-train[,!(names(train) %in% drops)]
#train <- subset( train, select = -c (Dbpedia_URL) ) # remove id column
train <- sapply(train,as.factor) # convert
train <- data.frame(train)
txns <- as(train,"transactions")
rules <- apriori(txns, parameter = list(confidence = 0.5, support= 0.01, minlen= 1, maxlen=5),appearance = list(rhs = c("Label=low", "Label=high"),default="lhs"))
rules <- sort(rules,by = "confidence") # sort
rules <- as(rules,"data.frame") # convert

write.csv(rules, "output/traffic_accidents_types.arules", row.names=TRUE,quote = TRUE)
#R makes changes to some values, replacing # and comma with dot
file.remove( "output/traffic_accidents_types.cleaned.csv")
write.table(train, "output/traffic_accidents_types.cleaned.csv", row.names=FALSE,quote = TRUE, append=FALSE, sep=";")
