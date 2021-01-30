import argparse
import io
import json
import os

from google.cloud import language_v1
import six
import html2text
import hashlib
import classificationexample
import time
import ftcalendar

pathname = "/Users/r/PycharmProjects/focus-tracker-dev/"



f = open(f'{pathname}linktable.json')
neededData = json.load(f)
f.close()

badcategories = []
snoozeimages = ["https://sayingimages.com/wp-content/uploads/back-to-work-break-over-now-meme.jpg", "https://sayingimages.com/wp-content/uploads/if-you-could-that-would-be-great-get-back-to-work-meme.png", "https://memegenerator.net/img/instances/55756181/breaks-over-now-get-back-to-work-.jpg"]
snoozecount = 0



def tabulate(isSupressed):
    htstr = classificationexample.getHtmlFromTab()
    if len(htstr) < 1000:
        return "Google Chrome Unclassified"
    hashval = abs(hash(htstr))
    import datetime
    date_object = datetime.date.today()
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if hashval not in neededData:
        listToPut = {}
        print(htstr)
        listToPut["classification"] = (classificationexample.classify(htstr))
        listToPut["sentiment"] = (classificationexample.sample_analyze_sentiment(htstr))
        listToPut["source"] = htstr
        neededData[hashval] = listToPut
        with open(f'{pathname}linktable.json', 'r+') as json_file:
            json.dump(neededData, json_file)
    last_chars = current_time[-2:]
    if last_chars != "00" and isSupressed == False:
        for key, value in neededData[hashval]["classification"].items():
            if "Games" in key and value >= 0.5:
                global snoozecount
                global snoozeimages
                if snoozecount > 2:
                    os.popen(f"osascript -e 'tell application \"Google Chrome\" to open location \"{snoozeimages[0]}\"'").read().strip()
                    resp = os.popen("osascript -e 'display alert \"No more snoozes avaliable\" buttons {\"ok\"}'").read().strip()
                else:
                    os.popen(f"osascript -e 'tell application \"Google Chrome\" to open location \"{snoozeimages[snoozecount]}\"'").read().strip()
                    resp = os.popen("osascript -e 'display alert \"Would you like to snooze?\" buttons {\"No\", \"Yes\"}'").read().strip()
                    if resp == "button returned:Yes":
                        fl = open(f"{pathname}communicate.txt", "r+")
                        fl.truncate(0)
                        fl.seek(0)
                        fl.write("2\n")
                        fl.write("0")
                        fl.close()
                        snoozecount = snoozecount+1

                # os.popen("osascript -e 'tell application \"Google Chrome\" to open location \"https://sayingimages.com/wp-content/uploads/back-to-work-break-over-now-meme.jpg\"'").read().strip()
                # resp = os.popen("osascript -e 'display alert \"did we guess correctly?\" buttons {\"No\", \"Yes\"}'").read().strip()
                # if resp == "button returned:Yes":
                #     fl = open(f"{pathname}correct.txt", "r+")
                #     x = fl.read().strip()
                #     fl.truncate(0)
                #     fl.seek(0)
                #     fl.write(str(int(x)+1))
                #     fl.close()
                # fl = open(f"{pathname}totalhits.txt", "r+")
                # x = fl.read().strip()
                # fl.truncate(0)
                # fl.seek(0)
                # fl.write(str((int(x) + 1)))
                # fl.close()
                # fl = open(f"{pathname}correct.txt", "r")
                # x1 = fl.read().strip()
                # fl.close()
                # fl = open(f"{pathname}totalhits.txt", "r")
                # x2 = fl.read().strip()
                # fl.close()
                # asdf = str(int(x1)/int(x2)*100.0)
                # inpstr = "osascript -e 'display alert \"We have guessed correctly "+asdf+"% of times\"'"
                # os.popen(inpstr).read().strip()
                return key

    if len(neededData[hashval]["classification"]) == 0:
        return "Google Chrome Unclassified"
    for key, value in neededData[hashval]["classification"].items():
        return key

def getCategoryOfTab():
    # get html from tab
    htstr = classificationexample.getHtmlFromTab()
    if len(htstr) < 1000:
        return
    # get hash value of the html
    hashval = abs(hash(htstr))

    # the dictionary that contains the categories
    retval = []
    if hashval not in neededData:
        return "Google Chrome Unclassified: "
    for k, v in neededData[hashval]["classification"].items():
        return k


def resetsnoozecount():
    global snoozecount
    snoozecount = 0


