from datetime import timezone, datetime as dt
import os
import signal
import sys
import pytz
from flask import Flask, request, jsonify, abort, render_template

DEBUG = os.getenv("GPS_DEBUG")
app = Flask(__name__)

LOCAL_TZ = pytz.timezone(os.getenv("LOCAL_TZ"))
OSM_ZOOM = 14

latest_entry = None


def info(content):
    app.logger.info(content)


def error(content):
    app.logger.error(content)


def debug(content):
    if DEBUG:
        app.logger.info(content)


def make_osm_url(latitude, longitude, zoom):
    url = f"https://www.openstreetmap.org/#map={zoom}/{latitude}/{longitude}"
    return url


def handle_post_auth(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        abort(401, "Missing Authorization header")
    
    if not auth_header.startswith("Bearer "):
        abort(401, "Invalid Authorization header")

    request_token = auth_header.replace("Bearer ", "")
    correct_token = os.getenv("GPS_POST_TOKEN")

    if not correct_token:
        abort(500, "Server configuration error: GPS_POST_TOKEN not set")
    
    if request_token != correct_token:
        abort(403, "Invalid authentication token")


@app.route("/", methods=["POST"])
def post():
    global latest_entry
    handle_post_auth(request)

    data = request.get_json()
    lat = data.get("latitude")
    long = data.get("longitude")

    timestamp = dt.now(LOCAL_TZ).strftime("%B %d, %Y at %-I:%M %p %Z")

    latest_entry = {
        "latitude": lat,
        "longitude": long,
        "osm_url": make_osm_url(lat, long, OSM_ZOOM),
        "timestamp": timestamp
    }

    return jsonify(latest_entry), 200


@app.route("/", methods=["GET"])
def get():

    if not latest_entry:
        res = render_template(
            'index.html',
            not_found=True,
        )
        return res, 404

    lat = latest_entry["latitude"]
    long = latest_entry["longitude"]

    res = render_template(
        'index.html',
        osm_url=make_osm_url(lat, long, OSM_ZOOM),
        coords=f"{lat}, {long}",
        timestamp=latest_entry["timestamp"],
    )

    return res, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=13856)