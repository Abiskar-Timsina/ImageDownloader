import json
import sys
import re


class __ParseConfigFile:
	def __init__(self) -> None:
		with open("./.config/config.ini", 'r') as config_file:
			self.config = json.load(config_file)

		self.verbose_commands = self.config["Commands"]["verbose"].split(" ")
		self.help_commands = self.config["Commands"]["help"].split(" ")
		self.__ParseParameter()
	
	def __ParseParameter(self) -> None:
		for parameter in sys.argv:
			if parameter in self.verbose_commands:
				self.config["Config"]["verbose"] = True
			elif parameter in self.help_commands:
				with open("./.config/help.info",'r') as help_file:
					print(help_file.read())

class Config(__ParseConfigFile):
	def __init__(self,search_param)->None:
		super().__init__()
		self.search_param = search_param

		Config.url = self.config["Data"]["url"]
		Config.Response_URL = self.config["Data"]['response_url']

		Config.PARAMS= self.config["INITIAL_PARAMS"]
		Config.PARAMS['q'] = self.search_param

		Config.HEADERS= self.config["HEADERS"]


	def GetVQD(self,page):
		x = page("script")
		y = str(x[0]).split("=")
		for i in y:
			if (re.match(r"[']\d[-]\d",i)):
				value = (i.split(";")[0])
				value = [a for a in value if a != "'"]
				value = ''.join(value)
				return value


	def GetResponseParams(self,vqd):
		Config.RESPONSE_PARAMS = self.config["RESPONSE_PARAMS"]
		Config.RESPONSE_PARAMS['q'] = str(self.search_param)
		Config.RESPONSE_PARAMS['vqd'] = str(vqd)
		return Config.RESPONSE_PARAMS

	@staticmethod
	def main(function):
		def ret_main():
			function()
		return ret_main
