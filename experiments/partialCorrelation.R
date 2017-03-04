library(ppcor)

args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  inputfile="stats/datafiles/V2-e8-quality.csv"  
  #outputfile = "output/mergedRegressionInput.out"  
} else if (length(args)==1) {
  # default output file
  inputfile = args[1]
}
cat("using",inputfile,"\n")


cf = read.csv(inputfile,sep=",")

normalCorr <- function(xname,yname)
{
	if (!(xname %in% colnames(data)))
	{
	  cat(xname,"not found, skipping\n")
	  return("")
	}
	cat("\n\noriginal rows:",nrow(data),"\n")
	dataF<-na.omit(data[,append(xname,yname)])
	cat("removed rows with missing, now rows:",nrow(dataF),"\n")

	x<-dataF[,xname]
	y<-dataF[,yname]
	x<-as.numeric(as.character(x))
	y<-as.numeric(as.character(y))

	
	cat("x:",xname,"\n")
	cat("y:",yname,"\n")

	

	result=cor.test(x,y,method="spearman",exact=FALSE)	
	cat(paste(inputfile,xname,result$estimate,result$p.value,"",nrow(dataF),"Spearman R", sep = ","),file="summary.csv",append=TRUE, sep="\n")
	print ("Spearman")
	print (result)

	result=cor.test(x,y,method="kendall")
	cat(paste(inputfile,xname,result$estimate,result$p.value,"",nrow(dataF),"Kendall R", sep = ","),file="summary.csv",append=TRUE, sep="\n")
	print ("Kendall")
	print (result)

}
partialCorr <- function(xname,yname,controlNames)
{
	if (!(xname %in% colnames(data)))
	{
	  cat(xname,"not found, skipping\n")
	  return("")
	}
	#remove any control names that are not present in the data frame
	NcontrolNames=intersect(controlNames, colnames(data))
	if (length(NcontrolNames)==0)
	{
		return ()
	}
	cat("\n\noriginal rows:",nrow(data),"\n")
	dataF<-na.omit(data[,append(append(xname,yname),NcontrolNames)])
	cat("removed rows with missing, now rows:",nrow(dataF),"\n")

	x<-dataF[,xname]
	y<-dataF[,yname]
	control<-subset(dataF, select=NcontrolNames)
	cat("x:",xname,"\n")
	cat("y:",yname,"\n")
	cat("control:",NcontrolNames,"\n")
	result=pcor.test(x,y,control,method="spearman")	
	cat(paste(inputfile,xname,result$estimate,result$p.value,paste("\"Controlling for: ",toString(NcontrolNames),"\""),nrow(dataF),"Partial Correlation (Spearman)", sep = ","),file="summary.csv",append=TRUE, sep="\n")
	print ("partial")
	print (result)
	result=spcor.test(x,y,control,method="spearman")	
	cat(paste(inputfile,xname,result$estimate,result$p.value,paste("\"Controlling for: ",toString(NcontrolNames),"\""),nrow(dataF),"Semi-partial Correlation (Spearman)", sep = ","),file="summary.csv",append=TRUE, sep="\n")
	print ("semi partial - Spearman")
	print (result)

	#Kendall has some advantage over Spearman http://stats.stackexchange.com/questions/3943/kendall-tau-or-spearmans-rho
	#And it is possible to apply it in case of ties 
	result=spcor.test(x,y,control,method="kendall")	
	cat(paste(inputfile,xname,result$estimate,result$p.value,paste("\"Controlling for: ",toString(NcontrolNames),"\""),nrow(dataF),"Semi-partial Correlation (Kendall)", sep = ","),file="summary.csv",append=TRUE, sep="\n")	
	print ("semi partial - Kendall ")
	print (result)


}


cf$target= factor(cf$target,levels=c("-2","-1","0","1","2"), ordered=TRUE)

cols=c("target","lenDelta","DepthMaxDelta","DepthMinDelta","LabelLengthMaxDelta","LabelLengthMinDelta","LabelLengthAvgDelta","MaxDistanceDelta","MinDepthLCSDelta","PageRankMaxDelta","PageRankMinDelta","PageRankAvgDelta","ConfDelta","SuppDelta","LitImpMaxDelta","LitImpMinDelta","LitImpAvgDelta","AttImpMaxDelta","AttImpMinDelta","AttImpAvgDelta","AttImpSumDelta","AttImpSumDelta","AttImpSumRatio","LitImpSumDelta","LitImpSumRatio")
existingCols=intersect(cols, colnames(cf))
cols=intersect(cols, colnames(cf))
data=cf[,existingCols]

allVars<-cols[-1]


for (i in 1:length(allVars)) {	
	tryCatch(normalCorr(c(allVars[i]),c("target")),error=function(e){})
	
	for (j in 1:length(allVars)) {	
		if (i!=j) {		
			tryCatch(partialCorr(c(allVars[i]),c("target"),allVars[j]),error=function(e){})
		}
	}
}

#Try without PageRank, it may not be available
tryCatch(partialCorr(c("lenDelta"),c("target"),c("AttImpMinDelta","LitImpMinDelta")),error=function(e){})
tryCatch(partialCorr(c("lenDelta"),c("target"),c("AttImpAvgDelta","LitImpAvgDelta")),error=function(e){})
tryCatch(partialCorr(c("lenDelta"),c("target"),c("AttImpMaxDelta","LitImpMaxDelta")),error=function(e){})
#Include PageRank 
tryCatch(partialCorr(c("lenDelta"),c("target"),c("AttImpMinDelta","LitImpMinDelta","PageRankMinDelta")),error=function(e){})
tryCatch(partialCorr(c("lenDelta"),c("target"),c("AttImpAvgDelta","LitImpAvgDelta","PageRankAvgDelta")),error=function(e){})
tryCatch(partialCorr(c("lenDelta"),c("target"),c("AttImpMaxDelta","LitImpMaxDelta","PageRankMaxDelta")),error=function(e){})


