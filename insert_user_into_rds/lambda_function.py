import pymysql
import json
import logging
import sys

# rds settings
rds_host = "riceup.chnmxqka46ge.us-east-1.rds.amazonaws.com"
rds_name = "admin"
password = "nu?$5lflf*=nEsw4dibr"
db_name = "rice_up"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create the database connection outside of the handler to allow connections to be
# re-used by subsequent function invocations.


def lambda_handler(event, context):

    try:
        conn = pymysql.connect(host=rds_host, user=rds_name,
                               passwd=password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        logger.error(
            "ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        sys.exit()

    logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

    user_id = event['userName']
    email = event['request']['userAttributes']['email']
    user_name = event['request']['userAttributes']['preferred_username']
    # user_phone = event['request']['userAttributes']["phone_number"]
    user_phone = event['request']['userAttributes']
    user_phone = user_phone.get("phone_number", None)

    cursor = conn.cursor()

    sql = "INSERT INTO User (User_ID, user_name, user_email, phone) VALUES (%s, %s, %s, %s)" if user_phone is not None else \
        "INSERT INTO User (User_ID, user_name, user_email) VALUES (%s, %s, %s)"
    values = (user_id, str(user_name), email, user_phone) if user_phone is not None else (
        user_id, user_name, email)

    cursor.execute(sql, values)

    conn.commit()

    cursor.close()
    conn.close()
    logger.info('Event: ' + json.dumps(event))

    return event
