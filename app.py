from flask import Flask, render_template

from content import get_content as get_internal_content

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/content")
def get_content():
    return get_internal_content()


if __name__ == '__main__':
    app.run()
