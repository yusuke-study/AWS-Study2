from aws_cdk import (
    Stack,
    aws_s3 as s3,
)
from constructs import Construct

class S3Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # バージョニング有効なS3バケットを作成
        s3.Bucket(self, "testVersionedBucket",
            versioned=True
        )
