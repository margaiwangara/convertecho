import gridfs, pika, json
from flask import Flask, request
from flask_pymongo import PyMongo, ObjectId
from lib import validate
from auth_srv import access
from storage import util
from config import settings

app = Flask(__name__)

mongo_videos = PyMongo(app, uri=settings.MONGO_VIDEOS_URI)
mongo_mp3s = PyMongo(app, uri=settings.MONGO_MP3S_URI)

fs_videos = gridfs.GridFS(mongo_videos.db)
fs_mp3s = gridfs.GridFS(mongo_mp3s.db)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="rabbitmq"))
channel = connection.channel()


@app.route("/", methods=["GET"])
def hello():
    return "Hello World!"


@app.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err


@app.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)

    if err:
        return err

    if access is None:
        print("access: ", access)
        return "Invalid file", 400

    access = json.loads(access)

    if access["role"] == "admin":
        if len(request.files) > 1 or len(request.files) < 1:
            return "Exactly 1 file required", 400

        for _, f in request.files.items():
            err = util.upload(f, fs_videos, channel, access)

            if err:
                return err

        return "Upload successfull", 200
    else:
        return "Unauthorized", 401


@app.route("/download", methods=["GET"])
def download():
    access, err = validate.token(request)

    if err:
        return err

    access = json.loads(access)

    if access["role"] == "admin":
        fid_string = request.args.get("fid")

        if not fid_string:
            return "MP3 ID is required", 401

        try:
            out = fs_mp3s.get(ObjectId(fid_string))
            return send_file(out, download_name=f"{fid_string}.mp3")
        except Exception as err:
            print(err)
            return "Internal server errror", 500
    else:
        return "Unauthorized", 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
