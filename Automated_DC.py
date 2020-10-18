try:
	from flask import Flask,render_template,request,redirect,url_for,Markup
	import netmiko
	from netmiko import ConnectHandler
	import threading
	import sys
	import os
	from get_conf import *
	from login_info import *
	from create_ospf import *
	from do_ospf import *
	from create_bgp import *
	from do_bgp import *
	from get_conf import *
	from time import *
	from do_nat import *
	from create_nat import *
	from s3_push_conf import *
	from golden_config_check import *
	from vpn import *

except Exception as e:
	print(e)
	print('Please install the required modules....')

app=Flask(__name__,template_folder='templates')

@app.route('/monitor/confs/<conf_opt>')
def mon2(conf_opt):
	if conf_opt=='R1':
		file1=open('R1_running_config.txt','r')
		lines=file1.readlines()
		return render_template('monitor2.html', data=lines)
	elif conf_opt=='R2':
		file1=open('R2_running_config.txt','r')
		lines=file1.readlines()
		return render_template('monitor2.html', data=lines)
	elif conf_opt=='R3':
		file1=open('R3_running_config.txt','r')
		lines=file1.readlines()
		return render_template('monitor2.html', data=lines)
	elif conf_opt=='R4':
		file1=open('R4_running_config.txt','r')
		lines=file1.readlines()
		return render_template('monitor2.html', data=lines)
	elif conf_opt=='R5':
		file1=open('R5_running_config.txt','r')
		lines=file1.readlines()
		return render_template('monitor2.html', data=lines)
	elif conf_opt=='R6':
		file1=open('R6_running_config.txt','r')
		lines=file1.readlines()
		return render_template('monitor2.html', data=lines)
	else:
		return render_template('error.html')

@app.route('/monitor/<info>')
def mon1(info):
	if info=='ip':
		main('1')
		file1=open('InterfacesIP.txt','r')
		lines=file1.readlines()
		return render_template('monitor2.html', data=lines)

	elif info=='bgp':
		main('2')
		file1=open('BGPinfo.txt','r')
		lines=file1.readlines()
		return render_template('monitor2.html', data=lines)

	elif info=='ospf':
		main('3')
		file1=open('OSPFinfo.txt','r')
		lines=file1.readlines()
		return render_template('monitor2.html', data=lines)

	elif info=='confs':
		main('4')
		return render_template('monitor3.html')

	else:
		return render_template('error.html')


@app.route('/<opt>')
def sub(opt):
	if opt=='m_ospf':
		filelist=ospfconf_create()
		return render_template('process1.html',data='OSPF config files',val=filelist)

	elif opt=='s_ospf':
		ospf('sshInfo-2.csv')
		return render_template('process2.html',data='OSPF files are successfully loaded into routers')

	elif opt=='m_bgp':
		filelist=bgpconf_create()
		return render_template('process1.html',data='BGP config files',val=filelist)

	elif opt=='s_bgp':
		bgp('sshInfo-2.csv')
		return render_template('process2.html',data='BGP files are successfully loaded into routers')

	elif opt=='m_nat':
		filelist=natconf_create()
		return render_template('process1.html',data='NAT config files',val=filelist)

	elif opt=='s_nat':
		nat('sshInfo-2.csv')
		return render_template('process2.html',data='NAT files are successfully loaded into routers')

	elif opt=='monitor':
#		file1=open('x2.txt','r')
#		lines=file1.readlines()
		return render_template('monitor1.html')

	else:
		return render_template('error.html')


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/backup')
def backup():
	try:
		return render_template('temp10-3.html',files=dev_backup_s3_push())
	except Exception as e:
		msg="<html><body><h1>"+str(e)+"</h1></body></html>"
		return msg

@app.route('/goldenconfig')
def goldenconfig():
	try:
		# print(goldenconfigcheck())
		return render_template('temp10-3.html',files=goldenconfigcheck())
	except Exception as e:
		msg="<html><body><h1>"+str(e)+"</h1></body></html>"
		return msg

@app.route('/ipsecconfig')
def ipsecconfig():
	try:
		vpn=vpn_conf()
		print(vpn)
		print(type(vpn))
		T=vpn[0]
		w=vpn[1]
		print(T)
		int_ip_table_html = T.get_html_string(attributes={"border": 1, "style": "border-width: 1px; border-collapse: collapse;"})
		int_ip_tvable_html = Markup(int_ip_table_html)
		return render_template('temp10-4.html',files=int_ip_table_html,files1=w)
	except Exception as e:
		msg="<html><body><h1>"+str(e)+"</h1></body></html>"
		return msg

@app.route('/f1')
def f1():
	try:
		#function for getting file configuration
		return render_template('temp10.html')
	except Exception as e:
		msg="<html><body><h1>"+str(e)+"</h1></body></html>"
		return msg

@app.route('/f2')
def f2():
	try:
		#function for getting file configuration
		return render_template('temp10-2.html')
	except Exception as e:
		msg="<html><body><h1>"+str(e)+"</h1></body></html>"
		return msg


@app.route('/clifun2', methods = ['GET', 'POST'])
def clifun2():
    T=PrettyTable()
    a1=request.form['cmd']
    b1=request.form['host']
    c1=request.form['username']
    d1=request.form['password']
    e1=request.form['device_type']
    T.field_names = ['Router Name',a1]
    if a1.split()[0]=='show':
        try:
            device = ConnectHandler(device_type=e1, host=b1, username=c1, password=d1)
            data=device.send_command(a1)
            device.disconnect()
            T.add_row((b1,data))
            int_ip_table_html = T.get_html_string(attributes={"border": 1, "style": "border-width: 1px; border-collapse: collapse;"})
            int_ip_table_html = Markup(int_ip_table_html)
            return render_template('temp10-3.html',files=int_ip_table_html)
        except Exception as e:
            msg="<html><body><h1>"+str(e)+"</h1></body></html>"
            return msg
    else:
        e='Operation not allowed. only show command is valid. User entered: '+a1
        msg="<html><body><h1>"+str(e)+"</h1></body></html>"
        return msg

@app.route('/clifun1', methods = ['GET', 'POST'])
def clifun1():
    a1=request.form['cmd']
    if a1.split()[0]=='show':
        def pushcmd(i,j,router):
            try:
                device=ConnectHandler(**i)
                data=device.send_command(j)
                device.disconnect()
                T.add_row((router,data))
            except Exception as e:
                T.add_row((router,e))
            return T
        def Parse_file(file):
            device=[]
            if os.path.exists(file):
                try:
                    f=open(file,'r')
                    data=csv.reader(f,delimiter=',')
                    print(data)
                    for i in data:
                        if i[0]!='device_name':
                            try:
                                D={}
                                D['device_name']=i[0]
                                D['username']=i[1]
                                D['password']=i[2]
                                D['ip']=i[3]
                                D['device_type']=i[4]
                                device.append(D)
                            except Exception as e:
                                print(e)
                    return device
                except Exception as e:
                    print(e)
            else:
                print("SSH-config File not found please check")
        file='D:/Fall2020/nanog/sshInfo-2.csv'
        ssh_details=Parse_file(file)
        if ssh_details!=None:
            global T
            print("Please wait. cmd started.....")
            T=PrettyTable()
            T.field_names = ['Router Name',a1]
            thread=[]
            for i in ssh_details:
                router= i['device_name']
                #making a new dictionary becasue jupyternotebook does not allow the pop item feature.
                m={}
                m['device_type']=i['device_type']
                m['username']=i['username']
                m['host']=i['ip']
                m['password']=i['password']
                #calling the individual thread for faster execution
                t1=threading.Thread(target=pushcmd,args=(m,a1,router))
                t1.start()
                thread.append(t1)
        else:
            print("Please check ssh configuration file")
        for m in thread:
            m.join()
        print(T)
        int_ip_table_html = T.get_html_string(attributes={"border": 1, "style": "border-width: 1px; border-collapse: collapse;"})
        int_ip_table_html = Markup(int_ip_table_html)
        return render_template('temp10-3.html',files=int_ip_table_html)
    else:
        e='Operation not allowed. only show command is valid. User entered: '+a1
        msg="<html><body><h1>"+str(e)+"</h1></body></html>"
        return msg


if __name__ == '__main__':
	app.run(host='127.0.0.1',port=1234,debug=True)
