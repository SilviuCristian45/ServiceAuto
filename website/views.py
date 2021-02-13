from flask import Blueprint,render_template, request, redirect,flash
from .models import *

views = Blueprint('views',__name__)

def getFixFormData():
    return request.form['fixdetails'],request.form['extracost'],request.form['fixesTypes']

def getClientFormData():
    return request.form['nume'],request.form['prenume'],request.form['nrtelefon'],request.form['email']

@views.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        fixes = Fix.query.filter_by(completed=0)
        return render_template('index.html', fixes=fixes)

@views.route('/reparatiiterminate',methods=['GET', 'POST'])
def solved_fixes():
    fixes_comp = Fix.query.filter_by(completed=1)
    return render_template('reparatiiterminate.html', fixes_completed=fixes_comp)

@views.route('/adaugareparatie',methods=['GET','POST'])
def add_fix():
    if request.method == 'GET':
        fixeTypes = FixDetail.query.all()
        return render_template('adaugareparatie.html', fixTypes=fixeTypes)
    else:
        fix_detail, extracost, fixType = getFixFormData()
        client_name, client_prenume, client_phone, client_email = getClientFormData()
        new_client = Client(firstName=client_name, lastName=client_prenume, phone=client_phone, email=client_email)
        new_fix = Fix(extra_cost=extracost, description=fix_detail)
        print(fixType)
        fixTypeObj = FixDetail.query.filter_by(title=fixType).first()
        fixTypeObj.fixes.append(new_fix)
        new_client.fixes.append(new_fix)
        try:
            db.session.add(new_fix)
            db.session.add(new_client)
            db.session.commit()
            return redirect('/')
        except:
            return 'Problema cu reparatia adaugata. Contactati suport IT'

@views.route('/adaugaretipreparatie',methods=['GET','POST'])
def addFixType():
    if request.method == 'GET':
        return render_template('adaugaretipreparatie.html')
    else:
        typeFixTitle = request.form['title']
        typeFixCost = request.form['cost']
        try:
            newFixType = FixDetail(title=typeFixTitle, cost=typeFixCost)
            db.session.add(newFixType)
            db.session.commit()
            return redirect('/')
        except:
            return 'Problema la adaugarea tipului de reparatie '

@views.route('/cautareincomplete/<int:flag>',methods=['GET','POST'])
def findFix(flag):
    if request.method == 'POST':
        what_to_find = request.form['cautare_reparatie']
        fixes = Fix.query.all()
        result = []
        for fix in fixes:
            if what_to_find in fix.description and fix.completed == flag:
                result.append(fix)
        return render_template('reparaticautate.html', fixDescription=result)

@views.route('/client/<int:id>')
def clientDetails(id):
    client = Client.query.get_or_404(id)
    return render_template('client.html', client=client)

@views.route('/tip-reparatie/<int:id>')
def serviceDetails(id):
    service = FixDetail.query.get_or_404(id)
    return render_template('tip-reparatie.html', service=service)

@views.route('/stergere/<int:id>')
def deleteFix(id):
    try:
        Fix.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect('/')
    except:
        return 'Nu se poate face stergerea acestei reparatii . '

@views.route('/editare/<int:id>',methods=['GET', 'POST'])
def editFix(id):
    if request.method == 'GET':
        fix = Fix.query.get_or_404(id)
        fixTypes = FixDetail.query.all()
        clientFix = Client.query.get_or_404(fix.idclient)
        return render_template('editare.html', fix=fix, fixTypes=fixTypes, client=clientFix)
    else:
        fix_detail,extracost,fixType = getFixFormData()
        client_name,client_prenume,client_phone,client_email = getClientFormData()

        try:
            #new_client = Client(firstName=client_name, lastName=client_prenume, phone=client_phone, email=client_email)
            fixfromdb = Fix.query.get_or_404(id)
            new_client = Client.query.get_or_404(fixfromdb.idclient)

            if client_name:
                new_client.firstName = client_name
            if client_prenume:
                new_client.lastName = client_prenume
            if client_phone:
                new_client.phone = client_phone
            if client_email:
                new_client.email = client_email
            if fix_detail:
                fixfromdb.description = fix_detail
            if extracost:
                fixfromdb.extra_cost = extracost

            fixTypeObj = FixDetail.query.filter_by(title=fixType).first()
            fixTypeObj.fixes.append(fixfromdb)
            new_client.fixes.append(fixfromdb)

            db.session.commit()
            return redirect('/')
        except:
            return 'Problema cu reparatia editata. Contactati suport IT'

@views.route('/completare/<int:id>')
def completeFix(id):
    try:
        fixfromdb = Fix.query.get_or_404(id)
        fixfromdb.completed = 1
        db.session.commit()
        return redirect('/')
    except:
        return 'Problema la terminarea reparatiei . Contactati suport IT'

@views.route('/necompletare/<int:id>')
def incompleteFix(id):
    try:
        fixfromdb = Fix.query.get_or_404(id)
        fixfromdb.completed = 0
        db.session.commit()
        return redirect('/')
    except:
        return 'Problema la terminarea reparatiei . Contactati suport IT'

