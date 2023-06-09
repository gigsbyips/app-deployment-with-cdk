
## This AWS CDK project creates typical AWS services required for deploying a Lambda function exposed via APIGW. Lmabda will access Database hosted in an Isolated Subnet of the application VPC.

# AWS CDK Version 2 is used.

The `cdk.json` file is used by CDK to run the application.

"cdk init" creates a virtual environment OR we can create it manually as below-

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
```