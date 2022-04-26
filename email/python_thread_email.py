#!/usr/bin/python3
import smtplib, os, sys
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from html.parser import HTMLParser
from email import encoders
from threading import Thread
from queue import Queue
from random import randrange as rand
from os import listdir
from tkinter import EXCEPTION
from datetime import datetime
import logging
import time


emails_to_send = 1000
ATTACHMENTS = False
NUM_THREADS = 2
LOCALSERVER = False
stop_threads = False

q = Queue()

attachments_dir = './attachments'

logging.basicConfig(filename='sendmail.log', level=logging.DEBUG)



class SendEmail(Thread):

    def __init__(self,name):
        Thread.__init__(self)
        self.name = name
        self.smtp_server = "smtp.sendgrid.net"
        self.smtp_user = 'apikey'
        self.smtp_pass = ''
        self.mail_from = 'Test Spoofing <test.spoofing@mydomain.com>'
        self.mail_to = 'Destination <destination@targetdomain.com>'
        self.mail_subject = 'Spoofing test against MailServer %s ' % (datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
        self.attachments = ""
        self.websites_list = ""
        self.websites_list_len = ""
        try :
            self.attachments = listdir(attachments_dir)
        except :
            pass

    def run(self):
        print('===================================================')
        print('Starting worker %s' % self.name)
        print('===================================================')        
        time.sleep(2)
        self.send()
        print('')        
        print('===================================================')
        print('Ending worker %s' % self.name)
        print('===================================================')                

    
    def send(self,id=""):
        global q

        try:
            while True :
                
                if q.qsize() == 0:
                    break
                website = self.get_compromised_website()
                #website = 'b-triple-t.com/'
                htmlmsgtext = """<h2>Rialto Capital Management!!!!!</h2>
                <p style="font-size=10pt;font-face:arial" >
                Rialto Capital is an integrated investment management and asset management platform, with a dedicated special servicer. Our mission is to be a world-class, industry leading organization that creates long term value for our investors and sustains results across market cycles. </p>
                <p> Click <a href="http://%s">here</a> to by us </p>""" % website            
                # Make text version from HTML - First convert tags that produce a line break to carriage returns
                msgtext = htmlmsgtext.replace('</br>',"\r").replace('<br />',"\r").replace('</p>',"\r")
                # Then strip all the other tags out
                msgtext = self.strip_tags(msgtext)

                # necessary mimey stuff
                msg = MIMEMultipart()
                msg.preamble = 'This is a multi-part message in MIME format.\n'
                msg.epilogue = ''


                body = MIMEMultipart('alternative')
                body.attach(MIMEText(msgtext))
                body.attach(MIMEText(htmlmsgtext, 'html'))
                msg.attach(body)
                qid = "%03d" % q.get()
                if qid != ""  : subj = "%s: %s" % (self.mail_subject, qid)
                else : subj = self.mail_subject
                msg.add_header('From', self.mail_from)
                msg.add_header('To', self.mail_to)
                msg.add_header('Subject', subj)
                msg.add_header('Reply-To', self.mail_from)
                if ATTACHMENTS :
                    if len(self.attachments) > 0: 
                        id = rand(0,len(self.attachments)-1)
                        filename = self.attachments[id]
                        f = "%s/%s" % (attachments_dir,filename)
                        part = MIMEBase('application', "octet-stream")
                        part.set_payload( open(f,"rb").read() )
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
                        msg.attach(part)
                else :
                    filename = '<no file>'
                logging.info('%s - Trying to send email to (%s) with attachment %s and URL %s..' % (qid,self.mail_to,filename,website))
                print('%s - Trying to send email to (%s) with attachment %s and URL %s..' % (qid,self.mail_to,filename,website), end=".")


                # The actual email sendy bits
                try:               
                    if LOCALSERVER :
                        server = smtplib.SMTP('localhost')
                        server.sendmail(msg['From'], [msg['To']], msg.as_string())                            
                    else :
                        server = smtplib.SMTP(self.smtp_server)
                        server.set_debuglevel(False) # set to True for verbose output                            
                        # tls onfiguration
                        server.starttls()
                        server.login(self.smtp_user,self.smtp_pass)

                    server.sendmail(msg['From'], [msg['To']], msg.as_string())
                    #logging.info('Sent')
                    server.quit() # bye bye
                except Exception as e:
                    # if tls is set for non-tls servers you would have raised an exception, so....
                    server.login(self.smtp_user,self.smtp_pass)
                    #server.sendmail(msg['From'], [msg['To']], msg.as_string())
                    #logging.info('Sent')
                    server.quit() # sbye bye
                q.task_done()        
        except Exception as e:
            logging.error(e)
            print(e)
            #print ('Email NOT sent to %s successfully. %s ERR: %s %s %s ', str(self.mail_to), 'tete', str(sys.exc_info()[0]), str(sys.exc_info()[1]), str(sys.exc_info()[2]) )
            #just in case

    def get_compromised_website(self):
        if self.websites_list == '' :
            self.websites_list = open('compromised_websites.txt','r').readlines()
            self.websites_list_len = len(self.websites_list)-1
        website = self.websites_list[rand(0,self.websites_list_len)]
        return website

    def strip_tags(self,html):
        s = MLStripper()
        s.handle_data(html)
        return s.get_data()

class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.fed = []
    
    def __doc__(self):
        print("""
        A snippet - class to strip HTML tags for the text version of the email
        """)
                
    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


if __name__ == "__main__" :

    #m = SendEmail() 

    for n in range(1,int(emails_to_send)+1) : q.put(n)

    worker1 = SendEmail('Thread 1')
    worker2 = SendEmail('Thread 2')
    worker3 = SendEmail('Thread 3')
    worker4 = SendEmail('Thread 4')
    worker5 = SendEmail('Thread 5')

    worker1.start()
    worker2.start()
    worker3.start()
    worker4.start()
    worker5.start()

    worker1.join()
    worker2.join()
    worker3.join()
    worker4.join()
    worker5.join()
