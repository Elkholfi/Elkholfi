import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

'''
A Blueprint is a way to organize a group of related views and other code. Rather than 
registering views and other code directly with an application, they are registered with
a blueprint. Then the blueprint is registered with the application when it is available 
in the factory function.
Flaskr will have two blueprints, one for authentication functions and one for the blog 
posts functions. The code for each blueprint will go in a separate module. Since the blog 
needs to know about authentication, you’ll write the authentication one first.
This creates a Blueprint named 'auth'. Like the application object, the blueprint needs to 
know where it’s defined, so __name__ is passed as the second argument. The url_prefix will 
be prepended to all the URLs associated with the blueprint.
Import and register the blueprint from the factory using app.register_blueprint(). Place 
the new code at the end of the factory function before returning the app.
When the user visits the /auth/register URL, the register view will return HTML with a form 
for them to fill out. When they submit the form, it will validate their input and either show 
the form again with an error message or create the new user and go to the login page.
For now you will just write the view code. On the next page, you’ll write templates to generate 
the HTML form.
'''


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
