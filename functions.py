import boto3
import botocore.exceptions
import os

s3 = boto3.client('s3')
lamb = boto3.client('lambda')
iam = boto3.client('iam')
api = boto3.client('apigatewayv2')
route53 = boto3.client('route53')
dynamo = boto3.client('dynamo') # optional
ses = boto3.client('sesv2') # optional

# build s3 for lambda
def build_lambda_bucket(name):
    path = os.getcwd()

    file = "index.zip"

    path = path + "/" + file

    try:
        s3.create_bucket(
            Bucket = name,
            CreateBucketConfiguration = {
                'LocationConstraint': 'us-west-2'
            }
        )
        s3.upload_file(path, name, file)
    except botocore.exceptions.ClientError as err:
        print('{}'.format(err.response['Error']['Message']))
    response = s3.list_objects(Bucket = name)
    objects = list(response.items())
    file = objects[3][1][0].get('Key')
    return file

# build s3 for website
def build_web_bucket(name, objects):
    try:
        s3.create_bucket(
            ACL = 'public-read',
            Bucket = name,
            CreateBucketConfiguration = {
                'LocationConstraint': 'us-west-2'
            }
        )
        s3.create_bucket(
            Bucket = 'www.' + name,
            CreateBucketConfiguration = {
                'LocationConstraint': 'us-west-2'
            }
        )
        for item in objects:
            files = objects[item]
            for file in files:
                if item[3:] == '':
                    d = item + '/' + file
                    s3.upload_file(d, name, file)
                else:    
                    f = item[3:] + '/' + file
                    d = item + '/' + file
                    s3.upload_file(d, name, f)
    except botocore.exceptions.ClientError as err:
        print('{}'.format(err.response['Error']['Message']))

# iam creator
def build_iam(name):
    with open('policy.json') as f: policy = f.read()
    with open('role.json') as f: role = f.read()
    try:
        policy_response = iam.create_policy(
            PolicyName = name + 'policy',
            PolicyDocument = policy
        )
        role_response = iam.create_role(
            RoleName = name + '-role',
            AssumeRolePolicyDocument = role
        )
        iam.attach_role_policy(
            RoleName = role_response['Role']['RoleName'],
            PolicyArn = policy_response['Policy']['Arn']
        )
    except botocore.exceptions.ClientError as err:
        print('{}'.format(err.response['Error']['Message']))
    return response.get('Arn') # type: ignore

# build lambda
def build_lambda(name, lang, role, code, desc):
    try:
        response = lamb.create_function(
            Runtime = lang,
            Role = role,
            Code = {
                'S3Bucket': code[0],
                'S3Key': code[1]
            },
            Description = desc,
            FunctionName = name.replace('.', 'dot') + '-function',
            Handler = 'index.lambda_handler'
        )
        return response.get('FunctionArn')
    except botocore.exceptions.ClientError as err:
        print('{}'.format(err.response['Error']['Message']))
        response = lamb.get_function(FunctionName = name)
        return response['Configuration']['FunctionArn']

# build api
def build_api(name, target):
    try:
        api.create_api(
            Name = name + '-api',
            ProtocolType = 'HTTP',
            CorsConfiguration = {
                'AllowOrigins': ['*']
            },
            Target = target
        )
    except botocore.exceptions.ClientError as err:
        print('{}'.format(err.response['Error']['Message']))

# build dynamo
def build_dynamo(name, key):
    try:
        dynamo.create_table(
            TableName = name + '-table',
            KeySchema = [{"AttributeName": key, "KeyType": "HASH"}],
            AttributeDefinitions = [{"AttributeName": key, "AttributeType": "N"}],
            ProvisionedThroughput = {
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
    except botocore.exceptions.ClientError as err:
        print('{}'.format(err.response['Error']['Message']))

# build hosted zone
def build_r53(name):
    try:
        ...
    except botocore.exceptions.ClientError as err:
        print('{}'.format(err.response['Error']['Message']))

# build email
def build_ses(name):
    try:
        ses.create_email(EmailIdentity = name + '-email')
    except botocore.exceptions.ClientError as err:
        print('{}'.format(err.response['Error']['Message']))