import DataAccess as da
import pandas as pd
import DataManipulate as dm
import ConfigReader as cr
import DataStatistics as st

#in this function all jobs for reading and clean data in terms of indexing or omitting invalid data will done
def readCleanData(isEducation):
    df = pd.DataFrame(da.readDataFromFile(isEducation)) #reading data from its main source
    #clean data from unexpected characters
    df = dm.replaceColumnCharacter(df, 0, '_', '')
    df = dm.replaceColumnCharacter(df, 0, '-', '')
    
    df = dm.splitDeletionColumn(df, 0, ',') #split index column
    columnManipTo = len(df.columns) - 1
    
    #remove constant keys (Age, sex, level, freq) due to being effectiveless 
    try:
        #remove unwanted columns
        df = df.drop(columns=['freq', 'unit', 'age', 'sex'], axis = 1) # drop due to same data for all records
        
        columnManipTo = columnManipTo - 4 #due to removeing 4 columns the number of columns will be reduced
        
    except:
        raise Exception(cr.getValueByKey("ColumnsNotFound", "Msg").format('freq, unit, age, sex'))
    
    columnDataFrom = 0
    
    columnDataTo = columnManipTo - 3 + 1 # resean of - 3: don't work on key columns , resean of + 1: to calculate last data column
    df = dm.prepareDataForFloatType(df, columnDataFrom, columnDataTo) #clean data from unexpected characters
    df = dm.setColumnsToFloat(df, columnDataFrom, columnDataTo) #convert the type of years columns to float
    
    #ready data for visual on map (country names must be full for plotly.express)
    dfCountries = da.getCountryName()
    
    df = dm.replaceColumnCharacter(df, columnManipTo - 1, '[\d+]+', '', True) #removing the zone time from country abberivation
    df = pd.merge(df, dfCountries, on = "geo\TIMEPERIOD", how="right")
    df = df.drop(columns=['geo\TIMEPERIOD'], axis = 1) # drop due to using country full name 
    
    if isEducation == False: # remove 2005-2007, because these columns are not in common by Eduction data so they would be useless
        df = dm.DeleteColumnsByIndex(df, 0, 2)   
    return df

#this function will check normalization status of data and find central tendency of them and finally delete extra data 
def hormonizeData(df, isEducation):
    #check normalization of data to set central point
    columnManipTo = len(df.columns) 
    isNormal = st.isNormalDataFrame(df, 0, columnManipTo)
    #set central point based on normal status of data
    df = dm.setCentralTendency(df, isNormal, isEducation, 0, columnManipTo - 3)

    #remove years from dataframes due to working on central point
    df = dm.DeleteColumnsByIndex(df, 0, len(df.columns) - 4)
    
    return isNormal, df