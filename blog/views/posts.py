from flask import request, redirect, url_for, render_template, flash, session, jsonify
from blog import app, db
from blog.models.models import Post, Tag, User, Comment, Like
from datetime import datetime
from blog.views.views import login_required

from blog.views import room

@app.route('/post/index', methods=['GET'])
@login_required
def post_index():
    # post order by create at
    posts = db.session.query(Post, User, Tag).join(User, Tag).filter(Post.type==0, Post.room_id == None).order_by(Post.id.desc()).all()

    point = []
    userLike = []
    for post in posts:
        _point_ = db.session.query(Like).filter(Like.post_id==post['Post'].id).all()
        point.append(len(_point_))
        like = db.session.query(Like).filter(Like.post_id == post['Post'].id, Like.user_id == session["logged_in"]['id']).count()
        userLike.append(like)
    # Post order by point number
    
    postPoints = db.session.query(Post, User, Tag).join(User, Tag).filter(Post.type==0, Post.room_id == None).order_by(Post.point.desc()).all()

    point1 = []
    userLike1 = []
    for post in postPoints:
        _point_ = db.session.query(Like).filter(Like.post_id==post['Post'].id).all()
        point1.append(len(_point_))
        like = db.session.query(Like).filter(Like.post_id == post['Post'].id, Like.user_id == session["logged_in"]['id']).count()
        userLike1.append(like)

    return render_template('post/list-post.html', posts=posts, point=point, length=len(point), userLike = userLike, postPoints=postPoints, point1=point1, length1=len(point1), userLike1 = userLike1)

@app.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.args.get('room') == None :
        room_id = None
    else:
        room_id = request.args.get('room')

    if request.method == 'GET':
        tags = Tag.query.filter(Tag.byUser == 0).filter(Tag.parent_tag == -1).all()
        return render_template('post/post-create.html', tags=tags, room_id=room_id)
    else:
        if request.form['type'] == '0':
            post = Post(
                title = request.form['title'],
                content = request.form['content'],
                tag_id = request.form['tag_id'],
                type = True,
                user_id = session['logged_in']['id'],
                deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%d'),
                finished = False
            )
            db.session.add(post)
            db.session.commit()
        else:
            post = Post(
                title = request.form['title'],
                content = request.form['content'],
                tag_id = request.form['tag_id'],
                type = False,
                user_id = session['logged_in']['id'],
                finished = False,
                room_id = room_id
            )
            db.session.add(post)
            db.session.commit()

    if room_id == None:
        if request.form['type'] == 1:
            return redirect(url_for('post_index'))
        else:
            return redirect(url_for('get_user'))
    else:
        return redirect(url_for('get_room', id=room_id))

@app.route('/post/update/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_post(id):
    if request.method == 'GET':
        post = db.session.query(Post).filter(Post.id==id).first()
        tags = Tag.query.all()
        return render_template('post/post-edit.html', post=post, id=id, tags=tags)

    else:
        if request.method == 'POST':
            post = Post.query.get(id)
            post.title = request.form['title']
            post.content = request.form['content']
            post.tag_id = request.form['tag_id']
            db.session.commit()
            return redirect(url_for('edit_post', id=id))

@app.route('/post/delete/<int:id>', methods=['GET'])
@login_required
def delete_post(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('user_index'))


@app.route('/post/<int:id>', methods=['GET'])
def detail_post(id):
    post = db.session.query(Post, User, Tag).join(User, Tag).filter(Post.user_id == User.id, Tag.id == Post.tag_id).filter(Post.id==id).first()
    comments = db.session.query(Comment, User).join(User).filter(Comment.user_id == User.id).filter(Comment.post_id==id).all()
    countLike = db.session.query(Like).filter(Like.post_id == id).count()
    userLike = db.session.query(Like).filter(Like.post_id == id, Like.user_id == session['logged_in']["id"]).count()

    return render_template('post/detail.html', post=post, comments = comments, countLike = countLike, userLike = userLike)

@app.route('/comment/add', methods=['POST'])
@login_required
def add_comment():
    comment = Comment(
            user_id = session['logged_in']["id"],
            post_id = request.args.get('post_id'),
            content = request.form['content']
        )
    data = {
        'user_id' : session['logged_in']["id"],
        'username' : session['logged_in']["username"],
        'content' : request.form['content']
    }
    
    db.session.add(comment)
    db.session.commit()

    return jsonify(data)

@app.route('/like/add', methods=['POST'])
@login_required
def add_like():
    like = Like(
            user_id = session['logged_in']["id"],
            post_id = request.args.get('post_id'),
        )
    db.session.add(like)
    db.session.commit()
    post = Post.query.filter_by(id=request.args.get('post_id')).first()
    user = User.query.filter_by(id=post.user_id).first()
    userUpdate = User.query.filter_by(id=user.id).update(dict(point = user.point + 1))
    db.session.commit()
    postUpdate = Post.query.filter_by(id=request.args.get('post_id')).update(dict(point = post.point + 1))
    db.session.commit()
    
    return jsonify(1)


@app.route('/comment/edit', methods=['POST'])
@login_required
def edit_comment():
    comment = Comment.query.filter_by(id=request.args.get('comment_id')).update(dict(content = request.form['content']))
    db.session.commit()
    comment = Comment.query.filter_by(id=request.args.get('comment_id')).first()

    return jsonify(comment.selialize())

@app.route('/comment/delete', methods=['DELETE'])
@login_required
def delete_comment():
    comment = Comment.query.filter_by(id=request.args.get('comment_id')).first()
    db.session.delete(comment)
    db.session.commit()

    return jsonify(1)
