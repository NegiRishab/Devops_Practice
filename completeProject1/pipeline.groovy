def RunTests() {
    echo "Running backend and frontend tests..."

    parallel(
        'Backend Tests': {
            dir('backend') {
                sh 'npm install'
                sh 'npm test'
            }
        },
        'Frontend Tests': {
            dir('frontend') {
                sh 'npm install'
                sh 'npm test'
            }
        }
    )
}

def CreateInfrastructure() {
    echo "Creating infrastructure..."

    dir('terraform') {
        withCredentials([
            string(
                credentialsId: 'linode_token',
                variable: 'LINODE_TOKEN'
            ),
            string(
                credentialsId: 'linode-public-ssh-key',
                variable: 'SSH_PUBLIC_KEY'
            )
        ]) {
            sh '''
                terraform init

                terraform apply -auto-approve \
                    -var="linode_token=$LINODE_TOKEN" \
                    -var="ssh_public_key=$SSH_PUBLIC_KEY"
            '''

            env.SERVER_IP = sh(
                script: 'terraform output -raw server_ip',
                returnStdout: true
            ).trim()

            echo "Linode Server IP: ${env.SERVER_IP}"
        }
    }
}

def IncrementBackendVersion() {
    echo "Incrementing backend version..."

    dir('backend') {
        sh 'npm version major --no-git-tag-version'

        def packageJsonFile = readJSON file: 'package.json'

        env.BACKEND_VERSION = packageJsonFile.version

        echo "Backend version: ${env.BACKEND_VERSION}"
    }
}

def BuildBackendImage() {
    echo "Building backend image..."

    withCredentials([
        usernamePassword(
            credentialsId: 'docker_hub',
            usernameVariable: 'DOCKER_USERNAME',
            passwordVariable: 'DOCKER_PASSWORD'
        )
    ]) {
        sh '''
            echo "$DOCKER_PASSWORD" | docker login \
                -u "$DOCKER_USERNAME" \
                --password-stdin

            docker build \
                -t "ankit42098/taskboard-backend:${BRANCH_NAME}-${BACKEND_VERSION}" \
                ./backend

            docker push \
                "ankit42098/taskboard-backend:${BRANCH_NAME}-${BACKEND_VERSION}"
        '''

        env.BACKEND_IMAGE = "ankit42098/taskboard-backend:${env.BRANCH_NAME}-${env.BACKEND_VERSION}"

        echo "Backend image: ${env.BACKEND_IMAGE}"
    }
}


def IncrementFrontendVersion() {
    echo "Incrementing frontend version..."

    dir('frontend') {
        sh 'npm version major --no-git-tag-version'

        def packageJsonFile = readJSON file: 'package.json'

        env.FRONTEND_VERSION = packageJsonFile.version

        echo "Frontend version: ${env.FRONTEND_VERSION}"
    }
}

def BuildFrontendImage() {
    echo "Building frontend image..."

    withCredentials([
        usernamePassword(
            credentialsId: 'docker_hub',
            usernameVariable: 'DOCKER_USERNAME',
            passwordVariable: 'DOCKER_PASSWORD'
        )
    ]) {
        sh '''
            echo "$DOCKER_PASSWORD" | docker login \
                -u "$DOCKER_USERNAME" \
                --password-stdin

            docker build \
                --build-arg VITE_API_URL="http://${SERVER_IP}:5000/api" \
                -t "ankit42098/taskboard-frontend:${BRANCH_NAME}-${FRONTEND_VERSION}" \
                ./frontend

            docker push \
                "ankit42098/taskboard-frontend:${BRANCH_NAME}-${FRONTEND_VERSION}"
        '''

        env.FRONTEND_IMAGE = "ankit42098/taskboard-frontend:${env.BRANCH_NAME}-${env.FRONTEND_VERSION}"

        echo "Frontend image: ${env.FRONTEND_IMAGE}"
    }
}

def DeployOnServer() {
    echo "Starting deployment..."

    echo "SERVER_IP: ${env.SERVER_IP}"
    echo "BACKEND_IMAGE: ${env.BACKEND_IMAGE}"
    echo "FRONTEND_IMAGE: ${env.FRONTEND_IMAGE}"

dir('ansible') {
    withCredentials([
        sshUserPrivateKey(
            credentialsId: 'linode_private_ssh_key',
            keyFileVariable: 'SSH_KEY',
            usernameVariable: 'SSH_USER'
        )
    ]) {
        sh '''
            ansible-playbook \
                -i "${SERVER_IP}," \
                playbook.yaml \
                -u "${SSH_USER}" \
                --private-key "${SSH_KEY}" \
                -e "frontend_image=${FRONTEND_IMAGE}" \
                -e "backend_image=${BACKEND_IMAGE}" \
                -e "server_ip=${SERVER_IP}"
        '''
    }
}
}
def VersionBump() {
    echo "Version bumping..."

    withCredentials([
        usernamePassword(
            credentialsId: 'git_hub',
            usernameVariable: 'GITHUB_USERNAME',
            passwordVariable: 'GITHUB_PASSWORD'
        )
    ]) {
        sh '''
            git config --global user.name "Jenkins"
            
            git config --global user.email "jenkins@taskboard.com"

            git remote set-url origin \
                "https://${GITHUB_USERNAME}:${GITHUB_PASSWORD}@github.com/${GITHUB_USERNAME}/Devops_Practice.git"

            git add .
            git commit -m "Version bump"
            git push origin HEAD:${BRANCH_NAME}
        '''
    }
}

return this