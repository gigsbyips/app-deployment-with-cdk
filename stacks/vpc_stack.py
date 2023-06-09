from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ssm as ssm,
    CfnOutput  # LEVEL1 contruct.
)
from constructs import Construct

class VPCStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Read Context variables.
        cidr = self.node.try_get_context("vpc_cidr")
        env = self.node.try_get_context("env")
        prj_name = self.node.try_get_context("prj_name")

        ## VPC for the application
        ## self.<<VarName>> helps to refer this variable in other stacks.
        self.vpc = ec2.Vpc(self, f"{prj_name}-vpc",
            cidr=cidr,
            max_azs=2,
            enable_dns_hostnames=True,
            enable_dns_support=True,                      
            nat_gateways=2, # One per AZ.
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name=f"{prj_name}-pbl-sbnt",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name=f"{prj_name}-prv-sbnt",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24,
                ),
                ec2.SubnetConfiguration(
                    name=f"{prj_name}-isl-sbnt",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24
                )
            ]
        )
        
        prv_sbnts = [subnet.subnet_id for subnet in self.vpc.private_subnets]

        for i in range(len(prv_sbnts)):
            ssm.StringParameter(self,f"{prj_name}-prv-sbnt-"+str(i), string_value=prv_sbnts[i], 
                                parameter_name = "/" + env + "/" + f"{prj_name}-prv-sbnt-" + str(i))

        CfnOutput(self, "VpcId",
            value=self.vpc.vpc_id
        )
    

