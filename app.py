#!/usr/bin/env python3
import aws_cdk as cdk
from stacks.vpc_stack import VPCStack
from stacks.security_stack import SecurityStack
from stacks.bastion_host_stack import BastionHostStack
from stacks.kms_stack import KMSStack
from stacks.s3_stack import S3Stack
from stacks.rds_stack import RDSStack
from stacks.redis_stack import RedisStack
from stacks.cognito_stack import CognitoStack
from stacks.apigw_stack import APIGWStack


app = cdk.App()

vpc_stack = VPCStack(app, "serverless-app-vpc-stack")
sec_stack = SecurityStack(app, "serverless-app-security-stack",vpc=vpc_stack.vpc)
bastn_stack = BastionHostStack(app, "serverless-app-bstn-host-stack", vpc=vpc_stack.vpc, sgrp=sec_stack.bastion_sgrp)
kms_stack = KMSStack(app, "serverless-app-kms-stack")
s3_stack = S3Stack(app, "serverless-app-s3-stack")
rds_stack = RDSStack(app, "serverless-app-rds-stack", vpc=vpc_stack.vpc, 
    rds_sgrp=sec_stack.rds_sgrp, rds_kms_key=kms_stack.kms_rds
)
redis_stack = RedisStack(app, "serverless-app-redis-stack", vpc=vpc_stack.vpc, redis_sgrp=sec_stack.redis_sgrp)
cognito_stack = CognitoStack(app, "serverless-app-cognito-stack")
apigw_stack = APIGWStack(app, "serverless-app-apigw-stack")

app.synth()