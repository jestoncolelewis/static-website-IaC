from constructs import Construct
from aws_cdk import (
    aws_s3 as s3,
    RemovalPolicy
)
import json

name = 'mybreadventure.blog'

class Buckets(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        @property
        def main_bucket(self):
            return self._main_bucket
        
        @property
        def www_bucket(self):
            return self._www_bucket
        
        # Buckets
        self._main_bucket = s3.Bucket(
            self, 'MainBucket',
            public_read_access=True,
            website_index_document='index.html',
            website_error_document='404.html',
            bucket_name=name,
            block_public_access=s3.BlockPublicAccess(block_public_acls=False),
            removal_policy=RemovalPolicy.DESTROY
        )

        policy = '{"Version": "2012-10-17", "Statement": [{"Sid": "PublicReadGetObject","Effect": "Allow","Principal": "*","Action": "s3:GetObject","Resource": "arn:aws:s3:::{}]/*"}]}'.format(name)
        self._main_bucket.add_to_resource_policy(permission=json.loads(policy))

        self._www_bucket = s3.Bucket(
            self, 'wwwBucket',
            website_redirect=s3.RedirectTarget(host_name=name),
            bucket_name='www.' + name,
            removal_policy=RemovalPolicy.DESTROY
        )