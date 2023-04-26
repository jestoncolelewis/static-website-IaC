#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stack.static_website_stack import StaticWebsiteIaCStack


app = cdk.App()
StaticWebsiteIaCStack(app, "StaticWebsiteIaCStack")

app.synth()
