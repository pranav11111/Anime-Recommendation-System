pipeline{

    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'anime-rec-471013'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'
        KUBECTL_AUTH_PLUGIN = '/usr/lib/google-cloud-sdk/bin'


    }

    stages{
        stage('cloning from github'){
            steps{
                script{
                    echo 'cloning from github'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'githubtoken', url: 'https://github.com/pranav11111/Anime-Recommendation-System.git']])
                }
            }
        }

        stage('Making a virtual enviorment'){
            steps{
                script{
                    echo 'Making a virtual enviorment....................'
                    sh'''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

        stage('DVC PULL'){
            steps{
                withCredentials([file(credentialsId:'gcp-key', variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'dvc pull.....'
                        sh'''
                        . ${VENV_DIR}/bin/activate
                        dvc pull
                        '''
                    }
                }
                
        }
    }

    stage('BUild and push to GCR'){
            steps{
                withCredentials([file(credentialsId:'gcp-key', variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Build and push to GCR.....'
                        sh'''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quite
                        docker build -t gcr.io/${GCP_PROJECT}/animerecom:latest .
                        docker push gcr.io/${GCP_PROJECT}/animerecom:latest
                        '''
                    }
                }
                
        }
    }    

    stage('Deploying'){
            steps{
                withCredentials([file(credentialsId:'gcp-key', variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'deploying.....'
                        sh'''
                        export PATH=$PATH:${GCLOUD_PATH}:${KUBECTL_AUTH_PLUGIN}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud container clusters get-credentials autopilot-cluster-1 --region us-central1
                        kubectl apply -f deployment.yaml
                        '''
                    }
                }
                
        }
    }  

    
   }

}