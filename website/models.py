from . import db

class Client(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    firstName = db.Column(db.String(25))
    lastName = db.Column(db.String(25))
    phone = db.Column(db.String(25))
    email = db.Column(db.String(25))
    fixes = db.relationship('Fix',backref='client')

class FixDetail(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String)
    cost = db.Column(db.Float,default=0)
    fixes = db.relationship('Fix',backref='fixdetail')
    def __repr__(self):
        return '<Fix detail %r>' % self.id

class Fix(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    extra_cost = db.Column(db.Float, default=0)
    description = db.Column(db.String,nullable=False)
    completed = db.Column(db.Integer, default=0)  # not repaired
    idclient = db.Column(db.Integer,db.ForeignKey('client.id'))
    idfixType = db.Column(db.Integer,db.ForeignKey('fix_detail.id'))
    def __repr__(self):
        return '<Fix %r>' % self.id
