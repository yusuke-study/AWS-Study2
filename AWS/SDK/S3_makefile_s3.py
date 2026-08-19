import boto3

# ファイル作成
with open('makefile_upload.txt', 'w', encoding='utf-8') as f:
    f.write('これはS3バケット「test-bucket-20251015」にアップロードするサンプルファイルです。\n')

# S3クライアント作成
s3 = boto3.client('s3')

# アップロード
s3.upload_file('makefile_upload.txt', 'test-bucket-20251015', ' makefile_upload.txt')

print("アップロード完了")
