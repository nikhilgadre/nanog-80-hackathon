import os
import csv

def Parse_file(file):
    device=[]
    D={}
    if os.path.exists(file):
        try:
            f=open(file,'r')
            data=csv.reader(f,delimiter=',')
            print(data)
            for i in data:
                if i[0]!='device_name':
                    try:
                        D[i[0]]={}
                        D[i[0]]['username']=i[1]
                        D[i[0]]['password']=i[2]
                        D[i[0]]['ip']=i[3]
                        D[i[0]]['device_type']=i[4]
                        #device.append(D)
                    except Exception as e:
                        print(e)
            return D
        except Exception as e:
            print(e)
    else:
        print("SSH-config File not found please check")

if __name__=='__main__':
    file='sshInfo-2.csv'
    ssh_details=Parse_file(file)
    print(ssh_details)
