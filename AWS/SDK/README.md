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
