# import asyncio
# import websockets

# async def hello(websocket, path):
#     name = await websocket.recv()
#     print(f"<<< {name}")

#     greeting = f"Hello {name}!"

#     await websocket.send(greeting)
#     print(f">>> {greeting}")

# async def main():
#     async with websockets.serve(hello, "127.0.0.1", 8677):
#         await asyncio.Future()  # run forever

# asyncio.run(main())

import threading
import time
from socket import *

serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', 4587))
serverSock.listen(5)
connectionSock, addr = serverSock.accept() 
print(str(addr),'에서 접속이 확인되었습니다.')

def send(sock):
    while True:
        senddata=input('>>>')
        senddata = senddata + "\n"
        sock.send(senddata.encode('utf-8'))
        print('전송완료')


def receive(sock):
    while True:
        try:
            recvdata = sock.recv(1024)
            if recvdata.decode('utf-8') == '/quit':
               sock.close()

            print('받은 데이터:', recvdata.decode('utf-8'))
        except:
            pass

sender = threading.Thread(target=send, args=(connectionSock,))
sender.daemon = True  #메인프로세스 종료시 같이 종료
receiver = threading.Thread(target=receive, args=(connectionSock,))
receiver.daemon = True

sender.start()
receiver.start()

while True:
    time.sleep(1)
    pass