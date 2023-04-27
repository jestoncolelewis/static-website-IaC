#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stack.static_website_stack import StaticWebsiteIaCStack

env_USA = cdk.Environment(account='706391136734', region='us-west-2')
app = cdk.App()
StaticWebsiteIaCStack(app, "StaticWebsiteIaCStack", env=env_USA)

app.synth()
