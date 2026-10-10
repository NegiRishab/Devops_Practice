def PrepareBuild() {
    def commit = sh(script: 'git rev-parse --short=12 HEAD', returnStdout: true).trim()
    def jobName = (env.JOB_NAME ?: 'taskboard')
        .replaceAll('[^a-zA-Z0-9_.-]', '-').take(80)
    env.IMAGE_TAG = "build-${jobName}-${env.BUILD_NUMBER}-${commit}"
    sh 'mkdir -p .ci && chmod 700 .ci'
}

def RunTests() {
    parallel(
        'Backend Tests': {
            dir('backend') {
                sh 'npm ci'
                sh 'npm test'
            }
        },
        'Frontend Tests': {
            dir('frontend') {
                sh 'npm ci'
                sh 'npm test'
            }
        }
    )
}

def WithAws(Closure body) {
    withCredentials([[
        $class: 'AmazonWebServicesCredentialsBinding',
        credentialsId: 'aws_credentials'
    ]]) {
        body()
    }
}

def CreateInfrastructure() {

    withCredentials([
        file(credentialsId: 'taskboard_tfvars', variable: 'TFVARS_FILE'),
        file(credentialsId: 'taskboard_tf_backend', variable: 'TF_BACKEND_FILE')
    ]) {
        WithAws {
            withEnv(["TF_VAR_aws_region=${env.AWS_REGION}"]) {
                dir('EKswithterraform') {
                    sh '''
                        terraform init -input=false -backend-config="$TF_BACKEND_FILE"
                        terraform validate
                        terraform plan -input=false -lock-timeout=5m \
                            -var-file="$TFVARS_FILE" -out=../.ci/infrastructure.tfplan
                        terraform apply -input=false -lock-timeout=5m ../.ci/infrastructure.tfplan
                    '''
                    env.EKS_CLUSTER_NAME = sh(script: 'terraform output -raw cluster_name', returnStdout: true).trim()
                    env.ECR_REGISTRY = sh(script: 'terraform output -raw ecr_registry', returnStdout: true).trim()
                    env.BACKEND_REPOSITORY = sh(script: 'terraform output -raw backend_repository_url', returnStdout: true).trim()
                    env.FRONTEND_REPOSITORY = sh(script: 'terraform output -raw frontend_repository_url', returnStdout: true).trim()
                }
            }
        }
    }
}

def LoginToEcr() {
    sh '''
        set +x
        ECR_PASSWORD=$(aws ecr get-login-password --region "$AWS_REGION")
        printf '%s' "$ECR_PASSWORD" | docker login \
            --username AWS --password-stdin "$ECR_REGISTRY"
        unset ECR_PASSWORD
    '''
}


def BuildBackendImage() {
    env.BACKEND_IMAGE = "${env.BACKEND_REPOSITORY}:${env.IMAGE_TAG}"
    WithAws {
        withEnv(["DOCKER_CONFIG=${pwd()}/.ci/docker"]) {
            LoginToEcr()
            sh '''
                docker build --platform linux/amd64 -t "$BACKEND_IMAGE" ./backend
                docker push "$BACKEND_IMAGE"
            '''
        }
    }
}

def BuildFrontendImage() {
    env.FRONTEND_IMAGE = "${env.FRONTEND_REPOSITORY}:${env.IMAGE_TAG}"
    WithAws {
        withEnv(["DOCKER_CONFIG=${pwd()}/.ci/docker"]) {
            LoginToEcr()
            sh '''
                docker build --platform linux/amd64 --build-arg VITE_API_URL=/api \
                    -t "$FRONTEND_IMAGE" ./frontend
                docker push "$FRONTEND_IMAGE"
            '''
        }
    }
}

def DeployToEks() {
    WithAws {
        withEnv(["KUBECONFIG=${pwd()}/.ci/kubeconfig"]) {
            sh 'bash k8s/deploy.sh'
        }
    }
}


return this
