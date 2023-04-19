#!/bin/bash 

dxEngineProd=$1 
shift
vdbID=$1
shift
latestSnap=$1

response=$(curl -s -X POST -k --data @- http://${dxEngineProd}/resources/json/delphix/database/${vdbID}/refresh \
-b "cookies.txt" -H "Content-Type: application/json"<<EOF
{"timeflowPointParameters":{"snapshot":"${latestSnap}","type":"TimeflowPointSnapshot"},"type":"RefreshParameters"}
EOF)

echo "${response}" > ${vdbID}.txt
