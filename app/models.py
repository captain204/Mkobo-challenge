from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
import bleach
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from app.exceptions import ValidationError
from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    location = db.Column(db.String(64))
    accounts = db.relationship('Account', backref='user', lazy='dynamic')
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic')
    registered_since = db.Column(db.DateTime(), default=datetime.utcnow)
    

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id),
            'firstname': self.firstname,
            'lastname': self.lastname,
            'registerd_since': self.registered_since,
            'location':self.location
        }
        return json_user

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.username




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.Text)
    balance = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow) 

    def to_json(self):
        json_account ={
            'url':url_for('api.get_user_account', id =self.id),
            'account_type': self.account_type,
            'balance': self.balance,
            'user_url':url_for('api.get_user', id=self.user_id),
            'created_at':self.created_at
        }
        return json_account

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    amount = db.Column(db.Integer)
    description = db.Column(db.Text)
    transaction_type = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_json(self):
        json_transaction = {
            'url':url_for('api.get_user_transactions', id =self.id),
            'user_url':url_for('api.get_user', id=self.user_id),
            'amount':self.amount,
            'description':self.description,
            'transaction_type':self.transaction_type,
            'timestamp':self.timestamp
        }
        return json_transaction





