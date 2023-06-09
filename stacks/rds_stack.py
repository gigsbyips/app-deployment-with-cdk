from aws_cdk import (
    Stack,
    aws_rds as rds,
    aws_ssm as ssm,
    aws_secretsmanager as sm,
    aws_ec2 as ec2
)
from aws_cdk import RemovalPolicy
from constructs import Construct

class RDSStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id)

        # Read Context variables.
        env = self.node.try_get_context("env")
        prj_name = self.node.try_get_context("prj_name")

        # Read input params from the Kwargs.
        vpc = kwargs["vpc"]
        rds_sgrp = kwargs["rds_sgrp"]
        rds_kms_key = kwargs["rds_kms_key"]
        db_user_name = self.node.try_get_context("db_user_name")
        
        # Secret Manager auto generated password.
        db_secret= sm.Secret(self, f"{prj_name}-db-secret",
            secret_name=f"{prj_name}-{env}-db-secret",
            generate_secret_string=sm.SecretStringGenerator(
                generate_string_key='db_password',
                include_space=False,
                password_length=12,
                secret_string_template="{'username': db_user_name}",
                exclude_punctuation=True)
            )
        
        db_mysql= rds.DatabaseCluster(self,f"{prj_name}-db-clstr",
            default_database_name=f"{prj_name}-{env}-mysql-db",
            engine=rds.DatabaseClusterEngine.aurora_mysql(version=rds.AuroraMysqlEngineVersion.VER_3_03_0),
            instance_props=rds.InstanceProps(instance_type=ec2.InstanceType(instance_type_identifier="t3.small"),
                vpc=vpc, vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
                security_groups=[rds_sgrp]
            ),
            instances=1,
            storage_encrypted=True,
            storage_encryption_key=rds_kms_key,
            credentials= rds.Credentials.from_secret(db_secret, db_user_name),
            parameter_group=rds.ParameterGroup(self, f"{prj_name}-{env}-mysql-db-pgrp", 
                description="param group for aurora mysql",
                engine=rds.DatabaseClusterEngine.aurora_mysql(version=rds.AuroraMysqlEngineVersion.VER_3_03_0)
            ),
            removal_policy=RemovalPolicy.DESTROY  # Default policy is "snapshot" which is charged.
        )
        
        # SSM to store DB HostName.
        ssm.StringParameter(self,f"{prj_name}-db-hostname-ssm",
            parameter_name="/"+env+"/"+f"{prj_name}-db-hostname-ssm",
            string_value=db_mysql.cluster_endpoint.hostname
        )
        
        
        
        
        
        
        
        