def incrementBackendVersion() {
    echo 'Incrementing backend version...'
    dir('backend') {
        sh 'mvn build-helper:parse-version versions:set -DnewVersion=\\${parsedVersion.majorVersion}.\\${parsedVersion.minorVersion}.\\${parsedVersion.nextIncrementalVersion} -DgenerateBackupPoms=false'
    }

    def newVersion = sh(
        script: 'cd backend && mvn help:evaluate -Dexpression=project.version -q -DforceStdout',
        returnStdout: true
    ).trim()
    echo "New backend version: ${newVersion}"
    env.BACKEND_IMAGE_TAG = "${newVersion}-${env.BUILD_NUMBER}"
    echo "Backend image tag set to: ${env.BACKEND_IMAGE_TAG}"
}

def backendImageBuild() {
    echo 'Building backend Docker image...'
    withCredentials([usernamePassword(credentialsId: 'docker_hub', usernameVariable: 'DOCKERHUB_USERNAME', passwordVariable: 'DOCKERHUB_PASSWORD')]) {
        sh "echo ${DOCKERHUB_PASSWORD} | docker login -u ${DOCKERHUB_USERNAME} --password-stdin"
        sh "docker build -t ankit42098/employee-backend:${env.BACKEND_IMAGE_TAG} ./backend"
        sh "docker push ankit42098/employee-backend:${env.BACKEND_IMAGE_TAG}"
        env.BACKEND_IMAGE = "ankit42098/employee-backend:${env.BACKEND_IMAGE_TAG}"
    }
}

def incrementFrontendVersion() {
    echo 'Incrementing frontend version...'
    dir('frontend') {
        sh 'npm version patch --no-git-tag-version'
    }

    def newVersion = sh(
        script: "cd frontend && node -p \"require('./package.json').version\"",
        returnStdout: true
    ).trim()
    echo "New frontend version: ${newVersion}"
    env.FRONTEND_IMAGE_TAG = "${newVersion}-${env.BUILD_NUMBER}"
    echo "Frontend image tag set to: ${env.FRONTEND_IMAGE_TAG}"
}

def frontendImageBuild() {
    echo 'Building frontend Docker image...'
    withCredentials([usernamePassword(credentialsId: 'docker_hub', usernameVariable: 'DOCKERHUB_USERNAME', passwordVariable: 'DOCKERHUB_PASSWORD')]) {
        sh "echo ${DOCKERHUB_PASSWORD} | docker login -u ${DOCKERHUB_USERNAME} --password-stdin"
        sh "docker build -t ankit42098/employee-frontend:${env.FRONTEND_IMAGE_TAG} ./frontend"
        sh "docker push ankit42098/employee-frontend:${env.FRONTEND_IMAGE_TAG}"
        env.FRONTEND_IMAGE = "ankit42098/employee-frontend:${env.FRONTEND_IMAGE_TAG}"
    }
}

def deployContainers() {
    echo 'Deploying containers with docker-compose...'

    def ec2instance = 'ec2-user@13.232.43.163'
    def dockerComposeContent = "bash ./script.sh ${env.BACKEND_IMAGE} ${env.FRONTEND_IMAGE}"

   sshagent(['aws-cred']) {
    sh "scp -o StrictHostKeyChecking=no script.sh ${ec2instance}:/home/ec2-user/"
    sh "scp -o StrictHostKeyChecking=no docker-compose.yml ${ec2instance}:/home/ec2-user/"
    sh "ssh -o StrictHostKeyChecking=no ${ec2instance} '${dockerComposeContent}'"
}
}

def versionBump() {
    echo 'Bumping versions...'
    withCredentials([usernamePassword(credentialsId: 'gitlab', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
        // Single-quoted script: shell expands GIT_* env vars; Groovy does not log secrets.
        sh '''
            git config --global user.name "${GIT_USERNAME}"
            git config --global user.email "jenkins@jenkins.com"
            git add .
            git commit -m "Bump versions for backend and frontend"
            git push "https://${GIT_USERNAME}:${GIT_PASSWORD}@gitlab.com/rishabhvicky98/aws_demo.git" HEAD:main
        '''
    }
}

return this
