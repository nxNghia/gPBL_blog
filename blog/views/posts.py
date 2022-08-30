from flask import request, redirect, url_for, render_template, flash, session
from blog import app, db
from blog.models.models import Post, Tag, User, Comment, Like
from datetime import datetime

@app.route('/post/index', methods=['GET'])
def post_index():
    posts = db.session.query(Post, User, Tag).join(User, Tag).filter(User.id==Post.user_id, Post.type==0, Post.tag_id==Tag.id).all()
    
    point = []
    for post in posts:
        _point_ = db.session.query(Like).filter(Like.post_id==post['Post'].id).all()
        point.append(len(_point_))

    print(point)

    return render_template('post/list-post.html', posts=posts, point=point, length=len(point))

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
                deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%d')
            )
            db.session.add(post)
            db.session.commit()
        else:
            post = Post(
                title = request.form['title'],
                content = request.form['content'],
                tag_id = request.form['tag_id'],
                type = False,
                user_id = session['logged_in']['id']
            )
            db.session.add(post)
            db.session.commit()

    return redirect(url_for('post_index'))


@app.route('/post/<int:id>', methods=['GET'])
def detail_post(id):
    post = Post.query.join(Comment, User, Tag, Like).filter_by(id = id).first()
    return render_template('post/detail.html', post=post)