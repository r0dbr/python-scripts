#!/usr/bin/python
import smtplib
import imaplib
import poplib
import sys

print 'Starting mail test'

try :
    recipient = sys.argv[1]
except :
    recipient = 'recipient@test.com'

# Server configurations
IMAP_SERVER="mail.domain.com"
POP_SERVER="mail.domain.com"
POP_PORT=110
SMTP_SERVER="mail.domain.com"
SMTP_PORT = 587
MAIL_FROM = 'user@domain.com'
FROM = 'user@domain.com'
LOGIN = 'user@domain.com'
SENHA = 'password'


def imap_test():
    try :
        print '* Testing your IMAP connection:'
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(LOGIN, SENHA)
        mail.list()
        print '    Nice! Everytihing is OK with you server and credentials'
        print mail.select("inbox") 
    except :
        print '    Fail to connect on your IMAP  server %s' % (IMAP_SERVER)


def pop3_test():    

    try:
        print '* Testing your POP3 connection:'
        M = poplib.POP3(POP_SERVER)
        M.user(LOGIN)
        M.pass_(SENHA)
        print '    Nice! There is %d messages on your server %s ' % (len(M.list()[1]),POP_SERVER)
    except :
        print '    Oh Oh! Error trying to connect on your POP3 server %s' % (POP_SERVER)

def pop3ssl_test():    

    try:
        print '* Testando conexao POP3 SSL:'
        M = poplib.POP3_SSL(POP_SERVER)
        print M.getwelcome()
        M.user(LOGIN)
        M.pass_(SENHA)
        print '    Nice! There is %d messages on your server %s ' % (len(M.list()[1]),POP_SERVER)
    except :
        print '    Oh Oh! Error trying to connect on your POP3 server %s' % (POP_SERVER)

def smtp_test():     
    print '* Testing SMTP connection to %s ' % (recipient)
    subject = 'SMTP Test'
    body = 'blah blah blah'
     
    "Sends an e-mail to the specified recipient."
     
    body = "" + body + ""
     
    headers = [
               "MAIL FROM:  " + MAIL_FROM,
               "RCPT TO: " + recipient,
               "From: %s <%s>" % ('Nao responda', FROM),
               "Subject: " + subject,
               "To: " + recipient,
               "MIME-Version: 1.0",
               "Content-Type: text/html"]
    headers = "\r\n".join(headers)
     
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
     
    session.ehlo()
    session.starttls()
    session.login(LOGIN, SENHA)
    session.sendmail(MAIL_FROM, recipient, headers + "\r\n\r\n" + body)
    session.quit()

if __name__ == '__main__':
    pop3_test()
    pop3ssl_test()
    imap_test()
    smtp_test()

