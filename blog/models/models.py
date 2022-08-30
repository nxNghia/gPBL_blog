from email.policy import default
from blog import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    point = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Integer, nullable=False)
    school_year = db.Column(db.Integer, nullable=False)

    # def __init__(self, data):
    #     """
    #     Class constructor
    #     """
    #     # print(data)
    #     self.username = data.get('username')
    #     self.password = data.get('password')
    #     self.point = 0
    #     self.gender = data.get('gender')

    def __repr__(self):
        return '<User id:{} username:{} password:{} point:{} gender:{} school_year:{}>'.format(self.id, self.username, self.password, self.point, self.gender, self.school_year)

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    type = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    deadline = db.Column(db.Date, nullable=True)
    finished = db.Column(db.Boolean, nullable=False)

    # def __init__(self, data):
    #     """
    #     Class constructor
    #     """
    #     self.content = data.get('content')
    #     self.tag_id = data.get('tag_id')
    #     self.type = data.get('type')

    def __repr__(self):
        return '<Posts id:{} title:{} content:{} tag_id:{} type:{} user_id:{} deadline:{} finished:{}>'.format(self.id, self.title, self.content, self.tag_id, self.type, self.user_id, self.deadline, self.finished)

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    byUser = db.Column(db.Boolean, nullable=True)
    parent_tag = db.Column(db.Integer, default=-1)

    # def __init__(self, data):
    #     """
    #     Class constructor
    #     """
    #     self.name = data.get('name')

    def __repr__(self):
        return '<Tags id:{} name:{}>'.format(self.id, self.name)

class UserTag(db.Model):
    __tablename__ = 'user_tags'

    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    # def __init__(self, data):
    #     """
    #     Class constructor
    #     """
    #     self.tag_id = data.get('tag_id')
    #     self.user_id = data.get('user_id')

    def __repr__(self):
        return '<UserTag id:{} tag_id:{} user_id:{}>'.format(self.id, self.tag_id, self.user_id)

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    # def __init__(self, data):
    #     """
    #     Class constructor
    #     """
    #     self.content = data.get('content')
    #     self.user_id = data.get('user_id')
    #     self.post_id = data.get('post_id')

    def __repr__(self):
        return '<Comments id:{} content:{} user_id:{} post_id:{}>'.format(self.id, self.content, self.user_id, self.post_id)

class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    # def __init__(self, data):
    #     """
    #     Class constructor
    #     """
    #     self.user_id = data.get('user_id')
    #     self.post_id = data.get('post_id')

    def __repr__(self):
        return '<Likes id:{} user_id:{} post_id:{}>'.format(self.id, self.user_id, self.post_id)

class Follow(db.Model):
    __tablename__ = 'follows'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # def __init__(self, data):
    #     """
    #     Class constructor
    #     """
    #     self.user_id = data.get('user_id')
    #     self.follower_id = data.get('follower_id')

    def __repr__(self):
        return '<Follows id:{} user_id:{} follower_id:{}>'.format(self.id, self.user_id, self.follower_id)
