#!/usr/bin/python
# -*- coding: utf-8 -*-

import redis
import smtplib

SERVER = "10.1.1.10" #Redis ip address
TOTAL_LIMIT = 150   #Connection limit total
SERVER_LIMIT = 100  #Connection limit by client
RECIPIENT='support@domain.com'
SMTP_SERVER="email-smtp.us-east-1.amazonaws.com"
SMTP_PORT = 587
MAIL_FROM = 'monitor@company.com'
FROM = 'monitor@company.com'
LOGIN = '' #SMTP USER
SENHA = '' #SMTP PASS
STATUS = {}

def send_email(msg_body):
        subject = 'Problemas com Redis Fael'
        body = ''
        body = "" + msg_body + ""

        headers = [
                   "MAIL FROM:  " + MAIL_FROM,
                   "RCPT TO: " + RECIPIENT,
                   "From: %s <%s>" % ('Monitoramento Wsu', FROM),
                   "Subject: " + subject,
                   "To: " + RECIPIENT,
                   "Content-Type: text/html"]
        headers = "\r\n".join(headers)

        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

        session.ehlo()
        session.starttls()
        session.login(LOGIN, SENHA)
        session.sendmail(MAIL_FROM, RECIPIENT, headers + "\r\n\r\n" + body)
        session.quit()

def kill_conn(conn,client_list):
    for i in client_list :
        killed_conn = 0
        if (len(client_list[i]) > SERVER_LIMIT) :
            print 'Numero de conexoes excedidas para o servidor %s' % (i)
            for port in client_list[i] :
                ip_port = '%s:%s' % (i,port)
                print 'Matando conexão %s' % (ip_port)
                #conn.client_kill(ip_port)
                killed_conn += 1
        if ( killed_conn == 0 ) :
            STATUS[i]='Nenhuma conexão foi morta neste servidor'
        else :
            STATUS[i]='%d conexões foram mortas neste servidor' % (killed_conn)

def get_list():
    clients = {}
    for i in rs_list:
        ip = i['addr'].split(':')[0]
        port = i['addr'].split(':')[1]
        if ip in clients.keys() :
            clients[ip].append(port)
        else :
            clients[ip] = [port]
    return clients

def format_connections(client_list):
    res = []
    for i in client_list.keys():
        res.append('IP: %s  com  %s conexoes nas portas: %s' % (i,len(client_list[i]),', '.join(client_list[i])) )
    return res

def format_email(client_list):
    body = ''
    body += '<br><h1>Conexoes no Redis</h1><br>'
    body+= '<br><br><br>O servidor esta com %d conexoes<br>' % (nconn)
    body+= 'O limite de conexoes total é de: %s<br>' % (TOTAL_LIMIT)
    body+= 'O limite de conexoes por servidor é de: %s <br><br><br>' % (SERVER_LIMIT)
    body += '<table border=1>'
    body += '<thead><tr bgcolor="#cccccc"><th>CONEXOES</th><th>IP</th><th>PORTAS</th><th>STATUS</th><tr></thead><tbody>'
    for i in client_list.keys():
        body += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (len(client_list[i]),i,'|'.join(client_list[i]),STATUS[i])
    body += '<tbody></table>'
    return body

if __name__ == '__main__' :

    rs = redis.Redis(SERVER)
    rs_list = rs.client_list()
    nconn = len(rs_list)

    if nconn > TOTAL_LIMIT :
        c = get_list()
        kill_conn(rs,c)
        body = format_email(c)
        send_email(body)
        for i in format_connections(c):
            print i

