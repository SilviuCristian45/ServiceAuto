from flask import Blueprint,render_template, request, redirect,flash
from flask_login import login_user,login_required,logout_user,current_user
from .models import *
from website import photos,cv

views = Blueprint('views',__name__)

def getFixFormData():
    return request.form['fixdetails'],request.form['extracost'],request.form['fixesTypes']

def getClientFormData():
    return request.form['nume'],request.form['prenume'],request.form['nrtelefon'],request.form['email']

@views.route('/',methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'GET':
        fixes = Fix.query.filter_by(completed=0,iduser=current_user.id).all()
        return render_template('index.html', fixes=fixes)

@views.route('/reparatiiterminate',methods=['GET', 'POST'])
@login_required
def solved_fixes():
    fixes_comp = Fix.query.filter_by(completed=1,iduser=current_user.id)
    return render_template('reparatiiterminate.html', fixes_completed=fixes_comp)

@views.route('/adaugareparatie',methods=['GET','POST'])
@login_required
def add_fix():
    if request.method == 'GET':
        fixeTypes = FixDetail.query.filter_by(iduser=current_user.id).all()
        return render_template('adaugareparatie.html', fixTypes=fixeTypes)
    else:
        fix_detail, extracost, fixType = getFixFormData()
        client_name, client_prenume, client_phone, client_email = getClientFormData()
        idclient = request.form['idclient']
        employees_ids = request.form['idemployees'].split(' ')
        if not idclient:
            new_client = Client(firstName=client_name+" ", lastName=client_prenume+" ", phone=client_phone, email=client_email+" ",iduser=current_user.id)
        else:
            new_client = Client.query.get(idclient)
        new_fix = Fix(extra_cost=extracost, description=fix_detail,iduser=current_user.id)
        for employee_id in employees_ids:
            new_fix.employees.append(Employee.query.get_or_404(employee_id))
        # image handling
        if 'image' in request.files:
            filename = photos.save(request.files['image'])
            new_fix.image_path = filename

        fixTypeObj = FixDetail.query.filter_by(title=fixType,iduser=current_user.id).first()
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
@login_required
def addFixType():
    if request.method == 'GET':
        return render_template('adaugaretipreparatie.html')
    else:
        typeFixTitle = request.form['title']
        typeFixCost = request.form['cost']
        try:
            newFixType = FixDetail(title=typeFixTitle, cost=typeFixCost,iduser=current_user.id)
            db.session.add(newFixType)
            db.session.commit()
            return redirect('/')
        except:
            return 'Problema la adaugarea tipului de reparatie '

@views.route('/cautareincomplete/<int:flag>',methods=['GET','POST'])
@login_required
def findFix(flag):
    if request.method == 'POST':
        what_to_find = request.form['cautare_reparatie']
        fixes = Fix.query.filter_by(iduser=current_user.id).all()
        result = []
        for fix in fixes:
            if what_to_find in fix.description and fix.completed == flag:
                result.append(fix)
        return render_template('reparaticautate.html', fixDescription=result)

@views.route('/client/<int:id>')
@login_required
def clientDetails(id):
    client = Client.query.get_or_404(id)
    return render_template('client.html', client=client)

@views.route('/tip-reparatie/<int:id>')
@login_required
def serviceDetails(id):
    service = FixDetail.query.get_or_404(id)
    return render_template('tip-reparatie.html', service=service)

@views.route('/stergere/<int:id>')
@login_required
def deleteFix(id):
    try:
        Fix.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect('/')
    except:
        return 'Nu se poate face stergerea acestei reparatii . '

@views.route('/editare/<int:id>',methods=['GET', 'POST'])
@login_required
def editFix(id):
    if request.method == 'GET':
        fix = Fix.query.get_or_404(id)
        fixTypes = FixDetail.query.filter_by(iduser=current_user.id).all()
        clientFix = Client.query.get_or_404(fix.idclient)
        return render_template('editare.html', fix=fix, fixTypes=fixTypes, client=clientFix)
    else:
        fix_detail,extracost,fixType = getFixFormData()
        image_path = request.files['image']
        client_name,client_prenume,client_phone,client_email = getClientFormData()
        client_id = request.form['idclient']
        employees_ids = request.form['idemployees'].split(" ")
        try:
            new_client = Client(firstName=client_name, lastName=client_prenume, phone=client_phone, email=client_email)
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
            if client_id:
                fixfromdb.idclient = client_id
            if employees_ids:
                fixfromdb.employees.clear()
                for employees_id in employees_ids:
                    fixfromdb.employees.append(Employee.query.get_or_404(employees_id))
            if fix_detail:
                fixfromdb.description = fix_detail
            if extracost:
                fixfromdb.extra_cost = extracost
            if image_path:
                fixfromdb.image_path = photos.save(image_path)

            fixTypeObj = FixDetail.query.filter_by(title=fixType).first()
            fixTypeObj.fixes.append(fixfromdb)
            new_client.fixes.append(fixfromdb)

            db.session.commit()
            return redirect('/')
        except:
            return 'Problema cu reparatia editata. Contactati suport IT'

@views.route('/completare/<int:id>')
@login_required
def completeFix(id):
    try:
        fixfromdb = Fix.query.get_or_404(id)
        fixfromdb.completed = 1
        db.session.commit()
        return redirect('/')
    except:
        return 'Problema la terminarea reparatiei . Contactati suport IT'

@views.route('/necompletare/<int:id>')
@login_required
def incompleteFix(id):
    try:
        fixfromdb = Fix.query.get_or_404(id)
        fixfromdb.completed = 0
        db.session.commit()
        return redirect('/')
    except:
        return 'Problema la terminarea reparatiei . Contactati suport IT'

@views.route('/clienti',methods=['GET', 'POST'])
@login_required
def viewClients():
    if request.method == 'GET':
        clients = Client.query.filter_by(iduser = current_user.id)
        return render_template('clienti.html',clients = clients)
    else:
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        if not email:
            email = " "
        if not firstname:
            firstname = " "
        if not lastname:
            lastname = " "
        clients = Client.query.filter(Client.email.contains(email)).filter(Client.firstName.contains(firstname)).filter(
            Client.lastName.contains(lastname)).filter_by(iduser=current_user.id).all()
        return render_template('clienti.html', clients=clients)

@views.route('/tipurireparatii',methods=['GET','POST'])
@login_required
def viewFixTypes():
    fixTypes = FixDetail.query.filter_by(iduser=current_user.id).all()
    return render_template('tipurireparatii.html',fixTypes=fixTypes)

@views.route('/fotografie/<string:image>')
@login_required
def viewImage(image):
    return render_template('fotografiemasina.html',image=image)

@views.route('/angajati',methods=['GET','POST'])
@login_required
def viewEmployees():
    if request.method == 'GET':
        employees = Employee.query.filter_by(iduser=current_user.id)
        return render_template('angajati.html',employees=employees)
    firstNamesearch = request.form['firstname']
    lastNamesearch = request.form['lastname']
    print(firstNamesearch+" "+lastNamesearch)
    employees = Employee.query.filter(Employee.firstName.contains(firstNamesearch)).filter(Employee.lastName.contains(lastNamesearch))
    return render_template('angajati.html',employees=employees)

@views.route('/adaugaangajat',methods=['GET','POST'])
@login_required
def addEmployee():
    if request.method == 'GET':
        return render_template('adaugareangajat.html')
    firstName = request.form['nume']
    lastName = request.form['prenume']
    phone = request.form['nrtelefon']
    role = request.form['rol']
    try:
        cv_path = cv.save(request.files['cv'])
    except:
        return '<h1> Eroare la adaugarea angajatului ! Incarcati un document cu extensiile cerute </h1>'
    try:
        new_employee = Employee(firstName=firstName,lastName=lastName,phone=phone,cv=cv_path,role=role,iduser=current_user.id)
        db.session.add(new_employee)
        db.session.commit()
        return redirect('/angajati')
    except:
        return '<h1> Eroare la adaugarea angajatului ! Contactati suport IT </h1>'

@views.route('/angajati/<int:id>')
@login_required
def viewEmployeesOnFix(id):
    fix = Fix.query.get_or_404(id)
    return render_template('angajati.html',employees=fix.employees)

@views.route('/angajat/<int:id>')
@login_required
def viewFixesOnEmployee(id):
    employee = Employee.query.get_or_404(id)
    return render_template('reparaticautate.html',fixDescription=employee.fixes)