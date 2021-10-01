import config
import requests
import sys
import time
import os
import json

token = ""
userid = "000085KR2105280234962"
reftoken = "ec89a20f2860091c04054f339969ab58704da234229b4fbd887f9daf3d6da9acd7ac23d38dcb53dca2cc7a9a4eacafd5"
groupcode = "101"
restype = "POI_LGIDM"

headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'x-api-key' : '6865c931892043f6bc7a6cc995aac762',
    'x-biz-channel' : 'CHN000085',
    'x-country-code' : 'KR',
    'x-language-code' : 'ko-KR',
    'x-message-id' : 'infiniq_test',
    'x-user-no' : userid,
    'x-user-role' : 'ADM085001'
}

mappoi = {}

host = "https://kic-svc.lgerobot.com"

def getpoi():
    global headers, token, userid, mappoi, groupcode, restype

    oheaders = headers
    oheaders["x-auth-token"] = token

    url = host + "/robot/b2b/v1.3/resource/group/" + groupcode + "/type/" + restype + "/latest"

    rtn = requests.get(url, headers=oheaders)
    res = rtn.json()
    
    if(str(res["resultCode"]) == "0114"):
        refreshtoken()
        return getpoi()
    
    url2 = ""
    
    for pois in res["result"]["mapInfoList"]:
        if(pois["buildingIndex"] == "TORDER_GURO"):
            url2 = pois["mapUrl"]
            break
    
    rtn2 = requests.get(url2)
    resdata = rtn2.json()
    mappoi = resdata["customPointData"]


def refreshtoken():
    global headers, token, userid

    print("refreshtoken !!")

    oheaders = headers
    oheaders["x-auth-token"] = token

    url2 = host + "/robot/b2b/v1.1/user/"+ userid +"/session"
    data2 = {
        "refreshToken" : reftoken
    }
    rtn2 = requests.put(url2, headers=oheaders, data=json.dumps(data2))
    res2 = rtn2.json()
    token = res2["result"]["authToken"]


def gocancel(robotid):
    global headers, token, userid
    
    rtnvalue = {
        "code" : 200,
        "error" : False,
        "msg" : ""
    }

    url = host + "/robot/b2b/v1.1/device/"+ robotid +"/control"
    
    oheaders = headers
    oheaders["x-auth-token"] = token
    data = {
        "ctrlKey" : "operationState",
        "command" : "Operation",
        "dataSetList": [ 
            {
                "deviceState.operationState.main" : "23"
            }
        ]
    }

    rtn = requests.post(url, headers=oheaders, data=json.dumps(data))
    res = rtn.json()

    if(str(res["resultCode"]) == "0114"):
        refreshtoken()
        return gocancel(robotid)
    elif(str(res["resultCode"]) != "0000"):
        rtnvalue["code"] = 600
        rtnvalue["error"] = True
        if "message" in res["result"]:
            rtnvalue["msg"] = res["result"]["message"]

    return rtnvalue

def gohome(robotid):
    global headers, token, userid

    rtnvalue = {
        "code" : 200,
        "error" : False,
        "msg" : ""
    }

    url = host + "/robot/b2b/v1.1/device/"+ robotid +"/control"
    
    oheaders = headers
    oheaders["x-auth-token"] = token
    data = {
        "ctrlKey" : "operationState",
        "command" : "Operation",
        "dataSetList": [ 
            {
                "deviceState.operationState.main" : "22"
            }
        ]
    }

    rtn = requests.post(url, headers=oheaders, data=json.dumps(data))
    res = rtn.json()

    if(str(res["resultCode"]) == "0114"):
        refreshtoken()
        return gohome(robotid)
    elif(str(res["resultCode"]) != "0000"):
        rtnvalue["code"] = 600
        rtnvalue["error"] = True
        if "message" in res["result"]:
            rtnvalue["msg"] = res["result"]["message"]

    return rtnvalue

def goreturn(robotid):
    global headers, token, userid

    rtnvalue = {
        "code" : 200,
        "error" : False,
        "msg" : ""
    }

    url = host + "/robot/b2b/v1.1/device/"+ robotid +"/control"
    
    oheaders = headers
    oheaders["x-auth-token"] = token
    data = {
        "ctrlKey" : "operationState",
        "command" : "Operation",
        "dataSetList": [ 
            {
                "deviceState.operationState.main" : "24"
            }
        ]
    }

    rtn = requests.post(url, headers=oheaders, data=json.dumps(data))
    res = rtn.json()

    if(str(res["resultCode"]) == "0114"):
        refreshtoken()
        return goreturn(robotid)
    elif(str(res["resultCode"]) != "0000"):
        rtnvalue["code"] = 600
        rtnvalue["error"] = True
        if "message" in res["result"]:
            rtnvalue["msg"] = res["result"]["message"]

    return rtnvalue

def gocharge(robotid):
    global headers, token, userid

    rtnvalue = {
        "code" : 200,
        "error" : False,
        "msg" : ""
    }

    url = host + "/robot/b2b/v1.1/device/"+ robotid +"/control"
    
    oheaders = headers
    oheaders["x-auth-token"] = token
    data = {
        "ctrlKey" : "operationState",
        "command" : "Operation",
        "dataSetList": [ 
            {
                "deviceState.operationState.main" : "20"
            }
        ]
    }

    rtn = requests.post(url, headers=oheaders, data=json.dumps(data))
    res = rtn.json()

    if(str(res["resultCode"]) == "0114"):
        refreshtoken()
        return gocharge(robotid)
    elif(str(res["resultCode"]) != "0000"):
        rtnvalue["code"] = 600
        rtnvalue["error"] = True
        if "message" in res["result"]:
            rtnvalue["msg"] = res["result"]["message"]

    return rtnvalue


def cancel(robotid):
    global headers, token, userid

    rtnvalue = {
        "code" : 200,
        "error" : False,
        "msg" : ""
    }

    url = host + "/robot/b2b/v1.1/device/"+ robotid +"/control"
    
    oheaders = headers
    oheaders["x-auth-token"] = token
    data = {
        "ctrlKey" : "location",
        "command" : "Operation",
        "dataSetList": [ 
            {
                "deviceState.location" : "0"
            }
        ]
    }

    rtn = requests.post(url, headers=oheaders, data=json.dumps(data))
    res = rtn.json()

    if(str(res["resultCode"]) == "0114"):
        refreshtoken()
        return gocharge(robotid)
    elif(str(res["resultCode"]) != "0000"):
        rtnvalue["code"] = 600
        rtnvalue["error"] = True
        if "message" in res["result"]:
            rtnvalue["msg"] = res["result"]["message"]

    return rtnvalue


def delivery(table, robotid):
    global headers, token, userid

    rtnvalue = {
        "code" : 200,
        "error" : False,
        "msg" : ""
    }

    if(mappoi == {}):
        print("start getpoi()")
        getpoi()
    else:
        print("get poi")

    callpoi = ""
    
    for poi in mappoi:
        if(mappoi[poi]["name"]["kr"] == table):
            callpoi = mappoi[poi]["cpId"]
            break
    
    if(callpoi != ""):
        url = host + "/robot/b2b/v1.1/device/"+ robotid +"/control"
        
        oheaders = headers
        oheaders["x-auth-token"] = token
        data = {
            "ctrlKey" : "location",
            "command" : "Serving",
            "dataSetList": [ 
                {
                    "deviceState.location.poiId": callpoi
                }
            ]
        }

        rtn = requests.post(url, headers=oheaders, data=json.dumps(data))
        res = rtn.json()

        if(str(res["resultCode"]) == "0114"):
            refreshtoken()
            return delivery(table, robotid)
        elif(str(res["resultCode"]) != "0000"):
            rtnvalue["code"] = 600
            rtnvalue["error"] = True
            if "message" in res["result"]:
                rtnvalue["msg"] = res["result"]["message"]

    else:
        rtnvalue["code"] = 800
        rtnvalue["error"] = True
        rtnvalue["msg"] = "poi data null"

    return rtnvalue


def status(robotid):
    global headers, token, userid

    rtnvalue = {
        "status" : "none",
        "battery" : 100,
        "x" : 0,
        "y" : 0,
        "a" : 0,
        "online": False
    }

    oheaders = headers
    oheaders["x-auth-token"] = token

    url = host + "/robot/b2b/v1.1/device/" + robotid

    rtn = requests.get(url, headers=oheaders)
    res = rtn.json()
    
    if(str(res["resultCode"]) == "0114"):
        refreshtoken()
        return status(robotid)
    
    resn = res["result"]["snapshot"]
    if(resn["deviceState"]["operationState"]["main"] == "STANDBY" and res["result"]["poiNameInOperation"] == "homepoi"):
        rtnvalue["status"] = "Ready"
    elif(resn["deviceState"]["operationState"]["main"] == "STANDBY" and res["result"]["poiNameInOperation"] == "chargepoi"):
        rtnvalue["status"] = "Charge"
    elif(resn["deviceState"]["operationState"]["move"] == 1):
        rtnvalue["status"] = "Moving"
    elif(resn["deviceState"]["operationState"]["main"] == "DELIVERY" and resn["deviceState"]["operationState"]["sub"] == "DISTRIBUTION_CONFIRM"):
        rtnvalue["status"] = "Arrive"
    else:
        rtnvalue["status"] = resn["deviceState"]["operationState"]["main"]
    
    rtnvalue["battery"] = resn["deviceState"]["partState"]["battery"]["level"]
    rtnvalue["x"] = resn["deviceState"]["location"]["x"]
    rtnvalue["y"] = resn["deviceState"]["location"]["y"]
    rtnvalue["a"] = resn["deviceState"]["location"]["degree"]
    rtnvalue["online"] = resn["online"]

    return rtnvalue


def devicelist():
    global headers, token, userid

    oheaders = headers
    oheaders["x-auth-token"] = token
    url = host + "/robot/b2b/v1.1/device?pageIndex=0"

    rtn = requests.get(url, headers=oheaders)
    res = rtn.json()
    if(str(res["resultCode"]) == "0114"):
        refreshtoken()
        return devicelist()
    
    return res

