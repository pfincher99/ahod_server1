#! /usr/bin/env bash

echo Please provide the following details on your lab environment.
echo
echo "What is the address of your Mantl Control Server?  "
echo "eg: control.mantl.internet.com"
read control_address
echo
echo "What is the username for your Mantl account?  "
read mantl_user
echo
echo "What is the password for your Mantl account?  "
read -s mantl_password
echo
echo "What is the your Docker Username?  "
read docker_username
echo
echo "What is the Lab Application Domain?  "
read mantl_domain
echo
echo "What is your spark token?  "
read spark_token
echo
echo "What is the spark room id?  "
read spark_room
echo

export SPARK_TOKEN=$spark_token
export SPARK_ROOM=$spark_room

cp sample-demoapp.json $docker_username-demoapp.json
sed -i "" -e "s/DOCKERUSER/$docker_username/g" $docker_username-demoapp.json

echo " "
echo "***************************************************"
echo "Installing the demoapp as  ahod/$docker_username"
curl -k -X POST -u $mantl_user:$mantl_password https://$control_address:8080/v2/apps \
-H "Content-type: application/json" \
-d @$docker_username-demoapp.json \
| python -m json.tool

echo "***************************************************"
echo

echo Installed

echo "Wait 2-3 minutes for the service to deploy. "
echo
echo "You can watch the progress from the GUI at: "
echo
echo "https://$control_address/marathon"
echo