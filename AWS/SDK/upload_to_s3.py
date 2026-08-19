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
