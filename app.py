from datetime import datetime, timedelta

from flask import Flask, render_template, request, redirect, url_for

from info.dt import get_current_date_time
from content import get_content as get_internal_content
from timer.timer import get_timer_diff

app = Flask(__name__)


@app.route("/")
def get_marquee():
    return render_template("marquee.html")


@app.route("/dt")
def get_current_dt():
    return render_template("current_dt.html")


@app.route("/timer")
def get_timer():
    return render_template("timer.html")


@app.route("/chrono")
def get_chrono():
    t_delta = timedelta(days=int(request.args.get("d", 0)), hours=int(request.args.get("h", 0)),
                        minutes=int(request.args.get("m", 0)), seconds=int(request.args.get("s", 0)))
    return redirect(url_for("get_timer", dt=datetime.now() + t_delta, **request.args))


@app.route("/text")
def get_text():
    return render_template("text.html", text_content=request.args.get("txt", 0))


@app.route("/content/marquee")
def get_marquee_text():
    return get_internal_content()


@app.route("/content/dt")
def get_current_dt_text():
    return get_current_date_time()


@app.route("/content/timer")
def get_timer_text():
    return get_timer_diff(
        request.args.get("dt"),
        count_up=request.args.get("up"), end_message=request.args.get("end_msg"))


if __name__ == '__main__':
    app.run()
