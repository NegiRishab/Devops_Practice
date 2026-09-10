def gv

pipeline {

    agent any
    tools {
        maven 'maven-3.9' 
    }

    stages {
        stage('init') {
            steps {
                echo 'Initializing...'
                script {
                    gv = load 'script.groovy'
                }
            }
        }
        stage('Increment Build Number') {
            steps {
                script {      
                gv.incrementBuildNumber()
                }
            }
        }
        stage('Build') {
            steps {
                script {
                gv.build()
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    gv.test()
                }
            }
        }
        stage('Build Image') {
            when{
                expression { return env.BRANCH_NAME == 'main' }
            }
            steps {
                script {
                    gv.buildImage()
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    gv.deploy()
                }
            }
        }
        stage('git') {
            when{
                expression { return env.BRANCH_NAME == 'main' }
            }
            steps {
                script {
                    gv.git()
                }
            }
        }
    }
    post {
      
        success {
            echo 'This will run only if the stages succeed.'
        }
        failure {
            echo 'This will run only if the stages fail.'
        }
    }
}