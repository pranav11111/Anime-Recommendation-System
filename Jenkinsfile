pipeline{

    agent any

    stages{
        stage{'cloning from github'}{
            steps{
                script{
                    echo 'cloning from github'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'githubtoken', url: 'https://github.com/pranav11111/Anime-Recommendation-System.git']])
                }
            }
        }
    }
}