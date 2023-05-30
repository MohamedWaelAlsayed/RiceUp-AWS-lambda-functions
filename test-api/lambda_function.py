import json

def lambda_handler(event, context):
    try:
        # 1.  parse out the query parameters
        transactionID = event["queryStringParameters"]["transactionID"]
        transactionType = event["queryStringParameters"]["transactionType"]
        transactionAmount = event["queryStringParameters"]["transactionAmount"]

        print("transactionID = " + transactionID)
        print("transactionType = " + transactionType)
        print("transactionAmount = " + transactionAmount)

        # # 2. Constrtruct the body of the reponse object
        transactionResponse = {}
        transactionResponse["transactionID"] = transactionID
        transactionResponse["Type"] = transactionType
        transactionResponse["Amount"] = transactionAmount
        transactionResponse["message"] = 'Hello From lambda'

        # 3. Constrtruct http response object
        responseObject = {}
        responseObject["statusCode"] = 200
        responseObject["headers"] = {}
        responseObject["headers"]["content-type"] = "application/json"
        responseObject["body"] = json.dumps(transactionResponse)

        # return responseObject
        return responseObject
    except KeyError as error:
        return {
            "statusCode": 400,
            "headers": {
                "content-type": "application/json"
            },
            "body": json.dumps({
                "message": "Error" + str(error)
            })}
    except:
        return {
            "statusCode": 502,
            "headers": {
                "content-type": "application/json"
            },
            "body": json.dumps({
                "message": "Error, there are not query parameters"
            })
        }
