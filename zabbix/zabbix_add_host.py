#!/usr/bin/env python
# -*- coding: utf-8 -*-

#author: Rodrigo C. Carvalho - http://rodbr.com

from zabbix_api import ZabbixAPI
import requests
import subprocess

# Server Configuration
zabbix_host="http://monitor.company.com"
zabbix_server="monitor.company.com"
zabbix_user="username"
zabbix_password="password"
ip = "host-ip-address"
hostname = "hostname"
zapi = ZabbixAPI(server=zabbix_host)
zapi.login(zabbix_user, zabbix_password)
zbx_config_file = '/etc/zabbix/zabbix_agentd.conf'


def restart_service(name):
    command = ['/usr/sbin/service', name, 'restart'];
    #shell=FALSE for sudo to work.
    subprocess.call(command, shell=False)

def cadastra_host(hostname,ip):
    print "Cadastrando host %s com %s" % (hostname,ip)
    hostcriado = zapi.host.create({
        "host": hostname,
        "status": 0,
        "interfaces": [{"type": 1,"main": 1,"useip": 1,"ip": ip,"dns": "","port": 10050}],
        "groups": [{"groupid": 296}],
        "templates": [{"templateid": 10676}]
    })

def configura_zabbix(hostname):
    zbx_config = """PidFile=/var/run/zabbix/zabbix_agentd.pid
LogFile=/var/log/zabbix-agent/zabbix_agentd.log
LogFileSize=0
Server=%s
ServerActive=%s
Hostname=%s
Include=/etc/zabbix/zabbix_agentd.conf.d/*.conf
""" % (zabbix_server,zabbix_server,hostname)

    f = open(zbx_config_file,"w+")
    f.write(zbx_config)
    f.close()

def main():
    cadastra_host(hostname,ip)
    configura_zabbix(hostname)
    restart_service('zabbix-agent')

if __name__ == "__main__" :
    main()
