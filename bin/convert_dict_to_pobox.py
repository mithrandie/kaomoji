#!/usr/bin/env python
#-*-coding: utf-8 -*-

SUCCESS_COLOR = "\033[36m"
ERROR_COLOR = "\033[31m"
WARN_COLOR = "\033[33m"
ESC_COLOR = "\033[0m"

import codecs
import os
import sys
import xml.etree.ElementTree as ElementTree

def error(message):
    print(ERROR_COLOR + "Error: " + message + ESC_COLOR)
    sys.exit(1)


macJaDict = os.path.join(os.getcwd(), "Text Substitutions.plist")
poboxDictHeader = os.path.join(os.getcwd(), "JPNUserDict_Header.txt")
poboxDict = os.path.join(os.getcwd(), "JPNUserDict.txt")


if not os.path.exists(macJaDict):
    error("Mac Japanese Dictionary File Does Not Exist. [" + macJaDict + "]")

if not os.path.exists(poboxDictHeader):
    error("POBox Dictionary Header Does Not Exist. [" + poboxDictHeader + "]")

if os.path.isfile(poboxDict):
    error("POBox Dictionary File Already Exists. [" + poboxDict + "]")


words = []
wordTree = ElementTree.parse(macJaDict)
for dictionary in wordTree.iter("dict"):
    key = ""
    phrase = ""
    for item in list(dictionary):
        if item.tag == "key" and item.text == "phrase":
            key = "phrase"
        elif item.tag == "string" and key == "phrase":
            phrase = item.text
        elif item.tag == "key" and item.text == "shortcut":
            key = "shortcut"
        elif item.tag == "string" and key == "shortcut" and phrase != "":
            if 50 < len(item.text):
                error("Shortcut is too long. len:" + str(len(item.text)) + " [" + item.text + "]")
            if 50 < len(phrase):
                error("Phrase is too long. len:" + str(len(phrase)) + " [" + item.text + " : " + phrase + "]")

            words.append({"shortcut": item.text, "phrase": phrase})
            break


with codecs.open(poboxDictHeader, "r", "utf-8") as pbhf:
    header = pbhf.read()
    with codecs.open(poboxDict, "w", "utf-8") as pbf:
        pbf.write(header)
        pbf.write("\n")

        for word in words:
            pbf.write(word["shortcut"] + "\t" + word["phrase"] + "\n")

sys.exit(0)

