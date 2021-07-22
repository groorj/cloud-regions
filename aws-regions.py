import json
import logging
import os
import inspect
import urllib
import urllib.request
from urllib.error import HTTPError

# logger
logger = logging.getLogger()
logger_level = logging.getLevelName(os.environ['LOGGER_LEVEL'])
logger.setLevel(logger_level)

# validate access
def validate_access(event, context):
    logger.debug("Inside function: [%s]", inspect.currentframe().f_code.co_name)
    logger.debug("RESTRICTED_ACCESS_ENABLED: [%s]", os.environ['RESTRICTED_ACCESS_ENABLED'])
    error_message = "You are not allowed, get out!"
    if os.environ['RESTRICTED_ACCESS_ENABLED'] == 'true':
        logger.info("Restricted access is enabled")
        logger.info("Value for header [%s] is: [%s]", os.environ['RESTRICTED_ACCESS_HTTP_HEADER'], event["headers"][os.environ['RESTRICTED_ACCESS_HTTP_HEADER']])
        if event["headers"][os.environ['RESTRICTED_ACCESS_HTTP_HEADER']] != os.environ['RESTRICTED_ACCESS_SECRET']:
            logger.info("Key provided is not valid")
            logger.debug("Error: [%s]", error_message)
            http_code = 403
            raise ValueError(http_code, error_message)
        else:
            logger.info("Key provided is valid")
    else:
        logger.info("Restricted access is NOT enabled")

# create response
def create_response_new(status_code, message_body):
    logger.debug("Inside function: [%s]", inspect.currentframe().f_code.co_name)
    return {
        'statusCode': str(status_code),
        'body': json.dumps(message_body),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
            },
        }

# download json file
def get_json():
    logger.debug("Inside function: [%s]", inspect.currentframe().f_code.co_name)
    try:
        response = urllib.request.urlopen(os.environ['AWS_REGIONS_JSON_URL'])
    except HTTPError as err:
        # catch HTTP error
        logger.debug("HTTP error: [%s]", err)
        raise
    json_data = json.loads(response.read())
    return json_data

# entry point -> return region info
def get_region_info(event, context):
    logger.debug("Inside function: [%s]", inspect.currentframe().f_code.co_name)
    return_info_final = {}
    # validate the access to this resource
    try:
        validate_access(event, context)
    except ValueError as err:
        return_info_final['request'] = { "request_status": "Fail", "error_message": err.args[1], "http_error_code": err.args[0] }
        return create_response_new(err.args[0], return_info_final)
    # get region info
    region_code = event['pathParameters']['region_code']
    logger.debug("region_code: [%s]", region_code)
    try:
        json_data = get_json()
    except HTTPError as err:
        # http_code = err.code
        http_code = 500
        return_info_final['request'] = { "request_status": "Fail", "error_message": "Error getting Regions information.", "http_error_code": err.code }
        return create_response_new(http_code, return_info_final)
    # logger.debug("json_data: [%s]", json_data)
    # logger.debug("type(json_data): [%s]", type(json_data))
    for element in json_data['data']:
        # logger.debug("code: [%s] && region_code: [%s]", element['code'], region_code)
        if element['code'] == region_code:
            logger.info("region_code found")
            http_code = 200
            return_info_final['request'] = { "request_status": "Success" }
            return_info_final['info'] = json_data['info']
            return_info_final['data'] = element
            break
        else:
            logger.info("region_code NOT found")
            return_info = "Region code NOT found."
            http_code = 404
            return_info_final['request'] = { "request_status": "Fail", "error_message": "Region code NOT found.", "http_error_code": http_code }
    return create_response_new(http_code, return_info_final)

# entry point -> return region info
def get_all_regions_info(event, context):
    logger.debug("Inside function: [%s]", inspect.currentframe().f_code.co_name)
    return_info_final = {}
    # validate the access to this resource
    try:
        validate_access(event, context)
    except ValueError as err:
        return_info_final['request'] = { "request_status": "Fail", "error_message": err.args[1], "http_error_code": err.args[0] }
        return create_response_new(err.args[0], return_info_final)
    # get regions info
    try:
        json_data = get_json()
    except HTTPError as err:
        # http_code = err.code
        http_code = 500
        return_info_final['request'] = { "request_status": "Fail", "error_message": "Error getting Regions information.", "http_error_code": err.code }
        return create_response_new(http_code, return_info_final)
    logger.debug("json_data: [%s]", json_data)
    http_code = 200

    return_info_final['request'] = { "request_status": "Success" }
    return_info_final['info'] = json_data['info']
    return_info_final['data'] = json_data['data']

    return create_response_new(http_code, return_info_final)

# End;