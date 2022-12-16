import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

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

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        security_question = request.form['security_question']
        answer = request.form['answer']
        password = request.form['password']
        db = get_db()
        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (first_name, last_name, email, security_question, answer, password) VALUES (?, ?, ?, ?, ?, ?)",
                    (first_name, last_name, email, security_question, answer, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Email {email} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        print(email)
        password = request.form['password']
        print(password)
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            session["logged_in"] = True
            return redirect(url_for('home.index'))

        flash(error)

    return render_template('auth/login.html')

@bp.route('/forgot_password', methods=('GET', 'POST'))
def forgot_password():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        security_question = request.form['security_question']
        answer = request.form['answer']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE email = ? and first_name = ? and last_name = ? and security_question =? and answer = ?', (email, first_name, last_name, security_question, answer)
        ).fetchone()

        if user is None:
            error = 'Incorrect answer'

        if error is None:
            session.clear()
            return redirect(url_for('change_password', inputvalue=user['email']))

        flash(error)
        return render_template('auth/forgot_password.html')

    else:
        return render_template('auth/forgot_password.html')

@bp.route('/change_password', methods=('GET', 'POST'))
def change_password(email = None):
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        if not email:
            error = 'Email is required'
        elif not password:
            error = 'Password is required'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (password) VALUES (?) where email = ?",
                    (generate_password_hash(password), email),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Email {email} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)
    else:
        if email is None:
            return redirect(url_for('auth.login'))
    return render_template('auth/change_password.html', email=email)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))