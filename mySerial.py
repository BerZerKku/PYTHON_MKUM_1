# -*- coding: cp1251 -*-
'''
Created on 24.12.2012

@author: Shcheblykin
'''
import sys
import serial
from PyQt4 import QtGui
from PyQt4 import QtCore
import time


class mySerial(QtGui.QWidget):
    ''' class
    
        Widget ������ � ���-������.
        ������� ����������� ������ ��������� ������ � �������,
        ��������� ���������� ������, �������� � �������� �����.
        ����������/������������ ���-�� ��������� �� �����.
    '''
    def __init__(self, port='COM1', baudrate=1200, bytesize=serial.EIGHTBITS,
                 parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_TWO,
                 parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.PARITY = {'N': 'None', 'O': 'Odd', 'E': 'Even', \
                       'M': 'Mark', 'S': 'Space'}
        
        # ��������� �������������� ������� ����
        flag = QtCore.Qt.Window
        flag |= QtCore.Qt.MSWindowsFixedSizeDialogHint
        self.setWindowFlags(flag)
        
        # ���� ������� ���������
        self._modify = False
        
        # ��������� ��������� �����
        self.settings = {}
        self.setPort(port)
        self.setBaudRate(baudrate)
        self.setByteSize(bytesize)
        self.setParity(parity)
        self.setStopBits(stopbits)
        
        # �������� ��������� �������
        self.createWidget()
        
        # ���������������� ����
        self._port = serial.Serial()
        self._port.setTimeout(0)
        self.setCom("55 AA 02 00 02")
        
        # ���� �������� ������� (True - ���� �������)
        self._bRead = False
        # ����� �������� ��������� ����� �������� ���������
        self._cnt = 0
        # ������ ������
        self._data = []
        # ���-��� ���� ������
        self._lenght = 0
        # ����������� �����
        self._crc = 0
        
        # ������ �����������
        self._timerTr = QtCore.QTimer()
        self._timerTr.setInterval(500)
        self._timerTr.timeout.connect(self._cycleTr)
        
        # ������ ���������
        self._timerRc = QtCore.QTimer()
        self._timerRc.setInterval(5)
        self._timerRc.timeout.connect(self._cycleRc)
        
        # ����
        self._clock = QtCore.QTime.currentTime()
            
    def openPort(self):
        ''' (self) -> bool
        
            ������ ������ � ������. � ������ ������ ���������� False.
        '''
        self._port.setPort(self.settings['port'])
        self._port.setBaudrate(self.settings['baudrate'])
        self._port.setByteSize(self.settings['bytesize'])
        self._port.setParity(self.settings['parity'])
        self._port.setStopbits(self.settings['stopbits'])
        
        try:
            self._port.open()
            self._timerTr.start()
            self._timerRc.start()
        except:
            print self.openPort
            print "�� ������� ������� ����",
            
    def closePort(self):
        ''' (self) -> bool
        
            ��������� ������ � ������. � ������ ������ ���������� False.
        '''
        try:
            self._port.close()
            self._timerTr.stop()
            self._timerRc.stop()
        except:
            print self.closePort
            print "�� ������� ������� ����"
            raise
    
    def _cycleRc(self):
        ''' (self) -> None
        
            ���� ������ ���������
        '''
        tmp = self._port.readall()
         
        # ������� � ������ ������ ������
        if not tmp:
            return
        # ������� ���� ���������� ��������� ��� �� ����������
        if self._bRead:
            return
        
        # ������������ �������� �� ������������ ���������
        for x in tmp:
            self._protocol(x.encode('hex').upper())
    
    def _cycleTr(self):
        ''' (self) -> None
            
            ���� ������ ������� �����������.
        '''        
        self._port.write(bytearray.fromhex(self._command))
#        print self._command
        
    def fillPortBox(self, data=None, val='COM1'):
        ''' (self, list, str) -> None
        
            ���������� ��������������� ������ ������ ������� data
            �� ������� � ������ �������� val, ��� ����� �������.
        '''
        # �������� ��������� ����� ����������� � �� ����� ����������,
        # ���� �� ��� ����������
        tmp = self.isFlagModify()
        
        if not data:
            data = self.scanPorts()

        self.portEdit.clear()
        self.portEdit.addItems(data)
        if val in data:
            self.portEdit.setCurrentIndex(data.index(val))
            if not tmp:
                self.clearFlagModify()
        else:
            self.portEdit.setCurrentIndex(0)
    
    def fillBaudRateBox(self, data=None, val='1200'):
        ''' (self, list, str) -> None
        
            ���������� ��������������� ������ ��������� ������� data.
            ��� ������� � ������ �������� val, ��� ����� �������.
        '''
        # �������� ��������� ����� ����������� � �� ����� ����������,
        # ���� �� ��� ����������
        tmp = self.isFlagModify()
        
        if not data:
            data = [str(x) for x in serial.Serial.BAUDRATES]
        
        self.baudRateEdit.clear()
        self.baudRateEdit.addItems(data)
        if val in data:
            self.baudRateEdit.setCurrentIndex(data.index(val))
            if not tmp:
                self.clearFlagModify()
        else:
            self.baudRateEdit.setCurrentIndex(0)
    
    def fillStopBitsBox(self, data=None, val='2'):
        ''' (self, list, str) -> None
        
            ���������� ��������������� ������ ����-����� ������� data.
            ��� ������� � ������ �������� val, ��� ����� �������.
        '''
        # �������� ��������� ����� ����������� � �� ����� ����������,
        # ���� �� ��� ����������
        tmp = self.isFlagModify()
        
        if not data:
            data = [str(serial.STOPBITS_ONE), str(serial.STOPBITS_TWO)]
        
        self.stopBitsEdit.clear()
        self.stopBitsEdit.addItems(data)
        if val in data:
            self.stopBitsEdit.setCurrentIndex(data.index(val))
            if not tmp:
                self.clearFlagModify()
        else:
            self.stopBitsEdit.setCurrentIndex(0)
        
    def fillParityBox(self, data=None, val='None'):
        ''' (self, list, str) -> None
        
            ���������� ��������������� ������ ��������� ������� data.
            ��� ������� � ������ �������� val, ��� ����� �������.
        '''
        # �������� ��������� ����� ����������� � �� ����� ����������,
        # ���� �� ��� ����������
        tmp = self.isFlagModify()
        
        if not data:
            data = [self.PARITY[x] for x in serial.Serial.PARITIES]
        
        self.parityEdit.clear()
        self.parityEdit.addItems(data)
        if val in data:
            self.parityEdit.setCurrentIndex(data.index(val))
            if not tmp:
                self.clearFlagModify()
        else:
            self.parityEdit.setCurrentIndex(0)
    
    def fillByteSize(self, data=None, val='8'):
        ''' (self, list, str) -> None
        
            ���������� ��������������� ������ ���-�� ��� ������ ������� data.
            ��� ������� � ������ �������� val, ��� ����� �������.
        '''
        # �������� ��������� ����� ����������� � �� ����� ����������,
        # ���� �� ��� ����������
        tmp = self.isFlagModify()
        
        if not data:
            data = [str(x) for x in serial.Serial.BYTESIZES]
        
        self.byteSizeEdit.clear()
        self.byteSizeEdit.addItems(data)
        if val in data:
            self.byteSizeEdit.setCurrentIndex(data.index(val))
            if not tmp:
                self.clearFlagModify()
        else:
            self.byteSizeEdit.setCurrentIndex(0)
    
    def refreshData(self):
        ''' (self) -> None
        
            ���������� ���������� � ����� ��������.
        '''
        self.fillPortBox(val=self.portEdit.currentText())
    
    def setFlagModify(self, val=None):
        ''' (self, val) -> None
            
            ��������� ����� ������� ��������� ����������.
            val - ������ �������������� ��������
        '''
        self._modify = True
        self.pApply.setEnabled(True)
    
    def isFlagModify(self):
        ''' (self) -> None
        
            �������� ������� ��������� ����������.
        '''
        return self._modify
        
    def clearFlagModify(self):
        ''' (self) -> None
            
            ����� ����� ������� ��������� ����������
        '''
        self._modify = False
        self.pApply.setDisabled(True)
        
    def setPort(self, val):
        ''' (self, str) -> None
        
            ��������� �����.
        '''
        
#        QtGui.QMessageBox.warning(self, u"������",
#                                   u"������ ������� �� � HEX-�������",
#                                   QtGui.QMessageBox.Yes)

        try:
            val = str(val)
            self.settings['port'] = val
        except:
            print self.setPort
            print "������ ��������� ����� ����������������� �����",
            print type(val), val
            raise
        
    def setBaudRate(self, val):
        ''' (self, str) -> None
            
            ��������� �������� ������ ����� val, ���/�.
        '''
        try:
            val = int(val)
            if val in serial.Serial.BAUDRATES:
                self.settings['baudrate'] = val
        except:
            print self.setBaudRate
            print "������ ��������� �������� ������ ����������������� �����",
            print type(val), val
            raise
        
    def setByteSize(self, val):
        ''' (self, str) -> None
        
            ��������� ���-�� ��� ������ val.
        '''
        try:
            val = int(val)
            if val in serial.Serial.BYTESIZES:
                self.settings['bytesize'] = val
        except:
            print self.setByteSize
            print "������ ��������� ���-�� ��� ������ ����������������� �����",
            print type(val), val
            raise
        
    def setParity(self, val):
        ''' (self, str) -> None
        
            ��������� �������� val.
        '''
        try:
            val = val[0]
            if val in serial.Serial.PARITIES:
                self.settings['parity'] = val
        except:
            print self.setParity
            print "������ ��������� �������� ����������������� �����",
            print type(val), val
            raise
    
    def setStopBits(self, val):
        ''' (self, val) -> None
        
            ��������� ���-�� ����-��� val.
        '''
        try:
            val = int(val)
                
            if val in serial.Serial.STOPBITS:
                self.settings['stopbits'] = val
        except:
            print self.setStopBits
            print "������ ��������� ����-����� ����������������� �����.",
            print type(val), val
            raise
    
    def setSettings(self, checked=False, settings={}):
        ''' (self, dict) -> None
        
            ��� �������� ���������� � settings, ��������� ����� �����������
            �� ����. ��������� ����� � �����.
                'port' - ��� �����
                'baudrate' - ��������
                'bytesize' - ���-�� ���� ������
                'parity' - �������� ��������
                'stopbits' - ���-�� ����-���
            �������� checked, ������������ ��� SIGNAL ������� ������
        '''
        try:
            port = self.portEdit.currentText()
            if 'port' in settings:
                port = settings['port']
            self.setPort(port)
            
            baudrate = self.baudRateEdit.currentText()
            if 'baudrate' in settings:
                baudrate = settings['baudrate']
            self.setBaudRate(baudrate)
            
            bytesize = self.byteSizeEdit.currentText()
            if 'bytesize' in settings:
                bytesize = settings['bytesize']
            self.setByteSize(bytesize)
            
            parity = self.parityEdit.currentText()
            if 'parity' in settings:
                parity = self.setParity(settings['parity'])
            self.setParity(parity)
            
            stopbits = self.stopBitsEdit.currentText()
            if 'stopbits' in settings:
                stopbits = settings['stopbits']
            self.setStopBits(stopbits)
        except:
            print self.setSettings
            print "������ ��������� ���������� �����"
            print "������� ������: ", settings
            raise
        
        self.clearFlagModify()
        self.pApply.setDisabled(True)
        
    def scanPorts(self):
        ''' () -> [(int, str)]

        Scan for available ports.
        Return list of tuples [(num, name)]

        ������ ������.
        ���������� ������ ��������� [(num, name)]
        
        >>> ports.scanPorts()
        [(0, 'COM1'), (5, 'COM6')]
        
        >>> ports.scanPorts()
        [(0, 'COM1'), (1, 'COM2'), (5, 'COM6')]
        '''
        available = []
        for i in range(256):
            try:
                s = serial.Serial(i)
                available.append(s.portstr)
                s.close()
            except serial.SerialException, e:
                # print s, e
                pass
            
        return available

    def createWidget(self):
        ''' (self, bool) -> None
        
            ������������ ��������� ����.
        '''
        vboxl = QtGui.QVBoxLayout()
        vboxe = QtGui.QVBoxLayout()
        
        self.portEdit = QtGui.QComboBox()
        self.portLabel = QtGui.QLabel(u'���:')
        vboxl.addWidget(self.portLabel, alignment=QtCore.Qt.AlignRight)
        vboxe.addWidget(self.portEdit)
        
        self.baudRateEdit = QtGui.QComboBox()
        self.baudRateLabel = QtGui.QLabel(u'�������� ���/�:')
        vboxl.addWidget(self.baudRateLabel, alignment=QtCore.Qt.AlignRight)
        vboxe.addWidget(self.baudRateEdit)
        
        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vboxl)
        hbox.addLayout(vboxe)
        groupbox1 = QtGui.QGroupBox(u'��������')
        groupbox1.setLayout(hbox)
        
        vboxl = QtGui.QVBoxLayout()
        vboxe = QtGui.QVBoxLayout()
        
        self.byteSizeEdit = QtGui.QComboBox()
        self.byteSizeLabel = QtGui.QLabel(u'���� ������:')
        vboxl.addWidget(self.byteSizeLabel, alignment=QtCore.Qt.AlignRight)
        vboxe.addWidget(self.byteSizeEdit)
        
        self.parityEdit = QtGui.QComboBox()
        self.parityLabel = QtGui.QLabel(u'��������:')
        vboxl.addWidget(self.parityLabel, alignment=QtCore.Qt.AlignRight)
        vboxe.addWidget(self.parityEdit)
        
        self.stopBitsEdit = QtGui.QComboBox()
        self.stopBitsLabel = QtGui.QLabel(u'�������� ����:')
        vboxl.addWidget(self.stopBitsLabel, alignment=QtCore.Qt.AlignRight)
        vboxe.addWidget(self.stopBitsEdit)
        
        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vboxl)
        hbox.addLayout(vboxe)
        
        groupbox2 = QtGui.QGroupBox(u'������ ������')
        groupbox2.setLayout(hbox)
        
        self.pScan = QtGui.QPushButton(u'��������')
        self.connect(self.pScan, QtCore.SIGNAL('clicked()'), self.refreshData)
        
        self.pApply = QtGui.QPushButton(u'�������')
        self.pApply.clicked.connect(self.setSettings)
        self.pAbort = QtGui.QPushButton(u'��������')
        
        vboxl = QtGui.QVBoxLayout()
        vboxl.addWidget(groupbox1)
        vboxl.addWidget(groupbox2)
        
        vboxr = QtGui.QVBoxLayout()
        vboxr.addWidget(self.pApply)
        vboxr.addWidget(self.pScan)
        vboxr.addWidget(self.pAbort)
        vboxr.addStretch()

        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vboxl)
        hbox.addLayout(vboxr)
        
        self.setLayout(hbox)
        
        # ���������� ����� ��������
        self.fillPortBox()
        self.fillBaudRateBox()
        self.fillStopBitsBox()
        self.fillParityBox()
        self.fillByteSize()
        
        # ��������� �������
        self.portEdit.currentIndexChanged.connect(self.setFlagModify)
        self.baudRateEdit.currentIndexChanged.connect(self.setFlagModify)
        self.byteSizeEdit.currentIndexChanged.connect(self.setFlagModify)
        self.stopBitsEdit.currentIndexChanged.connect(self.setFlagModify)
        self.parityEdit.currentIndexChanged.connect(self.setFlagModify)
        
    def _protocol(self, char):
        ''' (self, str) -> None
         
             �������� �������� ���� �� ���������. 
             ������� ������� ������: 'AA' '31'
        '''
        if self._cnt == 0:
            if char == '55':
                self._cnt = 1
        elif self._cnt == 1:
            if char == 'AA':
                self._cnt = 2
            else:
                self._cnt = 0
        elif self._cnt == 2:
            self._com = char
            self._cnt += 1
        elif self._cnt == 3:
            self._lenght = int(char, 16)
            self._cnt += 1
        else:
            if self._cnt < (5 + self._lenght - 1):
                self._data.append(char)
                self._cnt += 1
            else:
                if self._checkCRC(char):
                    self._bRead = True
#                    print self._data
                    self.emit(QtCore.SIGNAL("readData(PyQt_PyObject, \
                                            PyQt_PyObject, PyQt_PyObject)"),
                              self._com, self._lenght, self._data)
                self._cnt = 0

    def _checkCRC(self, crc, com=None, lenght=None, data=None):
        ''' (self, str, str, int, str) -> crc
            
            �������� ����������� CRC (�������� 'AB') � ������������.
            
            ���������� True � ������ ����������
            
            >>> _checkCRC('02', '02', 0, [])
            True
        '''
        if com is None:
            com = self._com
        if isinstance(com, str):
            com = int(com, 16)
        calcCRC = com
        
        if lenght is None:
            lenght = self._lenght
        if isinstance(lenght, str):
            lenght = int(lenght, 16)
        calcCRC += lenght
        
        if data is None:
            data = self._data
        for x in data:
            if isinstance(x, str):
                x = int(x, 16)
            calcCRC += x
        calcCRC %= 256
        
        if isinstance(crc, str):
            crc = int(crc, 16)

        return calcCRC == crc
        
    def clrReadFlag(self):
        ''' (self) -> Non
        
            ���������� ������ ��������� ������� ������
        '''
        self._bRead = False
        self._data = []
    
    def setCom(self, data):
        ''' (self, str) -> None
        
            ��������� ������� �� ��������
        '''
        self._command = data
    
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    QtGui.QApplication.setStyle('Cleanlooks')
    
    my_frame = mySerial()
    
    # �������� �������� ����� � ����������� �� ���������
    my_frame.openPort()
    my_frame.closePort()
    
    # �������� �������� ����� � ������� �����������
    my_frame.setSettings(settings={'port': 'COM2', 'baudrate': 1200})
    my_frame.openPort()
    my_frame.closePort()
    
    my_frame.show()
    app.exec_()
