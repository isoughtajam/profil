# server.py
import hashlib
import json
import logging

from flask import Flask, render_template, send_from_directory, request, redirect, url_for

from admin.forms import validate_write_post_form
from admin.util import (save_written_post, get_post_content, 
    get_latest_post, get_pre_login_info)

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")

logger = logging.getLogger(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/images/<path:path>")
def images(path):
    return send_from_directory('../static/images', path)


@app.route("/css/<path:path>")
def css(path):
    return send_from_directory('../static/css', path)


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("../static/images/favicon.gif")


@app.route("/get-post/<slug>")
def get_post(slug):
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


@app.route("/blog/<slug>/")
def blog_post(slug):
  return render_template("app.html", slug=slug, content_type="blog")


@app.route("/blog/")
def application():
    return render_template("app.html", content_type="blog")


@app.route("/links/")
def links():
    return render_template("links.html", content_type="links")


@app.route("/write/", methods=['GET', 'POST'])
def write():
    messages = []
    if request.method == 'POST':
        if set(request.form.keys()) == set(['username', 'pw']):
            return render_template("write.html")

        validate_result, validate_text = validate_write_post_form(request.form)
        if validate_result:
            save_result, save_text = save_written_post(request.form)
        messages.append(validate_text)
        return render_template("write.html", messages=messages)
    return redirect(url_for("login"))


@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        pw = request.form.get('pw')

        # Get username and nacl from user table
        nacl, passhash = get_pre_login_info(username)
        if nacl and passhash:
            yum = hashlib.sha512(pw + nacl)
            if yum.hexdigest() == passhash:
                return redirect(url_for('write'), code=307)
        return render_template("login.html", messages=["Login failed."])
    return render_template("login.html")


if __name__ == "__main__":
  app.run()
