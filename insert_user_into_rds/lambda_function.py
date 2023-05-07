import pymysql
import json
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    user_id = event['userName']
    email = event['request']['userAttributes']['email']
    user_name = event['request']['userAttributes']['preferred_username']

    conn = pymysql.connect(
        host='',
        port=3306,
        user='',
        password='',
        database='rice_up'
    )

    cursor = conn.cursor()

    sql = "INSERT INTO User (User_ID, user_name, user_email) VALUES (%s, %s, %s)"
    values = (user_id, str(user_name), email)

    cursor.execute(sql, values)

    conn.commit()

    cursor.close()
    conn.close()
    logger.info('Event: ' + json.dumps(event))

    return event
