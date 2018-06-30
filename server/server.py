# server.py
import json
import logging

from flask import Flask, render_template, send_from_directory, request

from admin.util import save_written_post, get_post_content, get_latest_post

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")

logger = logging.getLogger(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/post/<slug>")
def post(slug):
    """
    find post via slug in db
    """
    post_content = get_post_content(slug)
    return json.dumps(post_content)


@app.route("/latest-post")
def latest_post():
    """
    Get most recent post
    """
    post_content = get_latest_post()
    return json.dumps(post_content)


@app.route("/blog/")
def application():
    return render_template("app.html")

@app.route("/images/<path:path>")
def images(path):
    return send_from_directory('../static/images', path)


@app.route("/css/<path:path>")
def css(path):
    return send_from_directory('../static/css', path)


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("../static/images/favicon.gif")


if __name__ == "__main__":
  app.run()
