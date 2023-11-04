import socket
import ipcalc,re
import threading


bg=''

G = bg+'\033[32m'
O = bg+'\033[33m'
GR = bg+'\033[37m'
R = bg+'\033[31m'

print(O+'''
\tWEBSOCKET SCANNER
\tBy : DHOOM
'''+GR)

ipranges={"CLOUDFRONT_GLOBAL_IP_LIST": ["52.85.0.0/24"],
 "CLOUDFRONT_REGIONAL_EDGE_IP_LIST": ["13.113.196.64/26", "13.113.203.0/24", "52.199.127.192/26", "13.124.199.0/24", "3.35.130.128/25", "52.78.247.128/26", "13.233.177.192/26", "15.207.13.128/25", "15.207.213.128/25", "52.66.194.128/26", "13.228.69.0/24", "52.220.191.0/26", "13.210.67.128/26", "13.54.63.128/26", "99.79.169.0/24", "18.192.142.0/23", "35.158.136.0/24", "52.57.254.0/24", "13.48.32.0/24", "18.200.212.0/23", "52.212.248.0/26", "3.10.17.128/25", "3.11.53.0/24", "52.56.127.0/25", "15.188.184.0/24", "52.47.139.0/24", "18.229.220.192/26", "54.233.255.128/26", "3.231.2.0/25", "3.234.232.224/27", "3.236.169.192/26", "3.236.48.0/23", "34.195.252.0/24", "34.226.14.0/24", "13.59.250.0/26", "18.216.170.128/25", "3.128.93.0/24", "3.134.215.0/24", "52.15.127.128/26", "3.101.158.0/23", "52.52.191.128/26", "34.216.51.0/25", "34.223.12.224/27", "34.223.80.192/26", "35.162.63.192/26", "35.167.191.128/26", "44.227.178.0/24", "44.234.108.128/25", "44.234.90.252/30"] }
 
 
frstarray=ipranges["CLOUDFRONT_GLOBAL_IP_LIST"]
secondarray=ipranges["CLOUDFRONT_REGIONAL_EDGE_IP_LIST"]
	

def scanner(host):
	sock=socket.socket()
	sock.settimeout(5)
	try:
		sock.connect((str(host),80))
		payload='GET / HTTP/1.1\r\nHost: {}\r\n\r\n'.format(host)
		sock.send(payload.encode())
		response=sock.recv(1024).decode('utf-8','ignore')
		for data in response.split('\r\n'):
			data=data.split(':')
			if re.match(r'HTTP/\d(\.\d)?' ,data[0]):
				print('response status : {}{}{}'.format(O,data[0],GR))
			if data[0]=='Server':
				try:
					if data[1] ==' CloudFront':
						print('{}server : {}\nFound working {}..'.format(G,host,GR))
						with open('wrCloudfrontIp.txt','a') as fl:
							fl.write(str(host)+'\n')
							fl.close()
				except Exception as e:
					print(e)
	except Exception as e:print(e)

def Main():
	for k,v in ipranges.items():
		print('{',k,' : ',v,'}',end='\n')
	dicts=[frstarray,secondarray]
	choose = int(input('enter dict number of cloudront ipranges (1/2) : '.title()))-1
	cidrs_list = dicts[choose]
	for cidr in cidrs_list:
			iprange=[]
			for ip in ipcalc.Network(cidr):
				iprange.append(ip)
			for index in range(len(iprange)):			
					try:
						print("{}[INFO] Probing... ({}/{}) [{}]{}".format(
						R,index+1,len(iprange),iprange[index],GR))
						sc=threading.Thread(target=scanner,args=(iprange[index],))
						sc.start()
					except KeyboardInterrupt:
						print('{}Scan aborted by user!{}'.format(R,GR))
						break
Main()				
