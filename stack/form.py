from constructs import Construct
from aws_cdk import (
    aws_lambda as alamb,
    aws_ses as ses
)
from .static_website_stack import name
from .hosting import Hosting

class FormSubmit(Construct):
    @property
    def handler(self):
        return self._handler
    
    @property
    def identity(self):
        return self._identity

    def __init__(self, scope:Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Form Lambda
        self._handler = alamb.Function(
            self, 'FormFunctionHandler',
            runtime=alamb.Runtime.PYTHON_3_9,
            code=alamb.Code.from_asset('lambda'),
            handler='form_submit.handler'
        )

        # SES
        zone = Hosting(self, 'HostedZone')
        self._identity = ses.EmailIdentity(
            self, 'Identity',
            identity=ses.Identity.public_hosted_zone(zone._zone),
            mail_from_domain=name
        )