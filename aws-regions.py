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
def create_response(status_code, message_content, message_key='key'):
    logger.debug("Inside function: [%s]", inspect.currentframe().f_code.co_name)
    return {
        'statusCode': str(status_code),
        'body': json.dumps({ message_key: message_content }),
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
    region_code = event['pathParameters']['region_code']
    logger.debug("region_code: [%s]", region_code)
    try:
        json_data = get_json()
    except HTTPError as err:
        return create_response(err.code, "Error getting Regions information.", 'return')
    logger.debug("json_data: [%s]", json_data)
    # logger.debug("type(json_data): [%s]", type(json_data))
    for element in json_data:
        # logger.debug("code: [%s] && region_code: [%s]", element['code'], region_code)
        if element['data']['code'] == region_code:
            logger.info("region_code found")
            http_code = 200
            return_info = element
            break
        else:
            logger.info("region_code NOT found")
            return_info = "Region code NOT found."
            http_code = 404
    return create_response(http_code, return_info, 'return')

# return region info
def get_all_regions_info(event, context):
    logger.debug("Inside function: [%s]", inspect.currentframe().f_code.co_name)
    try:
        json_data = get_json()
    except HTTPError as err:
        return create_response(err.code, "Error getting Regions information.", 'return')
    logger.debug("json_data: [%s]", json_data)
    http_code = 200
    return_info = json_data
    return create_response(http_code, return_info, 'return')

# End;