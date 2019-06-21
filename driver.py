#           IMPORTS
from datetime import datetime
import socket
import ssl
from urllib.parse import urlparse
import urllib.request, urllib.error
from email.message import EmailMessage
import smtplib

#           CONSTANTS
BUFFER = 70
port = 443
# As of now, the SMTP that is being used is GMAIL, however with small edits one can change that
FRMADDR = ""#ADDRESS OF EMAIL THAT YOU WANT REMINDER SENT
PWD = ""#PASSWORD OF THE EMAIL THAT YOU WANT REMINDER SENT FROM
TOADDR = ""#ADDRESS OF EMAIL THAT YOU WANT REMINDER SENT TO

sites = ['https://expired.badssl.com','https://self-signed.badssl.com/','https://badssl.com','https://google.com','https://github.com','https://alfonso.github.io','https://github.com','https://www.instagram.com/fonz15/']

#           FUNCTIONS
def email(subject,body):

    msg = EmailMessage()
    msg['Subject'] = subject + " - SSL monitoring"
    msg['From'] = FRMADDR
    msg['To'] = TOADDR
    msg.add_header('Content-Type','text/html')
    msg.set_payload(body)

    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.login(FRMADDR,PWD)
        s.sendmail(msg['From'], [msg['To']], msg.as_string())
    except Exception as e:
        print('failed')
    return


def checkSSL(hostname):
    o = urlparse(hostname)
    netloc = o.netloc

    context = ssl.create_default_context()

    try:
        conn = context.wrap_socket(socket.socket(socket.AF_INET),server_hostname=netloc)
        conn.connect((netloc, 443))
    #except ssl.SSLError as e:
    except ssl.SSLCertVerificationError
    # python 3.7 allows the use of ssl.SSLCertVerificationError to be more specific
    # As for now, any of the subclasses of ssl.SSLError can activate this except block
        return 2
    except Exception as err:
        print('error: ',err)
        print('Please make sure the urls are inputted correctly')
        exit()

    cert = conn.getpeercert()
    expire = cert['notAfter']
    date_time_obj = datetime.strptime(expire, '%b %d %H:%M:%S %Y %Z')
    delta = date_time_obj - datetime.now()

    if delta.days <= BUFFER:
        return 1
    return 0

#           BODY
badCerts = list()
warningCerts = list()

for name in sites:
    check = checkSSL(name)
    if check == 1:
        warningCerts.append(name)
    elif check == 2:
        badCerts.append(name)

badMes = ''
warnMes = ''

for name in badCerts:
    badMes += name + '<br>'
email('[CRITICAL SSL WARNING]','CRITICAL WARNING! SSl Certificate has expired. Action required!<br>'+badMes)

for name in warningCerts:
    warnMes += name + '<br>'
email('[SSL Reminder]','Your SSL Certificate for the below sites expire soon. Please take action.<br>'+warnMes)
