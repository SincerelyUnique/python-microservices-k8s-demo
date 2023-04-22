import logging
import os, gridfs, pika, json
import traceback

from flask import Flask,request, send_file
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
from bson.objectid import ObjectId

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(filename)s:%(lineno)d:%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)

server = Flask(__name__)

mongo_video = PyMongo(
    server,
    uri="mongodb://host.minikube.internal:27017/videos"
)

mongo_mp3 = PyMongo(
    server,
    uri="mongodb://host.minikube.internal:27017/mp3s"
)

fs_videos = gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq", heartbeat=0))
channel = connection.channel()


@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)
    if not err:
        return token
    else:
        return err


@server.route("/upload", methods=["POST"])
def upload():
    logger.info("user upload file")
    access, err = validate.token(request)
    if err:
        return err
    access = json.loads(access)
    logger.info(access)
    if access["admin"]:
        logger.info("111111")
        if len(request.files) > 1 or len(request.files) < 1:
            return "exactly 1 file required", 400
        logger.info("22222")
        for _, f in request.files.items():
            logger.info("33333")

            connect_close = connection.is_closed
            connect_open = connection.is_open
            channel_close = channel.is_closed
            channel_open = channel.is_open

            logger.info("connection is_closed ", connect_close)
            logger.info("connection is_open ", connect_open)
            logger.info("channel is_closed ", channel_close)
            logger.info("channel is_open ", channel_open)

            err = util.upload(f, fs_videos, channel, access)
            logger.info(err)
            if err:
                logger.info("44444")
                return err

        return "success!", 200
    else:
        return "not authorized", 401


@server.route("/download", methods=["GET"])
def download():
    access, err = validate.token(request)
    if err:
        return err
    access = json.loads(access)
    logger.info("user download mp3")
    logger.info(access)
    if access["admin"]:
        fid_string = request.args.get("fid")
        if not fid_string:
            return "fid is required", 400
        try:
            out = fs_mp3s.get(ObjectId(fid_string))
            return send_file(out, download_name=f"{fid_string}.mp3")
        except Exception as err:
            logger.error(err)
            logger.error(traceback.format_exc())
            return "internal server error", 500
    return "not authorized", 401


if __name__ == '__main__':
    server.run(host="0.0.0.0", port=8080)
