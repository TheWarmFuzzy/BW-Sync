import datetime
import json

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
		with open(url,"w+") as file:
			try:
				data = json.dump(data,file)
			except:
				pass
	
	def log(self,msg):
		pass
		

if __name__ == "__main__":
	fm = FileManager()
	configs = fm.load_json("config/client.conf")
	while True:
		pass