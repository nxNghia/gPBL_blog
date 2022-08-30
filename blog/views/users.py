from flask import request, redirect, url_for, render_template, flash, session
from blog import app, db
from blog.models.models import User, Tag, UserTag

@app.route('/user/create', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        user = User(
            username = request.form['username'],
            password = request.form['password'],
            point = 0,
            gender = request.form['sex'],
            school_year = request.form['school_year']
        )

        db.session.add(user)
        db.session.commit()

        userTags = []

        if request.form['tag1'] != '-1':
            userTags.append(UserTag(
                tag_id = request.form['tag1'],
                user_id = user.id
            ))

        if request.form['tag2'] != '-1':
            userTags.append(UserTag(
                tag_id = request.form['tag2'],
                user_id = user.id
            ))

        if request.form['tag3'] != '-1':
            userTags.append(UserTag(
                tag_id = request.form['tag3'],
                user_id = user.id
            ))

        db.session.add_all(userTags)
        db.session.commit()

        _session = {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "point": user.point,
            "gender": user.gender,
            "school_year": user.school_year
        }
        session['logged_in'] = _session

        user_tags = db.session.query(Tag).filter(UserTag.tag_id==Tag.id, UserTag.user_id==user.id).all()

        tags = []

        for tag in user_tags:
            tags.append({
                "id": tag.id,
                "name": tag.name
            })

        session['tags'] = tags

        return redirect(url_for('get_user'))
    else:
        tags = Tag.query.all()
        return render_template('signin.html', tags=tags)

@app.route('/user/index', methods=['GET'])
def user_index():
    return render_template('user/list-user.html')

@app.route('/user', methods=['GET', 'POST'])
def get_user():
    if request.method == 'GET':
        return render_template('user/user-info.html', user_info=session['logged_in'])
