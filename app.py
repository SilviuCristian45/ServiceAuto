from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)#setez varia bila pentru migrations

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


@app.route('/' , methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        fixes = Fix.query.filter_by(completed = 0)
        fixeTypes = FixDetail.query.all()
        return render_template('index.html',fixes=fixes,fixTypes=fixeTypes)
    else:#method post
        fix_detail = request.form['fixdetails']
        extracost = request.form['extracost']
        fixType = request.form['fixesTypes']
        client_name = request.form['nume']
        client_prenume = request.form['prenume']
        client_phone = request.form['nrtelefon']
        client_email = request.form['email']
        new_client = Client(firstName=client_name, lastName=client_prenume, phone=client_phone, email=client_email)
        new_fix = Fix(extra_cost=extracost, description=fix_detail)
        fixTypeObj = FixDetail.query.filter_by(title = fixType).first()
        fixTypeObj.fixes.append(new_fix)
        new_client.fixes.append(new_fix)
        try:
            db.session.add(new_fix)
            db.session.add(new_client)
            db.session.commit()
            return redirect('/')
        except:
            return 'Problema cu reparatia adaugata. Contactati suport IT'


@app.route('/client/<int:id>')
def clientDetails(id):
    client = Client.query.get_or_404(id)
    return render_template('client.html',client=client)

@app.route('/tip-reparatie/<int:id>')
def serviceDetails(id):
    service = FixDetail.query.get_or_404(id)
    return render_template('tip-reparatie.html',service=service)

@app.route('/stergere/<int:id>')
def deleteFix(id):
    try:
        Fix.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect('/')
    except:
        return 'Nu se poate face stergerea acestei reparatii . '

@app.route('/editare/<int:id>',methods=['GET', 'POST'])
def editFix(id):
    if request.method == 'GET':
        fix = Fix.query.get_or_404(id)
        fixTypes = FixDetail.query.all()
        clientFix = Client.query.get_or_404(fix.idclient)
        return render_template('editare.html',fix=fix,fixTypes=fixTypes,client=clientFix)
    else:#Method POST
        fix_detail = request.form['fixdetails']
        extracost = request.form['extracost']
        fixType = request.form['fixesTypes']
        client_name = request.form['nume']
        client_prenume = request.form['prenume']
        client_phone = request.form['nrtelefon']
        client_email = request.form['email']
        # #new_client = Client(firstName=client_name, lastName=client_prenume, phone=client_phone, email=client_email)
        # new_fix = Fix(extra_cost=extracost, description=fix_detail)
        # fixTypeObj = FixDetail.query.filter_by(title=fixType).first()
        # fixTypeObj.fixes.append(new_fix)
        # new_client.fixes.append(new_fix)
        try:
            fix = Fix.query.get_or_404(id)
            fix.description = fix_detail
            fix.extra_cost = extracost
            fixTypeObj = FixDetail.query.filter_by(title=fixType.strip()).first()
            fixTypeObj.fixes.append(fix)
            db.session.commit()
            return redirect('/')
        except:
            return 'Problema cu reparatia editata. Contactati suport IT'

if __name__ == '__main__':
    app.run()
