from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_ssm as ssm,
    CfnOutput
)
from constructs import Construct

class SecurityStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id)
        
        # Read Context variables.
        local_ip = self.node.try_get_context("local_ip")
        env = self.node.try_get_context("env")
        prj_name = self.node.try_get_context("prj_name")
        
        # Read input parameter from kwargs
        vpc = kwargs["vpc"]

        # Security Group for Lambda.
        self.lambda_sgrp = ec2.SecurityGroup(self, f"{prj_name}-lambda-sg",
            vpc=vpc, allow_all_outbound=True, 
            description="security group for Lambda",
            security_group_name=f"{prj_name}-lambda-sg"
        )
        
        # IAM Role for Lambda.
        lambda_role = iam.Role(self, f"{prj_name}-lambda-role",
            assumed_by=iam.ServicePrincipal(service='lambda.amazonaws.com'),
            role_name=f"{prj_name}-lambda-role",
            managed_policies=[iam.ManagedPolicy.from_managed_policy_name(self,"LambdaBasicExecutionRole",
            managed_policy_name="service-role/AWSLambdaBasicExecutionRole")]
        )

        lambda_role.add_to_policy(
            statement = iam.PolicyStatement(
                actions = ['s3:*','rds:*'],
                resources = ['*']
            )
        )

        ssm.StringParameter(self,f"{prj_name}-lambda-sgrp-ssm",
            parameter_name="/"+env+"/"+f"{prj_name}-lambda-sgrp-ssm",
            string_value=self.lambda_sgrp.security_group_id 
        )
        
        ssm.StringParameter(self,f"{prj_name}-lambda-role-arn-ssm",
            parameter_name="/"+env+"/"+f"{prj_name}-lambda-role-arn-ssm",
            string_value=lambda_role.role_arn
        )

        ssm.StringParameter(self,f"{prj_name}-lambda-role-name-ssm",
            parameter_name="/"+env+"/"+f"{prj_name}-lambda-role-name-ssm",
            string_value=lambda_role.role_name
        )                

        # Bastion Host SGRP
        self.bastion_sgrp = ec2.SecurityGroup(self, f"{prj_name}-bstn-sg",
            vpc=vpc, allow_all_outbound=True,
            description="security group for bastion host",
            security_group_name=f"{prj_name}-bstn-sg"
        )
        
        self.bastion_sgrp.add_ingress_rule(ec2.Peer.ipv4(local_ip), ec2.Port.tcp(22), 
            "SSH from personal machine")

        # Aurora Mysql SGRP
        self.rds_sgrp = ec2.SecurityGroup(self, f"{prj_name}-db-sg",
            vpc=vpc, 
            allow_all_outbound=True, allow_all_ipv6_outbound=True,
            description="security group for database",
            security_group_name=f"{prj_name}-db-sg"
        )
        
        self.rds_sgrp.add_ingress_rule(ec2.Peer.security_group_id(security_group_id=self.lambda_sgrp.security_group_id),
            ec2.Port.tcp(3306),"Traffic from lambda functions")           
        
        self.rds_sgrp.add_ingress_rule(ec2.Peer.security_group_id(security_group_id=self.bastion_sgrp.security_group_id), 
            ec2.Port.tcp(3306), "Traffic from Bastion host")      
        
        # Redis Security Group
        self.redis_sgrp = ec2.SecurityGroup(self, f"{prj_name}-redis-sg",
            vpc=vpc, 
            allow_all_outbound=True, allow_all_ipv6_outbound=True,
            description="security group for redis cluster",
            security_group_name=f"{prj_name}-redis-sg"
        )
        
        self.redis_sgrp.add_ingress_rule(ec2.Peer.security_group_id(security_group_id=self.lambda_sgrp.security_group_id),
            ec2.Port.tcp(6379),"Traffic from lambda functions")   
        
        CfnOutput(self, "RedisSecurityGroup",
            value=self.redis_sgrp.security_group_id
        )