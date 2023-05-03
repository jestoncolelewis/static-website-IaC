from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as alamb,
    aws_apigateway as apigw,
    aws_dynamodb as ddb,
    aws_ses as ses,
    aws_route53 as r53,
    aws_route53_targets as targets,
    CfnOutput
)
from constructs import Construct

name = 'mybreadventure.blog'

class StaticWebsiteIaCStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        # Buckets
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

        # Hosting
        zone = r53.HostedZone(
            self, 'HostedZone',
            zone_name=name
        )

        main_record = r53.RecordSet(
            self, 'MainRecord',
            record_type=r53.RecordType.A,
            target=r53.RecordTarget.from_alias(targets.BucketWebsiteTarget(main_bucket)),
            zone=zone,
            record_name=name
        )

        www_record = r53.RecordSet(
            self, 'wwwRecord',
            record_type=r53.RecordType.A,
            target=r53.RecordTarget.from_alias(targets.BucketWebsiteTarget(www_bucket)),
            zone=zone,
            record_name='www.' + name
        )

        # SES
        identity = ses.EmailIdentity(
            self, 'Identity',
            identity=ses.Identity.public_hosted_zone(zone),
            mail_from_domain=name
        )

        # Post Lambda
        post_func = alamb.Function(
            self, 'PostFunctionHandler',
            runtime=alamb.Runtime.PYTHON_3_9,
            code=alamb.Code.from_asset('lambda'),
            handler='post_return.handler'
        )

        # Form Lambda
        form_func = alamb.Function(
            self, 'FormFunctionHandler',
            runtime=alamb.Runtime.PYTHON_3_9,
            code=alamb.Code.from_asset('lambda'),
            handler='form_submit.handler'
        )

        # API
        post_gateway = apigw.LambdaRestApi(
            self, 'PostEndpoint',
            handler=post_func # type: ignore
        )
        
        self.post_endpoint = CfnOutput(
            self, 'PostGatewayUrl',
            value=post_gateway.url
        )

        form_gateway = apigw.LambdaRestApi(
            self, 'FormEndpoint',
            handler=form_func # type: ignore
        )

        self.form_endpoint = CfnOutput(
            self, 'FormGatewayUrl',
            value=form_gateway.url
        )

        # Dynamo
        table = ddb.Table(
            self, name + 'Table',
            partition_key={'name': 'path', 'type': ddb.AttributeType.STRING}
        )