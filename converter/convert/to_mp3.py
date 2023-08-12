import pika
import json
import tempfile
import os
from bson.objectid import ObjectId
import moviepy.editor
from config import settings
import logging

logging.basicConfig()
logger = logging.getLogger("my-app")


def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message)

    # empty temp file
    tf = tempfile.NamedTemporaryFile()
    # video contents
    out = fs_videos.get(ObjectId(message["video_fid"]))
    # add video contents to empty file
    tf.write(out.read())
    # convert video file into audio
    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()

    # write audio to file
    tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(tf_path)

    # save file to mongo
    f = open(tf_path, "rb")
    data = f.read()
    fid = fs_mp3s.put(data)
    f.close()
    os.remove(tf_path)

    message["mp3_fid"] = str(fid)

    try:
        channel.basic_publish(
            exchange="",
            routing_key=settings.MP3_QUEUE,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            )
        )
    except Exception as e:
        fs_mp3s.delete(fid)
        print(e)
        return "Failed to publish message"
