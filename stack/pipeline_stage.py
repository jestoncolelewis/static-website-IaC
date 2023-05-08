from constructs import Construct
from aws_cdk import (
    Stage
)
from .static_website_stack import StaticWebsiteIaCStack

class StaticWebsitePipeline(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        websiteStack = StaticWebsiteIaCStack(self, 'WebsiteStack')