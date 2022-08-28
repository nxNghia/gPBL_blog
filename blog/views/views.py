from flask import request, redirect, url_for, render_template, flash, session
from blog import app
from blog.models.models import User

@app.route('/')
def show_entries():
    if not session.get('logged_in'):
        return redirect('/login')
    return render_template('entries/index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if users is None:
            flash('ユーザ名やパスワードが正しくない。')
        else:
            print(users.id)
            _session = {
                "id": users.id,
                "username": users.username,
                "password": users.password,
                "point": users.point,
                "gender": users.gender
            }
            session['logged_in'] = _session
            return redirect(url_for('get_user'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('show_entries'))
