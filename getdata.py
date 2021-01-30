import csv
from applescript import asrun, asquote
import os
import subprocess, sys
import datetime
import time
import managedata

lol = []

def addData(li):
    with open('/Users/r/PycharmProjects/focus-tracker/data.csv', 'a', newline='') as csvfile:
        dwr = csv.writer(csvfile, delimiter=',',
                     quotechar='|', quoting=csv.QUOTE_MINIMAL)
        dwr.writerow(li)


endsupresstime = 0

while 1 > 0:
    if time.time() >= endsupresstime:
        endsupresstime = 0
    time.sleep(.1)
    fl = open("/Users/r/PycharmProjects/focus-tracker/communicate.txt", "r+")
    # applescript = '''
    # tell application "System Events"
    #     set processName to name of processes whose frontmost is true
    #     do shell script "echo " & processName
    # end tell
    # '''
    # ret = asrun(applescript)
    ret1 = os.popen("osascript -e 'tell application \"System Events\" to count every process whose name is \"zoom.us\"'").read().strip()
    onzoom = "false"
    if ret1 == "1":
        onzoom = "true"
    ret2 = os.popen("osascript -e 'tell application \"System Events\" to get name of application processes whose frontmost is true and visible is true'").read().strip()
    ret3 = "no"
    if ret2 == "Google Chrome":
        ret3 = "yes"
    if ret2 == "Shadow":
        ret2 = "Xcode"
    ret4 = "N/A"
    if ret3 == "yes":
       ret4 = os.popen("osascript -e 'tell application \"Google Chrome\" to return URL of active tab of front window'").read().strip()
    ret5 = "N/A"
    if ret3 == "yes":
        ret5 = os.popen("osascript -e 'tell application \"Google Chrome\" to return title of active tab of front window'").read().strip()
    import datetime
    date_object = datetime.date.today()

    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if endsupresstime != 0:
        lol.append(["2", onzoom, ret2, ret3, ret4, ret5, date_object, current_time, " ", "Supressed"])
    else:
        lol.append(["2", onzoom, ret2, ret3, ret4, ret5, date_object, current_time, " ", "Not Supressed"])
    if ret3 == "yes" and endsupresstime == 0:
        managedata.tabulate()
    if ret2 == "Discord" and endsupresstime == 0:
        managedata.triggersequence()
    if os.stat("/Users/r/PycharmProjects/focus-tracker/communicate.txt").st_size != 0:
        inp = fl.readline().strip()
        print(inp)
        if inp == "1":
            inp = fl.readline().strip()
            print(inp)
            fl.truncate(0)
            fl.seek(0)
            if inp == "Y":
                for li in lol:
                    li[8] = "Yes"
                    addData(li)
                lol.clear()
            else:
                for li in lol:
                    li[8] = "No"
                    addData(li)
                lol.clear()
        if inp == "2":
            inp = fl.readline().strip()
            print(inp)
            fl.truncate(0)
            fl.seek(0)
            endsupresstime = time.time()+int(inp)*60
    if now.second == 0:
        for li in lol:
            addData(li)
        lol.clear()
    fl.close()










