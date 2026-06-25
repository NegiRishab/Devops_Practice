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
  
      withDockerRegistry([credentialsId: 'docker-hub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD']){
        sh 'echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USERNAME} --password-stdin'
        sh 'docker build -t ankit42098/taskboard-backend:${env.BACKEND_VERSION} ./backend'
        sh 'docker push ankit42098/taskboard-backend:${env.BACKEND_VERSION}'
        env.BACKEND_IMAGE = "ankit42098/taskboard-backend:${env.BACKEND_VERSION}"
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
      withDockerRegistry([credentialsId: 'docker-hub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD']){
        sh 'echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USERNAME} --password-stdin'
        sh 'docker build -t ankit42098/taskboard-frontend:${env.FRONTEND_VERSION} ./frontend'
        sh 'docker push ankit42098/taskboard-frontend:${env.FRONTEND_VERSION}'
        env.FRONTEND_IMAGE = "ankit42098/taskboard-frontend:${env.FRONTEND_VERSION}"
      }
}

def DeployOnServer(){
    echo "Deploying on server..."
}

def VersionBump(){
    echo "Version bumping..."
    withCredentials([usernamePassword(credentialsId: 'github', usernameVariable: 'GITHUB_USERNAME', passwordVariable: 'GITHUB_PASSWORD')]){
      sh '''
      git config --global user.name "Jenkins"
      git config --global user.email "jenkins@taskboard.com"
      git add .
      git commit -m "Version bump"
      git push "https://${GITHUB_USERNAME}:${GITHUB_PASSWORD}@github.com/NegiRishab/Devops_Practice.git" HEAD:main
      '''
    }
}
 return this 