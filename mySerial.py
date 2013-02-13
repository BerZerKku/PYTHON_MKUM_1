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
    
        Widget работы с ком-портом.
        Имеется возможность поиска доступных портов в системе,
        настройка параметров работы, открытие и закрытие порта.
        Полученная/отправленная инф-ия выводится на экран.
    '''
    def __init__(self, port='COM1', baudrate=1200, bytesize=serial.EIGHTBITS,
                 parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_TWO,
                 parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.PARITY = {'N': 'None', 'O': 'Odd', 'E': 'Even', \
                       'M': 'Mark', 'S': 'Space'}
        
        # установка фиксированного размера окна
        flag = QtCore.Qt.Window
        flag |= QtCore.Qt.MSWindowsFixedSizeDialogHint
        self.setWindowFlags(flag)
        
        # флаг наличия изменений
        self._modify = False
        
        # начальная настройка порта
        self.settings = {}
        self.setPort(port)
        self.setBaudRate(baudrate)
        self.setByteSize(bytesize)
        self.setParity(parity)
        self.setStopBits(stopbits)
        
        # создание элементов виджета
        self.createWidget()
        
        # последовательный порт
        self._port = serial.Serial()
        self._port.setTimeout(0)
        self.setCom("55 AA 02 00 02")
        
        # флаг принятой посылки (True - есть посылка)
        self._bRead = False
        # номер текущего принятого байта согласно протоколу
        self._cnt = 0
        # массив данных
        self._data = []
        # кол-вод байт данных
        self._lenght = 0
        # контрольная сумма
        self._crc = 0
        
        # таймер передатчика
        self._timerTr = QtCore.QTimer()
        self._timerTr.setInterval(500)
        self._timerTr.timeout.connect(self._cycleTr)
        
        # таймер приемника
        self._timerRc = QtCore.QTimer()
        self._timerRc.setInterval(5)
        self._timerRc.timeout.connect(self._cycleRc)
        
        # часы
        self._clock = QtCore.QTime.currentTime()
            
    def openPort(self):
        ''' (self) -> bool
        
            Начало работы с портом. В случае ошибки возвращает False.
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
            print "Не удалось открыть порт",
            
    def closePort(self):
        ''' (self) -> bool
        
            Окончание работы с портом. В слечае ошибки возвращает False.
        '''
        try:
            self._port.close()
            self._timerTr.stop()
            self._timerRc.stop()
        except:
            print self.closePort
            print "Не удалось закрыть порт"
            raise
    
    def _cycleRc(self):
        ''' (self) -> None
        
            Цикл работы приемника
        '''
        tmp = self._port.readall()
         
        # возврат в случае пустой строки
        if not tmp:
            return
        # возврат если предыдущее сообщение еще не обработано
        if self._bRead:
            return
        
        # посимвольная проверка на соответствие протоколу
        for x in tmp:
            self._protocol(x.encode('hex').upper())
    
    def _cycleTr(self):
        ''' (self) -> None
            
            Цикл работы таймера передатчика.
        '''        
        self._port.write(bytearray.fromhex(self._command))
#        print self._command
        
    def fillPortBox(self, data=None, val='COM1'):
        ''' (self, list, str) -> None
        
            Заполнение раскрывающегося списка портов данными data
            ри наличии в списке значения val, оно будет выбрано.
        '''
        # Заполним состояние флага модификации и не будет сбрасывать,
        # если он был установлен
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
        
            Заполнение раскрывающегося списка скоростей данными data.
            При наличии в списке значения val, оно будет выбрано.
        '''
        # Заполним состояние флага модификации и не будет сбрасывать,
        # если он был установлен
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
        
            Заполнение раскрывающегося списка стоп-битов данными data.
            При наличии в списке значения val, оно будет выбрано.
        '''
        # Заполним состояние флага модификации и не будет сбрасывать,
        # если он был установлен
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
        
            Заполнение раскрывающегося списка четностей данными data.
            При наличии в списке значения val, оно будет выбрано.
        '''
        # Заполним состояние флага модификации и не будет сбрасывать,
        # если он был установлен
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
        
            Заполнение раскрывающегося списка кол-ва бит данных данными data.
            При наличии в списке значения val, оно будет выбрано.
        '''
        # Заполним состояние флага модификации и не будет сбрасывать,
        # если он был установлен
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
        
            Обновление информации в полях настроек.
        '''
        self.fillPortBox(val=self.portEdit.currentText())
    
    def setFlagModify(self, val=None):
        ''' (self, val) -> None
            
            Установка флага наличия изменений параметров.
            val - индекс установленного элемента
        '''
        self._modify = True
        self.pApply.setEnabled(True)
    
    def isFlagModify(self):
        ''' (self) -> None
        
            Проверка наличия изменений параметров.
        '''
        return self._modify
        
    def clearFlagModify(self):
        ''' (self) -> None
            
            Сброс флага наличия изменений параметров
        '''
        self._modify = False
        self.pApply.setDisabled(True)
        
    def setPort(self, val):
        ''' (self, str) -> None
        
            Установка порта.
        '''
        
#        QtGui.QMessageBox.warning(self, u"Ошибка",
#                                   u"Строка введена не в HEX-формате",
#                                   QtGui.QMessageBox.Yes)

        try:
            val = str(val)
            self.settings['port'] = val
        except:
            print self.setPort
            print "Ошибка установки имени последовательного порта",
            print type(val), val
            raise
        
    def setBaudRate(self, val):
        ''' (self, str) -> None
            
            Установка скорости работы порта val, бит/с.
        '''
        try:
            val = int(val)
            if val in serial.Serial.BAUDRATES:
                self.settings['baudrate'] = val
        except:
            print self.setBaudRate
            print "Ошибка установки скорости работы последовательного порта",
            print type(val), val
            raise
        
    def setByteSize(self, val):
        ''' (self, str) -> None
        
            Установка кол-ва бит данных val.
        '''
        try:
            val = int(val)
            if val in serial.Serial.BYTESIZES:
                self.settings['bytesize'] = val
        except:
            print self.setByteSize
            print "Ошибка установки кол-ва бит данных последовательного порта",
            print type(val), val
            raise
        
    def setParity(self, val):
        ''' (self, str) -> None
        
            Установка четности val.
        '''
        try:
            val = val[0]
            if val in serial.Serial.PARITIES:
                self.settings['parity'] = val
        except:
            print self.setParity
            print "Ошибка установки четности последовательного порта",
            print type(val), val
            raise
    
    def setStopBits(self, val):
        ''' (self, val) -> None
        
            Установка кол-ва стоп-бит val.
        '''
        try:
            val = int(val)
                
            if val in serial.Serial.STOPBITS:
                self.settings['stopbits'] = val
        except:
            print self.setStopBits
            print "Ошибка установки стоп-битов последовательного порта.",
            print type(val), val
            raise
    
    def setSettings(self, checked=False, settings={}):
        ''' (self, dict) -> None
        
            При передаче параметров в settings, параметры будут установлены
            из него. Остальное взято с формы.
                'port' - имя порта
                'baudrate' - скорость
                'bytesize' - кол-во байт данных
                'parity' - контроль четности
                'stopbits' - кол-во стоп-бит
            Параметр checked, используется для SIGNAL нажатия кнопки
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
            print "Ошибка установки параметров порта"
            print "Входные данные: ", settings
            raise
        
        self.clearFlagModify()
        self.pApply.setDisabled(True)
        
    def scanPorts(self):
        ''' () -> [(int, str)]

        Scan for available ports.
        Return list of tuples [(num, name)]

        Сканер портов.
        Возвращает список доступных [(num, name)]
        
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
        
            Формирование элементов окна.
        '''
        vboxl = QtGui.QVBoxLayout()
        vboxe = QtGui.QVBoxLayout()
        
        self.portEdit = QtGui.QComboBox()
        self.portLabel = QtGui.QLabel(u'Имя:')
        vboxl.addWidget(self.portLabel, alignment=QtCore.Qt.AlignRight)
        vboxe.addWidget(self.portEdit)
        
        self.baudRateEdit = QtGui.QComboBox()
        self.baudRateLabel = QtGui.QLabel(u'Скорость бит/с:')
        vboxl.addWidget(self.baudRateLabel, alignment=QtCore.Qt.AlignRight)
        vboxe.addWidget(self.baudRateEdit)
        
        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vboxl)
        hbox.addLayout(vboxe)
        groupbox1 = QtGui.QGroupBox(u'Основные')
        groupbox1.setLayout(hbox)
        
        vboxl = QtGui.QVBoxLayout()
        vboxe = QtGui.QVBoxLayout()
        
        self.byteSizeEdit = QtGui.QComboBox()
        self.byteSizeLabel = QtGui.QLabel(u'Биты данных:')
        vboxl.addWidget(self.byteSizeLabel, alignment=QtCore.Qt.AlignRight)
        vboxe.addWidget(self.byteSizeEdit)
        
        self.parityEdit = QtGui.QComboBox()
        self.parityLabel = QtGui.QLabel(u'Четность:')
        vboxl.addWidget(self.parityLabel, alignment=QtCore.Qt.AlignRight)
        vboxe.addWidget(self.parityEdit)
        
        self.stopBitsEdit = QtGui.QComboBox()
        self.stopBitsLabel = QtGui.QLabel(u'Стоповые биты:')
        vboxl.addWidget(self.stopBitsLabel, alignment=QtCore.Qt.AlignRight)
        vboxe.addWidget(self.stopBitsEdit)
        
        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vboxl)
        hbox.addLayout(vboxe)
        
        groupbox2 = QtGui.QGroupBox(u'Формат данных')
        groupbox2.setLayout(hbox)
        
        self.pScan = QtGui.QPushButton(u'Обновить')
        self.connect(self.pScan, QtCore.SIGNAL('clicked()'), self.refreshData)
        
        self.pApply = QtGui.QPushButton(u'Принять')
        self.pApply.clicked.connect(self.setSettings)
        self.pAbort = QtGui.QPushButton(u'Отменить')
        
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
        
        # заполнение полей настроек
        self.fillPortBox()
        self.fillBaudRateBox()
        self.fillStopBitsBox()
        self.fillParityBox()
        self.fillByteSize()
        
        # подключим сигналы
        self.portEdit.currentIndexChanged.connect(self.setFlagModify)
        self.baudRateEdit.currentIndexChanged.connect(self.setFlagModify)
        self.byteSizeEdit.currentIndexChanged.connect(self.setFlagModify)
        self.stopBitsEdit.currentIndexChanged.connect(self.setFlagModify)
        self.parityEdit.currentIndexChanged.connect(self.setFlagModify)
        
    def _protocol(self, char):
        ''' (self, str) -> None
         
             Проверка принятых байт по протоколу. 
             Примеры входных данных: 'AA' '31'
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
            
            Проверка полученного CRC (например 'AB') и вычисленного.
            
            Возвращает True в случае совпадения
            
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
        
            Разрешение приема следующей посылки данных
        '''
        self._bRead = False
        self._data = []
    
    def setCom(self, data):
        ''' (self, str) -> None
        
            Установки команды на передачу
        '''
        self._command = data
    
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    QtGui.QApplication.setStyle('Cleanlooks')
    
    my_frame = mySerial()
    
    # проверка открытия порта с настройками по умолчанию
    my_frame.openPort()
    my_frame.closePort()
    
    # проверка открытия порта с нужными настройками
    my_frame.setSettings(settings={'port': 'COM2', 'baudrate': 1200})
    my_frame.openPort()
    my_frame.closePort()
    
    my_frame.show()
    app.exec_()
