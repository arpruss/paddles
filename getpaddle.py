import serial
import time
import serial.tools.list_ports
import re
from math import isnan 

class Paddles:
    def __init__(self, port=None, timeout=0.1):
        self.timeout = timeout
        if port is None:
            ports = serial.tools.list_ports.comports()
            for p in ports:
                try:
                    self.ser = serial.Serial(p.device, baudrate=230400, timeout=1)
                    self.ser.readline()
                    l = self.ser.readline().decode("ascii")
                    if re.match("[LR][0-9]+", l):
                        return
                except:
                    pass
            raise Exception("Cannot open port")
        self.ser = serial.Serial(port, baudrate=230400)
		
    def getPaddle(self, side):
        self.ser.reset_input_buffer()
        t0 = time.time()
        while self.timeout == 0 or t0 + self.timeout > time.time():
            line = self.ser.readline().decode("ascii")
            if line[0] == side:
                return float(line[1:])/1023.
        return float("nan")

    def getPaddles(self):
        self.ser.reset_input_buffer()
        t0 = time.time()
        paddles = [float("nan"), float("nan")]
        while (isnan(paddles[0]) or isnan(paddles[1])) and (self.timeout == 0 or t0 + self.timeout > time.time()) :
            line = self.ser.readline().decode("ascii")
            if line[0] == "R":
                paddles[1] = float(line[1:])/1023.
            elif line[0] == "L":
                paddles[0] = float(line[1:])/1023.
        return paddles

if __name__ == '__main__':
    paddles = Paddles()
    for i in range(100):
        print(paddles.getPaddle("L"), paddles.getPaddle("R"))
        print(paddles.getPaddles())
