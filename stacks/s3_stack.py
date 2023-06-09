from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_ssm as ssm,
)
from aws_cdk import RemovalPolicy
from constructs import Construct

class S3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Read Context variables.
        env = self.node.try_get_context("env")
        prj_name = self.node.try_get_context("prj_name")

        self.s3_bucket = s3.Bucket(self,f"{prj_name}-{env}-lambda-bkt",
            bucket_name=f"{prj_name}-{env}-lambda-bkt",
            encryption=s3.BucketEncryption.S3_MANAGED,
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )
        
        ssm.StringParameter(self,f"{prj_name}-lambda-bkt-ssm",
            parameter_name="/"+env+"/"+f"{prj_name}-lambda-bkt-ssm",
            string_value=self.s3_bucket.bucket_arn
        )        
        
        
        