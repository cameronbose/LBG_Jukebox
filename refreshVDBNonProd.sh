#!/bin/bash 

dxEngineNonProd=$1
shift 
templateID=$1
shift 

response=$(curl -s -X POST -k --data @- http://${dxEngineNonProd}/resources/json/delphix/database/${templateID}/refresh \
-b "cookies.txt" -H "Content-Type: application/json"<<EOF
{"type":"RefreshParameters","timeflowPointParameters":{"type":"TimeflowPointSemantic"}}
EOF)

echo "${response}" > ${templateID}.txt 

