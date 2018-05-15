import serial
import time
import string
import sys
ser = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)
#ser.open()
start = time.clock()
try:
    while 1:
        end = time.clock()
        print('duty cycle is %s' %(end-start))
        start = time.clock()
        response = ser.readline()
        try:
            s_r = response
            temp = s_r.split(":")
            #print temp
            temp = temp[1].split(",")
            #print temp
            power = string.atof(temp[0])
            left_speed = string.atof(temp[1])
            right_speed = string.atof(temp[2])
            sonar = string.atof(temp[3].strip())
            print ('msg is %f %f %f %f' %(power, left_speed , right_speed, sonar))

            ser.write('RASPI:0.0,0.0\n')# %('50.0', '20.0'));
            print sys.argv[1], sys.argv[2]
            time.sleep(0.03);
        except:
            print response
        #print n

except KeyboardInterrupt:
    ser.close()