import socket
import sys
import json
import struct
import os.path as path
import io


def socket_create():
	try:
		global host
		global port
		global soc
		host = '127.0.0.1'
		port = 9100
		soc = socket.socket()
	except socket.error as msg:
		print("Socket creation error: " + str(msg))

def socket_bind():
	try:
		global host
		global port
		global soc
		print("Binding Socket to port" + str(port))
		soc.bind((host, port))
		soc.listen(1)
	except socket.error as msg:
		print("Socket binding error: " +str(msg) + "\n" + "Retrying...")
		socket_bind()


def Socket_accept():
	try:
		httpOk = "HTTP/1.1 200 Ok\r\n"
		httpEr = "HTTP/1.1 400 ERROR\r\n"
		httpNf = "HTTP/1.1 404 Ok\r\n"
		htmlStart = '\r\n\r\n'
		conn, address = soc.accept()
		print ("Conexion ha sido establecida | " + "ip " + address[0] + " | port " + str(address[1]))
		
		#client_response = str(conn.recv(1024), "utf-8")
		Cl_res = conn.recv(1024)#recive request
		#separacion por caracteres espacios y saltos de linea
		line = Cl_res.split('\r\n'.encode())
		filePath = line[0].split(' '.encode())
		
		
		print ("------HEADERS------")
		for p in line[1:]:
			if p:
				header = p.split(':'.encode())
				print (header[0]+header[1], sep='\n')

		print (str(line[0]).replace("b",""))

		filePath[0] = str(filePath[0]).replace("b","")
		f0 = str(filePath[0]).replace("'","")
		print (f0)
		filePath[1] = str(filePath[1]).replace("b","")
		filePath[1] = str(filePath[1]).replace("'","")
		f1 = str(filePath[1]).replace("/","",1)
		print(f1)
		filePath[2] = str(filePath[2]).replace("b","")
		f2 = str(filePath[2]).replace("'","")
		print (f2)
				
		JsonResp = "X-RequestEcho: {"+'"'+"path"+'":'+" "+'"'+f1+'", '+'"'+"protocol"+'":'+f2+'", "method": '+f0+'"headers": {"Accept": "text/html", "Accept-Language": "es-ES", "Host": "localhost:9100"}}'
		print (JsonResp)

		if path.exists(str(f1)):
			file = open(f1,"r")
			readline = file.read()
			conn.send(str.encode(httpOk))
			conn.send(str.encode(JsonResp))
			conn.send(str.encode(htmlStart))
			conn.send(str.encode(readline))

			#Resp = "HTTP/1.1 200 Ok\r\n'Accept': 'text/html', 'Accept-Language': 'es-ES'\n'Host': 'localhost:9100'\r\n\r\n"+ readline
			#bytes = str.encode(Resp)
			#conn.send(bytes)
		else:
			Resp = "HTTP/1.1 404 ERROR\n"
			bytes = str.encode(Resp)
			conn.send(bytes)
		print ("\n")
		
		printHTML = "HTTP/1.1 200 Ok\n"+ readline
		#bytes = str.encode(printHTML)
		#conn.send(bytes)
		conn.close()
	except:	
		printHTML = "HTTP/1.1 400 ERROR\n"
		bytes_resp = str.encode(printHTML)
	print (printHTML)



def main():
	socket_create()
	socket_bind()
	while True:
		Socket_accept()



main()

 


#################################################################################################################################
#################################################################################################################################
####################               PROGRAM DEVELOPED BY GROUP OF MAGISTER PUCV                               ####################
#################################################################################################################################
####################                                                                                         ####################
####################   - BRYAN ARANCIBIA LAYANA                                                              ####################
####################   - PABLO GONZALEZ OLGUIN                                                               ####################
####################   - MAURICIO SAAVEDRA                                                                   ####################
#################################################################################################################################
#################################################################################################################################
