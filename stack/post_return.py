from constructs import Construct
from aws_cdk import (
    aws_lambda as alamb,
    aws_dynamodb as ddb
)

class PostReturn(Construct):
    @property
    def handler(self):
        return self._handler
    
    @property
    def table(self):
        return self._table
    
    def __init__(self, scope:Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Post Lambda
        self._handler = alamb.Function(
            self, 'PostFunctionHandler',
            runtime=alamb.Runtime.PYTHON_3_9,
            code=alamb.Code.from_asset('lambda'),
            handler='post_return.handler'
        )

        # Dynamo
        self._table = ddb.Table(
            self, 'Table',
            partition_key={'name': 'path', 'type': ddb.AttributeType.STRING}
        )

        self._table.grant_read_write_data(self._handler)