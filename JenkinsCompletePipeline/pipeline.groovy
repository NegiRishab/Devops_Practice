def RunTests(){
   echo "Running backend and frontend tests..."
   parallel(
      'Backend Tests': {
         dir('backend'){
            sh 'npm install'
            sh 'npm test'
         }
      },
      'Frontend Tests': {
         dir('frontend'){
            sh 'npm install'
            sh 'npm test'
         }
      }
   )
}

def IncrementBackendVersion(){
   echo "Incrementing backend version..."
   dir('backend'){
      sh 'npm version major --no-git-tag-version'
      def packageJsonFile = readJSON file: 'package.json'
      echo "Backend version incremented to ${packageJsonFile.version}"
      env.BACKEND_VERSION = packageJsonFile.version
     
   }
}

def BuildBackendImage(){
    echo "Building backend image..."
  
      withCredentials([usernamePassword(credentialsId: 'docker_hub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]){
        sh 'echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin'
        sh "docker build -t ankit42098/taskboard-backend:${env.BRANCH_NAME}-${env.BACKEND_VERSION} ./backend"
        sh "docker push ankit42098/taskboard-backend:${env.BRANCH_NAME}-${env.BACKEND_VERSION}"
        env.BACKEND_IMAGE = "ankit42098/taskboard-backend:${env.BRANCH_NAME}-${env.BACKEND_VERSION}"
      }
}

def IncrementFrontendVersion(){
  echo "Incrementing frontend version..."
  dir('frontend'){
    sh 'npm version major --no-git-tag-version'
    def packageJsonFile = readJSON file: 'package.json'
    echo "Frontend version incremented to ${packageJsonFile.version}"
    env.FRONTEND_VERSION = packageJsonFile.version
  }
}

def BuildFrontendImage(){
      echo "Building frontend image..."
      withCredentials([usernamePassword(credentialsId: 'docker_hub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]){
        sh 'echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin'
        sh "docker build -t ankit42098/taskboard-frontend:${env.BRANCH_NAME}-${env.FRONTEND_VERSION} ./frontend"
        sh "docker push ankit42098/taskboard-frontend:${env.BRANCH_NAME}-${env.FRONTEND_VERSION}"
        env.FRONTEND_IMAGE = "ankit42098/taskboard-frontend:${env.BRANCH_NAME}-${env.FRONTEND_VERSION}"
      }
}

def DeployOnServer(){
    echo "lets start the deployment..."
}

def VersionBump(){
    echo "Version bumping..."
    withCredentials([usernamePassword(credentialsId: 'gitHub', usernameVariable: 'GITHUB_USERNAME', passwordVariable: 'GITHUB_PASSWORD')]){
      sh '''
      git config --global user.name "Jenkins"
      git config --global user.email "jenkins@taskboard.com"
      git remote set-url origin "https://${GITHUB_USERNAME}:${GITHUB_PASSWORD}@github.com/${GITHUB_USERNAME}/Devops_Practice.git"
      git add .
      git commit -m "Version bump"
      git push origin HEAD:${BRANCH_NAME}
     
      '''
    }
}
 return this 