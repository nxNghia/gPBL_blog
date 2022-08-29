from flask import request, redirect, url_for, render_template, flash, session
from blog import app, db
from blog.models.models import Post

@app.route('/post/index', methods=['GET'])
def post_index():
    return render_template('post/list-post.html')
