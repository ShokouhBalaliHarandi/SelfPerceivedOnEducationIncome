#this module is created to clean and manipulate the data 
import ConfigReader as cr
import numpy as np
import pandas as pd

#this function will replace exist character by given character for column which is specified by its index number
# df: dataframe which is need to manupulate data
# columnIndex: the index of column which is need to manipulate data
# oldChar: the character which is need to be replaced
# newChar: the new character which is used in data instead of oldchar
# isRegex: True value if oldChar is defined by regular experssions, Otherwise False
def replaceColumnCharacter(df, columnIndex, oldChar, newChar, isRegex=False):
    df.iloc[:, columnIndex].replace(oldChar , newChar, inplace = True, regex=isRegex) #use iloc to access to the specified column and manipulate its data
    return df

#this function will replace exist character by given character for columns which are specified by their index range
# df: dataframe which is need to manupulate data
# columnFrom: start index of columns which are need  to manipulate data
# columnTo: end index of columns which are need to manipulate data
# oldChar: the character which is need to be replaced
# newChar: the new character which is used in data instead of oldchar
# isRegex: True value if oldChar is defined by regular experssions, Otherwise False
def replaceCharacter(df, columnFrom, columnTo, oldChar, newChar, isRegex):
    df.iloc[:, columnFrom:columnTo] = df.iloc[:, columnFrom:columnTo].replace(oldChar , newChar , regex=isRegex) #use iloc to access to specified columns and manipulate their data
    return df

#by this function index column will split to multi columns base on splitter
#df: dataframe which is need to manupulate data
#columnIndex: the index of column which is need to be splitted
#splitter: the character which is used to specified in which way header's name must be seprated
def splitDeletionColumn(df, columnIndex, splitter):
    headerAttributes = df.columns[columnIndex].split(splitter) #make new string for header of new columns by splitting the old column header name
    df[headerAttributes] = df.iloc[:, columnIndex].str.split(splitter, expand = True) #split the value of given column and put them in new columns which are made in previous line
    df = df.drop(df.columns[[columnIndex]], axis=1) #eliminate old column 
    return df

#by this function the columns which are specified by their index ranges can be eliminate
#df: pd.DataFrame: dataframe which is need to manupulate data (for some errors in runtime, the type of df is determined)
#columnFrom: start index of columns which are need to be deleted
#columnTo: end index of columns which are need to be deleted
def DeleteColumnsByIndex(df : pd.DataFrame, columnFrom, columnTo):
    df = df.drop(df.iloc[:, columnFrom:columnTo], axis = 1)
    return df

#elimitate charactes (except .) and convert empty value to 0 to prepare data to convert into float numbers
#df: dataframe which is need to manupulate data
#columnFrom: start index of columns which are need to be checked and changed
#columnTo: end index of columns which are need to be checked and changed
def prepareDataForFloatType(df, columnFrom, columnTo):
    df = replaceCharacter(df, columnFrom, columnTo, "[^\d+\.]+", '', True) #replace all spaces and non-digit characters by nothing execpt . for float ones
    df = replaceCharacter(df, columnFrom, columnTo, '', 0,  False) #replace empty values by 0 value
    return df

#by this function the type of specified columns will be changed to float type
#df: dataframe which is need to convert its data type
#columnFrom: start index of columns which are need to change their type
#columnTo: end index of columns which are need to change their type
def setColumnsToFloat(df, columnFrom, columnTo):
    try:
        df.iloc[:, columnFrom:columnTo] = df.iloc[:, columnFrom:columnTo].astype(float)
        return df
    except: #if converting is fail the function will throw an error
        raise Exception(cr.getValueByKey("DataNotValid", "Msg"))

# this function will set given column(s) of dataframe as an Index
#df: data frame
#columnFrom: start index of columns must be set
#columnTo: end index of columns must be set
def setIndex(df : pd.DataFrame, columnFrom, columnTo):
    try:
        columns = list(df.columns[columnFrom:columnTo + 1])  #+1: to include last column
        df.set_index(columns, inplace=True)
        return df
    except:
        raise Exception(cr.getValueByKey("ColIndexRangeNotFound", "Msg").format(columnFrom, columnTo))    

#return central tendency of data based on their normal status
#df: data frame
#isNormal: True: if dataframe's data is normal; otherwise: False
#isEducation: True if dataframe is for education; otherwise false
#columnFrom: start index of columns must be manipulated
#columnTo: end index of columns must be manipulated
def setCentralTendency(df, isNormal, isEducation,columnFrom, columnTo):
    #set name for central point columns based on type of dataframe
    colName = "centralPoint{0}" 
    if isEducation:
        colName = colName.format("Edu")
    else:
        colName = colName.format("InCom")
    
    #set central point column
    if isNormal: #use mean for normal data
        df[colName] = df[df.columns[columnFrom:columnTo]].mean(axis = 1)
    else:
        df[colName] = df[df.columns[columnFrom:columnTo]].median(axis = 1)
        
    return df