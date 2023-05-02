from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config
# `set` for windows
# export FLASK_APP=flaskblog.py
# flask run
# export FLASK_DEBUG=1
#
# >>> pip install flask-wtf
# >>> pip install flask-sqlalchemy
# >>> pip install flask-login
"""
>>> import secrets
>>> secrets.token_hex(16)
"""

db = SQLAlchemy()

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()

"""Creating DB"""
# >>> python
# >>> from flaskblog import db
# >>> db.create_all()
# Creating a user
# >>> from flaskblog import User, Post
# >>> user_1 = User(username='name', email='email', password='1234')
# >>> db.session.add(user_1)
# >>> db.session.commit()
# Queries
# >>> User.query.all()
# >>> User.query.first()
# >>> User.query.filter_by(username='name').all()
# >>> User.query.filter_by(username='name').first()
# >>> user = User.query.filter_by(username='name').first()
# >>> user.id
# >>> user = User.query.get(1)
# >>> user
# >>> user.posts
# Create a Post
# >>> post_1 = Post(title='BLog 1', content='1st post', user_id=user.id)
# >>> db.session.add(post_1)
# >>> db.session.commit()
# >>> for post in user.posts:
# ...   print(post.title)
# >>> post = Post.query.first()
# >>> post
# >>> post.user_id
# >>> post.author
# Delete db
# >>> db.drop_all()

"""Encryption"""
# pip install flask-bcrypt
# >>> python
# >>> from flask_bcrypt import Bcrypt
# >>> bcrypt = Bcrypt()
# >>> bcrypt.generate_password_hash('testing')
# >>> hashed_pw = bcrypt.generate_password_hash('testing').decode('utf-8')
# >>> bcrypt.check_password_hash(hashed_pw, 'testing')

"""Pagination"""
# >>> posts = Post.query.paginate()
# >>> posts # <flask_sqlalchemy.Pagination object at 0x10bde5cc0>
# >>> dir(posts)
# >>> posts.per_page
# >>> posts.page
# >>> for post in posts.items:
# ...   print(post)
# >>> posts = Post.query.paginate(per_page=5)

"""Mail and Password Reset""" # USE `authlib` or `pyjwt`
# >>> from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# >>> s = Serializer('secret', 30)
# >>> token = s.dumps({'user_1': 1}).decode('utf-8')
# >>> token
# >>> s.loads(token)
#
# pip install flask-mail



# >>>
# >>>
# >>>
# >>>
# >>>
# >>>
# >>>
# >>>
# >>>
# >>>
# >>>
# >>>
# >>>
# >>>
# >>>
# >>>
# >>>
# >>>
# >>>
# >>>


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
