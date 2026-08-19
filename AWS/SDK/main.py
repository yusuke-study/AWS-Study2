import boto3

# S3クライアントの作成
s3 = boto3.client('s3')

# S3バケットの一覧を取得
response = s3.list_buckets()

# バケット名を表示
print("S3 Buckets:")
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')