properties([parameters([string(defaultValue: '10.44.1.160', name: 'dxEngineProd', trim: true), string(defaultValue: '10.44.1.119', name: 'dxEngineNonProd', trim: true), choice(choices: ['6.0.14.0', '6.0.15.0', '6.0.16.0', '6.0.17.0'], name: 'dxVersion'), string(defaultValue: 'FN', name: 'dSourceName', trim: true), string(defaultValue: 'VFN_RCP', name: 'vdbProdName', trim: true), string(defaultValue: 'LBG Replication', name: 'replicationName', trim: true), string(defaultValue: 'Masked Master Replication Template', name: 'templateName', trim: true), string(defaultValue: 'Template_VDB', name: 'templateVDBName', trim: true)])])
pipeline { 
    agent any 
    environment { 
        PROD_ENGINE = credentials('fwdview-prod-virtualization-engine')
        NON_PROD_ENGINE = credentials('fwdview-non-prod-virtualization-engine')
    }
    stages { 
        stage('Git Checkout') {
            steps {
                bat 'rmdir /s /q LBG_Toolchain'; 
                bat 'git clone https://github.com/cameronbose/LBG_Toolchain.git';
            }
        }
        
        stage("Creating Snapshot of dSource on Prod Engine.") { 
            steps {
                bat "python getParameters.py ${params.dxEngineProd} ${params.dxEngineNonProd} ${params.dxVersion} ${params.dSourceName} ${params.vdbProdName} \"${params.replicationName}\" \"${params.templateName}\" ${params.templateVDBName} ${PROD_ENGINE_USR} ${PROD_ENGINE_PSW} ${NON_PROD_ENGINE_USR} ${NON_PROD_ENGINE_PSW} snapshot_dSource";    
            }
        } 
        stage("Refreshing masked VDB.") { 
            steps {
                bat "python getParameters.py ${params.dxEngineProd} ${params.dxEngineNonProd} ${params.dxVersion} ${params.dSourceName} ${params.vdbProdName} \"${params.replicationName}\" \"${params.templateName}\" ${params.templateVDBName} ${PROD_ENGINE_USR} ${PROD_ENGINE_PSW} ${NON_PROD_ENGINE_USR} ${NON_PROD_ENGINE_PSW} refreshVDBProd";    
            }
        }
        stage("Replicating to Non Prod Engine.") { 
            steps {
                bat "python getParameters.py ${params.dxEngineProd} ${params.dxEngineNonProd} ${params.dxVersion} ${params.dSourceName} ${params.vdbProdName} \"${params.replicationName}\" \"${params.templateName}\" ${params.templateVDBName} ${PROD_ENGINE_USR} ${PROD_ENGINE_PSW} ${NON_PROD_ENGINE_USR} ${NON_PROD_ENGINE_PSW} replicate";    
            }
        }
        stage("Refreshing Template on Non Prod Engine.") { 
            steps {
                bat "python getParameters.py ${params.dxEngineProd} ${params.dxEngineNonProd} ${params.dxVersion} ${params.dSourceName} ${params.vdbProdName} \"${params.replicationName}\" \"${params.templateName}\" ${params.templateVDBName} ${PROD_ENGINE_USR} ${PROD_ENGINE_PSW} ${NON_PROD_ENGINE_USR} ${NON_PROD_ENGINE_PSW} refreshTemplate";    
            }
        }
        stage("Creating Bookmark.") { 
            steps {
                bat "python getParameters.py ${params.dxEngineProd} ${params.dxEngineNonProd} ${params.dxVersion} ${params.dSourceName} ${params.vdbProdName} \"${params.replicationName}\" \"${params.templateName}\" ${params.templateVDBName} ${PROD_ENGINE_USR} ${PROD_ENGINE_PSW} ${NON_PROD_ENGINE_USR} ${NON_PROD_ENGINE_PSW} createBookmark";    
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
