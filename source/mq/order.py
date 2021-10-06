import config
import setdb
import time
import setmq
import sys
import vdcon
import dyccon
import lgscon
import nmrcon

queue2 = "robot_main"
cut_time = 60 * 5
now_ordercode = ""
now_count = 0
now_step = 1
run_time = 0
now_robot_step1 = ""
now_robot_step2 = ""
now_robot_step3 = ""


def selectRobot(rtype, rcorp):
    devices = setdb.getDevice()
    for device in devices:
        # print(str(device[10]) + " / " + device[6])
        if(device[10] == rtype and (rcorp == device[1] or rcorp == "")): # 1: 로봇팔 / 2: 서빙로봇
            if(device[6] == "Ready" or device[6] == "Home" or device[6] == "none"): #준비상태
                return device[3]
                break
    return ""

def getRobotStatus(deviceid):
    devices = setdb.getDevice()

    rtnvalue = {
        "status" : "",
        "pstatus" : "",
        "stype" : "",
        "id" : "",
        "appkey" : ""
    }

    for device in devices:
        if(deviceid == device[3]):
            rtnvalue["status"] = device[6]
            rtnvalue["pstatus"] = device[2]
            rtnvalue["stype"] = device[1]
            rtnvalue["id"] = device[3]
            rtnvalue["appkey"] = device[4]
            break
    
    return rtnvalue

def setStatus(ocode, step1, step2, step3, step4, status, now_count):
    setdb.setChangeOrder(ocode, step1, step2, step3, step4, status, now_count)
    setmq.send(queue2, {
        "tp" : "orderstatus",
        "id" : config.serverid,
        "ocode" : ocode,
        "step1" : step1,
        "step2" : step2,
        "step3" : step3,
        "step4" : step4,
        "status" : status,
        "nqty" : now_count
    })

while True:

    rows = setdb.getOrderOne()

    for row in rows:

        seq = row[0]
        otype = row[1]
        ocode = row[2]
        oname = row[3]
        omenu = row[4]
        step1 = row[5]
        step2 = row[6]
        step3 = row[7]
        step4 = row[8]
        status = row[9]
        oqty = row[12]
        otable = row[14]
        ice = 0
        ade = 0
        camera = 0

        if(omenu == "9"):
            omenu = "coffeeice"
            ice = 1

        if(omenu == "coffeeice" or omenu == "ade1" or omenu == "ade2" or omenu == "ade3" or omenu == "ade4" or omenu == "ade5" or omenu == "spacle"):
            ice = 1
        
        if(omenu == "ade1" or omenu == "ade2" or omenu == "ade3" or omenu == "ade4" or omenu == "ade5" or omenu == "spacle"):
            ade = 1

        if(ocode != now_ordercode):
            now_ordercode = ocode
            now_count = 0
            run_time = 0
            now_step = 1
            now_robot_step1 = ""
            now_robot_step2 = ""
            now_robot_step3 = ""

        if(otype == 1 or otype == 2): #뉴로메카 로봇팔 + LG 서빙로봇
            # print("start Robot + Serving")
            if(now_robot_step1 == ""):
                now_robot_step1 = selectRobot(1, "NMRA")
            if(now_robot_step2 == ""):
                now_robot_step2 = selectRobot(2, "LGSR")
                # if(str(otable) >= "13" and str(otable) <= "20"):
                #     now_robot_step2 = selectRobot(2, "LGSR")
                # else:
                #     now_robot_step2 = selectRobot(2, "")
            if(now_robot_step3 == ""):
                now_robot_step3 = selectRobot(3, "DYCM")
            
            step1status = getRobotStatus(now_robot_step1)  # 뉴로메카 상태정보
            step2status = getRobotStatus(now_robot_step2)  # LG 서빙로봇
            step3status = getRobotStatus(now_robot_step3)  # 동양 커피머신

            print("\n###########################\nstatus :: ", step1status["status"], "/ ", step2status["status"], "/ ", step3status["status"], " / now_step :: ", now_step, "/ step1 :: ", step1, "/ step2 :: ", step2 , " / run_time ", run_time , " / qty :: ", oqty , " / now :: ", now_count)

            if(now_count <= oqty):

                if(step1status["pstatus"] != ""):
                    arrStatus = step1status["pstatus"].split("|")
                else:
                    arrStatus = ["", "0", "0", "0"]

                ########### 음료제조 ###########
                if(now_step == 1):
                    ## 1. 커피머신 상태 체크 후 뉴로메카 로봇 구동
                    if(step1 == 0 and (step1status["status"] == "Ready" or step1status["status"] == "Home") and step3status["status"] == "Ready"):
                        print("Start step1")
                        setStatus(ocode, 1, step2, step3, step4, 1, 1)
                        nmrcon.start(10)
                        now_count = now_count + 1
                        step1 = 1
                        nmrcon.setvar(10, 610, 1)

                    ## 2. 홈위치 확인 및 비전카메라 위치 확인
                    if(step1 == 1 and arrStatus[3] == "1" and otype == 2 and now_count == 1):
                        print("step1 :: camera")
                        
                        nmrcon.setvar(10, 610, 2)
                        # if(step2status["stype"] == "LGSR"):
                        #     nmrcon.setvar(10, 610, 2)
                        # elif(step2status["stype"] == "VDCS"):
                        #     nmrcon.setvar(10, 610, 10)

                        time.sleep(5)
                        
                    ## 3. 컵배출
                    if(step1 == 1 and (arrStatus[3] == "2" or arrStatus[3] == "10" or otype == 1 or (otype == 2 and now_count > 1))):
                        if(ice == 1):
                            print("step1 :: icecup")
                            if(ade == 1):
                                dyccon.order("cup3")
                            else:
                                dyccon.order("cup1")

                            nmrcon.setvar(10, 610, 3)
                        else:
                            print("step1 :: hotcup")
                            dyccon.order("cup0")
                            nmrcon.setvar(10, 610, 4)

                        setStatus(ocode, 2, step2, step3, step4, 1, 1)

                    ## 4. 음료제조
                    if(step1 == 2 and (arrStatus[3] == "3" or arrStatus[3] == "4")):
                        if(ade == 1):
                            print("step2 :: ade")
                            nmrcon.setvar(10, 610, 6)
                            time.sleep(10)
                        else:
                            if(ice == 1):
                                print("step2 :: coffee ice")
                                nmrcon.setvar(10, 610, 11)
                                time.sleep(4)
                            else:
                                print("step2 :: coffee hot")
                                nmrcon.setvar(10, 610, 5)
                                time.sleep(4)

                        print("step3 :: ", omenu)
                        dyccon.order(omenu)
                        setStatus(ocode, 3, step2, step3, step4, 1, 1)
                    
                    ## 4. 음료 배치
                    if(step1 == 3 and (arrStatus[3] == "5" or arrStatus[3] == "6")):
                        print(step2status["stype"], otype, otable, flush=True)
                        if(otype == 2 and step2status["status"] == "Ready" and otable != "" and otable != "local"): # 서빙까지 보낼 경우 
                            if(step2status["stype"] == "LGSR"):
                                nmrcon.setvar(10, 610, 7)
                            elif(step2status["stype"] == "VDCS"):
                                nmrcon.setvar(10, 610, 9)
                            
                            nmrcon.setvar(10, 612, now_count)
                            setStatus(ocode, 4, step2, step3, step4, 1, 1)
                            
                        if(otype == 1 or (otable == "" and otable == "local")): # 음료제조만 할 경우 종료
                            nmrcon.setvar(10, 610, 8)
                            setStatus(ocode, 4, step2, step3, step4, 1, 1)

                    ## 5. 음료 제조 완료 or 새 음료 제조
                    if(step1 == 4 and (arrStatus[3] == "7" or arrStatus[3] == "8" or arrStatus[3] == "9")):
                        nmrcon.setvar(10, 610, 1)

                        if(now_count >= oqty):
                            if(arrStatus[3] == "8"):
                                setStatus(ocode, 9, step2, step3, step4, 9, 9)
                            else:
                                setStatus(ocode, 9, step2, step3, step4, 1, 1)
                                now_step = now_step + 1
                            
                            time.sleep(5)
                            nmrcon.stop(10)
                        else:
                            setStatus(ocode, 0, step2, step3, step4, 1, 1)

                            time.sleep(5)

            ########### 서빙 ###########
            if(now_step == 2 or (step1 == 9 and otype == 2)):
                ## 5. 서빙로봇 호출
                if(step2 == 0 and step2status["status"] == "Ready"):
                    if(step2status["stype"] == "LGSR"):
                        # lgscon.gohome(step2status["id"])
                        # time.sleep(3)
                        print(lgscon.delivery(str(otable), step2status["id"]))
                    if(step2status["stype"] == "VDCS"):
                        print(vdcon.delivery(str(otable), step2status["appkey"], step2status["id"]))

                    setStatus(ocode, 9, 1, step3, step4, 1, 1)
                ## 6. 서빙로봇 도착정보 확인
                if((step2status["status"] == "Arrive" or run_time >= cut_time) and step2 == 1):
                    setStatus(ocode, 9, 9, step3, step4, 9, 9)
                    print("End step2")
                else:
                    print("Ing step2")
                    
        elif(otype == 5): #음료만 출력
            if(now_robot_step1 == ""):
                now_robot_step1 = selectRobot(1, "NMRA")
            if(now_robot_step3 == ""):
                now_robot_step3 = selectRobot(3, "DYCM")

            step1status = getRobotStatus(now_robot_step1)
            step3status = getRobotStatus(now_robot_step3)

            if(step1 == 0 and (step1status["status"] == "Ready" or step1status["status"] == "Home") and step3status["status"] == "Ready"):
                print("Start step1")
                print("step3 :: ", omenu)
                dyccon.order(omenu)
                setStatus(ocode, 1, step2, step3, step4, 1, 1)

            if(step1 == 1 and run_time > 10):
                dyccon.order(omenu)
                setStatus(ocode, 9, step2, step3, step4, 9, 9)

        if(step1 > 0):
            run_time = run_time + 1

    print(time.strftime('%Y-%m-%d %H:%M:%S'), 'sleep', flush=True)
    print(arrStatus)
    time.sleep(1)      #1초단위로 실행