def function (){
    echo "Hello World"
}

def versonIncrement(){
    echo "Version Incremented"
    sh "npm version patch --no-git-tag-version"
    env.VERSION = sh(script: "node -p \"require('./package.json').version\"", returnStdout: true).trim()
    echo "New version is: ${env.VERSION}"
}

def build(){
    echo 'Building...'
    
}
def buildImage(){
    echo 'Building Docker image...'
                // Add your Docker build commands here
                withCredentials([usernamePassword(credentialsId: 'docker_hub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh "docker build -t ankit42098/myapp:${env.VERSION} ."
                    sh "echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USERNAME} --password-stdin"
                    sh "docker push ankit42098/myapp:${env.VERSION}"
                }

}
def test(){
    echo 'Testing...'
                // Add your test commands here
}

def deploy(){
    echo 'Deploying...'
    echo "Branch name is: ${env.BRANCH_NAME}"
                // Add your deployment commands here
    
}

def gitTagging(){
    echo 'Git Tagging...'
               withCredentials([usernamePassword(credentialsId: 'git-hub', usernameVariable: 'GITHUB_USERNAME', passwordVariable: 'GITHUB_TOKEN')]) {
                    sh "git config --global user.name \"${GITHUB_USERNAME}\""
                    sh "git config --global user.email jenkins@jenkins.com"

                    sh "git remote set-url origin https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@github.com/NegiRishab/Docker_understanding.git"
                    sh 'git add .'
                    sh "git commit -m 'Update version to ${env.VERSION}'"
                    sh "git push origin HEAD:${env.BRANCH_NAME}"
                }
}

return this