from flask import request, redirect, url_for, render_template, flash, session, jsonify
from blog import app, db
from blog.models.models import Room, RoomUser, User, Post, Tag, Like
from blog.views.views import login_required

@app.route('/room', methods=['GET'])
@login_required
def room_index():
    if request.method == 'GET':
        rooms = db.session.query(Room, User).join(User).all()

        return render_template('room/list-room.html', rooms=rooms)

@app.route('/room/create', methods=['GET', 'POST'])
@login_required
def room_create():
    if request.method == 'GET':
        return render_template('room/create-room.html')
    else:
        new_room = Room(
            name = request.form['name'],
            description = request.form['description'],
            owner_id = session['logged_in']['id']
        )

        db.session.add(new_room)
        db.session.commit()

        return redirect(url_for('room_index'))

@app.route('/room/join', methods=['POST'])
@login_required
def join_room():
    room_id = request.args.get('room')
    user_id = request.args.get('user_id')

    print(room_id, user_id)

    new_joinRoom = RoomUser(
        room_id = room_id,
        user_id = user_id
    )

    db.session.add(new_joinRoom)
    db.session.commit()

    return redirect(url_for('get_room', id=room_id))

@app.route('/room/exit', methods=['POST'])
@login_required
def exit_room():
    room_id = request.args.get('room')
    user_id = request.args.get('user_id')

    user_room = db.session.query(RoomUser).filter(RoomUser.room_id==room_id, RoomUser.user_id==user_id).first()

    db.session.delete(user_room)
    db.session.commit()

    return redirect(url_for('room_index'))

@app.route('/room/detail', methods=['GET'])
@login_required
def get_room():
    if request.method == 'GET':
        id = request.args.get('id')
        room_info = db.session.query(Room).filter(Post.id==id).first()
        posts = db.session.query(Post, User, Tag).join(User, Tag).filter(Post.type==0, Post.room_id==id).order_by(Post.id.desc()).all()
        point = []
        userLike = []
        for post in posts:
            _point_ = db.session.query(Like).filter(Like.post_id==post['Post'].id).all()
            point.append(len(_point_))
            like = db.session.query(Like).filter(Like.post_id == post['Post'].id, Like.user_id == session["logged_in"]['id']).count()
            userLike.append(like)

        userRoom = db.session.query(RoomUser).filter(RoomUser.user_id==session['logged_in']['id'], RoomUser.room_id==id).all()

        return render_template('room/detail-room.html', posts=posts, length=len(posts), id=id, userLike = userLike, point=point, joined=len(userRoom), room_info=room_info)
