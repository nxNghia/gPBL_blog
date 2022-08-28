from blog import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    point = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Integer, nullable=False)

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
        return '<User id:{} username:{} password:{} point:{} gender:{}>'.format(self.id, self.username, self.password, self.point, self.gender)

class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    type = db.Column(db.Boolean, nullable=False)

    # def __init__(self, data):
    #     """
    #     Class constructor
    #     """
    #     self.content = data.get('content')
    #     self.tag_id = data.get('tag_id')
    #     self.type = data.get('type')

    def __repr__(self):
        return '<Posts id:{} content:{} tag_id:{} type:{}>'.format(self.id, self.content, self.tag_id, self.type)

class Tags(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

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

class Comments(db.Model):
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

class Likes(db.Model):
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

class Follows(db.Model):
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
