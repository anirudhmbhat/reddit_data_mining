import subprocess,os,sys

p = {}

p['husky']=subprocess.Popen(['python','husky_images.py'])
p['corgi']=subprocess.Popen(['python','corgi_images.py'])

for key,value in p.items():
	p[key].communicate()