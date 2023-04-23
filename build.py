from functions import *
import os

name = "" #website name

# s3 lambda variables
key = build_lambda_bucket(name)

# s3 web variables
to_upload = {}

for path in os.walk('..'):
    with os.scandir(path[0]) as it:
        files = []
        for entry in it:
            if not entry.name.startswith('.') and not entry.name.endswith('.md') and not entry.name.endswith('.http') and not entry.name.endswith('.py') and not entry.name.endswith('ipynb') and not path[0].startswith('../.') and entry.is_file():
                files.append(entry.name)
        if not path[0].startswith('../.') and not path[0].startswith('../IaC') and len(files) != 0:
            to_upload[path[0]] = files

build_web_bucket(name, to_upload)

# dynamo variables
key_name = ""

attribute_name = ""

build_dynamo(name, key_name, attribute_name)

# lambda variables
lang = "python3.9"

iam = build_iam(name)

code = [name, key]

description = "function for retrieving and updating page views"

build_lambda(name, lang, iam, code, description)