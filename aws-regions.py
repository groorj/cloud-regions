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

# return region info
def get_region_info(event, context):
    logger.debug("Inside function: [%s]", inspect.currentframe().f_code.co_name)
    return_info_final = {}
    region_code = event['pathParameters']['region_code']
    logger.debug("region_code: [%s]", region_code)
    try:
        json_data = get_json()
    except HTTPError as err:
        # http_code = err.code
        http_code = 500
        return_info_final['request'] = { "request_status": "Fail", "error_message": "Error getting Regions information.", "http_error_code": err.code }
        return create_response_new(http_code, return_info_final)
    logger.debug("json_data: [%s]", json_data)
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

# return region info
def get_all_regions_info(event, context):
    logger.debug("Inside function: [%s]", inspect.currentframe().f_code.co_name)
    return_info_final = {}
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