from robot_controller import lgs_con
import time

# print(lgscon.gohome("1790020038f416499fb5abf28e11a6834411287b"))
# print(lgscon.cancel("1790020038f416499fb5abf28e11a6834411287b"))
# time.sleep(5)
# print(lgscon.delivery("26", "1790020038f416499fb5abf28e11a6834411287b"))
# time.sleep(60)
# print(lgscon.gocancel("1790020038f416499fb5abf28e11a6834411287b"))
# time.sleep(60)
print(lgs_con.gocharge("1790020038f416499fb5abf28e11a6834411287b"))

time.sleep(10)
print(lgs_con.delivery("26", "1790020038f416499fb5abf28e11a6834411287b"))