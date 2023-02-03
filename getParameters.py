import os 
import json 
import sys 
import time 

versionDict = {'6.0.14.0':'1.11.14','6.0.15.0':'1.11.15','6.0.16.0':'1.11.16','6.0.17.0':'1.11.17'}

def getAPIVersion(delphixVersion):
    apiVersion = versionDict[delphixVersion]
    major,minor,micro = apiVersion.split('.')
    return major,minor,micro  

def getdSourceContainerID(dSourceName): 
    APIQuery = os.popen(f'curl -X GET -k http://{dxEngineProd}/resources/json/delphix/database -b "cookies.txt" -H "Content-Type: application/json"').read()
    queryDict = json.loads(APIQuery) 
    for db in queryDict["result"]:
        if db['name'] == dSourceName: 
            dSourceContainer = db['reference']
            print(f"this is it ****************************{dSourceContainer}***************************")
    return dSourceContainer
    
def getSnapshotID(sourceID): 
    APIQuery = os.popen(f'curl -X GET -k http://{dxEngineProd}/resources/json/delphix/snapshot?database={sourceID} -b "cookies.txt" -H "Content-Type: application/json"').read()
    queryDict = json.loads(APIQuery)
    snapshotList = [db["reference"] for db in queryDict["result"]]
    latestSnapshot = snapshotList[-1]
    return latestSnapshot

def getReplicationSpec(replicationName): 
    APIQuery = os.popen(f'curl -X GET -k http://{dxEngineProd}/resources/json/delphix/replication/spec -b "cookies.txt" -H "Content-Type: application/json"').read()
    queryDict = json.loads(APIQuery)
    for replication in queryDict["result"]:
        if replication['name'] == replicationName:
            specID = replication["reference"]
    return specID

def getTemplateBranch(templateName): 
    APIQuery = os.popen(f'curl -X GET -k http://{dxEngineNonProd}/resources/json/delphix/selfservice/template -b "cookies.txt" -H "Content-Type: application/json"').read()
    queryDict = json.loads(APIQuery)
    for template in queryDict["result"]:
        if template['name'] == templateName: 
            templateReference = template["reference"]
            templateBranch = template["activeBranch"]
    print(f"{templateReference} & {templateBranch}")
    return templateReference,templateBranch 


if __name__ == "__main__": 
    username = "admin"
    password = "fwdview01!"
    dxEngineProd = sys.argv[1]
    dxEngineNonProd = sys.argv[2]
    dxVersion = sys.argv[3]
    dSourceName = sys.argv[4]
    vdbName = sys.argv[5]
    replicationName = sys.argv[6]
    templateName = sys.argv[7]
    major,minor,micro = getAPIVersion(dxVersion)
    
    os.system(f"sh login.sh 'admin' 'Fwdview01!' {dxEngineNonProd} {major} {minor} {micro}")
    templateReference,templateBranch = getTemplateBranch(templateName)
    print("logging in") 
    os.system(f"sh login.sh {username} {password} {dxEngineProd} {major} {minor} {micro}")
    sourceID = getdSourceContainerID(dSourceName)
    vdbID = getdSourceContainerID(vdbName)
    specID = getReplicationSpec(replicationName)
    os.system(f"sh snapshot.sh {dxEngineProd} {sourceID} {vdbID}")


    time.sleep(120)
    latestSnap = getSnapshotID(sourceID)
    print(latestSnap)
    
    os.system(f"sh commands.sh {dxEngineProd} {dxEngineNonProd} {sourceID} {vdbID} {latestSnap} {specID} {major} {minor} {micro} {templateReference} {templateBranch}")




# 2 more API's - replicate it then bookmark the template
