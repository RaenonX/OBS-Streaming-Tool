from flask import Flask, render_template, request

from info.dt import get_current_date_time
from content import get_content as get_internal_content

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/dt")
def get_current_dt():
    return render_template("current_dt.html")


@app.route("/content/marquee")
def get_content():
    return get_internal_content()


@app.route("/content/dt")
def get_current_dt_text():
    return get_current_date_time(request.args.get("suffix"))


if __name__ == '__main__':
    app.run()
