from setuptools import setup,find_packages

setup(
	name="imagedownloader",
	version="0.0.1",
	packages = find_packages(),

	entry_points = {
	"console_scripts":["imagedownloader=imagescrapper.download:main"]
	},
	
    data_files=[('imagescrapper/.config', ['imagescrapper/.config/config.ini', 'imagescrapper/.config/help.info'])],
     
	)