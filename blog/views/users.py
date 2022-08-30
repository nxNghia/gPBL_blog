from flask import request, redirect, url_for, render_template, flash, session, jsonify
from blog import app, db
from blog.models.models import Like, Post, User, Tag, UserTag, Follow

@app.route('/signup', methods=['POST', 'GET'])
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
        tags = Tag.query.filter(Tag.byUser == 0).all()
        return render_template('signin.html', tags=tags)

@app.route('/user/index', methods=['GET'])
def user_index():
    title = "ユーザリスト"
    users = db.session.query(User).filter(User.id != session['logged_in']['id']).all()
    countLikes = []
    for user in users:
        like = db.session.query(Like).join(Post).filter(Like.post_id == Post.id).filter(Post.user_id == user.id).count()
        countLikes.append(like)
    return render_template('user/list-user.html', users = users, countUser = len(users), countLikes = countLikes, title = title)

@app.route('/user', methods=['GET', 'POST'])
def get_user():
    if request.args.get('user_id') == None :
        userId = session['logged_in']['id']
        tagUser = session['tags']
    else :
        userId = request.args.get('user_id')

    tagUser = db.session.query(Tag, UserTag).filter(UserTag.tag_id == Tag.id).filter(UserTag.user_id == userId).all()
    if request.method == 'GET':
        userInfo = db.session.query(User).filter(User.id == userId).first()
        tags = db.session.query(Tag).all()
        posts = db.session.query(Post, Tag).join(Tag).filter(Post.user_id== userId, Post.type==0, Tag.id==Post.tag_id).all()
        userFollow = db.session.query(Follow).filter(Follow.user_id == userId, Follow.follower_id == session['logged_in']['id']).count()

        posts_point = []

        for post in posts:
            post_point = db.session.query(Like).filter(Like.post_id==post['Post'].id).all()
            posts_point.append(len(post_point))

        finished_tasks = db.session.query(Post).filter(Post.user_id == userId, Post.type==1, Post.finished==True).all()
        unfinished_tasks = db.session.query(Post).filter(Post.user_id == userId, Post.type==1, Post.finished==False).all()

        return render_template('user/user-info.html',
                                    user_info= userInfo,
                                    posts=posts,
                                    tags=tags,
                                    length=len(posts),
                                    posts_point=posts_point,
                                    finished_tasks=finished_tasks,
                                    unfinished_tasks=unfinished_tasks,
                                    tagUser = tagUser,
                                    userFollow = userFollow
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

@app.route('/follow/add', methods=['POST'])
def add_follow():
    follow = Follow(
            follower_id = session['logged_in']["id"],
            user_id = request.args.get('user_id'),
        )
    
    db.session.add(follow)
    db.session.commit()

    return jsonify(1)

@app.route('/follow/delete', methods=['DELETE'])
def un_follow():
    follow = db.session.query(Follow).filter(Follow.user_id == request.args.get('user_id'), Follow.follower_id == session['logged_in']['id']).first()
    
    db.session.delete(follow)
    db.session.commit()

    return jsonify(1)

@app.route('/search', methods=['GET'])
def searching():
    search_value = request.args.get('search-box')
    search_type = request.args.get('search-type')
    
    if search_type == '0':
        users = db.session.query(User).filter(User.username.contains(search_value)).all()
        info = []
        for user in users:
            related_tags = db.session.query(Tag).join(UserTag).filter(UserTag.user_id==user.id).all()
            _tags_ = []
            for tag in related_tags:
                _tags_.append({
                    "id": tag.id,
                    "name": tag.name
                })
            info.append({
                "user": user,
                "tags": _tags_
            })
        return render_template('user/list-user.html', users=users, info=info)
    else:
        if search_type == '2':
            posts = db.session.query(Post, Tag, User).join(Tag, User).filter(Post.title.contains(search_value) | Post.content.contains(search_value)).all()

            point = []
            userLike = []
            for post in posts:
                _point_ = db.session.query(Like).filter(Like.post_id==post['Post'].id).all()
                point.append(len(_point_))
                like = db.session.query(Like).filter(Like.post_id == post['Post'].id, Like.user_id == session["logged_in"]['id']).count()
                userLike.append(like)
            return render_template('post/list-post.html', posts=posts, point=point, length=len(point), userLike = userLike)
    return redirect(url_for('post_index'))
