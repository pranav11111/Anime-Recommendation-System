pipeline{

    agent any

    enviorment {
        VENV_DIR = 'venv'
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
                    python -m venv${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

        stage('DVC PULL'){
            steps{
                withCredentials([file(credentialsId;'gcp-key', variable = 'GOOGLE_APPLICATION_CREDENTIALS')]){
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

    
}