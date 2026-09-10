#!/bin/bash

# echo "lets check the latest java version"
# data=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}')

# if [[ "$data" ]]; then
#     echo "java is installed"
#     if [[ "$data" < "17" ]]; then
#         echo "java version is less than 17"
       
#     else
#        echo "java version is greater than or equal to 17"
#      exit 0
#     fi
# else
#     echo "java is not installed"

# fi
#  echo "Installing latest java version..."
#         sudo apt update
#         sudo apt install default-jre -y
#         echo "java has been installed successfully"



        # learnign from this code is   2>&1  to redirect the error output to standard output and then we can use awk to extract the version number from the output of java -version command.