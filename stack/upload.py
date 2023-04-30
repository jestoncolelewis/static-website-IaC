import os
import boto3
import botocore.exceptions

# build s3 for website
def upload(name):
    try:
        s3 = boto3.client('s3')

        # update script with 
        with open('../website/script.js', 'r') as script:
            lines =  script.readlines()

        with open('../website/script.js', 'w') as script:
            url = 'new.url'
            for code in lines:
                if code.startswith('const url'):
                    code = 'const url = "{}";\n'.format(url)
                script.write(code)

        # s3 web variables
        to_upload = {}

        for path in os.walk('../website'):
            with os.scandir(path[0]) as it:
                files = []
                for entry in it:
                    files.append(entry.name)
                to_upload[path[0]] = files

        for item in objects:
            files = objects[item]
            for file in files:
                if item[10:] == '':
                    d = item + '/' + file
                    s3.upload_file(d, name, file)
                else:    
                    f = item[10:] + '/' + file
                    d = item + '/' + file
                    s3.upload_file(d, name, f)
    except botocore.exceptions.ClientError as err:
        print('{}'.format(err.response['Error']['Message']))