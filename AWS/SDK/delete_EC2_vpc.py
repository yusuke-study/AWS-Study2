import boto3

ec2 = boto3.client('ec2')

# 1. EC2インスタンスの削除
instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'pending']}])
for reservation in instances['Reservations']:
    for instance in reservation['Instances']:
        ec2.terminate_instances(InstanceIds=[instance['InstanceId']])
        print(f"EC2インスタンスを削除しました: {instance['InstanceId']}")

# 2. セキュリティグループの削除（default以外）

security_groups = ec2.describe_security_groups()
for sg in security_groups['SecurityGroups']:
    if sg['GroupName'] != 'default':
        try:
            ec2.delete_security_group(GroupId=sg['GroupId'])
        except Exception:
            pass  # 削除失敗時は何も表示しない
        else:
            print(f"セキュリティグループを削除しました: {sg['GroupId']}")

# 3. ルートテーブルの削除（メイン以外）
route_tables = ec2.describe_route_tables()
for rtb in route_tables['RouteTables']:
    for assoc in rtb.get('Associations', []):
        if not assoc.get('Main', False):
            ec2.disassociate_route_table(AssociationId=assoc['RouteTableAssociationId'])
        try:
            ec2.delete_route_table(RouteTableId=rtb['RouteTableId'])
        except Exception:
            pass  # エラー時は何も表示しない
        else:
             print(f"ルートテーブルを削除しました: {rtb['RouteTableId']}")

# 4. インターネットゲートウェイの削除
igws = ec2.describe_internet_gateways()
for igw in igws['InternetGateways']:
    for attach in igw.get('Attachments', []):
        ec2.detach_internet_gateway(InternetGatewayId=igw['InternetGatewayId'], VpcId=attach['VpcId'])
    ec2.delete_internet_gateway(InternetGatewayId=igw['InternetGatewayId'])
    print(f"インターネットゲートウェイを削除しました: {igw['InternetGatewayId']}")

# 5. サブネットの削除
subnets = ec2.describe_subnets()
for subnet in subnets['Subnets']:
    try:
        ec2.delete_subnet(SubnetId=subnet['SubnetId'])
    except Exception:
        pass  # 削除失敗時は何も表示しない
    else:
        print(f"サブネットを削除しました: {subnet['SubnetId']}")

# 6. VPCの削除（default以外）
vpcs = ec2.describe_vpcs()
for vpc in vpcs['Vpcs']:
    if not vpc.get('IsDefault', False):
        try:
            ec2.delete_vpc(VpcId=vpc['VpcId'])
        except Exception:
            pass  # 削除失敗時は何も表示しない
        else:
            print(f"VPCを削除しました: {vpc['VpcId']}")
