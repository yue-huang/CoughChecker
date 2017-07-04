setwd("~/daphnehuang2006@gmail.com/yueCareer/Insight/coughSymptomChecker/data")
library(haven)
myData = read_dta("namcs2014_stata.dta")
write.csv(myData, file = "myStataFile.csv")

#load ('cough.RData')
#save.image(file = 'cough.RData')
