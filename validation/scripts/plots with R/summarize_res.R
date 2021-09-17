library(dplyr)
sum2<- summarize(group_by(res,proj,algo)
                 ,MCC=mean(MCC)
                 ,AUC_macro=mean(AUC_macro)
                 ,AUC_weight=mean(AUC_weight)
                 ,F1_macro=mean(F1_macro)
                 ,F1_weight=mean(F1_weight)
                 # ,F1_1=mean(F1_1)
                 # ,F1_2=mean(F1_2)
                 # ,F1_3=mean(F1_3)
                 # ,AUC_1=mean(AUC_1)
                 # ,AUC_2=mean(AUC_2)
                 # ,AUC_3=mean(AUC_3)
                )

sum3<- summarize(group_by(sum2,algo)
                 ,MCC=median(MCC)
                 ,AUC_macro=median(AUC_macro)
                 ,AUC_weight=median(AUC_weight)
                 ,F1_macro=median(F1_macro)
                 ,F1_weight=median(F1_weight)
                 # ,F1_1=median(F1_1)
                 # ,F1_2=median(F1_2)
                 # ,F1_3=median(F1_3)
                 # ,AUC_1=median(AUC_1)
                 # ,AUC_2=median(AUC_2)
                 # ,AUC_3=median(AUC_3)
                )
write.csv(sum3,"sum_rq.csv")
library(effsize)
library(ggplot2)
theme_set(theme_bw())

res = subset(res,!(res$algo=='random'))

ggplot(res, aes(x=algo, y=MCC, group=algo))  + 
  xlab("")+
 ylim(-1,1)+
  #ylim(0,1)+
  geom_boxplot(aes(fill=algo)) 
 
  #stat_summary(fun=mean, geom="point", shape=20, size=4, color="red", fill="red") +


