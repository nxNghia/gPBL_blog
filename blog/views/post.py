from flask import request, redirect, url_for, render_template, flash, session
from blog import app, db
from blog.models.models import Posts, Tags, User

@app.route('/post/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'GET':
        tags = Tags.query.all()
        return render_template('post/post-create.html', tags=tags)
    else:
        if request.form['type'] == 0:
            post = Posts(
                title = request.form['title'],
                content = request.form['content'],
                tag_id = request.form['tag_id'],
                type = True,
                user_id = session['logged_in']['id'],
                deadline = request.form['deadline']
            )
            db.session.add(post)
            db.session.commit()
        else:
            post = Posts(
                title = request.form['title'],
                content = request.form['content'],
                tag_id = request.form['tag_id'],
                type = False,
                user_id = session['logged_in']['id']
            )
            db.session.add(post)
            db.session.commit()

    return redirect(url_for('user_index'))
