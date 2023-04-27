import boto3

dynamo = boto3.client('dynamodb')
dynamor = boto3.resource('dynamodb')
table = dynamor.Table('breadtest')

def handler(event, context):
    response = ''
    posts = table.item_count

    for i in range(posts):
        item = dynamo.get_item(
            Key = {'post_num':{'N':'{}'.format(i)}},
            TableName = 'breadtest'
        )
        if i == posts:
            response += str(item)
        else:
            response += str(item) + '^*^'

    return response