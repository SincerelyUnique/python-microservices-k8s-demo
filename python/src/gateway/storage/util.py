import traceback

import pika, json

from server import logger


def upload(f, fs, channel, access):
    try:
        fid = fs.put(f)
    except Exception as err:
        logger.error(err)
        logger.info(traceback.format_exc())
        return "internal server error", 500

    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as err:
        logger.error(err)
        logger.info(traceback.format_exc())
        fs.delete(fid)
        return "internal server error", 500
