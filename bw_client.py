from file_manager import FileManager
import socket
from time import sleep

class BWClient:
	def __init__(self):
		self.fm = FileManager()
		
		#Default Configurations
		self.DEBUG = True
		self.HOST = socket.gethostname()
		self.PORT = 1234
		self.TIMEOUT = 30
		
		self.receiving_file = False
		
		#Load Configurations
		self.load_config("config/client.conf")
		
	def load_config(self,url):
		config = self.fm.load_json(url)
		
		if None == config:
			self.write_config(url)
			if self.DEBUG:
				print("Configuration file created. Defaults loaded.")
			return False
		
		if config["DEBUG"]:
			self.DEBUG = config["DEBUG"]
		
		if config["HOST_NAME"]:
			self.HOST = config["HOST_NAME"]
			
		if config["PORT"]:
			self.PORT = config["PORT"]
		
		if config["SOCKET_TIMEOUT"]:
			self.TIMEOUT = config["SOCKET_TIMEOUT"]
		
		if self.DEBUG:
			print("Configurations loaded.")
			
		return True
		
	def write_config(self,url):
	
		data = {
		"DEBUG":self.DEBUG,
		"HOST_NAME":None,
		"PORT":None,
		"SOCKET_TIMEOUT":self.TIMEOUT}
		
		self.fm.write_json(url,data)
		
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
		if not self.receiving_file:
			try:
				data = self.sock.recv(1024)
				if data:
					str_data = str(data,'UTF-8')
					
					if self.DEBUG:
						print (str_data)
					
					if str_data == "Pong":
						void_messages = 0
						sleep(1)
						
					if str_data == "File":
						self.receiving_file = True;
						self.fm.receive_file(self.sock,"wpt.bmp")	
						
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