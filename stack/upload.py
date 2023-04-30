import os
import boto3
import botocore.exceptions

s3 = boto3.client('s3')

name = "" #website name

# dynamo variables
key_name = "" # name for primary key

# update script with 
...

# s3 web variables
to_upload = {}

for path in os.walk('../website'):
    with os.scandir(path[0]) as it:
        files = []
        for entry in it:
            files.append(entry.name)
        to_upload[path[0]] = files

# build s3 for website
def build_web_bucket(name, objects):
    try:
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

build_web_bucket(name, to_upload)