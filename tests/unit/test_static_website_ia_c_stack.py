import aws_cdk as core
import aws_cdk.assertions as assertions

from static_website_ia_c.static_website_ia_c_stack import StaticWebsiteIaCStack

# example tests. To run these tests, uncomment this file along with the example
# resource in static_website_ia_c/static_website_ia_c_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = StaticWebsiteIaCStack(app, "static-website-ia-c")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
