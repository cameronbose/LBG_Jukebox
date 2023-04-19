#!/bin/bash 

dxEngine=$1 
shift
sourceID=$1

response=$(curl -s -X POST -k --data @- http://${dxEngine}/resources/json/delphix/database/${sourceID}/sync \
-b "cookies.txt" -H "Content-Type: application/json"<<EOF
{"compressionEnabled":false,"type":"MSSqlNewCopyOnlyFullBackupSyncParameters"}
EOF) 

echo "${response}" > ${sourceID}.txt