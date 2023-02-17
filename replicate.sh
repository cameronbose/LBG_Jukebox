#!/bin/bash 

dxEngineProd=$1 
shift
specID=$1

response=$(curl -s -X POST -k --data @- http://${dxEngineProd}/resources/json/delphix/replication/spec/${specID}/execute \
-b "cookies.txt" -H "Content-Type: application/json"<<EOF
{}
EOF)

echo "${response}" > ${specID}.txt
