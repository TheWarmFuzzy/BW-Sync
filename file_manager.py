import datetime
import json
from time import sleep
import socket
import sys

class FileManager:
	def __init__(self):
		
		pass
	
	def load_json(self,url):
		data = None
		try:
			with open(url,"r") as file:
				try:
					data = json.load(file)
				except:
					pass
		except:
			pass
				
		return data
		
	def write_json(self,url,data):
		try:
			with open(url,"w+") as file:
				try:
					data = json.dump(data,file)
				except:
					pass
		except:
			pass
	
	def send_file(self,sock,url):
		print("Sending file in:")
		print("3")
		sleep(1)
		print("2")
		sleep(1)
		print("1")
		sleep(1)
		try:
			with open(url,"rb+") as file:
				data = file.read(1024)
				while(data):
					sock.send(data)
					print("Sending")
					data = file.read(1024)
					
				data = bytes("EOF",'UTF-8')
				sock.send(data)
		except:
			pass
		
	def receive_file(self,sock,url):
		try:
			with open(url,"wb+") as file:
				EOF = False
				while not EOF:
					try:
						data = sock.recv(1024)
						while(data):
							print(len(data))
							if 3 == len(data):
								try:
									str_data = str(data,'UTF-8')
									if "EOF" == str_data:
										EOF = True
										break
								except:
									pass
							file.write(data)
							data = sock.recv(1024)
					except:
						pass
		except:
			pass
		print ("File transfer complete")
		
	def log(self,msg):
		pass
		

if __name__ == "__main__":
	fm = FileManager()
	configs = fm.load_json("config/client.conf")
	while True:
		pass