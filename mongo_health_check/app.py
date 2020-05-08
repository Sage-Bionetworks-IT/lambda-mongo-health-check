import json
import logging
import traceback
import pymongo
import urllib.parse

from os import environ

HOST = environ.get('HOST')
PORT = environ.get('PORT')
DBUSER = environ.get('DBUSER')
PASSWORD = environ.get('DBPASSWORD')
DATABASE = environ.get('DATABASE')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def make_connection():
    return pymongo.MongoClient(
        'mongodb://%s:%s@%s:%s' % (
            urllib.parse.quote_plus(DBUSER),
            urllib.parse.quote_plus(PASSWORD),
            HOST,
            PORT
        )
    )

def log_err(errmsg):
    logger.error(errmsg)
    return {"body": errmsg, "headers": {}, "statusCode": 400,
            "isBase64Encoded": "false"}

def handler(event, context):
    logger.debug("Received event: " + json.dumps(event, sort_keys=False))
    try:
        cnx = make_connection()
        db = cnx[DATABASE]

        try:
            results = db.list_collection_names()
            logger.debug("results = " + str(results))
        except:
            return log_err("ERROR: Cannot execute db query.\n{}".format(
                traceback.format_exc()))

        return {"body": str(results), "headers": {}, "statusCode": 200,
                "isBase64Encoded": "false"}


    except:
        return log_err("ERROR: Cannot connect to DATABASE from handler.\n{}".format(
            traceback.format_exc()))


    finally:
        try:
            cnx.close()
        except:
            pass


if __name__ == "__main__":
    handler(None, None)
