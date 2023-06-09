from aws_cdk import (
    Stack,
    aws_elasticache as redis,
    aws_ssm as ssm
)
from constructs import Construct

class RedisStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id)

        # Read Context variables.
        env = self.node.try_get_context("env")
        prj_name = self.node.try_get_context("prj_name")

        # Read input params from the Kwargs.
        vpc = kwargs["vpc"]
        redis_sgrp = kwargs["redis_sgrp"]
        
        # Extract List of Private Subnets.
        subnets = [subnet.subnet_id for subnet in vpc.private_subnets]
        
        sbnt_grp= redis.CfnSubnetGroup(self, f"{prj_name}-redis-sbnt-grp",
            subnet_ids=subnets,
            description="subnet group for redis"
        )
        
        redis_clstr = redis.CfnCacheCluster(self, f"{prj_name}-redis-clstr",
            cache_node_type='cache.t3.micro',
            num_cache_nodes=1,
            engine='redis',
            cache_subnet_group_name=sbnt_grp.ref,
            auto_minor_version_upgrade=True,
            cluster_name=f"{prj_name}-redis-clstr",
            vpc_security_group_ids=[redis_sgrp.security_group_id]
        )
        
        redis_clstr.add_depends_on(sbnt_grp) # Depends on.
        
        # SSM Params to store Redis Cluster Details.
        ssm.StringParameter(self,f"{prj_name}-redis-epoint-ssm",
            parameter_name="/"+env+"/"+f"{prj_name}-redis-epoint-ssm",
            string_value=redis_clstr.attr_configuration_endpoint_address
        )
        
        ssm.StringParameter(self,f"{prj_name}-redis-port-ssm",
            parameter_name="/"+env+"/"+f"{prj_name}-redis-port-ssm",
            string_value=redis_clstr.attr_configuration_endpoint_port
        )        
        
        