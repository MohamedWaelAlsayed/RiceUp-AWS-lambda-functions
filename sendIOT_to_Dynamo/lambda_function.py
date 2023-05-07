import json
import logging
import boto3
import time


logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.client('dynamodb')
# my_time = time.time()*1000


def lambda_handler(event: dict, context):
    # TODO implement
    # logger.info('Event: ' + json.dumps(event))
    # logger.info('Event: ' + str(time.localtime(my_time))

    # Extract device ID and timestamp from data
    device_id = event['device_id']
    my_items = {
        'device_id': {'S': str(device_id)},
        'timestamp': {'N':  str(int(time.time()*1000))},
      "__typename": {
                'S' : str("Reading")
            }
            
        }

    

    for kind, value in event.items():
        if kind != 'device_id':
            my_items[kind] = {'N': str(value)}

    # Insert data into DynamoDB table
    dynamodb.put_item(
        TableName='Reading-vdqocvk6tndfxby3qkhrqkolbq-dev',
        Item=my_items
    )

    logger.info('Event: ' + json.dumps(my_items))

    return {
        'statusCode': 200,
        'body': json.dumps("Inserted Succesfully")
    }
