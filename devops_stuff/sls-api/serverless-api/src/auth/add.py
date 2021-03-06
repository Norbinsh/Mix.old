import json
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

def handler(event, context):
    auth_token = event.get('authorizationToken')

    if not auth_token:
        return {"statusCode": 401, "body": "Unauthorized"}

    if validate_token(auth_token):
        return generate_policy(auth_token, "Allow", event['methodArn'])
        
    return {"statusCode": 401, "body": "Unauthorized"}

def generate_policy(principal_id, effect, resource):
    return {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource

                }
            ]
        }
    }

def validate_token(token):
    dynamodb = boto3.resource('dynamodb', region_name=os.environ['REGION'])
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    response = table.query(KeyConditionExpression=Key('customer').eq('master'))
    master_token = response['Items'][0]['token']
    if master_token == token:
        return True
    return
