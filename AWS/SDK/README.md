#	AWS SDK実行検証

AWS SDKの実行検証結果を下記に記載する。


## AWS SDK事前準備

(1)	VSCode（Visual Studio Code）を起動する。

(2)	Pythonをインストールする。
 
![SDK](./SDK_01.png)

(3)	VSCodeのメニューから「ターミナル」 > 「新しいターミナル」を選択して、ターミナルをクリックする。

(4)	ターミナルで、「pip install boto3」を実行する。
※boto3をインストールする。
 
![SDK](./SDK_02.png)

(5)	「aws configure」を実行する。
 
![SDK](./SDK_03.png)
 
##	AWS SDK動作検証

### S3バケット一覧表示

下記は、S3の汎用バケットを一覧表示するPythonコードの実行結果を下記に記載する。

(1)	事前にAWS上に汎用バケットを作成する。

![SDK](./SDK_04.png)

(2)	ターミナルで、下記内容の「main.py」を作成し、コードを実行する。
※S3バケットの一覧を取得する

------------------------------------------------------------------------------------------------------------
import boto3

# S3クライアントの作成
s3 = boto3.client('s3')

# S3バケットの一覧を取得
response = s3.list_buckets()

# バケット名を表示
print("S3 Buckets:")
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')
------------------------------------------------------------------------------------------------------------

![SDK](./SDK_05.png)

![SDK](./SDK_06.png)

###	S3にファイルアップロード

下記は、S3の汎用バケット内に、ファイルをアップロードさせた実行結果を下記に記載する。

(1)	ターミナルで、下記内容の「upload_to_s3.py」を作成し、コードを実行する。
S3にファイルを新規作成する。

------------------------------------------------------------------------------------------------------------
import boto3

# S3クライアントの作成
s3 = boto3.client('s3')

# ファイルのパスとS3のキー（保存名）
local_file = 'sample_upload.txt'
bucket_name = 'test-bucket-20251015'　#バケットを指定
s3_key = 'sample_upload.txt'　　#ファイルを指定

# ファイルをアップロード
s3.upload_file(local_file, bucket_name, s3_key)

print("アップロード完了")
------------------------------------------------------------------------------------------------------------


![SDK](./SDK_07.png)

![SDK](./SDK_08.png)

###	S3ファイル新規作成

下記は、S3の汎用バケット内に、ファイルを新規作成させた実行結果を下記に記載する。

(1)	ターミナルで、下記内容の「S3_makefile_s3.py」を作成し、コードを実行する。
S3にファイルを新規作成する。

------------------------------------------------------------------------------------------------------------
import boto3

# ファイル作成
with open('makefile_upload.txt', 'w', encoding='utf-8') as f:
    f.write('これはS3バケット「test-bucket-20251015」にアップロードするサンプルファイルです。\n')

# S3クライアント作成
s3 = boto3.client('s3')

# アップロード
s3.upload_file('makefile_upload.txt', 'test-bucket-20251015', ' makefile_upload.txt')

print("アップロード完了")
------------------------------------------------------------------------------------------------------------


![SDK](./SDK_09.png)

![SDK](./SDK_10.png)

結果：test-bucket-20251015に、sample_upload.txtが作成される。

###	S3アクセス権設定

下記は、S3の汎用バケットの、パブリックアクセスブロックの解除と、バケットポリシーの設定を全員に読み取り許可に変更させた実行結果を下記に記載する。

(1)	ターミナルで、下記内容の「S3_Access Rights.py」を作成し、コードを実行する。

------------------------------------------------------------------------------------------------------------
import boto3

s3 = boto3.client('s3')
bucket_name = 'test-bucket-20251015'

# パブリックアクセスブロックを解除
s3.delete_public_access_block(Bucket=bucket_name)
print(f"{bucket_name} のパブリックアクセスブロックを解除しました。")

# バケットポリシーの設定（全員に読み取り許可）
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Sid": "PublicReadGetObject",
        "Effect": "Allow",
        "Principal": "*",
        "Action": ["s3:GetObject"],
        "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
    }]
}

import json

s3.put_bucket_policy(
    Bucket=bucket_name,

    Policy=json.dumps(bucket_policy)
)

print(f"{bucket_name} にパブリック読み取りポリシーを設定しました。")
------------------------------------------------------------------------------------------------------------

![SDK](./SDK_11.png)

参考:コード実行前

![SDK](./SDK_12.png)

参考:コード実行後

![SDK](./SDK_13.png)


###	EC2_VPC作成

下記は、EC2インスタンス(Amazon Linux)と、それを実行させるために必要な最低限のシステム(VPC等)を作成させた実行結果である。

(1)	ターミナルで、下記内容の「create_EC2_vpc.py」を作成し、コードを実行する。
※EC2インスタンスのImageIdは、よく変わるので注意
------------------------------------------------------------------------------------------------------------
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
------------------------------------------------------------------------------------------------------------
  

 
 
###	EC2_VPC全削除

下記は、EC2インスタンスとVPC関連の下記コードに入力されているシステムを全て削除するコードの実行結果を下記に記載する。
※キーペアは含まない。
※デフォルトで削除できないシステム(セキュリティグループ、VPC、サブネットルートテーブル、)は削除しない。

(1)	ターミナルで、下記内容の「delete_EC2_vpc.py」を作成し、コードを実行する。
------------------------------------------------------------------------------------------------------------
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
------------------------------------------------------------------------------------------------------------
 

メモ①：デフォルトで削除できないシステム(セキュリティグループ、VPC、サブネットルートテーブル、)は削除失敗となるが、メッセージを出力しないために、下記内容でコードを修正した。

①	コード修正前
    try:
        ec2.delete_route_table(RouteTableId=rtb['RouteTableId'])
        print(f"ルートテーブルを削除しました: {rtb['RouteTableId']}")
    except Exception as e:
        print(f"削除失敗: {rtb['RouteTableId']} - {e}")

②	コード修正後
        try:
            ec2.delete_route_table(RouteTableId=rtb['RouteTableId'])
        except Exception:
            pass  # エラー時は何も表示しない
        else:
             print(f"ルートテーブルを削除しました: {rtb['RouteTableId']}")

メモ②：キーペアを全て削除したい場合は、下記を実行する。
#キーペアの削除
key_pairs = ec2.describe_key_pairs()
for key in key_pairs['KeyPairs']:
    ec2.delete_key_pair(KeyName=key['KeyName'])
    print(f"キーペアを削除しました: {key['KeyName']}")
 
