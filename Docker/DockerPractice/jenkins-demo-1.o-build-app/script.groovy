// def buildJar() {
//     echo 'building the application...'
//     sh 'mvn package'
// }

// def buildImage() {
//     echo "building the docker image..."
//     withCredentials([usernamePassword(credentialsId: 'docker-hub-repo', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
//         sh 'docker build -t nanatwn/demo-app:jma-2.0 .'
//         sh 'echo $PASS | docker login -u $USER --password-stdin'
//         sh 'docker push nanatwn/demo-app:jma-2.0'
//     }
// }

def deployApp() {
    echo 'deploying the application...'
}

def init() {
    echo "init stage"
    echo "New version is ${NEW_VERSION}"
    echo "Environment is ${ENVIRONMENT}"
    echo "RUN_TESTS is ${RUN_TESTS}"
    // echo "SERVER_CRED is ${SERVER_CRED}"
    withCredentials([usernamePassword(credentialsId: 'server-cred', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
        echo "Username is ${USER}"
        echo "Server credentials loaded successfully"
    }
}

def buildJar() {
    echo 'building the application...'
    sh 'mvn clean package'
}
def buildImage() {
    echo "building the docker image..."
    withCredentials([usernamePassword(credentialsId: 'docker-hub', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
        sh "docker build -t ankit42098/my-app:${IMAGE_NAME} ."
        sh 'echo $PASS | docker login -u $USER --password-stdin'
        sh "docker push ankit42098/my-app:${IMAGE_NAME}"
    }
}
return this
