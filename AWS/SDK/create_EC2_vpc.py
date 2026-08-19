import boto3

ec2 = boto3.client('ec2')

# 1. VPC作成
vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
vpc_id = vpc['Vpc']['VpcId']

# 2. サブネット作成
subnet = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.1.0/24')
subnet_id = subnet['Subnet']['SubnetId']

# 3. インターネットゲートウェイ作成とアタッチ
igw = ec2.create_internet_gateway()
igw_id = igw['InternetGateway']['InternetGatewayId']
ec2.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)

# 4. ルートテーブル作成と設定
route_table = ec2.create_route_table(VpcId=vpc_id)
rtb_id = route_table['RouteTable']['RouteTableId']
ec2.create_route(RouteTableId=rtb_id, DestinationCidrBlock='0.0.0.0/0', GatewayId=igw_id)
ec2.associate_route_table(RouteTableId=rtb_id, SubnetId=subnet_id)

# 5. セキュリティグループ作成
sg = ec2.create_security_group(GroupName='MySG', Description='Allow SSH', VpcId=vpc_id)
sg_id = sg['GroupId']
ec2.authorize_security_group_ingress(GroupId=sg_id, IpProtocol='tcp', FromPort=22, ToPort=22, CidrIp='0.0.0.0/0')

# 6. キーペア作成（または既存のものを使用）
key_name = 'NewKeyPair'
key = ec2.create_key_pair(KeyName=key_name)
with open(f'{key_name}.pem', 'w') as f:
    f.write(key['KeyMaterial'])

# 7. EC2インスタンス起動
instance = ec2.run_instances(
    ImageId='ami-0712bf5b0a7138d17',  
    InstanceType='t2.micro',
    KeyName=key_name,
    MaxCount=1,
    MinCount=1,
    NetworkInterfaces=[{
        'SubnetId': subnet_id,
        'DeviceIndex': 0,
        'AssociatePublicIpAddress': True,
        'Groups': [sg_id]
    }]
)

print(f"EC2インスタンス作成完了: {instance['Instances'][0]['InstanceId']}") 
