from aws_cdk import (
    Stack,
    aws_cognito as cognito,
    aws_ssm as ssm
) 
from constructs import Construct

class CognitoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        prj_name = self.node.try_get_context("prj_name")
        env_name = self.node.try_get_context("env")

        user_pool = cognito.CfnUserPool(self, 'cognitouserpool',
            auto_verified_attributes=[
                'email'
            ],
            username_attributes=[
                'email','phone_number'
            ],
            user_pool_name=f"{prj_name}-user-pool",
            schema=[
                {
                    'attributeDataType': 'String',
                    'name': 'param1',
                    'mutable': True
                }
            ],
            policies=cognito.CfnUserPool.PoliciesProperty(
                password_policy=cognito.CfnUserPool.PasswordPolicyProperty(
                    minimum_length=10,
                    require_lowercase=True,
                    require_numbers=True,
                    require_symbols=False,
                    require_uppercase=True
                )
            )
        )

        user_pool_client = cognito.CfnUserPoolClient(self, f"{prj_name}-pool-client",
            user_pool_id=user_pool.ref,
            client_name=f"{prj_name}-{env_name}-app-client"
        )

        identity_pool = cognito.CfnIdentityPool(self, 'identitypool',
            allow_unauthenticated_identities=False,
            cognito_identity_providers=[
                cognito.CfnIdentityPool.CognitoIdentityProviderProperty(
                    client_id=user_pool_client.ref,
                    provider_name=user_pool.attr_provider_name
                )
            ],
            identity_pool_name=f"{prj_name}-identity-pool"
        )

        ssm.StringParameter(self,f"{prj_name}-client-app-id-ssm",
            parameter_name='/'+env_name+'/'+f"{prj_name}-cognito-client-app-id-ssm",
            string_value=user_pool_client.ref
        )

        ssm.StringParameter(self, f"{prj_name}-user-pool-id-ssm",
            parameter_name='/'+env_name+'/'+f"{prj_name}-cognito-user-pool-id-ssm",
            string_value=user_pool_client.user_pool_id
        )

        ssm.StringParameter(self,f"{prj_name}-identity-pool-id-ssm",
            parameter_name='/'+env_name+'/'+f"{prj_name}-identity-pool-id-ssm",
            string_value=identity_pool.ref
        )