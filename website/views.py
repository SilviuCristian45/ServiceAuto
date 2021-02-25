from flask import Blueprint,render_template, request, redirect,flash,make_response
from flask_login import login_user,login_required,logout_user,current_user
from .models import *
from website import photos,cv
import hashlib,pdfkit,datetime
from . import utils

views = Blueprint('views',__name__)

#input : None
#output : A tuple which contains :  fixdetails : string
#                                   extracost of the fix : double
#                                   fixesType of the fix : string
def getFixFormData():
    return request.form['fixdetails'],request.form['extracost'],request.form['fixesTypes']

#input : None
#output : A tuple which contains :  the client first name : string
#                                   the client last name : double
#                                   the client phone number : string
#                                   the client email : string
def getClientFormData():
    return request.form['nume'],request.form['prenume'],request.form['nrtelefon'],request.form['email']

#input : fixes : a list of Fix objects
#output : priorities : a list of priorities color codes
def getPriorities(fixes):
    priorities = []
    for fix in fixes:
        #if current fix has a priority assigned
        if fix.idpriority:
            priorities.append(Priority.query.get(fix.idpriority).color)
    return priorities

#input : None
#output : the dashboard page where the user can see his fixes
@views.route('/',methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'GET':
        #store the not completed fixes of the current logged user
        fixes = Fix.query.filter_by(completed=0,iduser=current_user.id).all()
        priorities = getPriorities(fixes)
        #return the index.html page and pass to it the fixes list and priorities list
        return render_template('index.html', fixes=fixes,priorities=priorities)

#input : None
#output : the page which contains the completed fix list
@views.route('/reparatiiterminate',methods=['GET', 'POST'])
@login_required
def solved_fixes():
    # store the completed fixes of the current logged user
    fixes_comp = Fix.query.filter_by(completed=1,iduser=current_user.id)
    priorities = getPriorities(fixes_comp)
    return render_template('reparatiiterminate.html', fixes_completed=fixes_comp,priorities=priorities)

#input : None
#output : None - it adds a new fix / (or user if so) into the database
@views.route('/adaugareparatie',methods=['GET','POST'])
@login_required
def add_fix():
    if request.method == 'GET':
        fixeTypes = FixDetail.query.filter_by(iduser=current_user.id).all()
        priorities = Priority.query.all()
        return render_template('adaugareparatie.html', fixTypes=fixeTypes,priorities=priorities)
    else:
        # input : FORM : fix detail : string  fix extracost : float  fix type : string
        fix_detail, extracost, fixType = getFixFormData()
        # input : FORM : client firstNamename : string  client_lastName client_phone : string  client_email : string
        client_name, client_lastName, client_phone, client_email = getClientFormData()
        #get an id of a client directly (if the user entered so)
        idclient = request.form['idclient']
        #get the id's of the employees responsible for the fix
        employees_ids = request.form['idemployees'].split(' ')
        #get the priority of the fix entered by the user
        priorityname = request.form['priority']

        #if the user didnt enter an client id directly
        if not idclient:
            #create a new client in the database
            new_client = Client(firstName=client_name+" ", lastName=client_lastName+" ", phone=client_phone, email=client_email+" ",iduser=current_user.id)
        else:
            #else just get a reference to the client with corresponding id
            new_client = Client.query.get(idclient)

        #create the new fix
        new_fix = Fix(extra_cost=extracost, description=fix_detail,iduser=current_user.id)
        #set the awb based on sha01 on the user's id
        new_fix.awb = utils.encryptText(str(new_fix.iduser))
        #set the priority of the new fix
        new_fix.idpriority = Priority.query.filter_by(name=priorityname).first().id
        #insert the employee's ids in the linking table between employees and fixes
        for employee_id in employees_ids:
            new_fix.employees.append(Employee.query.get_or_404(employee_id))

        #send the awb through email to the client
        with utils.initMailServer() as server:
            message = utils.createEmailObject("Codul awb pentru reparatia ta",utils.MAIL,new_client.email,new_fix.awb)
            server.sendmail(utils.MAIL,new_client.email,message.as_string())

        #if the user entered an image we save it into our server
        if 'image' in request.files:
            filename = photos.save(request.files['image'])
            new_fix.image_path = filename

        #get the fixtype object with the given title
        fixTypeObj = FixDetail.query.filter_by(title=fixType,iduser=current_user.id).first()
        #make linking between added fix and fixType (1 to M)
        fixTypeObj.fixes.append(new_fix)
        # make linking between the client of the fix and fix :))
        new_client.fixes.append(new_fix)

        try:
            #insert a new fix into database
            db.session.add(new_fix)
            #insert the new client (if it already exits it will not be added)
            if not idclient:
                db.session.add(new_client)
            #commit the changes into the database
            db.session.commit()
            #redirect to the fix list
            return redirect('/')
        except:
            return 'Problema cu reparatia adaugata. Contactati suport IT'

#input : None
#output : None - it adds a new fix type in the database
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

#input : flag - a value which decides what type of fixes we find (completed - 0 or incompleted 1 )
#output : html page which contains the list of found fixes
@views.route('/cautareincomplete/<int:flag>',methods=['GET','POST'])
@login_required
def findFix(flag):
    if request.method == 'POST':
        #get the entered description
        what_to_find = request.form['cautare_reparatie']
        #store the fixes list of the curent logged user
        fixes = Fix.query.filter_by(iduser=current_user.id).all()
        priorities = getPriorities(fixes)
        #get the results
        result = []
        for fix in fixes:
            if what_to_find in fix.description and fix.completed == flag:
                result.append(fix)
        return render_template('reparaticautate.html', fixDescription=result,priorities=priorities)

#input : id : integer
#output : the page of coresponding client id
@views.route('/client/<int:id>')
@login_required
def clientDetails(id):
    client = Client.query.get_or_404(id)
    return render_template('client.html', client=client)

#input : id : integer
#output : the page of fix type of corresponding fixtype id
@views.route('/tip-reparatie/<int:id>')
@login_required
def serviceDetails(id):
    service = FixDetail.query.get_or_404(id)
    return render_template('tip-reparatie.html', service=service)

#input : id : int
#output : None : deletes a fix from database
@views.route('/stergere/<int:id>')
@login_required
def deleteFix(id):
    try:
        Fix.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect('/')
    except:
        return 'Nu se poate face stergerea acestei reparatii . '

#input : None
#output : None : edits a fix from database
@views.route('/editare/<int:id>',methods=['GET', 'POST'])
@login_required
def editFix(id):
    if request.method == 'GET':
        #just take some data about the fix in order to display in placeholders in the template
        fix = Fix.query.get_or_404(id)
        fixTypes = FixDetail.query.filter_by(iduser=current_user.id).all()
        clientFix = Client.query.get_or_404(fix.idclient)
        return render_template('editare.html', fix=fix, fixTypes=fixTypes, client=clientFix)
    else:
        #actualy here is the editing part
        fix_detail,extracost,fixType = getFixFormData()
        image_path = request.files['image']
        client_name,client_lastName,client_phone,client_email = getClientFormData()
        client_id = request.form['idclient']
        employees_ids = request.form['idemployees'].split(" ")
        try:
            new_client = Client(firstName=client_name, lastName=client_lastName, phone=client_phone, email=client_email)
            fixfromdb = Fix.query.get_or_404(id)
            new_client = Client.query.get_or_404(fixfromdb.idclient)

            #validations of the fields
            if client_name:
                new_client.firstName = client_name
            if client_lastName:
                new_client.lastName = client_lastName
            if client_phone:
                new_client.phone = client_phone
            if client_email:
                new_client.email = client_email
            if client_id:
                fixfromdb.idclient = client_id
            if employees_ids:
                #delete the currend employee list
                fixfromdb.employees.clear()
                #insert in fix-employee table the employee's ids
                for employees_id in employees_ids:
                    fixfromdb.employees.append(Employee.query.get_or_404(employees_id))
            if fix_detail:
                fixfromdb.description = fix_detail
            if extracost:
                fixfromdb.extra_cost = extracost
            if image_path:
                fixfromdb.image_path = photos.save(image_path)
            #store the fixTypeObject coresponding to given title
            fixTypeObj = FixDetail.query.filter_by(title=fixType).first()
            #make relationship between fix and fixType
            fixTypeObj.fixes.append(fixfromdb)
            #make relationship between client and fix
            new_client.fixes.append(fixfromdb)
            db.session.commit()
            return redirect('/')
        except:
            return 'Problema cu reparatia editata. Contactati suport IT'

#input : id : int - coresponding to the fix that the user wants to complete
#output : None : - it will modify the flag of the selected fix in 1 to mark as completed and update the datetime field
#                - this fix will be displayed in the completed fixes template
@views.route('/completare/<int:id>')
@login_required
def completeFix(id):
    try:
        fixfromdb = Fix.query.get_or_404(id)
        fixfromdb.completed = 1
        fixfromdb.loadDate = datetime.datetime.utcnow()
        db.session.commit()
        return redirect('/')
    except:
        return 'Problema la terminarea reparatiei . Contactati suport IT'

#input : id : int - coresponding to the fix that the user wants to undo the complete
#output : None : - reverse of the above function
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

#input : None
#output : None : a template  which contains the data about the clients of current logged user
@views.route('/clienti',methods=['GET', 'POST'])
@login_required
def viewClients():
    if request.method == 'GET':
        clients = Client.query.filter_by(iduser = current_user.id)
        return render_template('clienti.html',clients = clients)
    else:
        #this is for the search part - in clienti.html there is a form which points to this request
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        #validations
        if not email:
            email = " "
        if not firstname:
            firstname = " "
        if not lastname:
            lastname = " "
        #get the list of the clients with given email,firstname and lastname
        clients = Client.query.filter(Client.email.contains(email)).filter(Client.firstName.contains(firstname)).filter(
            Client.lastName.contains(lastname)).filter_by(iduser=current_user.id).all()
        #render the same template but with only the searched clients
        return render_template('clienti.html', clients=clients)

#input : None
#output : None : displays a template with all fix types
@views.route('/tipurireparatii',methods=['GET','POST'])
@login_required
def viewFixTypes():
    fixTypes = FixDetail.query.filter_by(iduser=current_user.id).all()
    return render_template('tipurireparatii.html',fixTypes=fixTypes)

#input : image path : string
#output : None : displays a template with the image with normal width and heigth
@views.route('/fotografie/<string:image>')
@login_required
def viewImage(image):
    return render_template('fotografiemasina.html',image=image)

#input : None
#output : returns template with all the employees of the user
@views.route('/angajati',methods=['GET','POST'])
@login_required
def viewEmployees():
    if request.method == 'GET':
        employees = Employee.query.filter_by(iduser=current_user.id)
        return render_template('angajati.html',employees=employees)
    #this is for the search part
    #the user cand find his emplyees with a given firstName or lastName
    firstNamesearch = request.form['firstname']
    lastNamesearch = request.form['lastname']
    employees = Employee.query.filter(Employee.firstName.contains(firstNamesearch)).filter(Employee.lastName.contains(lastNamesearch))
    return render_template('angajati.html',employees=employees)

#input : None
#output : GET : returns the form for adding an employee'
#         POST : adds an employee into database
@views.route('/adaugaangajat',methods=['GET','POST'])
@login_required
def addEmployee():
    if request.method == 'GET':
        return render_template('adaugareangajat.html')
    #just store the data from form
    firstName = request.form['nume']
    lastName = request.form['prenume']
    phone = request.form['nrtelefon']
    role = request.form['rol']
    #save the cv document in server's folder
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

#input : id : int : the id of current fix
#output : display the employees working on the selected fix
@views.route('/angajati/<int:id>')
@login_required
def viewEmployeesOnFix(id):
    fix = Fix.query.get_or_404(id)
    return render_template('angajati.html',employees=fix.employees)

#input : id : int : the id of current employee
#output : display the fixes of the selected employee
@views.route('/angajat/<int:id>')
@login_required
def viewFixesOnEmployee(id):
    employee = Employee.query.get_or_404(id)
    return render_template('reparaticautate.html',fixDescription=employee.fixes)

#input : None
#output : GET : returns a template containing the awb code form
#         POST : returns a template containing the fixes of the client based on the given awb
@views.route('/reparatii',methods=['GET','POST'])
def viewFixesOnClient():
    if request.method == 'GET':
        return render_template('reparatiiawb.html')
    awb = request.form['awb']
    fixes = Fix.query.filter_by(awb=awb).all()
    return render_template('reparatiiclient.html',fixes=fixes)

#input : id : the current selected fix
#output : GET : returns a pdf (in a new tab ) containing data of the selected fix
@views.route('/factura/<int:id>')
@login_required
def generateBill(id):
    #store the data we need about the fix
    fix = Fix.query.get_or_404(id)
    fix_client = Client.query.get_or_404(fix.idclient)
    fix_type = FixDetail.query.get_or_404(fix.idfixType)
    #store the rendered html template
    rendered = render_template('factura.html',fix=fix,client=fix_client,fixtype=fix_type)
    #a dictionary needed to generate the pdf
    options = {
        "enable-local-file-access": None
    }
    css = ['website/static/css/pdf.css','website/static/bootstrap/css/bootstrap.min.css']
    pdf = pdfkit.from_string(rendered,False,options=options,css=css)
    #generate the response
    response = make_response(pdf)
    response.headers['content-Type'] = 'application/pdf'
    response.headers['content-Disposition'] = 'inline:filename=factura.pdf'

    return response

#input : None
#output : GET : returns a template containing a form to insert the email needed
#         POST : sends an email to given email
@views.route('/forgotpassword',methods=['GET','POST'])
def generatePassword():
    if request.method == 'GET':
        return render_template('forgotpassword.html')
    email = request.form['mail']
    #create the email
    token = "http://localhost:5000/token/"+utils.encryptText(email)
    link = ("<html>"
               "<head> </head>"
                "<body>"
                 f" <a href={token}> Resetare parola man </a>"
               " </body>"
              "</html>")
    #send the email
    with utils.initMailServer() as server:
         message = utils.createMIMEobject("resetare parola",email,"ab",link)
         server.sendmail(utils.MAIL,email,message.as_string())
    flash("In maxim 5 minute vei primi un email cu un link pentru a putea sa iti resetezi parola.")
    return render_template('login.html')

#input : None
#output : GET : returns a template containing a form to insert the new password
@views.route('/token/<string:cod>')
def forgotPassword(cod):
    users = User.query.all()
    for user in users:
        if utils.encryptText(user.email) == cod:
            return render_template('resetareparola.html',userid=user.id)
    return '<h1> Nu avem acest email in baza de date </h1>'

#input : userid
#output : POST : modifies the password of the user (coresponding to userid)
@views.route('/forgotpassword/<int:userid>',methods=['GET','POST'])
def resetPassword(userid):
    user = User.query.filter_by(id=userid).first()
    pass1 = request.form['password']
    pass2 = request.form['passwordRepeat']
    #if the passwords are matching
    if pass1 == pass2:
        user.password = utils.encryptText(pass1)
        db.session.commit()
        login_user(user,remember=True)
        flash('Parola resetata cu succes')
        return redirect('/')
    #if the passwords doesnt match just redirect to same url
    #in order to give the opportunity to the user to modify again
    flash("Parolele nu corespund")
    return redirect('/forgotpassword/'+str(userid))