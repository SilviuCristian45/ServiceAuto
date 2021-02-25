from email.message import EmailMessage
import hashlib,smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MAIL = "silviu.dinca20@gmail.com"
PASSW = "23SDFFFxx323"

#input :  plaintext - string - the text we want to hash
#output : result : string - the unique hash specific to input
def encryptText(plaintext):
    result = hashlib.sha1(plaintext.encode('utf-8'))
    return result.hexdigest()

#input :  None
#output : result : a SMTP object
def initMailServer():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(MAIL, PASSW)
    return server

#input :  subject : stirng
#         fromm : string email address
#         to   : string email address
#         content : string
#         html : string
#output : result : a SMTP object
def createEmailObject(subject,fromm,to,content,html="<h1> No value </h1>"):
    result = EmailMessage()
    result['subject'] = subject
    result['from'] = fromm
    result['to'] = to
    res_content = '<h1>' + content + '</h1>'
    result.set_content(res_content,subtype='html')
    return result

#input :  subject : stirng
#         fromm : string email address
#         to   : string email address
#         content : string
#         html : string
#output : result : a SMTP object containing a link
def createMIMEobject(subject,to,content,html="<h1>x</h1>"):
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = MAIL
    msg['To'] = to
    # Create the body of the message (a plain-text and an HTML version).
    text = content
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    return msg