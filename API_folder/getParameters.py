import os 
import json 
import sys 
import time 

dxEngineProd = sys.argv[1]
dxEngineNonProd = sys.argv[2]
dxVersion = sys.argv[3]
dSourceName_1 = sys.argv[4]
dSourceName_2 = sys.argv[5]
vdbName_1 = sys.argv[6]
vdbName_2 = sys.argv[7]
replicationName = sys.argv[8]
templateName = sys.argv[9]
templateVDBName_1 = sys.argv[10]
templateVDBName_2 = sys.argv[11]
prod_username = sys.argv[12]
prod_password = sys.argv[13]
non_prod_username = sys.argv[14]
non_prod_password = sys.argv[15]
action = sys.argv[16]

versionDict = {'6.0.14.0':'1.11.14','6.0.15.0':'1.11.15','6.0.16.0':'1.11.16','6.0.17.0':'1.11.17'}

def run_command(command):
    os.system(command)

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
            elif state =="FAILED":
                state="FAILED"
                return state
            else: 
                return False

def getAction(sourceID):
    response = open(f"{sourceID}.txt", "r").read()
    responseJson = json.loads(response)
    action = responseJson["action"] 
    return action

def checkActionLoop(action,engine):
    while True: 
        if checkAction(action,engine):
            print("It has Completed!") 
            break 
        elif checkAction(action,engine) == "FAILED": 
            print("Action has failed, check engine logs.")
            sys.exit()
        else:
            print("Not yet Completed, check again in 10 seconds")
            time.sleep(10)

if __name__ == "__main__": 
    
    if action == "snapshot_dSource": 
        print("Creating snapshot of dSource.")
        major,minor,micro = getAPIVersion(dxVersion) 
        os.system(f"sh login.sh {prod_username} {prod_password} {dxEngineProd} {major} {minor} {micro}")
        sourceID_1 = getdSourceContainerID(dSourceName_1,dxEngineProd)
        sourceID_2 = getdSourceContainerID(dSourceName_2,dxEngineProd)
        os.system(f"sh snapshot.sh {dxEngineProd} {sourceID_1}")
        os.system(f"sh snapshot.sh {dxEngineProd} {sourceID_2}")
        action_1 = getAction(sourceID_1)
        action_2 = getAction(sourceID_2)
        checkActionLoop(action_1,dxEngineProd)
        checkActionLoop(action_2,dxEngineProd)
        time.sleep(5)

    if action == "refreshVDBProd": 
        print("Refreshing masked vdb in PROD environment to latest Snapshot.")
        major,minor,micro = getAPIVersion(dxVersion) 
        os.system(f"sh login.sh {prod_username} {prod_password} {dxEngineProd} {major} {minor} {micro}")
        vdbID_1 = getdSourceContainerID(vdbName_1,dxEngineProd)
        vdbID_2 = getdSourceContainerID(vdbName_2,dxEngineProd)
        sourceID_1 = getdSourceContainerID(dSourceName_1,dxEngineProd)
        sourceID_2 = getdSourceContainerID(dSourceName_2,dxEngineProd)
        latestSnap_1 = getSnapshotID(sourceID_1,dxEngineProd)
        latestSnap_2 = getSnapshotID(sourceID_2,dxEngineProd)
        os.system(f"sh refreshVDBProd.sh {dxEngineProd} {vdbID_1} {latestSnap_1}")
        os.system(f"sh refreshVDBProd.sh {dxEngineProd} {vdbID_2} {latestSnap_2}")
        action_1 = getAction(vdbID_1)
        action_2 = getAction(vdbID_2)
        checkActionLoop(action_1,dxEngineProd)
        checkActionLoop(action_2,dxEngineProd)
    
    if action == "replicate": 
        print("Replicating to Non-Prod Environment.")
        major,minor,micro = getAPIVersion(dxVersion) 
        os.system(f"sh login.sh {prod_username} {prod_password} {dxEngineProd} {major} {minor} {micro}")      
        specID = getReplicationSpec(replicationName)
        os.system(f"sh replicate.sh {dxEngineProd} {specID}")
        action = getAction(specID)
        checkActionLoop(action,dxEngineProd)
    
    if action == "refreshTemplate": 
        print("Refreshing Non-Prod Template VDB.")
        major,minor,micro = getAPIVersion(dxVersion)
        os.system(f"sh login.sh {non_prod_username} {non_prod_password} {dxEngineNonProd} {major} {minor} {micro}")
        templateID_1 = getdSourceContainerID(templateVDBName_1,dxEngineNonProd)
        templateID_2 = getdSourceContainerID(templateVDBName_2,dxEngineNonProd)
        os.system(f"sh refreshVDBNonProd.sh {dxEngineNonProd} {templateID_1}")
        os.system(f"sh refreshVDBNonProd.sh {dxEngineNonProd} {templateID_2}")
        action_1 = getAction(templateID_1)
        action_2 = getAction(templateID_2)
        checkActionLoop(action_1,dxEngineNonProd)
        checkActionLoop(action_2,dxEngineNonProd)
    
    if action == "createBookmark": 
        print("Creating bookmark of Template.") 
        major,minor,micro = getAPIVersion(dxVersion)
        os.system(f"sh login.sh {non_prod_username} {non_prod_password} {dxEngineNonProd} {major} {minor} {micro}")  
        templateReference,templateBranch = getTemplateBranch(templateName)
        os.system(f"sh bookmark.sh {dxEngineNonProd} {templateReference} {templateBranch}")
        action = getAction(templateReference)
        checkActionLoop(action,dxEngineNonProd)