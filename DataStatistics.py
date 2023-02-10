#this module is created to do functions related to analysing data
from scipy.stats import ttest_ind, normaltest, ttest_rel, kruskal
import pandas as pd
import ConfigReader as cr

#this function is created to check normality of data based on 0.05 criteria point
#lst: list of data which must be checked
def isNormalData(lst):
    t, p = normaltest(lst) 
    if p < 0.05: 
        return True
    else:
        return False

#this function is created to check normality of all raw data of given data frame
#df: dataframe which is must checked for value's normalization
#colIndxFrom: index of first column which includes in column set which must be checked
#colIndxTo: index of last column which includes in column set which must be checked
def isNormalDataFrame(df : pd.DataFrame, columnFrom, columnTo):
    isNormal = True
    colNamList = list(df.columns[columnFrom:columnTo]) #get the name of columns
    for col in colNamList: #check columns which are at the given range in input parameters
        if(col != "isced11" and col != "levels" and col != "country"):
            if isNormalData(list(df[col])): #if it is normal check next column
                continue
            else: #no need to continue due to one false result, all result will be false
                isNormal = False
                break
        else:
            continue
    return isNormal

#this function check coeffectiency of data and return the final result of them
#lstParam1: list 1
#lstParam2: list 2
def getCorrelation(lstParam1, lstParam2):
    relationResultKey = ""
    #calculate coefficient of data
    val = lstParam1.corr(lstParam2)
    #analyse data
    if val >= 0 and val < 0.5:
        relationResultKey = "CoeffPosStrong"
    elif val >= 0.5:
        relationResultKey = "CoeffPos"
    elif val < 0 and val >= -0.5:
        relationResultKey = "CoeffNegStrong"
    else:
        relationResultKey = "CoeffNeg"
    return cr.getValueByKey(relationResultKey, 'Msg')