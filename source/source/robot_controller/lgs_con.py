import requests
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

def get_poi():
    global headers, token, userid, mappoi, groupcode, restype

    oheaders = headers
    oheaders["x-auth-token"] = token

    url = host + "/robot/b2b/v1.3/resource/group/" + groupcode + "/type/" + restype + "/latest"

    rtn = requests.get(url, headers=oheaders)
    res = rtn.json()
    #print("get_poi!!", res)
    if(str(res["resultCode"]) == "0114"):
        refresh_token()
        return get_poi()
    
    url2 = ""
    
    for pois in res["result"]["mapInfoList"]:
        if(pois["buildingIndex"] == "TORDER_GURO"):
            url2 = pois["mapUrl"]
            break
    
    rtn2 = requests.get(url2)
    resdata = rtn2.json()
    mappoi = resdata["customPointData"]

def refresh_token():
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

refresh_token()
get_poi()

def go_cancel(robotid):
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
        refresh_token()
        return go_cancel(robotid)
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
        refresh_token()
        return gohome(robotid)
    elif(str(res["resultCode"]) != "0000"):
        rtnvalue["code"] = 600
        rtnvalue["error"] = True
        if "message" in res["result"]:
            rtnvalue["msg"] = res["result"]["message"]

    return rtnvalue

def go_return(robotid):
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
        refresh_token()
        return go_return(robotid)
    elif(str(res["resultCode"]) != "0000"):
        rtnvalue["code"] = 600
        rtnvalue["error"] = True
        if "message" in res["result"]:
            rtnvalue["msg"] = res["result"]["message"]

    return rtnvalue

def go_charge(robotid):
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
        refresh_token()
        return go_charge(robotid)
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
        refresh_token()
        return go_charge(robotid)
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
        get_poi()
    else:
        print("get poi")

    callpoi = ""
    #print("delivery mappoi", mappoi)
    for poi in mappoi:
        if len(table) == 1 :
            table = "0" + table
        if(mappoi[poi]["name"]["kr"] == table):
            callpoi = mappoi[poi]["cpId"]
            break
    print("callpoi!!", callpoi)
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
            refresh_token()
            print("lgs delivery!!", table, robotid)
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
        refresh_token()
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


def device_list():
    global headers, token, userid

    oheaders = headers
    oheaders["x-auth-token"] = token
    url = host + "/robot/b2b/v1.1/device?pageIndex=0"

    rtn = requests.get(url, headers=oheaders)
    res = rtn.json()
    if(str(res["resultCode"]) == "0114"):
        refresh_token()
        return device_list()
    
    return res

