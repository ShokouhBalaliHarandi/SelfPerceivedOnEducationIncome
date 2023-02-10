#the main purpose of this module is finding the given key and returning its value
import yaml as ym

#by this function the value of given key will be returned
#keyName: name of key which is needed to read
#configType: specifys the config file which must be read, App: configApp, Msg: configMsg
    # configApp: to read settings of aplication or general info about running codes
    # configMsg: to store output messages which will be shown to end-user as a success, alarm or error messages 
def getValueByKey(keyName, configType):
    """in except parts of this method: 
        the reason of raise exception message is hard code and is not used of this methode again is: 
            to prevent of loop if for any reason this function has error"""
    #opening config file
    configFileName = "config{0}.yaml".format(configType) #make the config file name which must be read
    try:
        with open(configFileName, 'r') as configFile: #open config file in readonly mode
            configDic = ym.safe_load(configFile) #read config file and put its content in dictionary
    except: #raising error if the config file was not found due to wrong configType or missing file(S) this 
        raise Exception("the requested config ({0}) is not found.".format(configType))
    
    #returning value 
    try:  #return the value of given key if it exists
        return configDic[keyName]
    except: #throw exception if the given key does not exist in the specific config file
        raise Exception("the {0} key was not found in {1}config file".format(keyName, configType)) 


#this function will return the datasource direction which is specified by its property
#isEducationData: boolean type to determine which datasource is needed
    # the reason that input parameter is boolean because there are only 2 datasources in this project;
    # Therefore by boolean type, function will create the name of key automatically
    # with out involving developer to memorize the name of keys
def getValueByDataSource(isEducation):
    """keyName = "FileEducationPath" #setting key's name by default value
    if isEducation == False : #changing key's name if input parameter is false (means income file is needed)
        keyName = "FileIncomePath" """
    keyName = "FileEducationPath" if isEducation == True else "FileIncomePath"
    return getValueByKey(keyName, 'App') #cal getValueByKey to get the value (path) of the needed file which is specified at input