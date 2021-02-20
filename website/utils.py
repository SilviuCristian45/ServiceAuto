from email.message import EmailMessage
import hashlib,smtplib

MAIL = "silviu.dinca20@gmail.com"
PASSW = "23SDFFFxx323"

#input :  plaintext - string - the text we want to hash
#output : result : string - the unique hash specific to input
def encryptText(plaintext):
    result = hashlib.sha1(plaintext.encode('utf-8'))
    return result.hexdigest()

def initMailServer():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(MAIL, PASSW)
    return server

def createEmailObject(subject,fromm,to,content):
    result = EmailMessage()
    result['subject'] = subject
    result['from'] = fromm
    result['to'] = to
    html = '<h1>' + content + '</h1>'
    result.set_content(html,subtype='html')
    return result