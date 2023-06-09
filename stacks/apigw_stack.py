from aws_cdk import (
    aws_apigateway as apigw,
    aws_ssm as ssm,
    Stack,
    Aws
) 
from constructs import Construct


class APIGWStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Read context variables.
        prj_name = self.node.try_get_context("prj_name")
        env_name = self.node.try_get_context("env")

        # Get Region
        region = Aws.REGION

        api_gateway = apigw.RestApi(self, f"{prj_name}-restapi",
            endpoint_types=[apigw.EndpointType.REGIONAL],
            rest_api_name=f"{prj_name}-restapi"
        )
        api_gateway.root.add_method('ANY')
        
        # ssm param for storing API's endpoint.
        ssm.StringParameter(self,f"{prj_name}-api-gw",
            parameter_name='/'+env_name+'/'+f"{prj_name}-api-gw-url",
            string_value='https://'+api_gateway.rest_api_id+'.execute-api.'+region+'.amazonaws.com/'
        )
        ssm.StringParameter(self,f"{prj_name}-api-gw-id",
            parameter_name='/'+env_name+'/'+f"{prj_name}-api-gw-id",
            string_value=api_gateway.rest_api_id
        )