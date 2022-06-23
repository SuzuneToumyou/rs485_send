#!/usr/bin/python3
# -*- coding: utf-8 -*

import pigpio
import serial
import time

ser_v = serial.Serial('/dev/ttyUSB0', 19200, timeout=None)

def senser_get(ser):

    d_ed = "big"

    s_code = b'\x02'
    s_ID = b'\x00'

    pi = pigpio.pi()
    addr = 0x0a

    try:
        h = pi.i2c_open(1,addr)
        pi.i2c_write_device(h, [0x4d])
        time.sleep(1)
        count, result = pi.i2c_read_device(h,2051)
        time.sleep(1)
        pi.i2c_close(h)
    except:
        count = -80

#    print(count)
#    print(result)

    if count <= 0: #device_error
        return (0)
    else:
        readbuff = bytes(result)

        s_bit = b"\x02"

        ser.write(s_bit)

        ser.write(s_code)

        ser.write(s_ID)

        for i in range(1025):
            ttmp = readbuff[i*2]
            msg = ttmp.to_bytes(1,d_ed)
            ser.write(msg)

            tttmp = readbuff[i*2+1]
            msg = tttmp.to_bytes(1,d_ed)
            ser.write(msg)

        tPEC = readbuff[2050]
        msg = tPEC.to_bytes(1,d_ed)
        ser.write(msg)

        msg = b"\x03"
        ser.write(msg)

        return(1)

if __name__ == "__main__":

    return_data = senser_get(ser_v)
    if return_data != 0:
        num = 0
        while return_data != 0 or num <= 3:
            return_data = senser_get(ser_v)
            num = num + 1
