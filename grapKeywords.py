#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import urllib.request
import re

from urllib.parse import urlparse
import os.path


def getCategorysUrl(companyUrl):
    allCategoryUrl = companyUrl + "/productlist.html"
    respData = getResponseData(allCategoryUrl)
    listUrl = re.findall(r'<ul class="productgroup-list">')


def getAllProductsUrl(productListUrl):
    parsedUri = urlparse(productListUrl)
    schemeAndProtocol = "{uri.scheme}://{uri.netloc}/".format(uri=parsedUri)
    paths = "{uri.path}".format(uri=parsedUri).split("/")
    temp = paths[1].split("-") #productgrouplist-803523792-1
    index = 1
    flag = True

    productsUrl = []

    while flag:
        pageUrl = schemeAndProtocol + temp[0] + "-" + temp[1] + "-" + str(index) + "/" + paths[2]
        respData = getResponseData(pageUrl)
        if "No matching results." not in str(respData):

            allPaths = re.findall(r'</span>\\n\\t\\t\\t\\t<a href="/product/(\d+)-(\d+)/(.*?)\.html', str(respData))

            scheme = 'https://www.alibaba.com/product-detail/'

            for path in allPaths:
                url = scheme + path[2] + "_" + path[0] + ".html"
                productsUrl.append(url)
        else:
            flag = False

        index += 1

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

import time
def getFileName(companyUrl):
    parsedUri = urlparse(companyUrl)
    host = "{uri.netloc}".format(uri=parsedUri)
    lastPart = os.path.basename(os.path.normpath(companyUrl)).replace(".html", "")
    nowTime = int(time.time())
    return host + "_" + lastPart + "_" + str(nowTime) + ".txt"


"""开始处理"""
print("Enter the company url:")

#companyUrl = input().strip()

print("Doing ......")

results = ""

productsUrl = getAllProductsUrl("https://younalchina.en.alibaba.com/productgrouplist-804089749/WPC_Wall_Panel.html")
print(productsUrl)

"""
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

print("Done!")
print("Saved in file: " + os.path.realpath(filename)) """








