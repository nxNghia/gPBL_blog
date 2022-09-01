from flask import request, redirect, url_for, render_template, flash, session, jsonify
from blog import app, db
from blog.models.models import Post, Tag, User, Comment, Like
from blog.views.views import login_required

@app.route('/tag-child', methods=['GET'])
def tag_child():
    
    tags = db.session.query(Tag).filter(Tag.parent_tag == request.args.get('tag_id')).all()
    
    tags = [tag.selialize() for tag in tags]
    

    return jsonify(tags)


@app.route('/tag-child/<int:id>', methods=['GET'])
@login_required
def post_by_tag(id):
    posts = db.session.query(Post, User, Tag).join(Tag, User).filter(Post.tag_id==id).order_by(Post.id.desc()).all()
    point = []
    userLike = []
    for post in posts:
        _point_ = db.session.query(Like).filter(Like.post_id==post['Post'].id).all()
        point.append(len(_point_))
        like = db.session.query(Like).filter(Like.post_id == post['Post'].id, Like.user_id == session["logged_in"]['id']).count()
        userLike.append(like)
    
    postPoints = db.session.query(Post, User, Tag).join(Tag, User).filter(Post.tag_id==id).order_by(Post.id.desc()).all()
    point1 = []
    userLike1 = []
    for post in postPoints:
        _point_ = db.session.query(Like).filter(Like.post_id==post['Post'].id).all()
        point1.append(len(_point_))
        like = db.session.query(Like).filter(Like.post_id == post['Post'].id, Like.user_id == session["logged_in"]['id']).count()
        userLike1.append(like)
    
    return render_template('post/list-post.html', posts=posts, point=point, length=len(point), userLike = userLike, postPoints=postPoints, point1=point1, length1=len(point1), userLike1 = userLike1)
