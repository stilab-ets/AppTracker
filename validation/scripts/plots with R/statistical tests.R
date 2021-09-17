library(effsize)
global<-NULL


compute <- function(element,feature) {
  
  stringg<-""
 
  
  for(algoName in c("LR","SVC","KNN","XGB","DT","RF","BNB","mono-GP") ){
    A<-as.numeric(unlist(subset(mydata,mydata$algo=="AppTracker")[feature]))
    B<-as.numeric(unlist(subset(mydata,mydata$algo==algoName)[feature]))
    print(algoName)
    pair = T
    
    wil<- wilcox.test( A,B ,paired=pair, conf.level=.95)
    VDA<- VD.A( A,B ,paired=pair, conf.level=.95)
    
    res<-NULL
    res$pValue<-wil$p.value
    res$estimate<-VDA$estimate
    res$magnitude<-VDA$magnitude
    global<-res[element] 
    if(element=="pValue"){
      if(res$pValue<2.2e-16){

        stringg<-  paste( stringg, "< 2.2e-16", sep = ",")#, algoName ,feature
      }else{
        stringg<-  paste( stringg, res$pValue, sep = ",")#, algoName ,feature
      }
     
    }
    if(element=="estimate"){
      stringg<-  paste( stringg, res$estimate ,sep = ",")
    }
    if(element=="magnitude"){
      stringg<-  paste( stringg, toupper(substr( res$magnitude, 1, 1)),sep = ",")
    }
  }
#stringg<-  paste(res$pValue, res$estimate,res$magnitude, res$algo<-algoName, res$metric<-feature ,sep = ",")
  
  return(stringg)
}
conti<-1
mat <- NULL
  for(feat in c("F1_weight","AUC_weight","AUC_macro","F1_macro","MCC" ) ){#
   
    print(shapiro.test(as.numeric(unlist(mydata[feat]))))
    
     for(eel in c("pValue","estimate","magnitude") ){
     mat[conti]<-compute(eel,feat)
     conti=conti+1
  }
}
write.csv(mat,"stats.csv")
for(feat in c("F1_weight","AUC_weight","AUC_macro","F1_macro","MCC" ) ){#
  
  print(shapiro.test(as.numeric(unlist(mydata[feat]))))
}



