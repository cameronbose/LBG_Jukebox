properties([parameters([string(defaultValue: '10.44.1.112', name: 'dxEngineProd', trim: true), string(defaultValue: '10.44.1.122', name: 'dxEngineNonProd', trim: true), choice(choices: ['6.0.14.0', '6.0.15.0', '6.0.16.0', '6.0.17.0'], name: 'dxVersion'), string(defaultValue: 'WideWorldImporters', name: 'dSourceName_1', trim: true), string(defaultValue: 'AdventureWorks2016', name: 'dSourceName_2', trim: true), string(defaultValue: 'FN', name: 'vdbProdName_1', trim: true), string(defaultValue: 'DM', name: 'vdbProdName_2', trim: true), string(defaultValue: 'LBG 2 dSource Replication', name: 'replicationName', trim: true), string(defaultValue: '2-dSource Template', name: 'templateName', trim: true), string(defaultValue: 'FN_VDB_Template', name: 'templateVDBName_1', trim: true), string(defaultValue: 'DM_VDB_Template', name: 'templateVDBName_2', trim: true)])])
pipeline { 
    agent any 
    environment { 
        PROD_ENGINE = credentials('fwdview-prod-virtualization-engine')
        NON_PROD_ENGINE = credentials('fwdview-non-prod-virtualization-engine')
    }
    stages { 
        stage('Git Checkout') {
            steps {
                sh 'rm -rf LBG_Toolchain'; 
                sh 'git clone https://github.com/cameronbose/LBG_Toolchain.git';
            }
        }
        
        stage("Creating Snapshot of dSource on Prod Engine.") { 
            steps {
                sh "python getParameters.py ${params.dxEngineProd} ${params.dxEngineNonProd} ${params.dxVersion} ${params.dSourceName_1} ${params.dSourceName_2} ${params.vdbProdName_1} ${params.vdbProdName_2} \"${params.replicationName}\" \"${params.templateName}\" ${params.templateVDBName_1} ${params.templateVDBName_2} ${PROD_ENGINE_USR} ${PROD_ENGINE_PSW} ${NON_PROD_ENGINE_USR} ${NON_PROD_ENGINE_PSW} snapshot_dSource";    
            }
        } 
        stage("Refreshing masked VDB.") { 
            steps {
                sh "python getParameters.py ${params.dxEngineProd} ${params.dxEngineNonProd} ${params.dxVersion} ${params.dSourceName_1} ${params.dSourceName_2} ${params.vdbProdName_1} ${params.vdbProdName_2} \"${params.replicationName}\" \"${params.templateName}\" ${params.templateVDBName_1} ${params.templateVDBName_2} ${PROD_ENGINE_USR} ${PROD_ENGINE_PSW} ${NON_PROD_ENGINE_USR} ${NON_PROD_ENGINE_PSW} refreshVDBProd";    
            }
        }
        stage("Replicating to Non Prod Engine.") { 
            steps {
                sh "python getParameters.py ${params.dxEngineProd} ${params.dxEngineNonProd} ${params.dxVersion} ${params.dSourceName_1} ${params.dSourceName_2} ${params.vdbProdName_1} ${params.vdbProdName_2} \"${params.replicationName}\" \"${params.templateName}\" ${params.templateVDBName_1} ${params.templateVDBName_2} ${PROD_ENGINE_USR} ${PROD_ENGINE_PSW} ${NON_PROD_ENGINE_USR} ${NON_PROD_ENGINE_PSW} replicate";    
            }
        }
        stage("Refreshing Template on Non Prod Engine.") { 
            steps {
                sh "python getParameters.py ${params.dxEngineProd} ${params.dxEngineNonProd} ${params.dxVersion} ${params.dSourceName_1} ${params.dSourceName_2} ${params.vdbProdName_1} ${params.vdbProdName_2} \"${params.replicationName}\" \"${params.templateName}\" ${params.templateVDBName_1} ${params.templateVDBName_2} ${PROD_ENGINE_USR} ${PROD_ENGINE_PSW} ${NON_PROD_ENGINE_USR} ${NON_PROD_ENGINE_PSW} refreshTemplate";    
            }
        }
        stage("Creating Bookmark.") { 
            steps {
                sh "python getParameters.py ${params.dxEngineProd} ${params.dxEngineNonProd} ${params.dxVersion} ${params.dSourceName_1} ${params.dSourceName_2} ${params.vdbProdName_1} ${params.vdbProdName_2} \"${params.replicationName}\" \"${params.templateName}\" ${params.templateVDBName_1} ${params.templateVDBName_2} ${PROD_ENGINE_USR} ${PROD_ENGINE_PSW} ${NON_PROD_ENGINE_USR} ${NON_PROD_ENGINE_PSW} createBookmark";    
            }
        }   
    }
    post { 
        always { 
            echo "Jenkins job run has completed."; 
        }
        success { 
            echo "Job ran successfully!"; 
        } 
        failure { 
            echo "Failed - please look at the error logs."; 
        } 
        unstable { 
            echo "Jenkins run was unstable, please check logs."; 
        } 
        changed { 
            echo "Job is now successful!"; 
            
        }
    }
}
