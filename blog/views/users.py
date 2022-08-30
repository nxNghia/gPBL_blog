from flask import request, redirect, url_for, render_template, flash, session
from blog import app, db
from blog.models.models import Like, Post, User, Tag, UserTag

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
        tags = db.session.query(Tag).all()
        posts = db.session.query(Post, Tag).join(Tag).filter(Post.user_id==session['logged_in']['id'], Post.type==0, Tag.id==Post.tag_id).all()

        posts_point = []

        for post in posts:
            post_point = db.session.query(Like).filter(Like.post_id==post['Post'].id).all()
            posts_point.append(len(post_point))

        finished_tasks = db.session.query(Post).filter(Post.user_id==session['logged_in']['id'], Post.type==1, Post.finished==True).all()
        unfinished_tasks = db.session.query(Post).filter(Post.user_id==session['logged_in']['id'], Post.type==1, Post.finished==False).all()

        return render_template('user/user-info.html',
                                    user_info=session['logged_in'],
                                    posts=posts,
                                    tags=tags,
                                    length=len(posts),
                                    posts_point=posts_point,
                                    finished_tasks=finished_tasks,
                                    unfinished_tasks=unfinished_tasks
                                )
    else:
        if request.method == 'POST':
            user = User.query.get(session['logged_in']['id'])
            user.username = request.form['username']
            user.gender = request.form['sex']
            user.school_year = request.form['school_year']

            db.session.commit()

            session.pop('logged_in', None)
            session['logged_in'] = {
                "id": user.id,
                "username": user.username,
                "password": user.password,
                "point": user.point,
                "gender": user.gender,
                "school_year": user.school_year
            }

            tags = UserTag.query.filter_by(user_id=user.id).all()
            
            tags[0].tag_id = request.form['tag1']
            tags[1].tag_id = request.form['tag2']
            tags[2].tag_id = request.form['tag3']

            db.session.commit()

            session.pop('tags', None)

            new_tags_session = []

            for tag in tags:
                _tag_ = db.session.query(Tag).filter(Tag.id==tag.tag_id).first()
                new_tags_session.append({
                    "id": _tag_.id,
                    "name": _tag_.name
                })

            session['tags'] = new_tags_session

            return redirect(url_for('get_user'))
            