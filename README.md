# This repo is a reference for setting commonly used AWS services using Python and CDK V2.

Context variables used for the stacks are listed in the `cdk.json` file. Please change it accordingly.

The `cdk.json` file is used by CDK to run the application.

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
```