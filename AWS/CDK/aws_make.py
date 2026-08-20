from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct

class MyVpcStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # VPC の作成（ip_addresses を使用）
        self.vpc = ec2.Vpc(
            self, "MainVPC",
            ip_addresses=ec2.IpAddresses.cidr("172.32.0.0/16"),
            max_azs=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="PrivateSubnet",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24
                )
            ]
        )

        # セキュリティグループの作成（RDP許可）
        self.sg = ec2.SecurityGroup(
            self, "WindowsSG",
            vpc=self.vpc,
            description="Allow incoming RDP connections",
            allow_all_outbound=True
        )

        self.sg.add_ingress_rule(
            peer=ec2.Peer.ipv4("xxx.xxx.xxx.xxx/32"),
            connection=ec2.Port.tcp(3389),
            description="Allow RDP"
        )

        # 既存のキーペアを参照（key_name の代わりに key_pair を使用）
        key_pair = ec2.KeyPair.from_key_pair_name(self, "ImportedKey", "Windows_Key")

        # EC2 インスタンスの作成
        self.instance = ec2.Instance(
            self, "WindowsInstance",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.generic_windows({
                "ap-northeast-1": "ami-0e0811efc08b3f2aa"
            }),
            vpc=self.vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_group=self.sg,
            key_pair=key_pair
        )
