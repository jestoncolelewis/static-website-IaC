from constructs import Construct
from aws_cdk import (
    aws_s3 as s3,
    aws_cloudfront as cf,
    aws_cloudfront_origins as origins,
    aws_iam as iam,
    aws_certificatemanager as cm,
    RemovalPolicy
)

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
        
        @property
        def main_distro(self):
            return self._main_distro
        
        @property
        def www_distro(self):
            return self._www_distro
        
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

        policy = iam.PolicyStatement(
            actions=["s3:GetObject"],
            sid="PublicReadGetObject",
            )
        policy.add_any_principal()
        policy.add_resources('arn:aws:s3:::{}/*'.format(name))
        self._main_bucket.add_to_resource_policy(permission=policy)

        self._www_bucket = s3.Bucket(
            self, 'wwwBucket',
            website_redirect=s3.RedirectTarget(host_name=name),
            bucket_name='www.' + name,
            removal_policy=RemovalPolicy.DESTROY
        )

        # Distribution
        self._main_distro = cf.Distribution(
            self, 'MainDistro',
            default_behavior=cf.BehaviorOptions(
                origin=origins.S3Origin(self._main_bucket)
            )
        )

        self._www_distro = cf.Distribution(
            self, 'wwwDistro',
            default_behavior=cf.BehaviorOptions(
                origin=origins.S3Origin(self._www_bucket)
            )
        )

        # Certificate
        cert = cm.Certificate(
            self, 'Certificate',
            domain_name='*.' + name
        )

        cert.apply_removal_policy(RemovalPolicy.DESTROY)