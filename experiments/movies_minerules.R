library(arules) # load lib + 
library(methods)
train <- read.csv("output/movies_shortened.csv",header=TRUE, sep = ",", colClasses = "character",  na.strings="0.0", check.names=TRUE) # load csv + 
#train <- na.omit(train) # remove rows with missing data
train <- train[,-match(c("Movie"),names(train))]

#drops <- c("Dbpedia_URL")
#train<-train[,!(names(train) %in% drops)]
#train <- subset( train, select = -c (Dbpedia_URL) ) # remove id column
train <- sapply(train,as.factor) # convert
train <- data.frame(train)
txns <- as(train,"transactions")
rules <- apriori(txns, parameter = list(confidence = 0.51, support= 0.01, minlen= 1, maxlen=5),appearance = list(rhs = c("Label=good", "Label=bad"),default="lhs"))
rules <- sort(rules,by = "confidence") # sort
rules <- as(rules,"data.frame") # convert

write.csv(rules, "output/movies.arules", row.names=TRUE,quote = TRUE)
#R makes changes to some values, replacing # and comma with dot
