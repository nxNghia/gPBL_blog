from flask import request, redirect, url_for, render_template, flash, session
from blog import app, db
from blog.models.models import User, Tag, UserTag

@app.route('/')
def show_entries():
    if not session.get('logged_in'):
        return redirect('/login')
    return redirect(url_for('get_user'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(User.query.all())
    if request.method == 'POST':
        users = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if users is None:
            flash('ユーザ名やパスワードが正しくありません。')
        else:
            _session = {
                "id": users.id,
                "username": users.username,
                "password": users.password,
                "point": users.point,
                "gender": users.gender,
                "school_year": users.school_year
            }
            session['logged_in'] = _session
            user_tags = db.session.query(Tag).filter(UserTag.tag_id==Tag.id, UserTag.user_id==users.id).all()

            tags = []

            for tag in user_tags:
                print(tag.name)
                tags.append({
                    "id": tag.id,
                    "name": tag.name
                })
            session['tags'] = tags
            return redirect(url_for('get_user'))
    return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('show_entries'))
