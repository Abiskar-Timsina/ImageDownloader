from string import Template
import json
import os
import re
import requests 

#internal class that's initialized just to initialize the config files
class __ParseConfigFile:
	def __init__(self) -> None:
		global parameter
		with open("imagescrapper/.config/config.ini", 'r') as config_file:
			self.config = json.load(config_file)

		self.verbose_commands = self.config["Commands"]["verbose"].split(" ")
		self.help_commands = self.config["Commands"]["help"].split(" ")
		self.link_commands = self.config["Commands"]["links"].split(" ")
		
		self.verbose = int(self.config["Config"]["verbose"])
		self.links = int(self.config["Config"]["links"])
		self.search_param = str()

		if (len(os.sys.argv) == 1):
			raise SystemExit(0)
		else:
			for parameter in os.sys.argv[1:]:
				if '-' not in str(parameter):
					self.search_param += parameter+' '

				if parameter in self.verbose_commands:
					self.verbose = 1

				elif parameter in self.link_commands:
					self.links = 1 

				elif (parameter in self.help_commands) or (len(os.sys.argv) == 1):
					with open("imagescrapper/.config/help.info",'r') as help_file:
						print(help_file.read())
					raise SystemExit(0)

		if (len(self.search_param) < 1):
			raise SystemExit(0)


class Config(__ParseConfigFile):
	def __init__(self) -> None:
		super().__init__()
		#getting the query/search param
		Config.search_query = self.search_param
		Config.verbose = self.verbose
		Config.show_links = self.links
		#initializing the necessary URLs 
		Config.url = self.config["Data"]["url"]
		Config.Response_URL = self.config["Data"]['response_url']

		#setting the 'q' query string to whatever the user needs
		Config.PARAMS= self.config["INITIAL_PARAMS"]
		Config.PARAMS['q'] = self.search_param

		#initializing the Header file
		Config.HEADERS= self.config["HEADERS"]


	def GetVQD(self,page) -> str:
		#list comprehension for generating script containing the VQD(encryption key) id
		search_scripts = [value.split("=") for value in page("script")[0]]

		for script_res in search_scripts[0]:
			#using regex to match the format 'x-xxxx' where x is an digit common format of a VQD 
			if (re.match(r"[']\d[-]\d",script_res)):
				value = (script_res.split(";")[0])
				value = [_i for _i in value if _i != "'"]
				value = ''.join(value)
				return value


	#the parameters required for the get request is different in both cases thus a different parameter dictionary is used
	def GetResponseParams(self,vqd) -> dict:
		Config.RESPONSE_PARAMS = self.config["RESPONSE_PARAMS"]
		Config.RESPONSE_PARAMS['q'] = str(self.search_param)
		Config.RESPONSE_PARAMS['vqd'] = str(vqd)
		return Config.RESPONSE_PARAMS

	#this wrapper function is present for further updates; as of now it's presence is redundent
	@staticmethod
	def main(function):
		try:
			os.system("clear")
		except:
			os.system("cls")

		def ret_main():
			function()
		return ret_main

class DownloadManager:
	i = 0
	def __init__(self,targeturl):
		self.query = Config.search_query.rstrip()
		self.targeturl = targeturl

		if (os.path.exists(self.query)):
			pass
		else:
			os.mkdir(os.path.join(os.getcwd(),self.query))

		pic_format = targeturl.split(".")[-1]

		t = Template("./$query/$i.$format")
		DownloadManager.i += 1

		if Config.verbose == 1:
			print(t.substitute({"query":self.query,"i":DownloadManager.i,"format":pic_format}))

		if Config.show_links == 1:
			print(targeturl)


		# with open(t.substitute({"query":self.query,"i":DownloadManager.i,"format":pic_format}),"wb") as f:
		# 	f.write(requests.get(self.targeturl).content)