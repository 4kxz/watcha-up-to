from flask import Flask, request, render_template, abort
import datetime as dt
import ics
import pytz
import requests

app = Flask(__name__)
app.config.from_envvar('FLASK_SETTINGS')


@app.route('/')
def index():
    calendar_url = app.config['CALENDAR_URL']
    response = requests.get(calendar_url)
    calendar = ics.Calendar(response.text)
    current_event = None
    for event in calendar.events:
        if event.begin <= dt.datetime.now(pytz.utc) <= event.end:
            current_event = event
    return render_template("index.html", event=current_event)


if __name__ == '__main__':
    app.run(debug=True)
