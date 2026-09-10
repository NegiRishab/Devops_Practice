#!/bin/bash
#

# this is a simple script to demonstrate the use of if-else statements in bash.
# echo "Enter a number: "
#  read -r number

#  if [ "$number" -gt 5 ]
#  then
# 	 echo " $number is greater than 5 "
#  else 
# 	 echo " $number is lower than 5 "
# fi





# echo "Enter a number: " 
# read -r number

# if (( number % 2 == 0))
# then 
#    echo "$number is even "
# else 
#    echo "$number is odd "
#    fi



# echo "Enter any numbers and i will tell you which one is the bigger one: "
# read -r -a numbers

# bigger=-9999999999 

# for number in "${numbers[@]}"
# do 
#    if (( number > bigger ))
#    then bigger=$number
# fi
# done

# echo "The bigger number is: $bigger"





# while true
# do 
# echo  "Enter the number and operation you want to perform: "
# read -r number1 operation number2
# if [[ "$number1" == "exit" ]]
# then 
# read -p "do you really want to exit press y for yes and n for No : " data

# if [[ "$data"  == "y" ]]
# then 
# break
# else
# continue
# fi
# fi
# Answer=0;

# case "$operation" in 
#     "+" )Answer=$(( number1 + number2 )) ;;
# 	"-" )Answer=$(( number1 - number2  )) ;;
# 	"*" )Answer=$(( number1 * number2  )) ;;
# 	"/" )Answer=$(( number1 /number2  )) ;;
# 	* )echo "invalid operation";;
# 	esac
# echo "The result is: $Answer"

# done


# read -p "Enter a number: " number

# count=0;
# while (( count <= number ))
# do 
#   echo "$count"
#   (( count++ ))
# done 


# read -p "Enter a file name : " name 

# match=( $name*)

# if [ ${#match[@]} -gt 0 ]
# then 
#    printf "The file name is : %s\n" "${match[@]}"
# else
#    echo "No file found with the name $name"
# fi
# read -p "Enter a file name to check if it exist or not: " file

# if [[ -e "$file" ]]
# then 
#   echo "file exist "
#   echo "this file has the size of : $(stat -c%s  "$file") "
#   else
#   echo "file not exist"
#   fi



# read -p  "Enter a file name for the backup: " file

# if [[ -e "$file" ]]
# then 
#     cp $file "${file}_$(date +%y%m%d)"
# 	echo "backup created successfully"
# else

# echo "file not exist"
# fi


# install latest java version 


# Exersise 2 install java 

# if command -v cowsay >/dev/null 2>&1; then

# echo "cowsay is already installed"
# else
# echo "cowsay is not installed"
# sudo apt update
# sudo apt install cowsay -y
# echo "cowsay has been installed successfully"

# fi
# version=$(dpkg -s cowsay | grep Version | awk -F ':' '{print $2}')
# echo "cowsay is already installed and the version is : $version"



# Exersise 3  

#!/bin/bash

# Check npm
#!/bin/bash

# # Check npm
# if command -v npm >/dev/null 2>&1; then
#     echo "npm already installed"
# else
#     echo "Installing node + npm..."
#     sudo apt update
#     sudo apt install nodejs npm -y
# fi

# echo "npm version: $(npm -v)"
# echo "node version: $(node -v)"

# # Create directory
# mkdir -p my_project

# # Download + extract safely
# curl -fSL https://node-envvars-artifact.s3.eu-west-2.amazonaws.com/bootcamp-node-envvars-project-1.0.0.tgz \
# | tar -xzv -C my_project --strip-components=1

# cd my_project || exit

# # Install dependencies
# npm install

# # Environment variables
# export APP_ENV=dev
# export DB_USER=myuser
# export DB_PWD=mysecret

# # Run app
# node server.js &

# # ps aux | grep node

# # ss -tuln | grep 3000 

# read -p "Press enter to see the logs of the app and stop it"  directory_name

# if [[ -d "$directory_name" ]]
# then 
#     echo "the directory $directory_name exist"
# else 
#     echo "the directory $directory_name does not exist"
#     mkdir "$directory_name"
#     echo "the directory $directory_name has been created"
# fi
# export LOG_DIR="$directory_name"





# Check npm
if command -v npm >/dev/null 2>&1; then
    echo "npm already installed"
else
    echo "Installing node + npm..."
    sudo apt update
    sudo apt install nodejs npm -y
fi

echo "npm version: $(npm -v)"
echo "node version: $(node -v)"

# Create directory
mkdir -p my_project

# Download safely
if curl -fSL https://node-envvars-artifact.s3.eu-west-2.amazonaws.com/bootcamp-node-envvars-project-1.0.0.tgz \
| tar -xz -C my_project --strip-components=1; then
    echo "Download successful"
else
    echo "Download failed"
    exit 1
fi

cd my_project || exit 1

# Install dependencies
npm install

# Env variables
export APP_ENV=dev
export DB_USER=myuser
export DB_PWD=mysecret

read -p "Enter a directory name for the logs: " directory_name

if [[ -z "$directory_name" ]]; then
    echo "Directory name cannot be empty"
    exit 1
fi

if [[ -d "$directory_name" ]]; then
    echo "Directory $directory_name exists"
else
    mkdir "$directory_name"
    echo "Directory $directory_name created"
fi
export LOG_DIR="$directory_name"


# Run app
node server.js &


