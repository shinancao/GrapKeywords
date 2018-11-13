#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import urllib.request
import re
import os

from urllib.parse import urlparse
import os.path

#获得所有分组列表的url
def getProductListUrls(companyUrl):
    allCategoryUrl = companyUrl
    if "/productlist.html" not in companyUrl:
        allCategoryUrl = companyUrl + "/productlist.html"

    if "https://" not in companyUrl and "http://" not in companyUrl:
        allCategoryUrl = "https://" + allCategoryUrl

    respData = getResponseData(allCategoryUrl)
    results = []


    firstUrls = re.findall(r'<li class=" first">\\n\\t\\t\\t<a href="(.*?)" title="', str(respData))
    subFirstUrls = re.findall(r'<li class="first"><a href="(.*?)" title="', str(respData))
    subUrls = re.findall(r'<li class=""><a href="(.*?)" title="', str(respData))
    listUrls = re.findall(r'<li class=" ">\\n\\t\\t\\t<a href="(.*?)" title="', str(respData))
    for urls in (firstUrls, subFirstUrls, subUrls, listUrls):
        if len(urls) > 0:
            for url in urls:
                results.append(companyUrl + url)

    return  results

#获得一个分类下所有商品详情的url
def getProductDetailUrls(productListUrl):
    parsedUri = urlparse(productListUrl)
    schemeAndProtocol = "{uri.scheme}://{uri.netloc}/".format(uri=parsedUri)
    paths = "{uri.path}".format(uri=parsedUri).split("/")
    temp = paths[1].split("-") #productgrouplist-803523792-1
    index = 1
    flag = True

    productsUrl = []

    while flag:
        print("index:" + str(index))
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
#companyUrl = "https://sysun.en.alibaba.com/productgrouplist-806535891/1_SPC_Flooring.html"

print("Doing ......")

#productUrls = getProductListUrls(companyUrl)

productUrls = ["https://sysun.en.alibaba.com/productgrouplist-806535891/1_SPC_Flooring.html"]


for productUrl in productUrls:
    detailUrls = getProductDetailUrls(productUrl)
    #一个产品列表生成一个文件
    results = ""
    print(detailUrls)
    for url in detailUrls:
        print(url)
        dict = getKeywordsAndTitle(url)
        if not (dict is None):
            results += "title:\n"
            results += dict["title"] + "\n"
            results += "keywords:\n"
            results += dict["keywords"] + "\n\n"
    filename = getFileName(productUrl)

    f = open(filename, "w")
    f.write(results)
    f.close()
    print(os.path.realpath(filename))


print("Done!")









