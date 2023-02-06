import os 
import json 
import sys 
import time 

versionDict = {'6.0.14.0':'1.11.14','6.0.15.0':'1.11.15','6.0.16.0':'1.11.16','6.0.17.0':'1.11.17'}

def getAPIVersion(delphixVersion):
    apiVersion = versionDict[delphixVersion]
    major,minor,micro = apiVersion.split('.')
    return major,minor,micro  

def getdSourceContainerID(dSourceName,engine): 
    APIQuery = os.popen(f'curl -X GET -k http://{engine}/resources/json/delphix/database -b "cookies.txt" -H "Content-Type: application/json"').read()
    queryDict = json.loads(APIQuery) 
    for db in queryDict["result"]:
        if db['name'] == dSourceName: 
            dSourceContainer = db['reference']
            print(f"this is it ****************************{dSourceContainer}***************************")
    return dSourceContainer
    
def getSnapshotID(sourceID,engine): 
    APIQuery = os.popen(f'curl -X GET -k http://{engine}/resources/json/delphix/snapshot?database={sourceID} -b "cookies.txt" -H "Content-Type: application/json"').read()
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

def checkAction(action,engine): 
    APIQuery = os.popen(f'curl -X GET -k http://{engine}/resources/json/delphix/action -b "cookies.txt" -H "Content-Type: application/json"').read()
    queryDict = json.loads(APIQuery)
    for actions in queryDict["result"]:
        if actions['reference'] == action:
            state = actions['state']
            print(state)
            if state == "COMPLETED":
                return True 
            else: 
                return False

def getAction():
    response = open("response.txt", "r").read()
    responseJson = json.loads(response)
    action = responseJson["action"] 
    return action

def checkActionLoop(action,engine):
    while True: 
        if checkAction(action,engine):
            print("It has Completed!") 
            break 
        else:
            print("Not yet Completed, check again in 10 seconds")
            time.sleep(10)
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
    
    print("Getting reference ID's for API POST calls. ")
    os.system(f"sh login.sh 'admin' 'Fwdview01!' {dxEngineNonProd} {major} {minor} {micro}")
    templateReference,templateBranch = getTemplateBranch(templateName)
    
    print("logging in") 
    os.system(f"sh login.sh {username} {password} {dxEngineProd} {major} {minor} {micro}")
    
    sourceID = getdSourceContainerID(dSourceName,dxEngineProd)
    vdbID = getdSourceContainerID(vdbName,dxEngineProd)
    specID = getReplicationSpec(replicationName)
    
    print("Creating Snapshot of dSource.")
    os.system(f"sh snapshot.sh {dxEngineProd} {sourceID}")
    
    action = getAction()
    checkActionLoop(action,dxEngineProd)
    
    latestSnap = getSnapshotID(sourceID,dxEngineProd)
    print(latestSnap)
    
    print("Refreshing masked vdb in PROD environment to latest Snapshot just taken & then replicating to Non-Prod Environment.")
    os.system(f"sh refreshVDBProd.sh {dxEngineProd} {vdbID} {latestSnap}")
    
    action = getAction()
    checkActionLoop(action,dxEngineProd)

    os.system(f"sh replicate.sh {dxEngineProd} {specID}")

    action = getAction()
    checkActionLoop(action,dxEngineProd)


    os.system(f"sh login.sh 'admin' 'Fwdview01!' {dxEngineNonProd} {major} {minor} {micro}")
    templateID = getdSourceContainerID("Template_VDB",dxEngineNonProd)
    templateReference,templateBranch = getTemplateBranch(templateName)
    # templateLatestSnap = getSnapshotID(templateID,dxEngineNonProd)
    # # do we need the snapID? 
    # print(f"{templateID} && {templateLatestSnap}")
    # print("Refreshing template vdb & creating bookmark on template.")
    os.system(f"sh refreshVDBNonProd.sh {dxEngineNonProd} {templateID}")
    
    action = getAction()
    checkActionLoop(action,dxEngineNonProd)

    os.system(f"sh bookmark.sh {dxEngineNonProd} {templateReference} {templateBranch}")
    
    action = getAction()
    checkActionLoop(action,dxEngineNonProd)
