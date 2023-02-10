#this module is created to be able to read requested files
import pandas as pd
import ConfigReader as cr
from countryCodes import countryCodes as cc

#this function will open the spicified file and return its data by dataframe
#isEducationData: boolean type to determine which datasource is needed
    # the reason that input parameter is boolean because there are only 2 datasource in this project; 
    # And it is essiest way to help developer to avoid remebering the name of file or hard-coding it;
    # the inner functions will make a file name automatically by given parameter
def readDataFromFile(isEducationData):
    try:
        file = cr.getValueByDataSource(isEducationData) #call the configreader function to get the direction of file
        return pd.read_csv(file, sep="\t") #return file's data in dataframe, the "\t" is defiend because the source is in tsv format
    except:
        fileType = getFileType(isEducationData) #get file Type name to insert in the error
        raise Exception(cr.getValueByKey("FileNotFound", "Msg").format(fileType)) #throw exception by using Messages in configMsg File

#this function will return the name of datafile type
#isEducationType: by this boolean value type will recognized
    #for true value: file type is Education, other wise equal to Income
def getFileType(isEducationType):
    return "Education" if isEducationType == True else "Income" # make the source file type name which is specified in input parameter

#this function returns full name of countries based on their 2-letter abberivations
def getCountryName():
    countCodes = cc.twoLetterAbb #get dictionary
    dfCountry = pd.DataFrame({"country": list(countCodes.values()), "geo\TIMEPERIOD": list(countCodes.keys())}) #put on country names in dataframe
    return dfCountry