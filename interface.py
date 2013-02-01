# -*- coding: cp1251 -*-

'''
Created on 25.12.2012

@author: Shcheblykin
'''

# -*- coding: cp1251 -*-
import serial
from PyQt4 import QtCore


class ReadThread(QtCore.QThread):
    def __init__(self, port, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.port = port
        
    def run(self):
        while True:
            s = self.port.readall()
            print s
            if len(s) > 0:
                read = []
                
                for c in s:
                    read.append(c.encode('hex').upper())
                
#                self.emit(QtCore.SIGNAL(str))


class Interface():
    def __init__(self, port=None, baudrate=19200, bytesize=serial.EIGHTBITS,
                 parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_TWO,
                 parent=None):
#        self.aviablePorts = self.scanPorts()
        
        self._portName = port
        self._portBaudRate = baudrate
        self._portByteSize = bytesize
        self._portStopBits = stopbits
        self._portParity = parity
        self.PARITY = {'N': 'None', 'O': 'Odd', 'E': 'Even', \
                       'M': 'Mark', 'S': 'Space'}
        self._port = None
        
        self.timerTr = QtCore.QTimer()
        self.timerTr.timeout.connect(self.repeatSendData)
        self.data_temp = ''
        
        self.readThread = ReadThread(self._port)
         
    def __str__(self):
        val = ''
        val += 'port = %s; ' % self.getPortName()
        val += 'baudrate = %s; ' % self.getBaudRate()
        val += 'bytesize = %s; ' % self.getByteSize()
        val += 'parity = %s; ' % self.getParity()
        val += 'stopbits = %s' % self.getStopBits()
        return val
    
    def openPort(self):
        ''' (self) -> None
            
            ������ ������ � ������.
        '''
        if self._portName == None:
            raise '���� �� ������'
        else:
            self._port = serial.Serial(self._portName,
                                       self._portBaudRate,
                                       self._portByteSize,
                                       self._portParity,
                                       self._portStopBits,
                                       timeout=0)
            self.readThread.start()
          
    def closePort(self):
        ''' (self) -> None
        
            ��������� ������ � ������.
        '''
        self.timerTr.stop()
        
        self.readThread.terminate()
        self.readThread.wait(100)
        
        self._port.close()
        
    def scanPorts(self):
        ''' () -> (int, str)

        Scan for available ports.
        Return list of tuples (num, name)

        ������ ������.
        ���������� ������ ��������� (num, name)
        
        >>> ports.scanPorts()
        [(0, 'COM1'), (5, 'COM6')]
        
        >>> ports.scanPorts()
        [(0, 'COM1'), (1, 'COM2'), (5, 'COM6')]
        '''
        available = []
        for i in range(256):
            try:
                s = serial.Serial(i)
                available.append((i, s.portstr))
                s.close()
            except serial.SerialException, e:
#                print e
                pass

        return available

    def getAvailablePorts(self):
        ''' (self) -> list
            
            ���������� ������ ��������� ��� ������ ������.
            
            >>> ports.getAviablePorts()
            ['COM1', 'COM2', 'COM6']
        '''
        tmp = []
        for item in self.scanPorts():
            tmp.append(item[1])
        
        return tmp
    
    def getAvailableBaudRates(self):
        ''' (self) -> list
        
            ���������� ������ ��������� ��������� ������ �����
            
            >> ports.getAvailableBaudRates()
            ['50', '75', '110', '134', '150'... ]
        '''
        tmp = [str(x) for x in serial.Serial.BAUDRATES]
        return tmp
    
    def getAvailableStopBits(self):
        ''' (self) -> list
        
            ���������� ������ ��������� ��������� ���-�� ����-�����.
            
            >>> ports.getAvailableStopBits()
            ['1', '1.5', '2']
        '''
        tmp = [str(serial.STOPBITS_ONE), str(serial.STOPBITS_TWO)]
        return tmp
    
    def getAvailableParities(self):
        ''' (self) -> list
        
            ���������� ������ ��������� ��������� �������� ��������.
            
            >>> ports.getAvailableParities()
            ['None', 'Even', 'Odd', 'Mark', 'Space']
        '''
        tmp = [self.PARITY[x] for x in serial.Serial.PARITIES]
        return tmp
    
    def getAvailableByteSize(self):
        ''' (self) -> list
        
            ���������� ������ ��������� ��������� ���-�� ��� ������ val.
            
            >>> ports.getAvailableByteSize()
            ['5', '6', '7', '8']
        '''
        tmp = [str(x) for x in serial.Serial.BYTESIZES]
        return tmp
    
    def setPortName(self, val):
        ''' (self, str) -> None
        
            ��������� �����.
        '''
        try:
            val = str(val)
            self._portName = val
        except:
            pass
        
    def setBaudRate(self, val):
        ''' (self, str) -> None
            
            ��������� �������� ������ ����� val, ���/�.
        '''
        try:
            val = int(val)
            if val in serial.Serial.BAUDRATES:
                self._portBaudRate = val
        except:
            print self.setBaudRate
        
    def setByteSize(self, val):
        ''' (self, str) -> None
        
            ��������� ���-�� ��� ������ val.
        '''
        try:
            val = int(val)
            if val in serial.Serial.BYTESIZES:
                self._portByteSize = val
        except:
            print self.setByteSize
        
    def setParity(self, val):
        ''' (self, str) -> None
        
            ��������� �������� val.
        '''
        try:
            val = val[0]
            if val in serial.Serial.PARITIES:
                self._portParity = val
        except:
            print self.setParity
            
    def setStopBits(self, val):
        ''' (self, val) -> None
        
            ��������� ���-�� ����-��� val.
        '''
        try:
            val = int(val)
                
            if val in serial.Serial.STOPBITS:
                self._portStopBits = val
        except:
            self.setStopBits(val)
        
    def getPortName(self):
        ''' (self) -> str
        
            ���������� ������� ��� �����.
        '''
        return str(self._portName)
    
    def getBaudRate(self):
        ''' (self) -> str
        
            ���������� ������� ��������� �������� �����, ���/�.
        '''
        return str(self._portBaudRate)
    
    def getByteSize(self):
        ''' (self) -> str
        
            ���������� ������� ��������� ���-�� ��� ������.
        '''
        return str(self._portByteSize)
    
    def getParity(self):
        ''' (self) -> str
        
            ���������� ������� ��������� ��������.
        '''
        return str(self._portParity)

    def getStopBits(self):
        ''' (self) -> str
        
            ���������� ������� ��������� ���-�� ����-�����.
        '''
        return str(self._portStopBits)
    
    def sendData(self, data, repeat=None):
        ''' (self, str) -> number
            
            �������� ������ data.
            repeat �������� �� ���� ����������, �������� � ��,
            None - ��� ���������.
            � ������ �������� ��������, ���������� ���-�� ���������� ����.
            
            ������� data:
            '55 AA 01 00 01'
        '''
#        try:
        if True:
            tmp = bytearray()
            for x in data.split():
                tmp.append(x.decode('hex'))
            self.data_temp = data
            
            a = QtCore.QObject()
            a.emit(QtCore.SIGNAL('signalSendData()'))
            
            # �������� ������������� ���������� �������� ��� ���.����.
            # ���������� �������
            if repeat != None:
                if repeat == 0:
                    self.timerTr.stop()
                else:
                    self.timerTr.stop()
                    self.timerTr.setInterval(repeat)
                    self.timerTr.start()
                    
            return self._port.write(tmp)
#        except:
#            print self.sendData, '������ ��� ������� ��������� ������'
    
    def repeatSendData(self):
        ''' (self) -> None
        
            ��������� �������� ���������
        '''
        self.sendData(self.data_temp)
        
    def repeatStop(self):
        ''' (self) -> None
        
            ��������� �������� ��������� ���������
        '''
        self.timerTr.stop()
    
    def _readData(self):
        ''' (self) -> None
        
            ������������ ���������� ������ �� �����
            
        '''
        pass
            
    
if __name__ == '__main__':
    print "������ ������� port, ������ 'COM1'"
    port = Interface('COM1')
    port.openPort()
#    port.closePort()
#    print "��� ������."
