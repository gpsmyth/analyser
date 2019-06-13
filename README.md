# analyser
python using botot3 - for ec2 instances to begin with

## About
Demo project using botot3 to interrogate info on ec2 instances

## Pre-requisites after git clone
```
pip3 install pipenv
pipenv install boto3
pipenv install -d ipython
```

## Configurating
analyser.py use the analyer profile created via the AWS CLI like:

`aws configure --profile analyser`

Creds obtained from IAM role of analyser also

## Running the program

From the checkout directory
`pipenv run python boto3/ec2.py`

