from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_apigateway as apigw,
    CfnOutput
)
from constructs import Construct
from .post_return import PostReturn
from .form import FormSubmit

name = 'mybreadventure.blog'

class StaticWebsiteIaCStack(Stack):
    @property
    def main_bucket(self):
        return self._main_bucket
    
    @property
    def www_bucket(self):
        return self._www_bucket

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
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

        # API
        post = PostReturn(self, 'PostReturn')
        post_gateway = apigw.LambdaRestApi(self, 'PostEndpoint', handler=post._handler)# type: ignore
        
        self.post_endpoint = CfnOutput(self, 'PostGatewayUrl', value=post_gateway.url)

        form = FormSubmit(self, 'FormSubmit')
        form_gateway = apigw.LambdaRestApi(self, 'FormEndpoint', handler=form._handler)# type: ignore

        self.form_endpoint = CfnOutput(self, 'FormGatewayUrl', value=form_gateway.url)       