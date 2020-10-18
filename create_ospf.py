#Code to create ospf configs for each router using jinja template, this code also enables respective interfaces and gives an ip address to those interfaces 
try:
	import jinja2
	from jinja2 import Environment, FileSystemLoader
	import json
except:
	print('Please install required modules')

#Dictionary containing information for configuring ospf
global filelist
filelist=[]
def ospfconf_create():
	#Loading ospfinfo
	f=open('ospf_info.txt','r')
	ospfinfo=json.load(f)
	
	#Using ospf.j2 jinja template
	file_loader=FileSystemLoader('templates')
	env=Environment(loader=file_loader)
	env.trim_blocks=True
	env.lstrip_blocks=True
	env.rstrip_blocks=True
	template=env.get_template('ospf.j2')

	# Creating a configuration file for each entry in the osfpinfo dictionary
	for i in ospfinfo:
		output= template.render(ospfinfo=ospfinfo[i])
		print('Configs for',i)
		filename=i+"_ospfconf.txt"
		print(filename)
		filelist.append(filename)
		f=open(filename,'w')
		f.write(output)
		f.close()
		print('file created')
	return(filelist)

if __name__=='__main__':
	ospfconf_create()
