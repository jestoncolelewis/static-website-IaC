from constructs import Construct
from aws_cdk import Stack
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep

name = 'mybreadventure.blog'

class StaticWebsitePipelineStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        pipeline = CodePipeline(
            self, 'Pipeline',
            pipeline_name='StaticWebsitePipeline',
            synth=ShellStep(
                'Synth',
                input=CodePipelineSource.git_hub('https://github.com/jestoncolelewis/static-website-IaC.git', 'main'),
                commands=[
                    'npm instlla -g aws_cdk',
                    'python pip install -r requirements.txt',
                    'cdk synth'
                ]
            )
        )