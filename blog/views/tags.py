from flask import request, redirect, url_for, render_template, flash, session, jsonify
from blog import app, db
from blog.models.models import Post, Tag, User, Comment, Like
from datetime import datetime
import numpy
import json


@app.route('/tag-child', methods=['GET'])
def tag_child():
    
    tags = db.session.query(Tag).filter(Tag.parent_tag == request.args.get('tag_id')).all()
    
    tags = [tag.selialize() for tag in tags]
    

    return jsonify(tags)
