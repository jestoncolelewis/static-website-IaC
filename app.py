#!/usr/bin/env python3
import aws_cdk as cdk

from stack.pipeline_stack import StaticWebsitePipelineStack

app = cdk.App()
StaticWebsitePipelineStack(app, "StaticWebsiteIaCStack", env=cdk.Environment(account='706391136734', region='us-west-2'))

app.synth()