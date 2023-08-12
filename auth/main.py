from flask import Flask, request
from flask_mysqldb import MySQL
from config import settings
from lib.auth import create_jwt
import jwt

app = Flask(__name__)
mysql = MySQL(app)

# config
app.config["MYSQL_HOST"] = settings.MYSQL_HOST
app.config["MYSQL_PORT"] = settings.MYSQL_PORT
app.config["MYSQL_USER"] = settings.MYSQL_USER
app.config["MYSQL_PASSWORD"] = settings.MYSQL_PASSWORD
app.config["MYSQL_DB"] = settings.MYSQL_DB


@app.route("/login", methods=["POST"])
def login():
    auth = request.authorization

    if not auth:
        return "Invalid credentials", 401

    # check db for username and password
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT `email`, `password` FROM `users` WHERE `email`=%s", (
            auth.username,)
    )

    if res > 0:
        user_row = cur.fetchone()
        print(user_row)
        (email, password) = user_row

        if auth.username != email or auth.password != password:
            return "Invalid credentials", 401
        else:
            return create_jwt(email, settings.JWT_SECRET, "admin"), 200
    else:
        return "Invalid credentials", 401


@app.route("/current-user", methods=["GET"])
def get_current_user():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "Invalid credentials", 401

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, settings.JWT_SECRET, algorithms=["HS256"])
    except Exception as e:
        print(e)
        return "Unauthorized", 401

    return decoded, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
