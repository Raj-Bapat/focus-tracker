from simple_term_menu import TerminalMenu
import csv
from applescript import asrun, asquote
import os
import subprocess, sys
import datetime
import time
import managedata
import sys

# open with truncate

pathname = "/Users/r/PycharmProjects/focus-tracker-dev/"


while True:

    print ("Choose selection: \n")

    line = input("1. Label for current time 2. Suppress action. Enter Number:")
    if '1' == line:
        line = input("Were you on task? (Y/N)")
        if line != "Y" and line != "N":
            continue
        fl = open(f"{pathname}communicate.txt", "r+")
        fl.truncate(0)
        fl.seek(0)
        fl.write("1\n")
        fl.write(f"{line}")
        fl.close()
        print('Input: 1')
    if '2' == line:
        print('Input: 2')
        line = input("How much time (minutes)? ")
        print(f'Input: {line}')
        fl = open(f"{pathname}communicate.txt", "r+")
        fl.truncate(0)
        fl.seek(0)
        fl.write("2\n")
        fl.write(f"{line}")
        fl.close()
    time.sleep(2)

