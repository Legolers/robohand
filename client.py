### Client for Arduino ###

import speech_recognition as sr
import serial
import serial.tools.list_ports
import struct,time

# "{LETTER}":[]
GESTURES = {
    "A": [50,100,150,200,250,300],
    "B": [50,100,150,200,250,300],
    "C": [50,100,150,200,250,300],
    "D": [50,100,150,200,250,300],
    "E": [50,100,150,200,250,300],
    "F": [50,100,150,200,250,300],
    "G": [50,100,150,200,250,300],
    "H": [50,100,150,200,250,300],
    "I": [50,100,150,200,250,300],
    "J": [50,100,150,200,250,300],
    "K": [50,100,150,200,250,300],
    "L": [50,100,150,200,250,300],
    "M": [50,100,150,200,250,300],
    "N": [50,100,150,200,250,300],
    "O": [50,100,150,200,250,300],
    "P": [50,100,150,200,250,300],
    "Q": [50,100,150,200,250,300],
    "R": [50,100,150,200,250,300],
    "S": [50,100,150,200,250,300],
    "T": [50,100,150,200,250,300],
    "U": [50,100,150,200,250,300],
    "V": [50,100,150,200,250,300],
    "W": [50,100,150,200,250,300],
    "X": [50,100,150,200,250,300],
    "Y": [50,100,150,200,250,300],
    "Z": [50,100,150,200,250,300]
}





class Client:
    def __init__(self) -> None:
        self.rc = sr.Recognizer()

    def hear(self):
        string = None
        try:
            with sr.Microphone() as src:
                self.rc.adjust_for_ambient_noise(src)
                print("[INFO] Listening...")
                vc = self.rc.listen(src,phrase_time_limit=6)
                string = self.rc.recognize_google(vc)
                print("Interperted:",string)
        except Exception as e:
            print(e)
        return string

    def ui_init(self):
        ports = serial.tools.list_ports.comports()
        self.serial = serial.Serial()
        allPorts = []

        print("All available COM ports:")
        for port in ports:
            allPorts.append(str(port))
            print(str(port))

        selection = input("Enter COM Port > ")
        for port in allPorts:
            if port.startswith(selection):
                break

        self.serial.baudrate = 9600
        self.serial.port = selection


    def run(self):
        self.ui_init()

        self.serial.open()

        while 1:
            inter = self.hear()
            inter = inter
            

            if not inter:
                continue

            for letter in inter:
                packet = b''
                if letter == " ":
                    time.sleep(.5)
                    continue
                for item in GESTURES[letter.upper()]:
                    packet += struct.pack("<h",item)
                
                self.serial.write(packet)
                while 1:
                    if self.serial.in_waiting:
                        p_recv = self.serial.readline().decode().rstrip('\n')
                        if p_recv == "ACK":
                            print("ACK received.")
                            break
                        else:
                            print("BAD PACKET TYPE",p_recv)
                            break


    def debug(self):
        self.ui_init()
        self.serial.open()
        while 1:
            jo = input("Set Servo Positions [0-5] (Sep: ','): ")
            servos = jo.split(",")
            packet = b''
            for pos in servos:
                packet += struct.pack("<H",int(pos))
                
            self.serial.write(packet)
            print("SENT")
            try:
                while 1:
                    if self.serial.in_waiting:
                        p_rcv = self.serial.readline().decode().rstrip('\n')
                        print("RECV:",p_rcv)
            except KeyboardInterrupt:
                pass

    def debug1(self):
        self.ui_init()
        self.serial.open()

        gests = [
            [180,0,0,0,0,0],
            [180,180,0,0,0,0],
            [100,10,100,0,0,0],
            [100,100,100,100,0,0],
            [100,100,100,100,100,0],
        ]
        #
        # self.ui_init()
        while 1:
            
            input()
            for i in range(5):
                servos = gests[i]
                packet = b''
                for pos in servos:
                    packet += struct.pack("<H",int(pos))

                self.serial.write(packet)
                time.sleep(2)