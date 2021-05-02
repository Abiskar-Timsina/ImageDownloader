import requests 
import bs4
import time

import json
import os
import threading
import sys

import utils

@utils.Config.main
def main():
	text = input("Enter the search param: ")
	obj = utils.Config(text)
	with requests.Session() as req:
		page = req.get(obj.url,params=obj.PARAMS,headers=obj.HEADERS)
		home_page = bs4.BeautifulSoup(page.text,"lxml")
		VQD = obj.GetVQD(home_page)
		x = obj.GetResponseParams(VQD)
		page2 = req.get(obj.Response_URL,params=x)
		
		response_json = json.loads(page2.text)
		data_results = response_json['results']

		for i in range(len(data_results)):
			image_url = data_results[i]['image']
			print(image_url)


if __name__ == "__main__":
	main()

