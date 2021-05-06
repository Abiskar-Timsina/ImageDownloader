# ImageDownloader:
##### About:
ImageDownloader is a simple web scraping tool that can be used to download images directly form duckduckgo.com. This is a personal project that I have been coding over the weekend. I built this because I found myself continuously downloading images from various sites for data collection. So, I decided to automate it.

## Features:
- CLI tool for image collection; use directly from the command line.
- Exactly like searching in the web browser; type in whatever you want and sit back as it is downloaded.
- Save different extensions; supports .jpg, .jpeg, .png
- Works in Windows and major Linux Distros.

## Installation 
Installing the imagedownloader is simple. You can simply download this repo and use the following command: 
_For Windows_ 
```console
$ python .\setup.py install 
```
_For Linux_ 
```console
$ python3 .\setup.py install 
```
##### OR
You can check the releases to find a stable version. (Executable binaries will be released later).

And, that's it. You have imagedownloader installed on your compute. Although, since the package isn't used all the time, it advised to install it in a virtual environment for easier management. Global install is ok too.


## Usage
Open a terminal and,

```console
$ imagedownloader --help
```
This will open the help page that shows available options and their flags.

## Todo:
- Implement better async function
- Better Memory management
- Logging

## License
MIT