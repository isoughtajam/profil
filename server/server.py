# server.py
from flask import Flask, render_template, send_from_directory

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/blog")
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
