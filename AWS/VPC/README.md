# VPC  ![VPC](./VPC_00.png)


## VPC関連確認(主要情報のみ)

VPCに関連するシステムの確認を行うコマンドについて、主要情報のみ出力させるコマンドを記載する。

(1)	VPCの主要な内容のみ出力する。
「aws ec2 describe-vpcs --query "Vpcs[*].[VpcId,CidrBlock,IsDefault]" --output text」を実行する。
  

(2)	サブネットの主要な内容のみ出力する。
「aws ec2 describe-subnets  --query "Subnets[*].[SubnetId,AvailabilityZone,CidrBlock,VpcId]"  --output text」を実行する。
 

(3)	ルートテーブルの主要な内容のみ出力する。
「aws ec2 describe-route-tables --query "RouteTables[*].[RouteTableId,VpcId]" --output text」を実行する。
 

(4)	インターネットゲートウェイの主要な内容のみ出力する。
下記コマンドを実施する。
aws ec2 describe-internet-gateways --query "InternetGateways[*].[InternetGatewayId,Attachments[0].VpcId]" --output text
 

(5)	Elastic IP の主要な内容のみ出力する。
下記コマンドを実施する。
aws ec2 describe-addresses --query "Addresses[*].{PublicIP:PublicIp,AllocationId:AllocationId,InstanceId:InstanceId}" --output table
 

(6)	NAT ゲートウェイの主要な内容のみ出力する。
下記コマンドを実施する。
aws ec2 describe-nat-gateways --query "NatGateways[*].{ID:NatGatewayId,State:State,Subnet:SubnetId,PublicIP:NatGatewayAddresses[0].PublicIp}" --output table



## VPC関連確認


## VPC関連作成


## VPC関連削除


## VPC関連備考
