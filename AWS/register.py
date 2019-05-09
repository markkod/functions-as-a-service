import json

import boto3
import json
import urllib.parse
from datetime import datetime
from boto3.dynamodb.conditions import Key

# https://edtheron.me/projects/store-messages-aws-dynamodb-lambda-api-gateway-cognito
def respond(err, response=None):
	return {
		'statusCode': '400' if err else '200',
		'body': err if err else json.dumps(response),
		'headers': {
			'Content-Type': 'application/json',
		},
	}

def parseToDict(event):
    # necessary for parsing @ sign
    urlencoded = urllib.parse.unquote(event['body'])
    # converts x-www-form-urlencoded to dict
    return {x.split('=')[0]: x.split('=')[1] for x in urlencoded.split("&")}

def lambda_handler(event, context):
    event_json = parseToDict(event)
    first_name = event_json['first_name']
    last_name = event_json['last_name']
    email = event_json['email']
    table = boto3.resource('dynamodb').Table('Registration')
    data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email
    }
    table.put_item(Item=data)
    return respond(None, data)