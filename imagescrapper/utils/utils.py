from string import Template
import json
import os
import re
import requests 
import imagescrapper

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
		self.max_pages = int(self.config["Config"]["maxpages"])
		self.search_param = str()


		if (len(os.sys.argv) == 1):
			print("Supply values for the following parameters:")
			try:
				self.search_param = str(input("Search: "))
			except KeyboardInterrupt:
				print(f"\n\nService Interrupeted")
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
					self.__ShowHelp()
					raise SystemExit(0)

		if (len(self.search_param) < 1):
			print("Supply values for the following parameters:")
			try:
				self.search_param = str(input("Search: "))
			except KeyboardInterrupt:
				print(f"\n\nService Interrupeted")
				raise SystemExit(0)

	def __ShowHelp(self):
		with open("imagescrapper/.config/help.info",'r') as help_file:
			print(help_file.read())

		print(f"\n--- Current Configutarion ---",end="\n\n")
		print(f"Verbose    -> {bool(self.verbose)}")
		print(f"Show links -> {bool(self.links)}")
		print(f"Max Pages  -> {self.max_pages}")

		print("\n--- About ---",end="\n\n")
		print(f"Version: {imagescrapper.__version__}")
		print(f"Author: {imagescrapper.__author__}")
		print(f"Author's Email: {imagescrapper.__email__}")
		print(f"Github: {imagescrapper.__github__}",end="\n\n")

class Config(__ParseConfigFile):
	def __init__(self) -> None:
		super().__init__()
		#getting additional config files
		Config.search_query = self.search_param
		Config.verbose = self.verbose
		Config.show_links = self.links
		Config.max_pages = self.max_pages

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
	def main(function)-> None:
		try:
			os.system("clear")
		except:
			os.system("cls")

		def ret_main():
			function()

			print(f"\n\n---:		Download Complete		:---")
			print(f"Total Images found: {DownloadManager.total_links_found}")
			print(f"Successful Image Downloads: {DownloadManager.successful_downloads}")
			print(f"Bad links: {DownloadManager.bad_links}")

		return ret_main

class DownloadManager:
	picture_count = 1
	successful_downloads = 0
	total_links_found = 0
	bad_links = 0

	def __init__(self,targeturl):
		pic_format = ''
		self.query = Config.search_query.rstrip()
		self.targeturl = targeturl

		if (os.path.exists(self.query)):
			pass
		else:
			os.mkdir(os.path.join(os.getcwd(),self.query))

		targeturl_extension = targeturl.split(".")[-1]
		DownloadManager.total_links_found +=  1

		try:
			if (re.match(r"[egjnp]{3,4}$",targeturl_extension)):	
				pic_format = targeturl_extension.lower()
			else:
				raise imagescrapper.NonSpecifiedExtention("Non Specified extention")


			naming_template = Template("./$query/$picture_count.$format")

			if Config.verbose == 1:
				print(naming_template.substitute({"query":self.query,"picture_count":DownloadManager.picture_count,"format":pic_format}))

			if Config.show_links == 1:
				print(targeturl)


			with open(naming_template.substitute({"query":self.query,"picture_count":DownloadManager.picture_count,"format":pic_format}),"wb") as f:
				try:
					f.write(requests.get(self.targeturl).content)
				except Exception as e:
					DownloadManager.bad_links += 1
				DownloadManager.picture_count += 1
				DownloadManager.successful_downloads += 1

		except imagescrapper.NonSpecifiedExtention:
			DownloadManager.bad_links += 1

