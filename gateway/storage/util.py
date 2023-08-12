import pika
import json
import logging

logging.basicConfig()

logger = logging.getLogger("my-app")


def upload(file, fs, channel, access):
    try:
        file_id = fs.put(file)
    except Exception as e:
        logger.error(e)
        return "Internal server error", 500

    # put message in rabbitmq queue
    message = {
        "video_fid": str(file_id),
        "mp3_fid": None,
        "username": access["username"]
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent,
            )
        )
    except Exception as e:
        logger.error(e)
        fs.delete(file_id)
        return "Internal server error", 500
