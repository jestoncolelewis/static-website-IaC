from constructs import Construct
from aws_cdk import (
    aws_lambda as alamb,
    aws_dynamodb as ddb
)

class PostReturn(Construct):
    def __init__(self, scope:Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # TODO