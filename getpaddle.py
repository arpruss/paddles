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
                self.ser = None
                try:
                    self.ser = serial.Serial(p.device, baudrate=230400, timeout=timeout)
                    self.ser.reset_input_buffer()
                    t0 = time.time()
                    while time.time() < t0 + 2:
                        c = self.ser.read()
                        while c == b":" and time.time() < t0 + 2:
                            data = b""         
                            i = 0
                            while i < 6 and time.time() <= t0 + 2:
                                c = self.ser.read()
                                if c == b":":
                                    break
                                data += c
                            if i < 6:
                                continue
                            try:
                                if re.match(data.decode("ascii"), '[01][01][0-9A-F][0-9][A-F]'):
                                    return
                            except:
                                pass
                except:
                    pass
                finally:
                    try:
                        if self.ser is not None:
                            self.ser.close()
                    except:
                        pass
            raise Exception("Cannot open port")
        self.ser = serial.Serial(port, baudrate=230400)
		
    def getData(self):
        self.ser.reset_input_buffer()
        t0 = time.time()
        while self.timeout == 0 or t0 + self.timeout > time.time():
            c = self.ser.read()
            if c == b":":
                data = self.ser.read(6)
                try:
                    data = data.decode("ascii")
                    if re.match(data, '[01][01][0-9A-F][0-9][A-F]'):
                        return int(data[0]),int(data[1]),int(data[2:4],16)/255.,int(data[5:7],16)/255.
                except:
                    pass
        return 0,0,float("nan"),float("nan")
        
    def close(self):
        self.ser.close()

if __name__ == '__main__':
    paddles = Paddles()
    for i in range(100):
        print(paddles.getData())
