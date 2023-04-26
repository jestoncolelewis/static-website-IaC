from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as alamb,
    aws_apigateway as apigw,
    aws_dynamodb as ddb,
    aws_ses as ses,
    aws_route53 as r53
)
from constructs import Construct

name = 'mybreadventure.blog'

class StaticWebsiteIaCStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        func = alamb.Function(
            self, 'FunctionHandler',
            runtime=alamb.Runtime.PYTHON_3_9,
            code=alamb.Code.from_asset('lambda'),
            handler='index.handler'
        )

        main_bucket = s3.Bucket(
            self, 'PublicBucket',
            public_read_access=True,
            website_index_document='index.html',
            website_error_document='404.html',
            bucket_name=name
        )

        www_bucket = s3.Bucket(
            self, 'wwwBucket',
            website_redirect=s3.RedirectTarget(host_name=name),
            bucket_name='www.' + name
        )

        gateway = apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=func
        )

        table = ddb.Table(
            self, name + 'Table',
            partition_key={'name': 'path', 'type': ddb.AttributeType.STRING}
        )

        zone = r53.HostedZone(
            self, 'HostedZone',
            zone_name=name
        )

        identity = ses.EmailIdentity(
            self, 'Identity',
            identity=ses.Identity.public_hosted_zone(zone),
            mail_from_domain=name
        )
