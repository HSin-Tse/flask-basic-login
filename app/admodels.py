from flask_login import UserMixin, login_user

from extensions import db, bcrypt

article_tag = db.Table('article_tag',
                       db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
                       db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
                       )

childservice_action = db.Table('childservice_action',
                               db.Column('childservice_id', db.Integer, db.ForeignKey('childservice.id'),
                                         primary_key=True),
                               db.Column('action_id', db.Integer, db.ForeignKey('action.id'), primary_key=True)
                               )



class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    tags = db.relationship('Tag', secondary=article_tag, backref=db.backref('articles'))

    def __repr__(self):
        return '<Article-%d %r>' % (self.id, self.title)


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return '<Tag-%d %r>' % (self.id, self.name)


class ChildService(db.Model):
    __tablename__ = 'childservice'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    tags = db.relationship('Action', secondary=childservice_action, backref=db.backref('childservice'))

    roles = db.relationship('Role', backref='childservice', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class Action(db.Model):
    __tablename__ = 'action'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<action %r>' % self.name


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    childservice_id = db.Column(db.Integer, db.ForeignKey('childservice.id'))

    # childservice = db.relationship('ChildService', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(255))
    mail = db.Column(db.String(64), unique=True, index=True)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def set_password(self, password):
        """Convert the password to cryptograph via flask-bcrypt"""
        self.password = password
        return bcrypt.generate_password_hash(password)

    def check_password(self, password):
        print(" password:", password, '-->File "admodels.py", line 42')

        """Check the entry-password whether as same as user.password."""
        return bcrypt.check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_actice(self):
        return True

    def is_anonymous(self):
        return False

    def get_username(self):
        return self.username

    def login(self):
        login_user(self)

    def __repr__(self):
        return '<User %r>' % self.username
