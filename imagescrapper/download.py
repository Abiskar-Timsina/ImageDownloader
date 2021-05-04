import bs4
import json
import requests 
import threading

from .utils import *

#created a empty list to handle threads
active_threads = list() 

@utils.Config.main
def main():
	search_query = input("Enter the search param: ")
	utils_obj = utils.Config(search_query)

	with requests.Session() as req:
		#this page is required to get the encryption key (VQD) 
		script_page = req.get(utils_obj.url,params=utils_obj.PARAMS,headers=utils_obj.HEADERS)
		home_page = bs4.BeautifulSoup(script_page.text,"lxml")

		#getting the encryption and the required query strings
		VQD = utils_obj.GetVQD(home_page)

		#note that different URL is used in this case compared to the former
		response_param = utils_obj.GetResponseParams(VQD)

		#sending the request with an encryption key to get a valid JSON output
		response_page = req.get(utils_obj.Response_URL,params=response_param)
		response_json = json.loads(response_page.text)
		
		#parsing for the required data
		data_results = response_json['results']

		#simple iteration over each image link
		for index_image_url in range(len(data_results)):
			image_url = data_results[index_image_url]['image']
			DownloadManager(search_query,image_url)

if __name__ == "__main__":
	main()