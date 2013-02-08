# -*- coding: cp1251 -*-

'''
Created on 25.12.2012

@author: Shcheblykin
'''

# -*- coding: cp1251 -*-
import serial
from PyQt4 import QtCore


class Interface():
    def __init__(self, port=None, baudrate=1200, bytesize=serial.EIGHTBITS,
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
        
        # цикл передачи посылки в мс
        self._repeatTime = 250
        # счетчик времени
        self._time = -1
        # флаг включенного цикла на предеачу
        self._repeat = False
        # буфер передаваемой команды
        self._bufTrData = bytearray()
        
#        self.timerTr = QtCore.QTimer()
#        self.timerTr.timeout.connect(self._timerCycle)
         
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
            
            Начало работы с портом.
        '''
        if self._portName == None:
            raise 'Порт не выбран'
        else:
            self._port = serial.Serial(self._portName,
                                       self._portBaudRate,
                                       self._portByteSize,
                                       self._portParity,
                                       self._portStopBits,
                                       timeout=0)
#            self.timerTr.startTimer(1)
          
    def closePort(self):
        ''' (self) -> None
        
            Окончание работы с портом.
        '''
        self.timerTr.stop()
        
        self._port.close()
        
    def scanPorts(self):
        ''' () -> (int, str)

        Scan for available ports.
        Return list of tuples (num, name)

        Сканер портов.
        Возвращает список доступных (num, name)
        
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
            
            Возвращает список доступных для работы портов.
            
            >>> ports.getAviablePorts()
            ['COM1', 'COM2', 'COM6']
        '''
        tmp = []
        for item in self.scanPorts():
            tmp.append(item[1])
        
        return tmp
    
    def getAvailableBaudRates(self):
        ''' (self) -> list
        
            Возвращает список доступных скоростей работы порта
            
            >> ports.getAvailableBaudRates()
            ['50', '75', '110', '134', '150'... ]
        '''
        tmp = [str(x) for x in serial.Serial.BAUDRATES]
        return tmp
    
    def getAvailableStopBits(self):
        ''' (self) -> list
        
            Возвращает список доступных установок кол-ва стоп-битов.
            
            >>> ports.getAvailableStopBits()
            ['1', '1.5', '2']
        '''
        tmp = [str(serial.STOPBITS_ONE), str(serial.STOPBITS_TWO)]
        return tmp
    
    def getAvailableParities(self):
        ''' (self) -> list
        
            Возвращает список доступных установок контроля четности.
            
            >>> ports.getAvailableParities()
            ['None', 'Even', 'Odd', 'Mark', 'Space']
        '''
        tmp = [self.PARITY[x] for x in serial.Serial.PARITIES]
        return tmp
    
    def getAvailableByteSize(self):
        ''' (self) -> list
        
            Возвращает список доступных установок кол-ва бит данных val.
            
            >>> ports.getAvailableByteSize()
            ['5', '6', '7', '8']
        '''
        tmp = [str(x) for x in serial.Serial.BYTESIZES]
        return tmp
    
    def setPort(self, val):
        ''' (self, str) -> None
        
            Установка порта.
        '''
        try:
            val = str(val)
            self._portName = val
        except:
            pass
        
    def setBaudRate(self, val):
        ''' (self, str) -> None
            
            Установка скорости работы порта val, бит/с.
        '''
        try:
            val = int(val)
            if val in serial.Serial.BAUDRATES:
                self._portBaudRate = val
        except:
            print self.setBaudRate
        
    def setByteSize(self, val):
        ''' (self, str) -> None
        
            Установка кол-ва бит данных val.
        '''
        try:
            val = int(val)
            if val in serial.Serial.BYTESIZES:
                self._portByteSize = val
        except:
            print self.setByteSize
        
    def setParity(self, val):
        ''' (self, str) -> None
        
            Установка четности val.
        '''
        try:
            val = val[0]
            if val in serial.Serial.PARITIES:
                self._portParity = val
        except:
            print self.setParity
    
    def setRepeatTime(self, val):
        ''' (self, int) -> bool
        
            Установка периода на передачу посылок 1-60000мс.
            Возращает Fale в случае ошибки.
        '''
        if type(val) != int:
            return False
        
        # макс. ограничение 1 минута
        if type(val > 60000):
            return
        
        self._repeatTime = val
        return True
            
    def setStopBits(self, val):
        ''' (self, val) -> None
        
            Установка кол-ва стоп-бит val.
        '''
        try:
            val = int(val)
                
            if val in serial.Serial.STOPBITS:
                self._portStopBits = val
        except:
            self.setStopBits(val)
        
    def getPortName(self):
        ''' (self) -> str
        
            Возвращает текущее имя порта.
        '''
        return str(self._portName)
    
    def getBaudRate(self):
        ''' (self) -> str
        
            Возвращает текущую настройку скорости порта, бит/с.
        '''
        return str(self._portBaudRate)
    
    def getByteSize(self):
        ''' (self) -> str
        
            Возвращает текущую настройку кол-ва бит данных.
        '''
        return str(self._portByteSize)
    
    def getParity(self):
        ''' (self) -> str
        
            Возвращает текущую настройку четности.
        '''
        return str(self._portParity)

    def getStopBits(self):
        ''' (self) -> str
        
            Возвращает текущую настройку кол-ва стоп-битов.
        '''
        return str(self._portStopBits)
    
    def sendData(self, data, repeat=False):
        ''' (self, str) -> None
            
            Передача данных data. При repeat = False включается режим
            цикличной передачи сообщения.
               
            Примеры data:
            '55 AA 01 00 01'
        '''
#        try:
        # Установка флага повторной передачи, с проверкой входных данных
        if type(repeat) == bool:
            self._repeat = repeat
        else:
            self._repeat = False
        self._time = 0

        tmp = bytearray()
        for x in data.split():
            tmp.append(x.decode('hex'))
        self._bufTrData = tmp
        
        print self._bufTrData
        print repeat
        print self._time
#        except:
#            print self.sendData, 'Ошибка при попытке отправить данные'
        
    def repeatStop(self):
        ''' (self) -> None
        
            Остановка отправки повторных сообщений
        '''
        self._repeat = False
    
    def _readData(self):
        ''' (self) -> None
        
            Производится считывание данных из порта
            
        '''
        s = self.port.readall()
        print s
        if len(s) <= 0:
            return

        read = []
                
        for c in s:
            read.append(c.encode('hex').upper())
     
    def _timerCycle(self):
        ''' (self) -> None
         
             Цикл таймера
        '''
        print "I am here"
    
        # проверим необходимость повторной передачи
        if self.time > 0:
            self._time -= 1
        if self._time == 0:
            self._port.write(self._bufTrData)
            if self._repeat == True:
                self._time = self._repeatTime
            else:
                self._time = -1
        
          
if __name__ == '__main__':
    print "Создан элемент port, выбран 'COM1'"
    port = Interface('COM1')
    port.openPort()
#    port.closePort()
#    print "Пор закрыт."
