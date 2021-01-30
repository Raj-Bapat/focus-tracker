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

f = open('/Users/r/PycharmProjects/focus-tracker/linktable.json')
neededData = json.load(f)
f.close()

badcategories = []

def triggersequence():
    os.popen(
        "osascript -e 'tell application \"Google Chrome\" to open location \"https://sayingimages.com/wp-content/uploads/back-to-work-break-over-now-meme.jpg\"'").read().strip()
    resp = os.popen("osascript -e 'display alert \"did we guess correctly?\" buttons {\"No\", \"Yes\"}'").read().strip()
    if resp == "button returned:Yes":
        fl = open("/Users/r/PycharmProjects/focus-tracker/correct.txt", "r+")
        x = fl.read().strip()
        fl.truncate(0)
        fl.seek(0)
        fl.write(str(int(x) + 1))
        fl.close()
    fl = open("/Users/r/PycharmProjects/focus-tracker/totalhits.txt", "r+")
    x = fl.read().strip()
    fl.truncate(0)
    fl.seek(0)
    fl.write(str((int(x) + 1)))
    fl.close()
    fl = open("/Users/r/PycharmProjects/focus-tracker/correct.txt", "r")
    x1 = fl.read().strip()
    fl.close()
    fl = open("/Users/r/PycharmProjects/focus-tracker/totalhits.txt", "r")
    x2 = fl.read().strip()
    fl.close()
    asdf = str(int(x1) / int(x2) * 100.0)
    inpstr = "osascript -e 'display alert \"We have guessed correctly " + asdf + "% of times\"'"
    os.popen(inpstr).read().strip()


def tabulate():
    htstr = classificationexample.getHtmlFromTab()
    if len(htstr) < 1000:
        return
    hashval = abs(hash(htstr))
    import datetime
    date_object = datetime.date.today()
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if hashval not in neededData:
        listToPut = {}
        # print(htstr)
        listToPut["classification"] = (classificationexample.classify(htstr))
        listToPut["sentiment"] = (classificationexample.sample_analyze_sentiment(htstr))
        listToPut["source"] = htstr
        neededData[hashval] = listToPut
        with open('/Users/r/PycharmProjects/focus-tracker/linktable.json', 'r+') as json_file:
            json.dump(neededData, json_file)
    last_chars = current_time[-2:]
    if last_chars != "00":
        for key, value in neededData[hashval]["classification"].items():
            if "Games" in key and value >= 0.5:
                triggersequence()
                break




