#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import urllib.request
import re


def getAllProductsUrl(companyUrl):
    respData = getResponseData(companyUrl)
    allPaths = re.findall(r'</span>\\n\\t\\t\\t\\t<a href="/product/(\d+)-(\d+)/(.*?)\.html', str(respData))

    scheme = 'https://www.alibaba.com/product-detail/'

    productsUrl = []
    for path in allPaths:
        url = scheme + path[2] + "_" + path[0] + ".html"
        productsUrl.append(url)

    return productsUrl

def getKeywordsAndTitle(productUrl):
    respData = getResponseData(productUrl)

    keywordsStr = re.search(r'<meta name="keywords" content="(.*?)"/>', str(respData))
    keywords = keywordsStr.group(1).replace("High Quality ", "").split(",")

    if len(keywords) > 1:
        dict = {"title": keywords[0].strip()}
        keywords.pop(0)

        dict["keywords"] = ",".join(keywords).strip()
        return dict
    else:
        return None

def getResponseData(htmlUrl):
    req = urllib.request.Request(htmlUrl)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    return respData

from urllib.parse import urlparse
from os.path import normpath, basename
import time
def getFileName(companyUrl):
    parsedUri = urlparse(companyUrl)
    host = '{uri.netloc}'.format(uri=parsedUri)
    lastPart = basename(normpath(companyUrl)).replace(".html", "")
    nowTime = int(time.time())
    return host + "_" + lastPart + "_" + str(nowTime) + ".txt"


"""开始处理"""
print("Enter the company url:")

companyUrl = input().strip()

print("Doing ......")

results = ""

productsUrl = getAllProductsUrl(companyUrl)

for url in productsUrl[0:4]:
    dict = getKeywordsAndTitle(url)
    if not (dict is None):
        results += "title:\n"
        results += dict["title"] + "\n"
        results += "keywords:\n"
        results += dict["keywords"] + "\n\n"


filename = getFileName(companyUrl)

f = open(filename, "w")
f.write(results)
f.close()

import os

print("Done! Saved in file:")
print(os.path.realpath(filename))








