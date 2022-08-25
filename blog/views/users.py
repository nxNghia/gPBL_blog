from crypt import methods
from flask import request, redirect, url_for, render_template, flash, session
from blog import app, db
from blog.models.models import User

@app.route('/user/create', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        # print(request.form)
        user = User(
            username = request.form['username'],
            password = request.form['password'],
            point = 0,
            gender = request.form['gender']
        )

        db.session.add(user)
        db.session.commit()
        flash('成功した')
        return redirect(url_for('show_entries'))
    else:
        return render_template('signin.html')
