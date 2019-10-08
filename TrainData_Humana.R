Opioid.Data <- read.csv(file="C:/Users/Megha/Documents/MScA/Humana_CaseCompetition/HMAHCC_COMP.csv", header=TRUE, sep=",")
Outcomes <- read.csv(file="C:/Users/Megha/Documents/MScA/Humana_CaseCompetition/df_outcomes.csv", header=TRUE, sep=",")

library(dplyr)
head(Opioid.Data)

library(sqldf)

###### Surgery Y/N on Day 0 
Opioid.Data$Surgery <- (Opioid.Data$event_descr == "Surgery")
Surgeries_stage <- data.frame()
Surgeries_stage <-filter(Opioid.Data, event_descr == "Surgery" & Days == 0)
Surgeries_stage <- distinct(Surgeries_stage, id)

Outcomes$SurgeryDay0 <- as.numeric(Outcomes$member_id %in% Surgeries_stage$id)

###### Surgery Y/N Prior to Day 0 
Opioid.Data$Surgery <- (Opioid.Data$event_descr == "Surgery")
Surgeries_stage <- data.frame()
Surgeries_stage <-filter(Opioid.Data, event_descr == "Surgery" & Days < 0)
Surgeries_stage <- distinct(Surgeries_stage, id)

Outcomes$SurgeryPrior <- as.numeric(Outcomes$member_id %in% Surgeries_stage$id)


###### Day 0 MME
head((Opioid.Data$event_descr == "RX Claim - Paid" & !is.na(Opioid.Data$MME)))

Day0MME_stage <- data.frame()
Day0MME_stage <- subset(Opioid.Data, Opioid.Data$event_descr == "RX Claim - Paid" & !is.na(Opioid.Data$MME) & Opioid.Data$Days == 0, select=c(id,MME))
#14080 observations - Some individuals received two separate opioid RX claims - should we average these MMEs? Or does this depend on drug type

count(distinct(Day0MME_stage, id))
#13760

##Thus, we will SUM the DOSAGE

Day0MME_stage$IsDuplicate <- duplicated(Day0MME_stage$id)

Day0MME_stage <- aggregate(Day0MME_stage$MME, by=list(id=Day0MME_stage$id), FUN=sum)

names(Day0MME_stage) <- c("id", "TotalMME")

Outcomes$Day0MME <- NA

Outcomes$IsInDay0MME <- Outcomes$member_id %in% Day0MME_stage$id
missingids_day0MME <- subset(Outcomes, Outcomes$IsInDay0MME == FALSE, select = c(member_id,Day0MME))

names(missingids_day0MME) <- c("id", "TotalMME")
Day0MME_stage <- rbind(Day0MME_stage, missingids_day0MME)

Outcomes$Day0MME <- Day0MME_stage$TotalMME[match(Outcomes$member_id, Day0MME_stage$id)]

Outcomes <- subset(Outcomes,select=-c(IsInDay0MME))

#What should we do about NAs? Should those be 0?

###### Day 0 Supply
head((Opioid.Data$event_descr == "RX Claim - Paid" & !is.na(Opioid.Data$PAY_DAY_SUPPLY_CNT)))

Day0Supply_stage <- data.frame()
Day0Supply_stage <- subset(Opioid.Data, Opioid.Data$event_descr == "RX Claim - Paid" & !is.na(Opioid.Data$PAY_DAY_SUPPLY_CNT) & Opioid.Data$Days == 0, select=c(id,PAY_DAY_SUPPLY_CNT))
#14083 observations - Some individuals received two separate opioid RX claims - should we average these Supply counts? Or does this depend on drug type

count(distinct(Day0Supply_stage, id))
#13760
#Thus we will use the MAX supply count

Day0Supply_stage$IsDuplicate <- duplicated(Day0Supply_stage$id)
Day0Supply_stage <- aggregate(Day0Supply_stage$PAY_DAY_SUPPLY_CNT, by=list(id=Day0Supply_stage$id), FUN=max)

names(Day0Supply_stage) <- c("id", "PAY_DAY_SUPPLY_CNT")

Outcomes$Day0Supply <- NA

Outcomes$IsInDay0Supply <- Outcomes$member_id %in% Day0Supply_stage$id
missingids_day0Supply <- subset(Outcomes, Outcomes$IsInDay0Supply == FALSE, select = c(member_id,Day0Supply))

names(missingids_day0Supply) <- c("id", "PAY_DAY_SUPPLY_CNT")
Day0Supply_stage <- rbind(Day0Supply_stage, missingids_day0Supply)

Outcomes$Day0Supply <- Day0Supply_stage$PAY_DAY_SUPPLY_CNT[match(Outcomes$member_id, Day0Supply_stage$id)]

Outcomes <- subset(Outcomes,select=-c(IsInDay0Supply))

###### Received More than 1 opioid on Day 0 ---- Is this worth it? Check in SQL to see if this number is even high enough to be valuable in the model
Gtr1Opioid_Stage <- data.frame()
Gtr1Opioid_Stage <- filter(Opioid.Data, event_descr == "RX Claim - Paid" & Days == 0 & !is.na(Opioid.Data$MME))



###### Number of New Diagnoses - Top 5 prior to Day 0

NewDiagnoses_Top5_stage <- data.frame()
NewDiagnoses_Top5_stage <- subset(Opioid.Data, select=c(id,event_descr, Days))
NewDiagnoses_Top5_stage <- filter(NewDiagnoses_Top5_stage, event_descr == "New diagnosis - Top 5" & Days < 1)
#2250 new diagnoses

count(distinct(NewDiagnoses_Top5_stage, id))
#2250 - so only 1 new diagnosis - top 5 per individual
#Should no longer do it as a Count, but as a binary 1/0 variable

Outcomes$NewDiagnoses_Top5 <- as.numeric(Outcomes$member_id %in% NewDiagnoses_Top5_stage$id)


###### Number of New Diagnosis - Diabetes prior to Day 0

NewDiagnosis_Diabetes_stage <- data.frame()
NewDiagnosis_Diabetes_stage <- subset(Opioid.Data, select=c(id,event_descr, Days))
NewDiagnosis_Diabetes_stage <- filter(NewDiagnosis_Diabetes_stage, event_descr == "New diagnosis - Diabetes" & Days < 1)
#1432 new diagnoses

count(distinct(NewDiagnosis_Diabetes_stage, id))
#1432- only 1 new diagnosis - diabetes per individual
#Should no longer do it as a Count, but as a binary 1/0 variable

Outcomes$NewDiagnosis_Diabetes <- as.numeric(Outcomes$member_id %in% NewDiagnosis_Diabetes_stage$id)


###### Number of New Diagnosis - Hypertension prior to Day 0

NewDiagnosis_Hypertension_stage <- data.frame()
NewDiagnosis_Hypertension_stage <- subset(Opioid.Data, select=c(id,event_descr, Days))
NewDiagnosis_Hypertension_stage <- filter(NewDiagnosis_Hypertension_stage, event_descr == "New diagnosis - Hypertension" & Days < 1)
#2256 new diagnoses

count(distinct(NewDiagnosis_Hypertension_stage, id))
#2256- only 1 new diagnosis - hypertension per individual
#Should no longer do it as a Count, but as a binary 1/0 variable

Outcomes$NewDiagnosis_Hypertension <- as.numeric(Outcomes$member_id %in% NewDiagnosis_Hypertension_stage$id)


###### Number of New Diagnosis - CAD prior to Day 0

NewDiagnosis_CAD_stage <- data.frame()
NewDiagnosis_CAD_stage <- subset(Opioid.Data, select=c(id,event_descr, Days))
NewDiagnosis_CAD_stage <- filter(NewDiagnosis_CAD_stage, event_descr == "New diagnosis - CAD" & Days < 1)
#1493 new diagnoses

count(distinct(NewDiagnosis_CAD_stage, id))
#1493- only 1 new diagnosis - CAD per individual
#Should no longer do it as a Count, but as a binary 1/0 variable

Outcomes$NewDiagnosis_CAD <- as.numeric(Outcomes$member_id %in% NewDiagnosis_CAD_stage$id)


###### Number of New Diagnosis - CPD prior to Day 0

NewDiagnosis_CPD_stage <- data.frame()
NewDiagnosis_CPD_stage <- subset(Opioid.Data, select=c(id,event_descr, Days))
NewDiagnosis_CPD_stage <- filter(NewDiagnosis_CPD_stage, event_descr == "New diagnosis - CPD" & Days < 1)
#2379 new diagnoses

count(distinct(NewDiagnosis_CPD_stage, id))
#2379- only 1 new diagnosis - CAD per individual
#Should no longer do it as a Count, but as a binary 1/0 variable

Outcomes$NewDiagnosis_CPD <- as.numeric(Outcomes$member_id %in% NewDiagnosis_CPD_stage$id)


###### Number of New Diagnosis - CHF prior to Day 0

NewDiagnosis_CHF_stage <- data.frame()
NewDiagnosis_CHF_stage <- subset(Opioid.Data, select=c(id,event_descr, Days))
NewDiagnosis_CHF_stage <- filter(NewDiagnosis_CHF_stage, event_descr == "New diagnosis - CHF" & Days < 1)
#1108 new diagnoses

count(distinct(NewDiagnosis_CHF_stage, id))
#1108- only 1 new diagnosis - CAD per individual
#Should no longer do it as a Count, but as a binary 1/0 variable

Outcomes$NewDiagnosis_CHF <- as.numeric(Outcomes$member_id %in% NewDiagnosis_CHF_stage$id)


######TOTAL COUNT OF DIAGNOSES prior to Day 0

TotalDxCount_stage <- data.frame()
TotalDxCount_stage <- filter(Opioid.Data, event_descr == "New diagnosis - Top 5" & Days < 1)
#2250 New Diagnosis - Top 5

TotalDxCount_stage <- subset(TotalDxCount_stage, select=c(id,event_descr))
TotalDxCount_stage$TotalDxCount <- 1
TotalDxCount_stage <- aggregate(TotalDxCount_stage$TotalDxCount, by=list(id=TotalDxCount_stage$id), FUN=sum)
names(TotalDxCount_stage) <- c("id", "TotalDxCount")

Outcomes$TotalDxCount <- 0

Outcomes$IsInTotalDxCount <- Outcomes$member_id %in% TotalDxCount_stage$id
missingids_TotalDxCount <- subset(Outcomes, Outcomes$IsInTotalDxCount == FALSE, select = c(member_id, TotalDxCount))

names(missingids_TotalDxCount) <- c("id", "TotalDxCount")
TotalDxCount_stage <- rbind(TotalDxCount_stage, missingids_TotalDxCount)

Outcomes$TotalDxCount <- TotalDxCount_stage$TotalDxCount[match(Outcomes$member_id,TotalDxCount_stage$id)]

Outcomes <- subset(Outcomes, select = -c(IsInTotalDxCount))


###### New provider in 180 days (6 months) prior to Day 0

NewProvider_stage <- data.frame()
NewProvider_stage <-filter(Opioid.Data, event_descr == "New provider" & Days < 1 & Days > -181)
NewProvider_stage <- distinct(NewProvider_stage, id)

Outcomes$NewProvider <- as.numeric(Outcomes$member_id %in% NewProvider_stage$id)


###### Inbound call by Member about refills prior to Day 0 (1/0 if they even made a call)
RefillCall_stage <- data.frame()
RefillCall_stage <- filter(Opioid.Data, event_descr == "Inbound Call by Mbr" & Days < 1 & (event_attr2 == "REFILL" | event_attr2 == "REFILL REQUEST"))
RefillCall_stage <- distinct(RefillCall_stage, id)
#4764 distinct members

Outcomes$RefillCall <- as.numeric(Outcomes$member_id %in% RefillCall_stage$id)

##number of times individual called for a refill


###### Inbound call by Member about refills prior to Day 0 (Count of calls they made)
RefillCallCount_stage <- data.frame()
RefillCallCount_stage <- filter(Opioid.Data, event_descr == "Inbound Call by Mbr" & Days < 1 & (event_attr2 == "REFILL" | event_attr2 == "REFILL REQUEST"))
#21913 calls

RefillCallCount_stage <- subset(RefillCallCount_stage, select=c(id,event_attr2))
RefillCallCount_stage$RefillCallCount <- 1
RefillCallCount_stage <- aggregate(RefillCallCount_stage$RefillCallCount, by=list(id=RefillCallCount_stage$id), FUN=sum)
names(RefillCallCount_stage) <- c("id","RefillCallCount")


Outcomes$RefillCallCount <- 0

Outcomes$IsInRefillCallCount <- Outcomes$member_id %in% RefillCallCount_stage$id
missingids_RefillCall <- subset(Outcomes, Outcomes$IsInRefillCallCount == FALSE, select = c(member_id, RefillCallCount))

names(missingids_RefillCall) <- c("id", "RefillCallCount")
RefillCallCount_stage <- rbind(RefillCallCount_stage, missingids_RefillCall)

Outcomes$RefillCallCount <- RefillCallCount_stage$RefillCallCount[match(Outcomes$member_id, RefillCallCount_stage$id)]

Outcomes <- subset(Outcomes, select=-c(IsInRefillCallCount))


write.csv(Outcomes,"C:/Users/Megha/Documents/MScA/Humana_CaseCompetition/df_outcomes.csv", row.names = FALSE)

