#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import smtplib
import pymysql

# Deixar estes parâmetros, via MACRO / Template
max_load = 10
DB_HOST='10.x.x.x'
DB_NAME='mysql'
DB_USER='mysql_user'
DB_PASS='mysql_pass'
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT = 587
LOGIN="user@gmail.com"
SENHA="gmailpass"
EMAIL_DST=['user1@domain.com','user2@domain.com']
EMAIL_SUB="Problemas no processamento do servidor Mysql do cliente"
LIMIT_MYSQL_CON=100
LIMIT_MYSQL_TIME=60

def db_init():
    conn = pymysql.connect(host=DB_HOST,port=3306,user=DB_USER,passwd=DB_PASS,db=DB_NAME,cursorclass=pymysql.cursors.DictCursor)
    return conn

def get_idle_workers():
    #/usr/sbin/apachectl status|grep -Eo '[0-9].+.*idle workers'|sed 's/^.* \([0-9]\+\) idle workers/\1/'

def get_mysql_processlist(conn):
    print 'Verificando processos no banco'
    query2 = "show full processlist";
    k = conn.cursor()
    k.execute(query2)
    y = k.fetchall()
    return y

def send_email(msg):
    try :
        for dst in EMAIL_DST :
            print 'Enviando email para %s ' % (dst)
            subject = EMAIL_SUB
            body = msg
            headers = ["From: " + LOGIN,
                       "Subject: " + EMAIL_SUB,
                       "To: " + dst,
                       "MIME-Version: 1.0",
                       "Content-Type: text/html"]
            headers = "\r\n".join(headers)

            session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

            session.ehlo()
            session.starttls()
            session.ehlo
            session.login(LOGIN, SENHA)

            session.sendmail(LOGIN, dst, headers + "\r\n\r\n" + msg)
            session.quit()
    except Exception, e :
        print '    Erro ao conectar-se no servidor SMTP %s' % (SMTP_SERVER)
        print e

def get_load() :
    load=open('/proc/loadavg','r').readlines()
    print 'Pegando informacoes de processamento do servidor'
    #return float('11.1')
    return float(load[0].split()[0])

def get_html(data):
    result = []
    processos = []
    html = []
    html.append('<h1> Processos Mysql </h1>')
    html.append('<table boder=1">')
    html.append('<tr bgcolor=#ccc>')
    for i in data[0].keys() :
        html.append('<th>%s</th>' % i)
    html.append('</tr>')
    for line in data:
        html.append('<tr style="font-size=10pt;">')
        for k in line.keys() :
            html.append('<td>%s</td>' % line[k])
        html.append('</tr>')
    html.append('</table>')
    return ''.join(html)

def mata_processo_mysql(conn,data) :
    processos = []
    for line in data:
        if line['Id'] != 'show processlist' and line['Command'] == 'Execute' and line['Time'] > LIMIT_MYSQL_TIME :
            processos.append(line['Id'])
    cur = conn.cursor()
    for pid in processos :
        query = 'kill %s' % (pid);
        try:
             print 'QUERY: %s ' % query
             #ret = cur.execute(query)
        except :
             pass
    cur.close()

if __name__ == '__main__'  :
    db = db_init()
    myprocs = get_mysql_processlist(db)
    nmyprocs = len(myprocs)
    laverage =  get_load()
    print '   Load: %2.f%%' % (laverage)
    if laverage > max_load or nmyprocs > LIMIT_MYSQL_CON :
        print '    Status: ALTO'
        send_email(get_html(myprocs))
        mata_processo_mysql(db,myprocs)
    else :
        print 'Tudo certo!'
