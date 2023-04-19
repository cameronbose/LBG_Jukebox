#!/bin/bash 

dxEngineNonProd=$1
shift 
containerID=$1
shift 

response=$(curl -s -X POST -k --data @- http://${dxEngineNonProd}/resources/json/delphix/selfservice/${containerID}/refresh \
-b "cookies.txt" -H "Content-Type: application/json"<<EOF
{"type":"JSDataContainerRefreshParameters","forceOption":false}
EOF)

echo "${response}" > ${containerID}.txt 

