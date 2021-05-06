import bs4
import json
import requests 
import asyncio

from .utils import *

@utils.Config.main
def main():
	utils_obj = utils.Config()
	with requests.Session() as req:
		#this page is required to get the encryption key (VQD) 
		script_page = req.get(utils_obj.url,params=utils_obj.PARAMS,headers=utils_obj.HEADERS)
		home_page = bs4.BeautifulSoup(script_page.text,"lxml")

		#getting the encryption and the required query strings
		VQD = utils_obj.GetVQD(home_page)

		#note that different URL is used in this case compared to the former
		response_param = utils_obj.GetResponseParams(VQD)

		#we go through multiple pages

		for page in range(Config.max_pages):
			#sending the request with an encryption key to get a valid JSON output
			response_page = req.get(utils_obj.Response_URL,params=response_param)
			response_json = json.loads(response_page.text)
			
			#parsing for the required data
			data_results = response_json['results']

			#simple iteration over each image link
			for index_image_url in range(len(data_results)):
				image_url = data_results[index_image_url]['image']

				#async functions
				loop = asyncio.get_event_loop()
				task = loop.create_task(DownloadManager().downloader(image_url))
				loop.run_until_complete(task)
			
			#the count starts from 0 and the first param is already 1
			'''
			first loop:
			page:0; p:1

			second loop:
			page:1; p: (0+2){from prev iterations} = 2

			third loop:
			page:2, p: (1+2){from prev iterations} = 3
			.
			.
			.
			and so on...
			'''

			response_param['p'] = page + 2
			loop.close()

if __name__ == "__main__":
	main()