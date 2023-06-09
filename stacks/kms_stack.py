from aws_cdk import (
    Stack,
    aws_kms as kms,
    aws_ssm as ssm
)
from constructs import Construct

class KMSStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Read Context variables.
        prj_name = self.node.try_get_context("prj_name")
        env = self.node.try_get_context("env")
        
        self.kms_rds = kms.Key(self, f"{prj_name}-key-rds",
                enable_key_rotation=True,
                description="key for RDS encryption",
                )

        self.kms_rds.add_alias(
            alias_name=f"alias/{prj_name}-key-rds"
        )
        
        ssm.StringParameter(self, f"{prj_name}-key-rds-ssm",
            parameter_name="/"+env+"/"+f"{prj_name}-key-rds-ssm",
            string_value=self.kms_rds.key_id
            )        