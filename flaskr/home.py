import functools
import json
import datetime
from flask import request
from stock import predict

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('home', __name__, url_prefix='/')

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


# home page
@bp.route('/')
@login_required
def index():
    return render_template('home.html')


# predict page
@bp.route('/prediction')
@login_required
def prediction(legend='UBER'):
    legend = request.args.get('legend')
    today = str(datetime.date.today())

    db = get_db()
    predictions = db.execute(
        'SELECT * FROM prediction WHERE prediction_date = ? and legend = ?',
         (today, legend)).fetchone()

    if predictions is None:
        x, y = predict.predict(legend)
        labels = json.dumps(x)
        prices = json.dumps(y)
        db.execute(
            "INSERT INTO prediction (labels, prices, legend, prediction_date) VALUES (?, ?, ?, ?)",
            (labels, prices, legend, today),
        )
        db.commit()
    else:
        x = json.loads(predictions["labels"])
        y = json.loads(predictions["prices"])

    # x y value for testing
    # x = ["11 Oct 2021", "12 Oct 2021", "13 Oct 2021", "14 Oct 2021", "15 Oct 2021", "18 Oct 2021", "19 Oct 2021", "20 Oct 2021", "21 Oct 2021", "22 Oct 2021", "25 Oct 2021", "26 Oct 2021", "27 Oct 2021", "28 Oct 2021", "29 Oct 2021", "01 Nov 2021", "02 Nov 2021", "03 Nov 2021", "04 Nov 2021", "05 Nov 2021", "Today"]
    # y = [46.29000091552735, 46.72000122070313, 46.40999984741212, 47.27999877929688, 48.36000061035156, 47.069999694824226, 47.049999237060554, 46.00000000000001, 46.470001220703125, 45.5099983215332, 45.720001220703125, 46.02000045776368, 44.72999954223633, 44.61999893188477, 43.81999969482422, 44.36000061035156, 42.88999938964844, 45.720001220703125, 45.27000045776367, 47.189998626708984, 46.61995580038365]

    return render_template('prediction.html', labels=x, values=y, legend=legend)