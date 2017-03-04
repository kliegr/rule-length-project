#http://www.ats.ucla.edu/stat/r/dae/ologit.htm
#http://www.ats.ucla.edu/stat/stata/output/stata_ologit_output.htm
#http://r.789695.n4.nabble.com/No-P-values-in-polr-summary-td4678547.html
require(MASS)
library(AER)


args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  inputfile="stats/datafiles/V2-e11-mushrooms.csv"
} else if (length(args)==1) {
  # default output file
  inputfile = args[1]  
}
cat("using",inputfile,"\n")
cf = read.csv(inputfile,sep=",")
cf$target= factor(cf$target,levels=c("-2","-1","0","1","2"), ordered=TRUE)
#do all except length analysis on arules data only, because inverted heuristics has many missing features
#cfArulesOnly <- cf[!(cf$tag == "dfInvertedHeuristicsOther" | cf$tag == "dfInvertedHeuristicsLargeDiffInRuleLen" | cf$tag == "dfInvertedHeuristics"), ]

evaluateModel <- function(m,filteredCF)
{
  if(length(coefficients(m))==0) {
   return ("NA")
   }
  pred1=predict(m, filteredCF, type = "class")
  pred1=factor(pred1,levels=c("-2","-1","0","1","2"), ordered=TRUE)  
  accuracy=sum(pred1!=filteredCF$target)/length(cf$target)
  cat("resubstitution error (on non missing)", accuracy,"\n")
  return(accuracy)
}

modelDetails <- function(m,filteredCF)
{
  print(summary(m))
  if(length(coefficients(m))==0) {   
   return ("NA")
   }
  (ctable <- coef(summary(m)))
  p <- pnorm(abs(ctable[, "t value"]), lower.tail = FALSE) * 2
  (ctable <- cbind(ctable, "p value" = p))
  (ci <- confint(m))
  print(ci)
  isSignifcant=((ci[1] < 0) && (ci[2]<0)) | ((ci[1] > 0) && (ci[2]>0)) # is isSignificant if CI does not include 0
  cat("coefficient interval does not cross zero", isSignifcant, '\n')
  #http://r.789695.n4.nabble.com/No-P-values-in-polr-summary-td4678547.html
  print(coeftest(m)) #AER package
   
  evaluateModel(m,filteredCF)
  return(isSignifcant)
}


modelDetailsMultiVariate <- function(m,filteredCF)
{
  print(summary(m))
  if(length(coefficients(m))==0) {
   return ("NA")
   }
  (ctable <- coef(summary(m)))
  p <- pnorm(abs(ctable[, "t value"]), lower.tail = FALSE) * 2
  (ctable <- cbind(ctable, "p value" = p))
  (ci <- confint(m))
  print(ci)
  print(coeftest(m)) #AER package   
  return(evaluateModel(m,filteredCF))
  
}
# DELTAS #

  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ lenDelta, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$lenDelta),])
  cat(paste(inputfile,"lenDelta",coefficients(m)[1],coeftest(m)[1,4],"",nrow(na.omit(cf)),"Logistic regression", sep = ","),file="summary.csv",append=TRUE, sep="\n")},error=function(e){})

  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ LitImpMaxDelta, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$LitImpMaxDelta),])
  cat(paste(inputfile,"LitImpMaxDelta",coefficients(m)[1],coeftest(m)[1,4],"",nrow(na.omit(cf)),"Logistic regression", sep = ","),file="summary.csv",append=TRUE, sep="\n")},error=function(e){})
  
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ LitImpMinDelta, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$LitImpMinDelta),])
  cat(paste(inputfile,"LitImpMinDelta",coefficients(m)[1],coeftest(m)[1,4],"",nrow(na.omit(cf)),"Logistic regression", sep = ","),file="summary.csv",append=TRUE, sep="\n")},error=function(e){})
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ LitImpAvgDelta, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$LitImpAvgDelta),])
  cat(paste(inputfile,"LitImpAvgDelta",coefficients(m)[1],coeftest(m)[1,4],"",nrow(na.omit(cf)),"Logistic regression", sep = ","),file="summary.csv",append=TRUE, sep="\n")},error=function(e){})



  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ AttImpMaxDelta, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$AttImpMaxDelta),])
  cat(paste(inputfile,"AttImpMaxDelta",coefficients(m)[1],coeftest(m)[1,4],"",nrow(na.omit(cf)),"Logistic regression", sep = ","),file="summary.csv",append=TRUE, sep="\n")},error=function(e){})
  
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ AttImpSumDelta, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$AttImpSumDelta),])
  cat(paste(inputfile,"AttImpMaxDelta",coefficients(m)[1],coeftest(m)[1,4],"",nrow(na.omit(cf)),"Logistic regression", sep = ","),file="summary.csv",append=TRUE, sep="\n")},error=function(e){})  

  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ AttImpMinDelta, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$AttImpMinDelta),])
  cat(paste(inputfile,"AttImpMinDelta",coefficients(m)[1],coeftest(m)[1,4],"",nrow(na.omit(cf)),"Logistic regression", sep = ","),file="summary.csv",append=TRUE, sep="\n")},error=function(e){})
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ AttImpAvgDelta, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$AttImpAvgDelta),])
  cat(paste(inputfile,"AttImpAvgDelta",coefficients(m)[1],coeftest(m)[1,4],"",nrow(na.omit(cf)),"Logistic regression", sep = ","),file="summary.csv",append=TRUE, sep="\n")},error=function(e){})
  


  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ DepthMaxDelta, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$lenDelta),])
  cat(paste(inputfile,"DepthMaxDelta",coefficients(m)[1],coeftest(m)[1,4],"",nrow(na.omit(cf)),"Logistic regression", sep = ","),file="summary.csv",append=TRUE, sep="\n")},error=function(e){})

  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ DepthMinDelta, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$DepthMinDelta),])
  cat(paste(inputfile,"DepthMinDelta",coefficients(m)[1],coeftest(m)[1,4],"",nrow(na.omit(cf)),"Logistic regression", sep = ","),file="summary.csv",append=TRUE, sep="\n")},error=function(e){})



  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ LabelLengthSumDelta, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$LabelLengthSumDelta),])
  cat(paste(inputfile,"LabelLengthSumDelta",coefficients(m)[1],coeftest(m)[1,4],"",nrow(na.omit(cf)),"Logistic regression", sep = ","),file="summary.csv",append=TRUE, sep="\n")},error=function(e){})

  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ LabelLengthMaxDelta, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$LabelLengthMaxDelta),])
  cat(paste(inputfile,"LabelLengthMaxDelta",coefficients(m)[1],coeftest(m)[1,4],"",nrow(na.omit(cf)),"Logistic regression", sep = ","),file="summary.csv",append=TRUE, sep="\n")},error=function(e){})

  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ LabelLengthAvgDelta, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$LabelLengthAvgDelta),])
  cat(paste(inputfile,"LabelLengthAvgDelta",coefficients(m)[1],coeftest(m)[1,4],"",nrow(na.omit(cf)),"Logistic regression", sep = ","),file="summary.csv",append=TRUE, sep="\n")},error=function(e){})

  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ LabelLengthMinDelta, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$LabelLengthMinDelta),])
  cat(paste(inputfile,"LabelLengthMinDelta",coefficients(m)[1],coeftest(m)[1,4],"",nrow(na.omit(cf)),"Logistic regression", sep = ","),file="summary.csv",append=TRUE, sep="\n")},error=function(e){})



  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ MinDistanceDelta, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$MinDistanceDelta),])
  cat(paste(inputfile,"MinDistanceDelta",coefficients(m)[1],coeftest(m)[1,4],"",nrow(na.omit(cf)),"Logistic regression", sep = ","),file="summary.csv",append=TRUE, sep="\n")},error=function(e){})
  
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ MaxDistanceDelta, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$MaxDistanceDelta),])
  cat(paste(inputfile,"MaxDistanceDelta",coefficients(m)[1],coeftest(m)[1,4],"",nrow(na.omit(cf)),"Logistic regression", sep = ","),file="summary.csv",append=TRUE, sep="\n")},error=function(e){})
  

  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ MinDepthLCSDelta, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$MinDepthLCSDelta),])
  cat(paste(inputfile,"MinDepthLCSDelta",coefficients(m)[1],coeftest(m)[1,4],"",nrow(na.omit(cf)),"Logistic regression", sep = ","),file="summary.csv",append=TRUE, sep="\n")},error=function(e){})
  
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ PageRankMaxDelta, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$PageRankMaxDelta),])
  cat(paste(inputfile,"PageRankMaxDelta",coefficients(m)[1],coeftest(m)[1,4],"",nrow(na.omit(cf)),"Logistic regression", sep = ","),file="summary.csv",append=TRUE, sep="\n")},error=function(e){})
  
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ PageRankMinDelta, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$PageRankMinDelta),])
  cat(paste(inputfile,"PageRankMinDelta",coefficients(m)[1],coeftest(m)[1,4],"",nrow(na.omit(cf)),"Logistic regression", sep = ","),file="summary.csv",append=TRUE, sep="\n")},error=function(e){})
  
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ PageRankAvgDelta, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$PageRankAvgDelta),])
  cat(paste(inputfile,"PageRankAvgDelta",coefficients(m)[1],coeftest(m)[1,4],"",nrow(na.omit(cf)),"Logistic regression", sep = ","),file="summary.csv",append=TRUE, sep="\n")},error=function(e){})
  
      
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ ConfDelta, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$ConfDelta),])
  cat(paste(inputfile,"ConfDelta",coefficients(m)[1],coeftest(m)[1,4],"",nrow(na.omit(cf)),"Logistic regression", sep = ","),file="summary.csv",append=TRUE, sep="\n")},error=function(e){})
   
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ SuppDelta, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$SuppDelta),])
  cat(paste(inputfile,"SuppDelta",coefficients(m)[1],coeftest(m)[1,4],"",nrow(na.omit(cf)),"Logistic regression", sep = ","),file="summary.csv",append=TRUE, sep="\n")},error=function(e){})
  
  
#  ALL
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")  
  #not including cf$MaxDistanceDelta, cf$MinDepthLCSDelta because they would be removed anyway, and the predict function would not work on the model   
  filteredCF= cf[!is.na(cf$lenDelta) & !is.na(cf$DepthMaxDelta)& !is.na(cf$LabelLengthAvgDelta)  & !is.na(cf$DepthMinDelta) & !is.na(cf$LabelLengthMaxDelta) & !is.na(cf$MinDistanceDelta)& !is.na(cf$PageRankMaxDelta) & !is.na(cf$PageRankMinDelta) & !is.na(cf$PageRankAvgDelta)  & !is.na(cf$SuppDelta)  & !is.na(cf$ConfDelta) & !is.na(cf$LitImpMaxDelta) & !is.na(cf$LitImpMinDelta) & !is.na(cf$LitImpAvgDelta),]    
  # some degenerate variables were removed causing modelDetailsMultiVariate to fail
  m <- polr(target ~ lenDelta + LabelLengthAvgDelta  + LabelLengthMaxDelta  +  PageRankMinDelta  + PageRankAvgDelta + SuppDelta  + ConfDelta, data = filteredCF, Hess=TRUE)
  modelDetailsMultiVariate(m,filteredCF)},error=function(e){})

# RATIOS #
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ lenRatio, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$lenRatio),])},error=function(e){})
  
  
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ LitImpMaxRatio, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$LitImpMaxRatio),])},error=function(e){})
  
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ LitImpMinRatio, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$LitImpMinRatio),])},error=function(e){})
  
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ LitImpAvgRatio, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$LitImpAvgRatio),])},error=function(e){})
    
    
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ DepthMaxRatio, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$DepthMaxRatio),])},error=function(e){})
  
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ DepthMinRatio, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$DepthMinRatio),])},error=function(e){})
  

  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ LabelLengthMaxRatio, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$LabelLengthMaxRatio),])},error=function(e){})
  
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ LabelLengthAvgRatio, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$LabelLengthAvgRatio),])},error=function(e){})
  
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ LabelLengthMinRatio, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$LabelLengthMinRatio),])},error=function(e){})
  

  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ MinDistanceRatio, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$MinDistanceRatio),])},error=function(e){})
  
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ MaxDistanceRatio, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$MaxDistanceRatio),])},error=function(e){})
  
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ MinDepthLCSRatio, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$MinDepthLCSRatio),])},error=function(e){})
  

  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ PageRankMaxRatio, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$PageRankMaxRatio),])},error=function(e){})
  
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ PageRankMinRatio, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$PageRankMinRatio),])},error=function(e){})
  
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ PageRankAvgRatio, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$PageRankAvgRatio),])},error=function(e){})

  
  
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ ConfRatio, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$ConfRatio),])},error=function(e){})
   
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
  m <- polr(target ~ SuppRatio, data = cf, na.action=na.omit, Hess=TRUE)
  isS = modelDetails(m,cf[!is.na(cf$SuppRatio),])},error=function(e){})
  
  
#  ALL
  tryCatch({cat("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")

  #not including cf$DepthMaxRatio, cf$MinDistanceRatio, cf$MaxDistanceRatio, cf$MinDepthLCSRatio  because they would be removed anyway, and the predict function would not work on the model     
  filteredCF= cf[!is.na(cf$lenRatio) & !is.na(cf$DepthMinRatio)& !is.na(cf$LabelLengthAvgDelta)  & !is.na(cf$LabelLengthMaxRatio)& !is.na(cf$PageRankMaxRatio) & !is.na(cf$PageRankMinRatio) & !is.na(cf$PageRankAvgRatio) & !is.na(cf$SuppRatio) & !is.na(cf$ConfRatio)& !is.na(cf$LitImpMaxRatio) & !is.na(cf$LitImpMinRatio) & !is.na(cf$LitImpAvgRatio) ,]},error=function(e){})

  # some degenerate variables were removed causing modelDetailsMultiVariate to fail
  tryCatch({
  m <- polr(target ~ lenRatio   + LabelLengthMaxRatio +  LabelLengthAvgDelta  + PageRankMinRatio + PageRankAvgRatio + SuppRatio + ConfRatio, data = filteredCF, na.action=na.omit, Hess=TRUE)
  modelDetailsMultiVariate(m,filteredCF)},error=function(e){})
  
  cat("total number of rows",nrow(cf),"\n")  
  cat("the resubstitution error of most frequent class",1-max(table(cf$target)/nrow(cf)),"\n")

#
