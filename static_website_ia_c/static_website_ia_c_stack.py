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

name = ''

class StaticWebsiteIaCStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        func = alamb.Function(
            self, 'FunctionHandler',
            runtime=alamb.Runtime.PYTHON_3_9,
            code=alamb.Code.from_asset('lambda'),
            handler='index.handler'
        )

        bucket = s3.Bucket(
            self, 'PublicBucket',
            public_read_access=True,
            bucket_name=name
        )

        gateway = apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=func
        )

        table = ddb.Table(
            self, name + 'Table',
            partition_key={'name': 'path', 'type': ddb.AttributeType.STRING}
        )

        zone = r53.IPublicHostedZone

        identity = ses.EmailIdentity(
            self, 'Identity',
            identity=ses.Identity.public_hosted_zone(zone),
            mail_from_domain=''
        )
