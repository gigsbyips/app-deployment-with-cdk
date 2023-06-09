from aws_cdk import (
    Stack,
    aws_ec2 as ec2
)
from constructs import Construct

class BastionHostStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id)
        
        # Read Context variables.
        prj_name = self.node.try_get_context("prj_name")
        
        # Read input parameters
        vpc = kwargs["vpc"]
        sgrp = kwargs["sgrp"]
       
        # EC2 Instance
        ec2.Instance(self,f"{prj_name}-bstn-host",
            instance_name=f"{prj_name}-bstn-host",
            instance_type=ec2.InstanceType('t3.micro'),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
            ),
            key_name=f"{prj_name}-bstn-key",
            security_group=sgrp,
            machine_image=ec2.AmazonLinuxImage(
                edition=ec2.AmazonLinuxEdition.STANDARD,
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2023,
                virtualization=ec2.AmazonLinuxVirt.HVM,
                storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
            )    
        )       

