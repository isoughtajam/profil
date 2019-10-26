# server.py
import hashlib
import json
import logging
from urlparse import urlparse

from flask import Flask, render_template, send_from_directory, request, redirect, url_for

from admin.forms import validate_write_post_form
from admin.util import (save_written_post, get_post_content, 
    get_latest_post, get_pre_login_info)
from search import parse_search_terms_into_tsquery, search_post_data


app = Flask(__name__, static_folder="../static/dist", template_folder="../static")
app.config.from_envvar('PROFIL_CONFIG')

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
    Endpoint to get blog post via slug
    """
    post_content = get_post_content(slug)
    return json.dumps(post_content)


@app.route("/latest-post")
def latest_post():
    """
    Endpoint to get latest blog post
    """
    post_content = get_latest_post()
    return json.dumps(post_content)


@app.route("/blog/<slug>/")
def blog_post(slug):
    """
    View for rendering a particular blog post
    - meta tag contains "blog"
    """
    return render_template("app.html", slug=slug, content_type="blog")


@app.route("/blog/")
def application():
    """
    View for rendering the latest blog post
    - meta tag contains "blog"
    """
    return render_template("app.html", content_type="blog")


@app.route("/links/")
def links():
    """
    View for rendering the links page
    - meta tag contains "links"
    """
    return render_template("links.html", content_type="links")


@app.route("/write/", methods=['GET', 'POST'])
def write():
    """
    Admin view for writing a blog post
    """
    messages = []
    if request.method == 'POST':
        referrer = request.headers.get('Referer')
        parsed = urlparse(referrer)
        if parsed.path == '/login/':
            return render_template("write.html")

        validate_result, validate_text = validate_write_post_form(request.form)
        messages.append(validate_text)
        if validate_result:
            save_result, save_text = save_written_post(request.form)
            messages = [save_text] if not save_result else []
        return render_template("write.html", messages=messages)
    return redirect("/login/")


@app.route("/get-search-results/<search_string>")
def get_search_results(search_string):
    """
    Endpoint to get search result data for a particular search string
    """
    terms = parse_search_terms_into_tsquery(search_string)
    results = search_post_data(terms)

    # Return json object of search results
    return json.dumps(results)


@app.route("/search/")
def search():
    """
    View for rendering search page
    - meta tag contains "search"
    """
    term_str = request.args.get('terms', '')
    return render_template("search.html", content_type="search", term_string=term_str)


@app.route("/login/", methods=['GET', 'POST'])
def login():
    """
    View for logging in to admin view
    """
    if request.method == 'POST':
        username = request.form.get('username')
        pw = request.form.get('pw')

        # Get username and nacl from user table
        nacl, passhash = get_pre_login_info(username)
        if nacl and passhash:
            yum = hashlib.sha512(pw + nacl)
            if yum.hexdigest() == passhash:
                if not app.config.get('DEBUG'):
                    request.environ['wsgi.url_scheme'] = 'https'
                return redirect("/write/", code=307)
        return render_template("login.html", messages=["Login failed."])
    return render_template("login.html")


if __name__ == "__main__":
  app.run()
