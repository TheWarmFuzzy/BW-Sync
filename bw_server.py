import socket
import sys
from _thread import *
from time import sleep
from os import walk

class BWServer:
	def __init__(self):
		self.DEBUG = True
		self.HOST = socket.gethostname()
		self.PORT = 1234
		self.LISTEN_QUEUE = 10
		
	def start(self):
		self.bind()
		while True:
			self.listen()
		
	def bind(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		if self.DEBUG: 
			print ("Socket created.")
			
		try:
			self.sock.bind((self.HOST, self.PORT))
			print ("Socket bound successfully")
			
		except socket.error as msg:
			if self.DEBUG:
				print ("Bind failed.",msg)
			sys.exit()
		
		self.sock.listen(self.LISTEN_QUEUE)
		
	def listen(self):
		client, client_addr = self.sock.accept()
		if self.DEBUG:
			print (str(client_addr[0]) + ":" + str(client_addr[1]), "- Client connected")
		
		start_new_thread(self.communicate,(client,client_addr))
		
	#I am a threaded function
	def communicate(self, client, client_addr):
		client.send(bytes("Welcome to the server!",'UTF-8'))
		while True:
			try:
				data = client.recv(1024)
				print(str(data,'UTF-8'))

				if not data:
					break
				reply = "Pong"
				client.send(bytes(reply,'UTF-8'))
			except socket.error as msg:
				#We lost them
				break;
				
		client.close()
		if self.DEBUG:
			print (str(client_addr[0]) + ":" + str(client_addr[1]), "- Client disconnected")

if __name__ == "__main__":
	server = BWServer()
	server.start()