from constructs import Construct
from aws_cdk import (
    Stack,
    aws_codecommit as codecommit,
    pipelines as pipelines
)
from stack.pipeline_stage import StaticWebsitePipeline

name = 'mybreadventure.blog'

class StaticWebsitePipelineStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        repo = codecommit.Repository(
            self, 'Repo',
            repository_name=name +'-Repo'
        )