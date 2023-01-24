import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QTextBrowser, QComboBox
from PyQt5.QtCore import QSize
from serial_class import SerialClass

class TerminalWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        #window config
        self.setMinimumSize(QSize(640, 480))    
        self.setWindowTitle("Python Serial Terminal") 

        #config button
        self.config_button = QPushButton('GRBL Configuration', self)
        self.config_button.resize(130, 25)
        self.config_button.move(490, 80)        
        self.config_button.clicked.connect(self.click_config)

        #clear output button
        self.clear_output_button = QPushButton('Clear Output', self)
        self.clear_output_button.resize(130, 25)
        self.clear_output_button.move(490, 120)
        self.clear_output_button.clicked.connect(self.click_clear_output)

        #ports dropdown button
        self.ports_button = QComboBox(self)
        self.ports_button.resize(130, 25)
        self.ports_button.move(20, 10)

        #update ports button
        self.update_ports_button = QPushButton('Update Ports', self)
        self.update_ports_button.resize(130, 25)
        self.update_ports_button.move(20, 40)
        self.update_ports_button.clicked.connect(self.click_update_ports)

        #baudrates dropdown button
        self.baud_button = QComboBox(self)
        self.baud_button.resize(130, 25)
        self.baud_button.move(170, 25)

        #connect button
        self.connect_button = QPushButton('Connect Device', self)
        self.connect_button.resize(130, 25)
        self.connect_button.move(340, 10)
        self.connect_button.clicked.connect(self.click_connect)

        #disconnect button
        self.disconnect_button = QPushButton('Disconnect Device', self)
        self.disconnect_button.resize(130, 25)
        self.disconnect_button.move(340, 40)
        self.disconnect_button.clicked.connect(self.click_disconnect)

        #input line
        self.input_line = QLineEdit(self)
        self.input_line.resize(520, 20)
        self.input_line.move(20, 440)
        self.input_line.returnPressed.connect(self.click_input)

        #input button
        self.input_button = QPushButton('Enter', self)
        self.input_button.resize(70, 22)
        self.input_button.move(550, 439)      
        self.input_button.clicked.connect(self.click_input)

        #output screen
        self.output_window = QTextBrowser(self, readOnly=True, overwriteMode=True)
        self.output_window.resize(450, 360)
        self.output_window.move(20, 70)

        #serial device
        self.serial = SerialClass()
        self.baud_button.addItems(self.serial.baudratesDIC.keys())
        self.baud_button.setCurrentText('115200')
        self.click_update_ports()
        self.serial.data_available.connect(self.update_output)

    #updates the output window with data received from serial comm
    def update_output(self,data):
        self.output_window.append(data)
        self.output_window.moveCursor(QtGui.QTextCursor.End)

    #update ports is clicked
    def click_update_ports(self):
        self.serial.update_ports()
        self.ports_button.clear()
        self.ports_button.addItems(self.serial.portList)

    #connect device is clicked
    def click_connect(self):
        self.connect_button.setEnabled(False)
        self.output_window.insertPlainText('\n'+'Connecting...')
        port = self.ports_button.currentText()
        baud = self.baud_button.currentText()
        self.serial.serialPort.port = port
        self.serial.serialPort.baudrate = baud
        self.serial.serial_connect()
        if(self.serial.serialPort.is_open):
            self.output_window.insertPlainText(' Connected'+'\n')
        else:
            self.output_window.insertPlainText('\n'+'Could not connected'+'\n')
            self.connect_button.setEnabled(True)
        self.output_window.moveCursor(QtGui.QTextCursor.End)
        
    #disconnect device is clicked
    def click_disconnect(self):
        self.connect_button.setEnabled(True)
        self.serial.serial_disconnect()

    #input button or enter is clicked
    def click_input(self):
        data = self.input_line.text()
        self.output_window.insertPlainText('\n'+self.input_line.text()+'\n')
        self.output_window.moveCursor(QtGui.QTextCursor.End)
        self.input_line.clear()
        self.serial.serial_sendData(data)

    #grbl configuration is clicked
    def click_config(self):
        self.output_window.insertPlainText('\n'+'$$'+'\n')
        self.output_window.moveCursor(QtGui.QTextCursor.End)
        self.serial.serial_sendData('$$')

    #clear output is clicked
    def click_clear_output(self):
        self.output_window.clear()

    #closes the thread when the serial comm is closed
    def close_event(self,e):
        self.serial.serial_disconnect()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    terminal = TerminalWindow()
    terminal.show()
    sys.exit(app.exec_())
