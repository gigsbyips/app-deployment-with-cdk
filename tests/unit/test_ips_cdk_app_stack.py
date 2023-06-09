import aws_cdk as core
import aws_cdk.assertions as assertions

from stacks.vpc_stack import VPCStack

def test_vpc_created():
    app = core.App()
    stack = VPCStack(app, "test-vpc-stack")
    template = assertions.Template.from_stack(stack)

    template.has_resource("AWS::EC2::VPC")
