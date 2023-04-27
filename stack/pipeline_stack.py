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

        pipeline = pipelines.CodePipeline(
            self, 'Pipeline',
            synth=pipelines.ShellStep(
                'Synth',
                input=pipelines.CodePipelineSource.code_commit(repo, 'main'),
                commands=[
                    'npm -g install aws-cdk',
                    'pip install -r requirements.txt',
                    'cdk synth'
                ]
            )
        )

        deploy = StaticWebsitePipeline(self, 'Deploy')
        deploy_stage = pipeline.add_stage(deploy)
        deploy_stage.add_post(
            pipelines.ShellStep(
                'TestViewerEndpoint',
                env_from_cfn_outputs={
                    'ENDPOINT_URL': deploy._hc_viewer_url
                },
                commands=['curl -Ssf $ENDPOINT_URL']
            )
        )
        deploy_stage.add_post(
            pipelines.ShellStep(
                'TestAPIGatewayEndpoint',
                env_from_cfn_outputs={
                    'ENDPOINT_URL': deploy._hc_endpoint
                },
                commands=[
                    'curl -Ssf $ENDPOINT_URL',
                    'curl -Ssf $ENDPOINT_URL/hello',
                    'curl -Ssf $ENDPOINT_URL/test'
                ]
            )
        )