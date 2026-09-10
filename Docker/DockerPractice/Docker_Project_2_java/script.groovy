
def incrementBuildNumber() {
    echo "Incrementing build number..."

       sh """
        mvn build-helper:parse-version \\
          versions:set \\
          '-DnewVersion=\${parsedVersion.majorVersion}.\${parsedVersion.minorVersion}.\${parsedVersion.nextIncrementalVersion}' \\
          versions:commit
    """
   def matcher = readFile('pom.xml') =~ /<version>(.+)<\/version>/
    def newVersion = matcher[0][1]
    env.IMAGE_TAG = newVersion
}
def build() {
    println "Building the project...1"
     sh 'mvn clean package'

}
def test() {
    println "Running tests..."
    // Add test logic here
}
def buildImage() {
    withCredentials([usernamePassword(credentialsId: 'docker_hub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
        sh "echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin"
        sh "docker build -t ankit42098/superhero-app:${env.IMAGE_TAG} ."
        sh "docker push ankit42098/superhero-app:${env.IMAGE_TAG}"
        env.IMAGE_NAME = "ankit42098/superhero-app:${env.IMAGE_TAG}"
    }
}
def deploy() {
    println "Deploying the application..."
    // Add deploy logic here
}
def git() {
    println "Performing git operations..."
    // Add git logic here
    withCredentials([usernamePassword(credentialsId: 'git-hub', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
        sh "git config --global user.name '$GIT_USERNAME'"
        sh "git config --global user.email 'jenkins@jenkins.com'"

        sh "git remote set-url origin https://$GIT_USERNAME:$GIT_PASSWORD@github.com/$GIT_USERNAME/Docker_understanding_java_application.git"
        sh "git add ."
        sh "git commit -m 'Automated commit from Jenkins'"
        sh "git push origin HEAD:${env.BRANCH_NAME}"
    }
}

return this