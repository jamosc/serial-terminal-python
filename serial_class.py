import serial, serial.tools.list_ports
from threading import Thread, Event
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class SerialClass(QObject):
    data_available = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.serialPort = serial.Serial()
        self.serialPort.timeout = 0.5
        self.baudratesDIC = {
        '1200':1200,
        '2400':2400,
        '4800':4800,
        '9600':9600,
        '19200':19200,
        '38400':38400,
        '57600':57600,
        '115200':115200
        }
        self.portList = []
        
        self.thread = None
        self.alive = Event()
    
    def update_ports(self):
        self.portList = [port.device for port in serial.tools.list_ports.comports()]

    def serial_connect(self):
        try:
            self.serialPort.open()
        except:
            self.data_available.emit('Serial error')
        if(self.serialPort.is_open):
            self.start_thread()

    def serial_disconnect(self):
        self.stop_thread()
        self.serialPort.close()

    def serial_readData(self):
        while (self.alive.isSet() and self.serialPort.is_open):
            data = self.serialPort.readline().decode("utf-8").strip()
            if(len(data)>1):
                self.data_available.emit(data)

    def serial_sendData(self,data):
        if(self.serialPort.is_open):
            message = str(data) + '\n'
            self.serialPort.write(message.encode())

    def start_thread(self):
        self.thread = Thread(target = self.serial_readData)
        self.thread.setDaemon(1)
        self.alive.set()
        self.thread.start()

    def stop_thread(self):
        if(self.thread is not None):
            self.alive.clear()
            self.thread.join()
            self.thread = None