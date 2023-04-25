import boto3

dynamo = boto3.client('dynamodb')
dynamor = boto3.resource('dynamodb')
table = dynamor.Table('breadtest') # type: ignore

def handler(event, context):
    response = ''
    if event.get('') == ...:
        posts = 12
    elif event.get('') == ...:
        posts = 8
    else:
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