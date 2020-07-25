import smtplib, sys, re
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
def add(email, password, aname):
    if not (re.search(regex,email)):
            print("Invalid Email")
            sys.exit()
    file = open(aname + '.txt', 'w')
    file.write(email)
    file.close()
    filep = open(aname + 'password.txt', 'w')
    filep.write(password)
    filep.close()
def send(aname, emailr, subject, body):
    if not (re.search(regex,emailr)):  
        print("Invalid Email")  
        sys.exit()
    try:
        fileo = open(aname + '.txt')
        email = fileo.read()
        fileop = open(aname + 'password.txt')
        password = fileop.read()
    except:
        print('Error getting credentials')
    if '@gmail.com' in email:
        smtpserver = 'smtp.gmail.com'
    elif '@icloud.com' in email:
        smtpserver = 'smtp.mail.me.com'
    elif '@outlook.com' in email:
        smtpserver = 'smtp.live.com'
    elif '@hotmail.com' in email:
        smtpserver = 'smtp.live.com'
    elif '@msn.com' in email:
        smtpserver = 'smtp.live.com'
    elif '@yahoo.com' in email:
        smtpserver = 'smtp.mail.yahoo.com'
    else:
        print('Email provider not yet supported')
        sys.exit()
    smtpObj = smtplib.SMTP(smtpserver, 587)
    smtpObj.starttls()
    smtpObj.ehlo()
    try:
        smtpObj.login(email, password)
    except:
        print('Login Error')
        sys.exit()
    smtpObj.sendmail(email, emailr, (f'Subject: {subject}\n{body}'))
def text(aname, receive, carrier, subject, body):
    try:
        fileo = open(aname + '.txt')
        email = fileo.read()
        fileop = open(aname + 'password.txt')
        password = fileop.read()
    except:
        print('Error getting credentials')
    if '@gmail.com' in email:
        smtpserver = 'smtp.gmail.com'
    elif '@icloud.com' in email:
        smtpserver = 'smtp.mail.me.com'
    elif '@outlook.com' in email:
        smtpserver = 'smtp.live.com'
    elif '@hotmail.com' in email:
        smtpserver = 'smtp.live.com'
    elif '@msn.com' in email:
        smtpserver = 'smtp.live.com'
    elif '@yahoo.com' in email:
        smtpserver = 'smtp.mail.yahoo.com'
    else:
        print('Email provider not yet supported')
        sys.exit()
    if carrier.lower() == 'verizon':
        carrier = '@vtext.com'
    elif carrier.lower() == 'at&t':
        carrier = '@txt.att.net'
    elif carrier.lower() == 'sprint':
        carrier = '@messaging.sprintpcs.com'
    elif carrier.lower() == 't-mobile':
        carrier = '@tmomail.net'
    else :
        print('Carrier not listed YET')
        sys.exit()
    receive = receive + carrier
    smtpObj = smtplib.SMTP(smtpserver, 587)
    smtpObj.starttls()
    smtpObj.ehlo()
    try:
        smtpObj.login(email, password)
    except:
        print('Error logging in')
        sys.exit()
    smtpObj.sendmail(email, receive, (f'Subject: {subject}\n{body}'))
    
    
    
    
            
