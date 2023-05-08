#!/usr/bin/env python3
import aws_cdk as cdk

from stack.pipeline_stack import StaticWebsitePipelineStack

app = cdk.App()
StaticWebsitePipelineStack(app, "StaticWebsiteIaCStack")

app.synth()