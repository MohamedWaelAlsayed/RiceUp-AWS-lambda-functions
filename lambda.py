import pymysql
import json
import logging
import sys

# rds settings
rds_host = "riceup.chnmxqka46ge.us-east-1.rds.amazonaws.com"
user_name = "admin"
password = "nu?$5lflf*=nEsw4dibr"
db_name = "rice_up"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create the database connection outside of the handler to allow connections to be
# re-used by subsequent function invocations.


def lambda_handler(event, context):
    # Extract the user_id from the request
    # user_id = event.get('user_id')
    user_id = transactionID = event["queryStringParameters"]["user_id"]

    try:
        conn = pymysql.connect(host=rds_host, user=user_name,
                               passwd=password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        logger.error(
            "ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        sys.exit()

    logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

    # Create a cursor object to execute SQL queries
    with conn.cursor() as cursor:
        try:
            # Execute the SQL query to retrieve the user's devices using an inner join
            sql = "SELECT d.Device_name, d.Device_ID FROM User u INNER JOIN Device d ON u.User_ID = d.User_ID WHERE u.User_ID = %s"
            cursor.execute(sql, (user_id,))

            # Fetch all the rows returned by the query
            devices = cursor.fetchall()
            print(devices)

            # response body
            data = {
                "number of devices": len(devices),
                "devices names": [device[0] for device in devices],
                "devices_id": [device[1] for device in devices]
            }

            # Return the devices as the response
            responseObject = {}
            responseObject["statusCode"] = 200
            responseObject["headers"] = {}
            responseObject["headers"]["content-type"] = "application/json"
            responseObject["body"] = json.dumps(data)

        except pymysql.MySQLError as e:
            logger.error(
                "ERROR: An error occurred while executing the SQL query.")
            logger.error(e)
            responseObject = {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Internal Server Error"})
            }

    return responseObject
