from constructs import Construct
from aws_cdk import (
    Stack,
    Environment
    )
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from .pipeline_stage import StaticWebsitePipeline

name = 'mybreadventure.blog'

class StaticWebsitePipelineStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        pipeline = CodePipeline(
            self, 'Pipeline',
            pipeline_name='StaticWebsitePipeline',
            synth=ShellStep(
                'Synth',
                input=CodePipelineSource.git_hub('jestoncolelewis/static-website-IaC', 'main'),
                commands=[
                    'npm install -g aws-cdk',
                    'python pip install -r requirements.txt',
                    'cdk synth'
                ]
            )
        )

        pipeline.add_stage(StaticWebsitePipeline(self, 'WebsiteStage', env=Environment(account='706391136734', region='us-west-2')))