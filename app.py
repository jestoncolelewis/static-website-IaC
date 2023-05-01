#!/usr/bin/env python3
import aws_cdk as cdk

from stack.pipeline_stack import StaticWebsitePipelineStack
from stack.upload import upload, update

env_USA = cdk.Environment(account='706391136734', region='us-west-2')
app = cdk.App()
StaticWebsitePipelineStack(app, "StaticWebsitePipelineStack", env=env_USA)

app.synth()