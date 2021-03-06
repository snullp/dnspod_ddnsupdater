#!/usr/bin/python
#-*- coding:utf-8 -*-

import httplib,urllib
import json

def buildquery(id,token,did=None):
    params = dict(
        login_token="{},{}".format(id,token),
        format="json"
    )
    if did!=None: params["domain_id"]=did
    return params

def query(params,api):
    headers = {"User-Agent": "Null's id finder/0.0.1 (snullp@gmail.com)","Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
    conn = httplib.HTTPSConnection("dnsapi.cn")
    conn.request("POST", api, urllib.urlencode(params), headers)
    response = conn.getresponse().read()
    conn.close()
    return response

token_id = raw_input("API ID? ")
token = raw_input("API Token? ")

try:
    params = buildquery(token_id,token)
    ret = json.loads(query(params,"/Domain.List"))
    if ret.get("status",{}).get("code")!="1": raise Exception(ret.get("status",{}).get("message"))
    domains = ret.get("domains",[])
    for domain in domains:
        print domain["name"] + " : " + str(domain["id"])
        params = buildquery(token_id,token,domain["id"])
        ret = json.loads(query(params,"/Record.List"))
        if ret.get("status",{}).get("code")!="1": raise Exception(ret.get("status",{}).get("message"))
        records = ret.get("records",[])
        for record in records:
            #filter A record here
            if record["type"] == "A": print "  " + record["name"] + " : " + str(record["id"])
except Exception as e:
    print "Got exception: " + str(e)
