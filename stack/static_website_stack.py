from constructs import Construct
from aws_cdk import (
    Stack,
    aws_apigateway as apigw,
    CfnOutput
)
from .post_return import PostReturn
from .form import FormSubmit

class StaticWebsiteIaCStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        @property
        def post_endpoint(self):
            return self._post_endpoint
        
        @property
        def form_endpoint(self):
            return self._form_endpoint

        # API
        post = PostReturn(self, 'PostReturn')
        post_gateway = apigw.LambdaRestApi(self, 'PostEndpoint', handler=post._handler)# type: ignore
        
        self._post_endpoint = CfnOutput(self, 'PostGatewayUrl', value=post_gateway.url)

        form = FormSubmit(self, 'FormSubmit')
        form_gateway = apigw.LambdaRestApi(self, 'FormEndpoint', handler=form._handler)# type: ignore

        self._form_endpoint = CfnOutput(self, 'FormGatewayUrl', value=form_gateway.url)