import boto3
import json

ses = boto3.client('sesv2')

def handler(event, context):
    body = event['body']
    print(body)
    body = json.loads(body)
    replyto = body['email']
    print(replyto)
    subject = body['subject']
    print(subject)
    message = 'Name: ' + body['name'] + '\n' + 'Phone: ' + body['phone'] + '\n' + 'Message: ' + body['message']
    print(message)
    response = ses.send_email(
        FromEmailAddress = 'web@jeston.click',
        Destination = {'ToAddresses': ['jeston@jeston.click']},
        ReplyToAddresses = [replyto],
        Content = {
            'Simple': {
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': message}}
            }
        }
    )
    return response
    