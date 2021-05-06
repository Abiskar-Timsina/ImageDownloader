from setuptools import setup,find_packages

with open("requirements.txt",'r',encoding="utf-16") as req:
	requirements = req.read().split('\n')

setup(
	name="imagedownloader",
	version="0.0.1",
	packages = find_packages(),

	install_requires = requirements[:-1],

	entry_points = {
	"console_scripts":["imagedownloader=imagescraper.download:main"]
	},
	
    data_files=[('imagescraper/.config', ['imagescraper/.config/config.ini', 'imagescraper/.config/help.info'])],
     
	)