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
