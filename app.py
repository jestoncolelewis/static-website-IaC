#!/usr/bin/env python3
import aws_cdk as cdk

from stack.static_website_stack import StaticWebsiteIaCStack

app = cdk.App()
StaticWebsiteIaCStack(app, "StaticWebsiteIaCStack", env=cdk.Environment(account='706391136734', region='us-west-2'))

app.synth()