import socket
from time import sleep

class BWClient:
	def __init__(self):
		self.DEBUG = True
		self.HOST = socket.gethostname()
		self.PORT = 1234
		self.TIMEOUT = 30
		pass
	
	def set_address(self,host,port):
		self.HOST = host
		self.PORT = port
		
	def connect(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if self.DEBUG: 
			print ("Socket created.")
		
		connected = False
		while not connected:
			try:
				self.sock.connect((self.HOST, self.PORT))
				connected = True
				if self.DEBUG:
					print ("Socket connected.")
			except socket.error as msg:
				if self.DEBUG:
					print ("Connection failed.")
			sleep(5)

		self.sock.setblocking(0)
		
	def reconnect(self):
		self.sock.close()
		if self.DEBUG:
			print ("Socket closed.")
		self.connect()
		
	def listen(self):
		void_messages = 0;
		try:
			data = self.sock.recv(1024)
			if data:
				str_data = str(data,'UTF-8')
				if self.DEBUG:
					print (str_data)
				
				if str_data == "Pong":
					void_messages = 0
					sleep(1)
		except socket.error as msg:
			if(void_messages > self.TIMEOUT):
				if self.DEBUG:
					print ("Connection timed out.")
				self.reconnect()
			else:
				try:
					self.sock.send(bytes("Ping",'UTF-8'))
					if self.DEBUG:
						print("Ping")
				except socket.error as msg:
					if self.DEBUG:
						print ("Connection to server lost.")
					self.reconnect()
			sleep(1)

	def start(self):
		self.connect()
		while True:
			self.listen()
		
if __name__ == "__main__":
	client = BWClient()
	client.start()