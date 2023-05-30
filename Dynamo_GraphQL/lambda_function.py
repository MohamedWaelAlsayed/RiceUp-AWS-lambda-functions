import requests
from requests_aws4auth import AWS4Auth
import time
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

session = requests.Session()

APPSYNC_API_ENDPOINT_URL = "https://ccid7g6a45huhhkx52rtmvrbm4.appsync-api.us-east-1.amazonaws.com/graphql"
API_KEY = "da2-azkuqy5zjjdmzazvvzxbfiv4xe"


def lambda_handler(event: dict, context):

    # event = {
    #     "device_id": "arn:aws:iot:us-east-1:404548260653:thing/ESP32_Farm1",
    #     "temperature": 20,
    #     "moisture": 10
    # }

    device_id = event["device_id"]
    if event.keys().__contains__("timestamp"):
        if event["timestamp"] == 0:
            event["timestamp"] = int(time.time())
            timestamp = event["timestamp"]
        else:
            timestamp = event["timestamp"]

    else:
        event["timestamp"] = int(time.time())
        timestamp = event["timestamp"]

    # timestamp = int(event.get("timestamp", time.time()))
    temperature = event.get("temperature", "null")
    if temperature < 0 or temperature == 0:
        return "Error in temperature. " + str(temperature)

    moisture = event.get("moisture", "null")

    if moisture < 0 or moisture == 0 or moisture == 100:
        return "Error in moisture. " + str(moisture)

    # logger.info('Event: ' + json.dumps(response.json()['data']))

    query = "mutation add_reading {createReading(input: {device_id: " + f'"{device_id}"' + \
        f', timestamp: {timestamp} , temperature: {temperature} , moisture: {moisture} ' + \
        "}) {device_id timestamp temperature moisture createdAt updatedAt _version _deleted _lastChangedAt}}"
    # print(query)

    try:
        response = session.request(
            url=APPSYNC_API_ENDPOINT_URL,
            method='POST',
            headers={'x-api-key': API_KEY},
            json={'query': query}
        )
        response.raise_for_status()  # Raise an exception for HTTP errors (status code >= 400)
        # print(response.json()['data'])
        logger.info('Event: ' + json.dumps(response.json()['data']))
    except requests.exceptions.RequestException as e:
        # print(f"An error occurred: {e}")
        logger.info('Event: ' + json.dumps(f"An error occurred: {e}"))

    return {
        'statusCode': 200,
        'body': json.dumps("Inserted Succesfully")
    }
