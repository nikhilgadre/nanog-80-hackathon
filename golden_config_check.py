try:
    from datetime import datetime, timedelta, timezone
    import os
    import sys
    import difflib
except:
    print("Install the required modules")
    exit()
def goldenconfigcheck():
    try:
        os.chdir('D:/Fall2020/finalalala/hast/Codes/')
        print(os.getcwd())
        print(str(datetime.now()) + " INFO: " + "RUN - Comparing Latest Config With Golden Config")
        csv_handler = open("sshInfo-2.csv", 'r')
        print(str(datetime.now()) + " INFO: " + "Opened sshInfo-2.csv")
        dev_det = []
        dev_det_l_d = []
        for i in csv_handler:
            dev_det.append(i.strip().split(","))
        for i in range(1, len(dev_det)):
            dev_det_l_d.append(dict(zip(dev_det[0], dev_det[i])))
        all_devices = {i['device_name']:i for i in dev_det_l_d}
        for i in all_devices:
            all_devices[i].pop('device_name')
        # print(all_devices)
    except Exception as e:
        print(e)
        print(str(datetime.now()) + " INFO: " + "EXIT - Comparing Latest Config With Golden Config")

    try:
        os.chdir('D:/Fall2020/finalalala/hast/Codes/nsot')
        print(os.getcwd())
        temp_list=[]
        file_list = os.listdir()
        for device in all_devices:
            # print (device)
            b = [j for j in file_list if device in j.split("__")]
            b.sort(reverse=True)
            newest_conf_name = b[0]
            # print(newest_conf_name)
            text1 = open(str(newest_conf_name)).readlines()
            text2 = open("golden_configs/" + str(device) + ".txt").readlines()
            log_differences = open('diff_configs.txt', 'a')
            print("------------------------------")
            print("Comparing %s & %s" %(device, newest_conf_name))
            print("------------------------------", file=log_differences)
            print(str(datetime.now()) + " INFO: " + "Comparing %s & %s" % (newest_conf_name, device))
            print(str(datetime.now()) + " INFO: " + "Comparing %s & %s" % (newest_conf_name, device), file=log_differences)
            diff = difflib.unified_diff(text1, text2)
            diff_length = len(list(diff))
            # print(diff_length)
            if diff_length != 0:
                print("Difference")
                print(str(datetime.now()) + " INFO: " + "Comparing %s & %s - DIFFERENCE" % (newest_conf_name, device))
                temp_list.append("Difference found for " + device)
                print(str(datetime.now()) + " INFO: " + "Comparing %s & %s - DIFFERENCE" % (newest_conf_name, device), file=log_differences)
                for line in difflib.unified_diff(text1, text2):
                    print(line)
                    print(line, file=log_differences)

            else:
                print("No Difference")
                print(str(datetime.now()) + " INFO: " + "Comparing %s & %s - NO DIFFERENCE" % (newest_conf_name, device))
                temp_list.append("Difference not found for " + device)
                print(str(datetime.now()) + " INFO: " + "Comparing %s & %s - NO DIFFERENCE" % (newest_conf_name, device), file=log_differences)
                # return "No Difference Found"
        print(str(datetime.now()) + " INFO: " + "STOP - Comparing Latest Config With Golden Config")
        return temp_list
    except Exception as e:
        print(e)
        print(str(datetime.now()) + " INFO: " + "EXIT - Comparing Latest Config With Golden Config")

# goldenconfigcheck()
