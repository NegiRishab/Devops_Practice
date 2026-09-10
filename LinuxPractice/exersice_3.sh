#!/bin/bash 
apt update 
NEW_USER="newOne"

nodeVersion=$(node -v)
npmVersion=$(npm -v)

if [[ $nodeVersion ]]; then
    echo "NOde is installed, version: $nodeVersion" 
else
    sudo apt install nodejs
fi

if [[ $npmVersion ]]; then
    echo "NPM is installed, version: $npmVersion"
else
     sudo apt install npm
fi


read -p "a directory where application will write logs." logDir

if [[ ! -d "$logDir" ]]; then
    echo "Directory does not exist. Creating directory..."
    mkdir -p "$logDir"
fi


useradd $NEW_USER -m
chown $NEW_USER -R $logDir 

sudo -u $NEW_USER bash -c '
 whoami
cd ~
curl -sl https://node-envvars-artifact.s3.eu-west-2.amazonaws.com/bootcamp-node-envvars-project-1.0.0.tgz | tar -xzv
cd package
export DB_USER="myuser"
export DB_PWD="mysecretpassword"
export APP_ENV="dev" 
export LOG_DIR="$logDir"
npm install
node server.js &

ps aux | grep "node server.js"

read -p "Press exit to stop the server..." exit 


# ps aux | grep "node server.js" | awk '{print $2}' | xargs kill -9
if [[ $exit == "exit" ]]; then
    echo "Stopping the server..."   
        pkill -9 -f "node server.js"
fi


'

