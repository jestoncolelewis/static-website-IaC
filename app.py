#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stack.pipeline_stack import StaticWebsitePipelineStack, name
from stack.static_website_stack import StaticWebsiteIaCStack
from stack.upload import upload, update

env_USA = cdk.Environment(account='706391136734', region='us-west-2')
app = cdk.App()
StaticWebsitePipelineStack(app, "StaticWebsiteIaCStack", env=env_USA)

app.synth()

update(endpoint = StaticWebsiteIaCStack.)

upload(name)