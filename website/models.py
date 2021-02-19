from . import db
from flask_login import UserMixin

class Client(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    firstName = db.Column(db.String(25))
    lastName = db.Column(db.String(25))
    phone = db.Column(db.String(25))
    email = db.Column(db.String(25))
    fixes = db.relationship('Fix',backref='client')
    iduser = db.Column(db.Integer, db.ForeignKey('user.id'))

class FixDetail(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String)
    cost = db.Column(db.Float,default=0)
    fixes = db.relationship('Fix',backref='fixdetail')
    iduser = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Fix detail %r>' % self.id

class Fix(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    extra_cost = db.Column(db.Float, default=0)
    description = db.Column(db.String,nullable=False)
    completed = db.Column(db.Integer, default=0)  # not repaired
    image_path = db.Column(db.String)
    idclient = db.Column(db.Integer,db.ForeignKey('client.id'))
    idfixType = db.Column(db.Integer,db.ForeignKey('fix_detail.id'))
    iduser = db.Column(db.Integer,db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Fix %r>' % self.id

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String,unique=True)
    password = db.Column(db.String)
    username = db.Column(db.String)
    activated = db.Column(db.Boolean)
    clients = db.relationship('Client',backref='user')
    fixdetails = db.relationship('FixDetail',backref='user')
    fixes = db.relationship('Fix',backref='user')
    employees = db.relationship('Employee',backref='user')
    def __repr__(self):
        return '<User %r>' % self.id

class Employee(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    firstName = db.Column(db.String)
    lastName = db.Column(db.String)
    cv = db.Column(db.String,nullable=True)
    phone = db.Column(db.String)
    role = db.Column(db.String)
    iduser = db.Column(db.Integer,db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Employee %r' % self.id


