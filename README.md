# About this Repo

This repo is a reference for setting commonly used AWS services using Python and CDK V2.

## Pre-requisites

- AWS CLI is installed and a profile is set up.
- AWS CDK is installed. First install node.js on machine and then run `npm i -g aws-cdk `.
- Python is installed on the machine.

## Creating a CDK App locally from this repo.

Clone the Repo on your machine.

```
git clone https://github.com/gigsbyips/app-infra-with-cdk.git
cd app-infra-with-cdk

```
The `cdk.json` file is used by CDK to run the application. Context variables used by some of the stacks are listed in the `cdk.json` file. Please change their values for your work.

Create and activate a python virtual environment. When we initialize a CDK app with `cdk init app --language=python`, then a virtual env is auto created for us. Here we need to create it manually.

```
$ python -m venv .venv
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, install the required dependencies.

```
$ pip install -r requirements.txt
```

## Bootstrapping your AWS environment
The bootstrap command creates some necessary resources that are used by CDK behind the scene like S3 bucket where the CloudFormation templates are uploaded by CDK.

```
cdk bootstrap       # Deploys a stack in the account and region of the default profile
cdk bootstrap <ACCOUNT-NUMBER/REGION>
cdk bootstrap --profile <test_profile> <ACCOUNT-NUMBER/REGION>
```

## Some useful commands for AWS CDK.

```
$ cdk ls                                                  # List all stacks
$ cdk synth --profile <PROFILE_NAME>
$ cdk synth <StackName> --profile <ProfileNamme>
$ cdk diff <StackName> --profile <ProfileNamme>           # Check changeset of a particular stack.
$ cdk deploy --profile <PROFILE_NAME>

```