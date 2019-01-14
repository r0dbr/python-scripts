#!/usr/bin/python

from sys import argv
import sys
import subprocess
from time import sleep

dir_configs='/etc/openvpn'
dir_keys='%s/clients-keys' % (dir_configs)
dir_export='/home/chaves_clientes'
arquivo = open(dir_configs + '/openvpn-cliente.orig','r').readlines()


def generate_cert(chave):
    p1 = subprocess.Popen(["/etc/openvpn/build-key",chave], stdout=subprocess.PIPE,stdin=subprocess.PIPE,cwd=r'/etc/openvpn')
    dados = ["BR\n","PR\n","Curitiba\n","Procyon\n","Procyon\n",chave+"\n","suporte@procyon.com.br\n","\n","\n","y\n","y\n"]
    for i in dados :
        print i
        sleep(0.2)
        p1.stdin.write(i)
    p1.wait()
    ret = p1.poll()

    if ret == 0 :
        print 'CERTIFICADO CRIADO COM SUCESSO!!!'
    else :
        print 'ERRO AO CRIAR CERTIFICADO'
    return ret

def get_ca():
    cert = open('%s/ca.crt' % (dir_keys) ).readlines()
    copy = False
    out = ''
    for line in cert:
        if line.strip() == '-----BEGIN CERTIFICATE-----' :
            copy = True
            out += line
        elif line.strip() == '-----END CERTIFICATE-----':
            copy = False
            out += line
        elif copy:
            out += line
    return out

def get_cert(chave):
    cert = open('%s/%s.crt' % (dir_keys,chave)).readlines()
    copy = False
    out = ''
    for line in cert:
        if line.strip() == '-----BEGIN CERTIFICATE-----' :
            copy = True
            out += line
        elif line.strip() == '-----END CERTIFICATE-----':
            copy = False
            out += line
        elif copy:
            out += line
    return out


def gera_config(chave):
    saida = ""
    KEY = open('%s/%s.key' % (dir_keys,chave)).read()
    CERT = get_cert(chave)
    CA = get_ca()
    #Certificado digital do cliente + chave
    print 'Gerando a configuracao da chave %s em %s/%s.ovpn' % (chave,dir_export,chave)
    for linha in arquivo :
        linha = linha.replace('\n','')
        if linha == '##CERT##' :
            saida+=CERT
        elif linha == '##KEY##' :
            saida+=KEY
        elif linha == '##CA##' :
            saida+=CA
        else :
            saida+='%s\n' % (linha)
    x = open('%s/%s.ovpn' % (dir_export,chave),'w+')
    print '\n'
    print '\n'
    print '+----------------------------------------------------------+'
    print '+   Configuracao criada em: %s/%s.ovpn' % (dir_export,chave)
    print '+----------------------------------------------------------+'
    print '\n'
    print '\n'
    x.write(saida)
    x.close()



def main() :
    try :
        chave = argv[1]
    except :
        print 'Voce precisa passar o nome de uma chave como parametro'
        sys.exit(1)
    ret = generate_cert(chave)
    gera_config(chave)

if __name__ == '__main__' :
    main()
