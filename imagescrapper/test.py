import re

y = ["vqd:","'313113131313131313131'"]
for i in y:
	if (re.match(r"[']\d",i)):
		print(i)