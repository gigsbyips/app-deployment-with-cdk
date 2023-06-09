# About this Repo

This repo is a reference for setting commonly used AWS services using Python and CDK V2.

## Pre-requisites

- AWS CLI is installed and a profile is set up.
- AWS CDK is installed. First install node.js on machine and then run `npm i -g aws-cdk `.
- Python is installed on the machine.


The `cdk.json` file is used by CDK to run the application. Context variables used by some of the stacks are listed in the `cdk.json` file. Please change the values. 

`cdk init` will create the virtual environment OR we can create it manually as shown below-

```
$ python -m venv .venv
```
Now activate the virtual environment (on Windows) by running command below-

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, install the required dependencies.

```
$ pip install -r requirements.txt
```

Get list of stack and synthesize the CloudFormation template.

```
$ cdk ls
$ cdk synth --profile <PROFILE_NAME>
$ cdk deploy --profile <PROFILE_NAME>
$ cdk ls                                                      # List all stacks
$ cdk diff <<StackName>> --profile <<ProfileNamme>>           # Check changeset of a particular stack.
$ cdk synth <<StackName>> --profile <<ProfileNamme>>

```