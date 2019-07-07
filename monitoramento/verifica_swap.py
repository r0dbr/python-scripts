#!/usr/bin/python

import subprocess


class get_memory():

   def __init__(self):
       self.swap_total=0.0
       self.swap_free=0.0
       self.swap_percent_usage=0.0
       self.get_swap()

   def get_swap(self):
       meminfo=open('/proc/meminfo','r').readlines()
       for line in meminfo:
           l=line.split()
           if l[0] == 'SwapTotal:' :
               self.swap_total = float(l[1])
           elif l[0] == 'SwapFree:' :
               self.swap_free = float(l[1])
       self.swap_percent_usage = round((self.swap_total-self.swap_free)/self.swap_total*100)


def execute(cmd):

    p = subprocess.Popen(cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
    stdout,stderr = p.communicate()
    return(stdout,stderr)

def main():
    m = get_memory()
    if m.swap_percent_usage > 10.0:
        print 'Reiniciando PHP 5.6...'
        print execute(['/usr/sbin/service','rh-php56-php-fpm','reload'])[0]
        print 'Limpando o Swap'
        print execute(['/usr/sbin/swapoff','-a'])[0]
        print execute(['/usr/sbin/swapon','-a'])[0]
        print 'Feito!'

if __name__ == '__main__' :

    main()
