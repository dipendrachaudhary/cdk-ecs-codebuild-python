from typing import Container
from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_ecr as ecr,
    core,
)


class ECSService(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, cluster, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "FargateService",
            cluster=cluster,                
            # task_image_options={
            #     'image': ecs.ContainerImage.from_registry("wordpress")
            # }

            memory_limit_mib= 1024,
            cpu= 512,
            desired_count= 2,
            task_image_options= {
                'image': ecs.ContainerImage.from_asset("./backend/"),
                'container_port': 9005,
                'container_name': "NodeJS",
            },
        )

        fargate_service.service.connections.security_groups[0].add_ingress_rule(
            peer = ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection = ec2.Port.tcp(80),
            description="Allow http inbound from VPC"
        )

        core.CfnOutput(
            self, "LoadBalancerDNS",
            value=fargate_service.load_balancer.load_balancer_dns_name
        )
        core.CfnOutput(
            self, "Service",
            value=fargate_service.service.service_name
        )