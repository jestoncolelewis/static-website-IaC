from constructs import Construct
from aws_cdk import (
    aws_s3 as s3
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
        
        # Buckets
        self._main_bucket = s3.Bucket(
            self, 'PublicBucket',
            public_read_access=True,
            website_index_document='index.html',
            website_error_document='404.html',
            bucket_name=name
        )

        self._www_bucket = s3.Bucket(
            self, 'wwwBucket',
            website_redirect=s3.RedirectTarget(host_name=name),
            bucket_name='www.' + name
        )