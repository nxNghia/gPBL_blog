from flask import request, redirect, url_for, render_template, flash, session, jsonify
from blog import app, db
from blog.models.models import Post, Tag, User, Comment, Like
from datetime import datetime

@app.route('/post/index', methods=['GET'])
def post_index():
    posts = db.session.query(Post, User, Tag).join(User, Tag).filter(User.id==Post.user_id, Post.type==0, Post.tag_id==Tag.id).all()
    
    point = []
    userLike = []
    for post in posts:
        _point_ = db.session.query(Like).filter(Like.post_id==post['Post'].id).all()
        point.append(len(_point_))
        like = db.session.query(Like).filter(Like.post_id == post['Post'].id, Like.user_id == session["logged_in"]['id']).count()
        userLike.append(like)

    return render_template('post/list-post.html', posts=posts, point=point, length=len(point), userLike = userLike)

@app.route('/post/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'GET':
        tags = Tag.query.all()
        return render_template('post/post-create.html', tags=tags)
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
                finished = False
            )
            db.session.add(post)
            db.session.commit()

    return redirect(url_for('post_index'))


@app.route('/post/<int:id>', methods=['GET'])
def detail_post(id):
    post = db.session.query(Post, User, Tag).join(User, Tag).filter(Post.user_id == User.id, Tag.id == Post.tag_id).filter(Post.id==id).first()
    comments = db.session.query(Comment, User).join(User).filter(Comment.user_id == User.id).filter(Comment.post_id==id).all()
    countLike = db.session.query(Like).filter(Like.post_id == id).count()
    userLike = db.session.query(Like).filter(Like.post_id == id, Like.user_id == session['logged_in']["id"]).count()

    return render_template('post/detail.html', post=post, comments = comments, countLike = countLike, userLike = userLike)

@app.route('/comment/add', methods=['POST'])
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
def add_like():
    like = Like(
            user_id = session['logged_in']["id"],
            post_id = request.args.get('post_id'),
        )
    
    db.session.add(like)
    db.session.commit()

    return jsonify(1)
