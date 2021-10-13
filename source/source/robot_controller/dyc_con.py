import sys
import time
from socket import *
import numpy as np
import time
import binascii

#동양커피머신 상태 가져오기
host = "192.168.103.140"
gseq = 0
gcrc_16 = 0x8005
table_crc = []

def build_table16(aPoly):
    for i in range(0, 256):
        data = np.uint16(i << 8)
        accum = 0
        for j in range(0, 8):
            if(((data ^ accum) & 0x8000) != 0):
                accum = np.uint16((accum << 1) ^ np.uint16(aPoly))
            else:
                accum <<= 1
            data <<= 1

        table_crc.append(np.uint16(accum))
    
    # print(table_crc)

def crc_16(data):
    accum = 0
    for i in range(0, len(data)):
        accum = np.uint16(accum << 8) ^ table_crc[(accum >> 8) ^ data[i]]

    return accum

build_table16(gcrc_16)

def send_packet(cmd, data, hport):
    global gseq, host

    gseq = (gseq + 1) % 256

    tmp = b'\x02'   # stx
    tmp += bytes([gseq])   # seq
    tmp += b'\x0B'   # sender id
    tmp += b'\x01'   # sender idx
    tmp += b'\x0E'   # receiver id
    tmp += b'\x01'   # receiver idx
    tmp += cmd
    tmp += bytes([int(len(data) / 256)])
    tmp += bytes([int(len(data) % 256)])
    if(data != b''):
        tmp += data
    
    tmp2 = b''
    for i in range(1, len(data) + 9):
        tmp2 += bytes([tmp[i]])

    tmp3 = crc_16(tmp2)

    tmp4 = int(tmp3 / 256)
    tmp5 = int(tmp3 % 256)

    tmp += bytes([int(tmp4)])
    tmp += bytes([int(tmp5)])

    tmp += b'\x03'

    print("request data :: ", binascii.hexlify(tmp))

    try:
        clso = socket(AF_INET, SOCK_STREAM)
        clso.connect((host, hport))
        print("connect")

        clso.send(tmp)
        print("send message")

        data = clso.recv(2028)
        print("response data :: ", binascii.hexlify(data))

        clso.close()
    except:
        print(sys.exc_info())
        return ""
    else:
        return binascii.hexlify(data)


def order(order):

    try_count = 0
    rtnval = {
        "code" : 200,
        "msg" : "ok",
        "result" : b''
    }

    while True:
        try:
            if(order == "cup0"): #일반컵
                rtn2 = send_packet(b'\xB4', b'\x11', 10201)
                if(rtn2[18:20] == b'00'):
                    return rtnval
                    break
            elif(order == "cup1"): #얼음컵
                rtn2 = send_packet(b'\xB4', b'\x12', 10201)
                if(rtn2[18:20] == b'00'):
                    time.sleep(2)
                    rtn3 = send_packet(b'\xB4', b'\x13\x21', 10201)

                    if(rtn3[18:20] == b'00'):
                        return rtnval
                        break

            elif(order == "cup2"): #얼음
                rtn = send_packet(b'\xB4', b'\x13\x21', 10201)
                if(rtn[18:20] == b'00'):
                    return rtnval
                    break

            elif(order == "cup3"): #얼음컵 1/2
                rtn2 = send_packet(b'\xB4', b'\x12', 10201)
                if(rtn2[18:20] == b'00'):
                    time.sleep(2)
                    rtn3 = send_packet(b'\xB4', b'\x13\x1b', 10201)

                    if(rtn3[18:20] == b'00'):
                        return rtnval
                        break
                
            elif(order == "ade1"): #ade1
                print("start ade 1 : valve")
                rtn2 = send_packet(b'\xB7', b'\x27\x01\x65', 10202)
                time.sleep(1)
                rtn4 = send_packet(b'\xB5', b'\x26\x01\x15', 10200)
                time.sleep(3)
                print("\nstart ade 1 : make")
                rtn3 = send_packet(b'\xB5', b'\x21\x00\x19', 10200)

                if(rtn2[18:20] == b'00' and rtn3[18:20] == b'00' and rtn4[18:20] == b'00'):
                    time.sleep(5)
                    rtn4 = send_packet(b'\xB5', b'\x26\x01\x10', 10200)

                    if(rtn4[18:20] == b'00'):
                        return rtnval
                        break
                    else:
                        rtnval["code"] = 601
                        rtnval["message"] = "ade make error"
                        return rtnval
                        break

            elif(order == "ade2"): #ade2
                print("start ade 2 : valve")
                rtn2 = send_packet(b'\xB7', b'\x27\x02\x65', 10202)
                time.sleep(1)
                rtn4 = send_packet(b'\xB5', b'\x26\x02\x10', 10200)
                time.sleep(3)
                print("\nstart ade 2 : make")
                rtn3 = send_packet(b'\xB5', b'\x22\x00\x19', 10200)

                if(rtn2[18:20] == b'00' and rtn3[18:20] == b'00' and rtn4[18:20] == b'00'):
                    time.sleep(5)
                    rtn4 = send_packet(b'\xB5', b'\x26\x02\x10', 10200)

                    if(rtn4[18:20] == b'00'):
                        return rtnval
                        break
                    else:
                        rtnval["code"] = 601
                        rtnval["message"] = "ade make error"
                        return rtnval
                        break

            elif(order == "ade3"): #ade3
                print("start ade 3 : valve")
                rtn2 = send_packet(b'\xB7', b'\x27\x03\x65', 10202)
                time.sleep(1)
                rtn4 = send_packet(b'\xB5', b'\x26\x05\x15', 10200)
                time.sleep(3)
                print("\nstart ade 3 : make")
                rtn3 = send_packet(b'\xB5', b'\x23\x00\x19', 10200)

                if(rtn2[18:20] == b'00' and rtn3[18:20] == b'00' and rtn4[18:20] == b'00'):
                    time.sleep(5)
                    rtn4 = send_packet(b'\xB5', b'\x26\x05\x10', 10200)

                    if(rtn4[18:20] == b'00'):
                        return rtnval
                        break
                    else:
                        rtnval["code"] = 601
                        rtnval["message"] = "ade make error"
                        return rtnval
                        break

            elif(order == "ade4"): #ade4
                print("start ade 4 : valve")
                rtn2 = send_packet(b'\xB7', b'\x27\x04\x65', 10202)
                time.sleep(1)
                rtn4 = send_packet(b'\xB5', b'\x26\x04\x15', 10200)
                time.sleep(3)
                print("\nstart ade 4 : make")
                rtn3 = send_packet(b'\xB5', b'\x24\x00\x19', 10200)

                if(rtn2[18:20] == b'00' and rtn3[18:20] == b'00' and rtn4[18:20] == b'00'):
                    time.sleep(6)
                    rtn4 = send_packet(b'\xB5', b'\x26\x04\x10', 10200)

                    if(rtn4[18:20] == b'00'):
                        return rtnval
                        break
                    else:
                        rtnval["code"] = 601
                        rtnval["message"] = "ade make error"
                        return rtnval
                        break

            elif(order == "ade5"): #ade5
                print("start ade 5 : valve")
                rtn2 = send_packet(b'\xB7', b'\x27\x05\x65', 10202)
                time.sleep(1)
                rtn4 = send_packet(b'\xB5', b'\x26\x03\x15', 10200)
                time.sleep(3)
                print("\nstart ade 5 : make")
                rtn3 = send_packet(b'\xB5', b'\x25\x00\x19', 10200)
                if(rtn2[18:20] == b'00' and rtn3[18:20] == b'00' and rtn4[18:20] == b'00'):
                    time.sleep(6)
                    rtn4 = send_packet(b'\xB5', b'\x26\x03\x10', 10200)

                    if(rtn4[18:20] == b'00'):
                        return rtnval
                        break
                    else:
                        rtnval["code"] = 601
                        rtnval["message"] = "ade make error"
                        return rtnval
                        break
            
            elif(order == "spacle"): #clear
                print("start clear")

                rtn2 = send_packet(b'\xB7', b'\x27\x02\x30', 10202)
                if(rtn2[18:20] == b'00'):
                    time.sleep(1)
                    print("\nade Make Start")
                    rtn4 = send_packet(b'\xB5', b'\x26\x02\x25', 10200)

                    if(rtn4[18:20] == b'00'):
                        return rtnval
                        break
                    else:
                        rtnval["code"] = 601
                        rtnval["message"] = "ade make error"
                        return rtnval
                        break

            elif(order == "coffee"):                
                send_packet(b'\xB9', b'\x00\x00\x00\x80', 10203)
                time.sleep(1)
                rtn2 = send_packet(b'\xB6', b'\x04\x02\x41\x4d\x65\x00\x60\x00\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 10203)
                if(rtn2[18:20] == b'00'):
                    return rtnval
                    break
            elif(order == "coffeedouble"):
                send_packet(b'\xB9', b'\x00\x00\x00\x80', 10203)
                time.sleep(2)
                rtn2 = send_packet(b'\xB6', b'\x04\x02\x41\x4d\x69\x00\x40\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 10203)
                if(rtn2[18:20] == b'00'):
                    return rtnval
                    break
            elif(order == "espresso"):
                send_packet(b'\xB9', b'\x00\x00\x00\x80', 10203)
                time.sleep(1)
                rtn2 = send_packet(b'\xB6', b'\x04\x02\x41\x4d\x50\x00\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 10203)
                if(rtn2[18:20] == b'00'):
                    return rtnval
                    break
            elif(order == "coffeeice"):
                send_packet(b'\xB9', b'\x00\x00\x00\x80', 10203)
                time.sleep(1)
                rtn2 = send_packet(b'\xB6', b'\x04\x02\x49\x41\x65\x00\x40\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 10203)
                if(rtn2[18:20] == b'00'):
                    return rtnval
                    break
            elif(order == "hotchoco"):
                send_packet(b'\xB9', b'\x00\x00\x00\x80', 10203)
                time.sleep(1)
                rtn2 = send_packet(b'\xB6', b'\x04\x02\x43\x4d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\x00\x85\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 10203)
                if(rtn2[18:20] == b'00'):
                    return rtnval
                    break
            elif(order == "capuccino"):
                send_packet(b'\xB9', b'\x00\x00\x00\x80', 10203)
                time.sleep(1)
                rtn2 = send_packet(b'\xB6', b'\x04\x02\x43\x41\x65\x00\x50\x00\x00\x00\x02\x00\x30\x00\x00\x00\x00\x00\x30\x00\x30\x00\x00\x00\x00\x00\x00\x00\x00', 10203)
                if(rtn2[18:20] == b'00'):
                    return rtnval
                    break
            elif(order == "latte"):
                send_packet(b'\xB9', b'\x00\x00\x00\x80', 10203)
                time.sleep(1)
                rtn2 = send_packet(b'\xB6', b'\x04\x02\x43\x4d\x65\x00\x50\x00\x00\x00\x02\x00\x30\x00\x00\x00\x00\x00\x30\x00\x30\x00\x00\x00\x00\x00\x00\x00\x00', 10203)
                if(rtn2[18:20] == b'00'):
                    return rtnval
                    break
            elif(order == "lattenosugar"):
                send_packet(b'\xB9', b'\x00\x00\x00\x80', 10203)
                time.sleep(1)
                rtn2 = send_packet(b'\xB6', b'\x04\x02\x43\x4d\x65\x00\x50\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x35\x00\x00\x00\x00\x00\x00\x00\x00', 10203)
                if(rtn2[18:20] == b'00'):
                    return rtnval
                    break
            elif(order == "mocha"):
                send_packet(b'\xB9', b'\x00\x00\x00\x80', 10203)
                time.sleep(1)
                rtn2 = send_packet(b'\xB6', b'\x04\x02\x43\x4d\x65\x00\x50\x00\x00\x00\x00\x00\x00\x00\x15\x00\x00\x00\x18\x00\x40\x00\x00\x00\x00\x00\x00\x00\x00', 10203)
                if(rtn2[18:20] == b'00'):
                    return rtnval
                    break

        except:
            print("error")
        
        try_count = try_count + 1

        if(try_count > 40):
            rtnval["code"] = 900
            rtnval["data"] = "time out"
            return rtnval
            break

        time.sleep(1)
    
    # while True:

# def order(order):

def status():
    cup = 1
    cupout = 1
    icup = 1
    icupout = 1
    coffee = 1
    ade = 1
    rtnval = "Ready"

    rtn = send_packet(b'\xB1', b'\x10', 10201)    
    if(rtn[18:20] == b'01'):
        if(rtn[20:22] == b'00'):
            rtnval = "CupEmpty"

        if(rtn[22:24] == b'01'):
            rtnval = "CupOut"

        if(rtn[24:26] == b'00'):
            rtnval = "IcecupEmpty"
        
        if(rtn[26:28] == b'01'):
            rtnval = "IcecupEmpty"

    rtn2 = send_packet(b'\xB2', b'', 10203)
    if(rtn2[18:20] == b'ff'):
        rtnval = "CoffeeError"

    rtn3 = send_packet(b'\xB2', b'', 10200)
    if(rtn3[18:20] == b'21'):
        rtnval = "AdeError"

    rtn4 = send_packet(b'\xB2', b'', 10202)
    if(rtn4[18:20] == b'21'):
        rtnval = "AdeError"

    return rtnval

# def status():


# print(order("cup1"))
# print(order("coffeedouble"))