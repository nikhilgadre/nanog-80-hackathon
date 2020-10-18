try:
    from datetime import datetime, timedelta, timezone
    from netmiko import ConnectHandler
    import boto3
    import os
    import sys
except:
    print("Install the required modules")
    exit()

def dev_backup_s3_push():
    try:
        print(str(datetime.now()) + " INFO: " + "RUN - Backing Up Configurations")
        csv_handler = open("sshInfo-2.csv", 'r')
        print(str(datetime.now()) + " INFO: " + "sshInfo-2.csv")
        dev_det = []
        dev_det_l_d = []
        for i in csv_handler:
            dev_det.append(i.strip().split(","))
        for i in range(1, len(dev_det)):
            dev_det_l_d.append(dict(zip(dev_det[0], dev_det[i])))
        all_devices = {i['device_name']:i for i in dev_det_l_d}
        for i in all_devices:
            all_devices[i].pop('device_name')
        os.chdir('nsot')
        for i in all_devices:
            try:
                print("----- Backing up config of %s -----" %(i))
                timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                file_name = i + '__' + timestamp + '.txt'
                file_handler = open(file_name, 'w+')
                net_connect_1 = ConnectHandler(**all_devices[i])
                net_connect_1.enable()
                output = net_connect_1.send_command("show run")
                file_handler.write(output)
                file_handler.close()
                net_connect_1.disconnect()
                print(str(datetime.now()) + " INFO: " + "Backed up config of %s" % (i))
                print(str(datetime.now()) + " INFO: " + "Created %s" % (file_name))
            except Exception as e:
                print(e)
                print(str(datetime.now()) + " ERROR: " + "%s" % (e))
        print(os.listdir())
        file_list = os.listdir()
        print(file_list)

    except Exception as e:
        print(e)
        print(str(datetime.now()) + " ERROR: " + "%s" % (e))
    try:
        print("\n----- Creating File Upload List -----")
        s3_upload_list = []
        # os.chdir('nsot')
        file_list = os.listdir()
        print(file_list)
        for i in all_devices:
            # print(i)
            b = [j for j in file_list if i in j.split("_")]
            # print("b - ORIGINAL")
            # print(b)
            if len(b) == 0:
                print("No Configurations Found For %s" % i)
            else:
                print("Configurations Found For %s" % i)
                b.sort(reverse=True)
                # print("b - reverse=True")
                # print(b)
                s3_upload_list.append(b[0])
        # print(s3_upload_list)
        print(str(datetime.now()) + " INFO: " + "Created S3 File Upload List")
    except Exception as e:
        print(e)
        print(str(datetime.now()) + " INFO: " + "EXIT - Backing Up Router Config To S3")
        print(str(datetime.now()) + " ERROR: " + "%s" % (e))
    try:
        s3_1 = boto3.client('s3')
        bucket_name = "itp-nanog80-hackathon"
        print(str(datetime.now()) + " INFO: " + "Created connection to S3 - %s" % (bucket_name))
    except Exception as e:
        print(e)
        print(str(datetime.now()) + " ERROR: " + "%s" % (e))
    try:
        print("\n----- Uploading Files to S3 - %s -----" %(bucket_name))
        print(str(datetime.now()) + " INFO: " + "Uploading Files to S3 - %s" %(bucket_name))
        for file_name in s3_upload_list:
            print("\n----- Uploading %s to S3 - %s -----" %(file_name, bucket_name))
            response = s3_1.upload_file(file_name, bucket_name, Key= file_name)
            print(str(datetime.now()) + " INFO: " + "Uploaded %s to S3 - %s" % (file_name, bucket_name))
            #print(response)
        print(str(datetime.now()) + " INFO: " + "STOP - Backing Up Router Config To S3")
        return "Router configs uploaded successfully on S3 Bucket"
    except Exception as e:
        print(e)
        print(str(datetime.now()) + " ERROR: " + "%s" % (e))

#dev_backup_s3_push()
